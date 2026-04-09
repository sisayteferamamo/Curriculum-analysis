import numpy as np
import pandas as pd
# ---------------------------
# COMPUTE INDIXES
# ---------------------------

def compute_tshape(df):

    df["Vertical"]=(df["V1"]+df["V2"]+df["V3"])/3
    df["Horizontal"]=(df["H1"]+df["H2"]+df["H3"]+df["H4"]+df["H5"])/5

    df["TShapeIndex"]=(
        np.sqrt(df["Vertical"]*df["Horizontal"])
        *(1-abs(df["Vertical"]-df["Horizontal"])/3)
    )

    df["CreditWeightedTShape"]=df["TShapeIndex"]*df["credits"]

    return df


# ------------------------------------------------
# NORMALIZED T-SHAPE INDEX
# ------------------------------------------------

def compute_normalized_tshape(df):

    df["Vertical_z"]=(df["Vertical"]-df["Vertical"].mean())/df["Vertical"].std()
    df["Horizontal_z"]=(df["Horizontal"]-df["Horizontal"].mean())/df["Horizontal"].std()

    df["Vertical_pos"]=df["Vertical_z"].clip(lower=0)
    df["Horizontal_pos"]=df["Horizontal_z"].clip(lower=0)

    df["TShapeIndex_Normalized"]=np.sqrt(
        df["Vertical_pos"]*df["Horizontal_pos"]
    )

    return df


# ---------------------------
# T-SHAPE INTERPRETATION
# --------------------------

def classify_tshape(df):

    def classify(x):

        if x<0.8:
            return "No T-shape"
        elif x<1.6:
            return "Narrow specialization"
        elif x<2.3:
            return "Emerging T-shape"
        else:
            return "Strong T-shape"

    df["TShapeCategory"]=df["TShapeIndex"].apply(classify)

    return df


def generate_summary_tables(df):

    # dataset overview
    table_dataset = pd.DataFrame({
        "Metric": ["Total courses"],
        "Value": [len(df)]
    })

    # courses by academic degree
    table_degree = df["academic_degree"].value_counts().reset_index()
    table_degree.columns = ["Academic Degree", "Courses"]

    # courses by course type
    table_course_type = df["course_type"].value_counts().reset_index()
    table_course_type.columns = ["Course Type", "Courses"]

    # competency frequency
    competencies = ["V1","V2","V3","H1","H2","H3","H4","H5"]

    table_comp_freq = pd.DataFrame({
        "Competency": competencies,
        "Frequency": [(df[c] > 0).sum() for c in competencies]
    })

    table_comp_freq["Percent"] = table_comp_freq["Frequency"] / len(df) * 100

    # vertical vs horizontal summary
    table_vh = pd.DataFrame({
        "Dimension": ["Vertical","Horizontal"],
        "Mean": [df["Vertical"].mean(), df["Horizontal"].mean()],
        "Std": [df["Vertical"].std(), df["Horizontal"].std()]
    })

    # degree scores
    table_degree_scores = df.groupby("academic_degree")[[
        "Vertical","Horizontal","TShapeIndex"
    ]].mean()

    # course type scores
    table_type_scores = df.groupby("course_type")[[
        "Vertical","Horizontal","TShapeIndex"
    ]].mean()

    # T-shape category distribution
    table_tshape = df["TShapeCategory"].value_counts().reset_index()
    table_tshape.columns = ["Category","Courses"]

    # export tables
    table_dataset.to_csv("table_dataset_summary.csv", index=False)
    table_degree.to_csv("table_courses_by_degree.csv", index=False)
    table_course_type.to_csv("table_courses_by_type.csv", index=False)
    table_comp_freq.to_csv("table_competency_frequency.csv", index=False)
    table_vh.to_csv("table_vertical_horizontal.csv", index=False)

    table_degree_scores.to_csv("table_scores_by_degree.csv")
    table_type_scores.to_csv("table_scores_by_course_type.csv")
    table_tshape.to_csv("table_tshape_distribution.csv", index=False)

    # curriculum balance index
    avg_vertical = df["Vertical"].mean()
    avg_horizontal = df["Horizontal"].mean()

    CBI = avg_horizontal / avg_vertical

    pd.DataFrame({
        "Average Vertical": [avg_vertical],
        "Average Horizontal": [avg_horizontal],
        "Curriculum Balance Index": [CBI]
    }).to_csv("table_curriculum_balance_index.csv", index=False)