import re
import json
import hashlib
import os
import time
import pandas as pd
from google import genai


# --------------------------------
# LLM CACHE
# --------------------------------

CACHE_FILE = "llm_cache.json"

def init_llm(api_key):

    client = genai.Client(api_key=api_key)

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE,"r") as f:
            cache = json.load(f)
    else:
        cache = {}

    return client, cache


def text_hash(text):
    return hashlib.md5(text.encode()).hexdigest()


# ---------------------------
# SCORING FUNCTION
# ---------------------------

def score_competency(text, keywords):

    words = len(text.split())

    matches = {
        word for word in keywords
        if re.search(r"\b" + re.escape(word) + r"\b", text)
    }

    density = len(matches) / words

    if density == 0:
        return 0
    elif density < 0.003:
        return 1
    elif density < 0.008:
        return 2
    else:
        return 3

# --------------------------------
# APPLY KEYWORD SCORING (SECTION BASED)
# --------------------------------

def apply_keyword_scoring(df, vertical_keywords, horizontal_keywords):

    for k,v in vertical_keywords.items():

        keyword_score = df["keywords"].apply(lambda x: score_competency(x.lower(), v))
        abstract_score = df["abstract"].apply(lambda x: score_competency(x.lower(), v))
        objective_score = df["objectives"].apply(lambda x: score_competency(x.lower(), v))

        df[k] = (keyword_score + 2*abstract_score + 3*objective_score) / 6

    for k,v in horizontal_keywords.items():

        keyword_score = df["keywords"].apply(lambda x: score_competency(x.lower(), v))
        abstract_score = df["abstract"].apply(lambda x: score_competency(x.lower(), v))
        objective_score = df["objectives"].apply(lambda x: score_competency(x.lower(), v))

        df[k] = (keyword_score + 2*abstract_score + 3*objective_score) / 6

    return df


# ------------------------------------------------
# COMPETENCY VARIANCE (UNCERTAINTY DETECTION)
# ------------------------------------------------

def detect_uncertain_courses(df):

    df["vertical_variance"] = df[["V1","V2","V3"]].var(axis=1)
    df["horizontal_variance"] = df[["H1","H2","H3","H4","H5"]].var(axis=1)

    return df[
        (df["vertical_variance"] > 1) |
        (df["horizontal_variance"] > 1)
    ]


# ------------------------------------------------
# # LLM SCORING FUNCTION - GEMINI BATCH SCORING
# ------------------------------------------------
def gemini_score_course(text, client, cache):

    h = text_hash(text)

    if h in cache:
        return cache[h]

    prompt = f"""
You are analyzing university course syllabus descriptions to identify competency development.

Your task is to evaluate how strongly each competency is represented in the course description.

Use the following scoring framework.

SCORING SCALE

0 = Not present
The competency is not mentioned in the course description.

1 = Mentioned
The competency appears briefly but is not connected to assignments, projects, or activities.

2 = Developed
The competency is practiced through assignments, labs, coursework, projects, or applied activities.

3 = Core learning objective
The competency is central to the course and clearly appears as a main learning objective or repeated focus.

COMPETENCIES

V1 Technical expertise  
Depth of disciplinary knowledge, engineering concepts, models, algorithms, or technical systems.

V2 Analytical problem solving  
Problem analysis, modelling, evaluation methods, quantitative reasoning.

V3 Specialized methods  
Use of specialized tools, software, laboratories, simulations, programming, or technical methodologies.

H1 Teamwork  
Collaborative work, group projects, team-based learning activities.

H2 Communication  
Presentations, reports, documentation, discussions, or written communication.

H3 Interdisciplinary integration  
Integration of knowledge across disciplines, systems thinking, cross-domain knowledge.

H4 Project-based learning  
Projects, applied coursework, design tasks, practical implementation.

H5 Sector / industry engagement  
Industry collaboration, case studies, real-world applications, partnerships with external organizations.

EVALUATION INSTRUCTIONS

For each course:

1. Read the course description carefully.
2. Identify explicit evidence of each competency.
3. Assign the score that best reflects the strongest evidence found.

Return scores between 0 and 3.

OUTPUT FORMAT

Return ONLY a valid JSON list.

Do not include explanations or commentary.

Example output:

[
{{"V1":2,"V2":2,"V3":1,"H1":1,"H2":1,"H3":0,"H4":2,"H5":1}}
]

COURSES TO ANALYZE:
{text}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        parsed = json.loads(response.text)

    except:

        parsed = {
            "V1":0,"V2":0,"V3":0,
            "H1":0,"H2":0,"H3":0,"H4":0,"H5":0
        }
    
    # SAVE TO CACHE
    cache[h] = parsed

    time.sleep(0.5)

    return parsed

# ------------------------------------------------
# APPLY LLM SCORING
# ------------------------------------------------

def apply_llm_scoring(df, llm_subset, client, cache):

    all_scores=[]

    for idx,row in llm_subset.iterrows():

        score = gemini_score_course(row["text"], client, cache)

        all_scores.append(score)

    llm_scores_df = pd.DataFrame(all_scores)

    llm_subset = llm_subset.reset_index()

    llm_subset[["V1_llm","V2_llm","V3_llm","H1_llm","H2_llm","H3_llm","H4_llm","H5_llm"]] = llm_scores_df

# ------------------------------------------------
# MERGE SCORES (LLM replaces keyword score)
# ------------------------------------------------
    for idx,row in llm_subset.iterrows():

        for c in ["V1","V2","V3","H1","H2","H3","H4","H5"]:
            df.loc[row["index"],c] = row[c+"_llm"]

    df["LLM_evaluated"]=False
    df.loc[llm_subset["index"],"LLM_evaluated"]=True
    llm_percentage = df["LLM_evaluated"].mean() * 100
    print("LLM evaluated courses:", round(llm_percentage,2), "%")

    return df
  