import os
from data import load_data
from scoring import init_llm, apply_keyword_scoring, detect_uncertain_courses, apply_llm_scoring
from analysis import compute_tshape, compute_normalized_tshape, classify_tshape, generate_summary_tables
from visualization import generate_all_visualizations

import json

# --------------------------------
# CREATE PROJECT STRUCTURE
# --------------------------------

def create_project_structure():

    folders = ["tables", "figures", "cache"]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)



API_KEY="YOUR_API_KEY"


# ---------------------------
# KEYWORD DICTIONARIES
# ---------------------------

vertical_keywords = {
     # V1 – Teamwork & Collaboration
     "V1": [ 
        "transport", "transportation", "infrastructure", "traffic", "railway", "aviation", "aircraft", 
        "airframe", "aerodynamic", "propulsion", "navigation", "engineering", "mechanic", "structur",
        "static", "thermodynamic", "control system",   "logistic", "supply chain", "safety", "regulat", 
        "legislation", "law", "convention",  "icao", "easa" 
    ], 

    # V2 – Analytical / Problem-Solving Skills 
    "V2": [ 
        "analysis", "analys", "optimization", "optimiz",  "algorithm", "statistics", "statistical", 
        "model", "modeling", "modelling", "problem solving", "problem", "evaluation", "evaluat", 
        "calculation", "calculat", "assessment", "assess", "quantitative", "quantitativ", "risk analysis", 
        "risk management", "logic", "derivative", "mathematics", "math",  "economic", "economics", "finance"  
    ], 

    # V3 – Technical Tools / Methods 
    "V3": [ 
        "software", "programming", "python", "cad", "gis", "simulation", "simulat", "data analysis", 
        "data processing", "database", "sensor", "instrumentation",  "measurement", "laboratory", 
        "experiment","iot", "automation",  "navigation system", "uav", "drone", "ui", "ux" 
    ] 
}

horizontal_keywords = {
    # H1 – Teamwork & Collaboration 
    "H1": [ 
        "team", "teamwork", "group work", "group project", "collaborat", "cooperat", "joint", "peer", 
        "leadership", "interpersonal", "collectiv", "working with others", "team-based", "soft skill" 
    ], 

    # H2 – Communication Skills 
    "H2": [ 
        "communication", "presentation", "present", "report", "documentation", "discussion", "written", 
        "oral", "seminar", "terminology", "defense", "thesis", "technical writing", "public speaking" 
    ], 

    # H3 – Interdisciplinary Systems Thinking 
    "H3": [ 
        "interdisciplinary", "multidisciplinary", "cross-domain", "cross-disciplinary", "integration", 
        "integrat", "system", "systems thinking", "system approach", "complex system", "holistic", 
        "system perspective", "interconnect" 
    ], 

    # H4 – Project-Based / Experiential Learning 
    "H4": [ 
        "project", "design project", "case study", "assignment", "applied", "practical", "hands-on", 
        "laboratory", "workshop", "field work", "seminar project", "internship", "design task" 
    ], 

    # H5 – Sector / Industry Engagement 
    "H5": [ 
        "industry", "professional practice", "stakeholder", "company", "corporate", "firm", "market", 
        "commercial", "expert", "guest lecture", "certification", "regulation", "sector", "real-world application" 
    ] 
}

# LOAD DATA
df=load_data("final_thesis_data.csv")

client,cache=init_llm(API_KEY)

# APPLY KEYWORD SCORING (SECTION BASED)
df=apply_keyword_scoring(df,vertical_keywords,horizontal_keywords)

# COMPETENCY VARIANCE (UNCERTAINTY DETECTION)
llm_subset=detect_uncertain_courses(df)

# SELECT COURSES FOR LLM ANALYSIS
df=apply_llm_scoring(df,llm_subset,client,cache)

df=compute_tshape(df)
df=compute_normalized_tshape(df)
df=classify_tshape(df)
df=generate_summary_tables(df)

df.to_csv("courses_full_scored_dataset.csv",index=False)

generate_all_visualizations(df)


#reliability_check()

with open("llm_cache.json","w") as f:
    json.dump(cache,f)

print("Pipeline complete")