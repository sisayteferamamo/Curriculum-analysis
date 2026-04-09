import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import numpy as np
import os


# ------------------------------------------------
# FACULTY COMPETENCY RADAR PROFILE
# ------------------------------------------------

def plot_faculty_competency_radar(df):

    competency_means = df[
        ["V1","V2","V3","H1","H2","H3","H4","H5"]
    ].mean()

    labels = competency_means.index.tolist()
    values = competency_means.values.tolist()

    # close radar loop
    values += values[:1]
    labels += labels[:1]

    angles = np.linspace(0, 2*np.pi, len(values), endpoint=False)

    plt.figure(figsize=(7,7))

    ax = plt.subplot(111, polar=True)

    ax.plot(angles, values, linewidth=2)

    ax.fill(angles, values, alpha=0.25)

    ax.set_thetagrids(angles * 180/np.pi, labels)

    ax.set_title("Faculty Competency Profile (T-Shape Radar)")

    save_fig("fig_competency_radar_profile.png")



# ------------------------------------------------
# INTERDISCIPLINARY GAP ANALYSIS
# ------------------------------------------------
def plot_interdisciplinary_gap(df):

    competency_means = df[
        ["V1","V2","V3","H1","H2","H3","H4","H5"]
    ].mean()

    import pandas as pd

    gap_table = pd.DataFrame({
        "Competency": competency_means.index,
        "Average Score": competency_means.values
    }).sort_values("Average Score")

    plt.figure(figsize=FIG_SIZE)

    sns.barplot(
        data=gap_table,
        x="Average Score",
        y="Competency"
    )

    plt.title("Interdisciplinary Competency Gaps")

    save_fig("fig_interdisciplinary_gap_analysis.png")



# ------------------------------------------------
# GLOBAL VISUAL STYLE
# ------------------------------------------------

sns.set_theme(style="whitegrid", context="paper")

FIG_DPI = 300
FIG_SIZE = (10, 8)

FIG_FOLDER = "figures"
os.makedirs(FIG_FOLDER, exist_ok=True)


def save_fig(name):
    plt.tight_layout()
    plt.savefig(f"{FIG_FOLDER}/{name}", dpi=FIG_DPI)
    plt.close()


# ------------------------------------------------
# BASIC DISTRIBUTION PLOTS
# ------------------------------------------------

def plot_course_distribution(df):

    plt.figure(figsize=FIG_SIZE)

    sns.countplot(data=df, x="academic_degree")

    plt.title("Courses by Academic Degree")

    save_fig("fig_courses_by_degree.png")


    plt.figure(figsize=FIG_SIZE)

    sns.countplot(data=df, x="course_type")

    plt.title("Courses by Course Type")

    save_fig("fig_courses_by_type.png")


# ------------------------------------------------
# COMPETENCY FREQUENCY
# ------------------------------------------------

def plot_competency_frequency(df):

    competencies = ["V1","V2","V3","H1","H2","H3","H4","H5"]

    table = {
        "Competency": competencies,
        "Frequency": [(df[c] > 0).sum() for c in competencies]
    }

    import pandas as pd
    table = pd.DataFrame(table)

    table["Percent"] = table["Frequency"] / len(df) * 100

    plt.figure(figsize=FIG_SIZE)

    sns.barplot(data=table, x="Percent", y="Competency")

    plt.title("Frequency of Competencies")

    save_fig("fig_competency_frequency.png")


# ------------------------------------------------
# VERTICAL VS HORIZONTAL DISTRIBUTION
# ------------------------------------------------

def plot_vertical_horizontal(df):

    plt.figure(figsize=FIG_SIZE)

    sns.boxplot(data=df[["Vertical","Horizontal"]])

    plt.title("Vertical vs Horizontal Competency Scores")

    save_fig("fig_vertical_horizontal.png")


    plt.figure(figsize=FIG_SIZE)

    sns.histplot(df["TShapeIndex"], bins=20)

    plt.title("Distribution of T-Shape Index")

    save_fig("fig_tshape_distribution.png")


# ------------------------------------------------
# DEGREE AND COURSE TYPE COMPARISONS
# ------------------------------------------------

def plot_scores_by_degree(df):

    degree_scores = df.groupby("academic_degree")[[
        "Vertical","Horizontal","TShapeIndex"
    ]].mean()

    plt.figure(figsize=FIG_SIZE)

    degree_scores.plot(kind="bar", ax=plt.gca())

    plt.title("Competency Scores by Academic Degree")

    plt.ylabel("Score")

    save_fig("fig_scores_by_degree.png")


def plot_scores_by_course_type(df):

    type_scores = df.groupby("course_type")[[
        "Vertical","Horizontal","TShapeIndex"
    ]].mean()

    plt.figure(figsize=FIG_SIZE)

    type_scores.plot(kind="bar", ax=plt.gca())

    plt.title("Competency Scores by Course Type")

    plt.ylabel("Score")

    save_fig("fig_scores_by_course_type.png")


# ------------------------------------------------
# T-SHAPE COMPETENCY MAP
# ------------------------------------------------

def plot_tshape_map(df):

    plt.figure(figsize=FIG_SIZE)

    sns.scatterplot(
        data=df,
        x="Vertical",
        y="Horizontal",
        hue="course_type",
        palette="viridis",
        alpha=0.7
    )

    plt.axvline(df["Vertical"].mean(), linestyle="--")
    plt.axhline(df["Horizontal"].mean(), linestyle="--")

    plt.xlabel("Technical Depth (Vertical)")
    plt.ylabel("Interdisciplinary Breadth (Horizontal)")

    plt.title("T-Shape Competency Map")

    save_fig("fig_tshape_competency_map.png")


# ------------------------------------------------
# T-SHAPE CURRICULUM MAP
# ------------------------------------------------

def plot_tshape_curriculum_map(df):

    plt.figure(figsize=(12,9))

    sns.scatterplot(
        data=df,
        x="Vertical",
        y="Horizontal",
        hue="course_type",
        palette="viridis",
        alpha=0.7,
        s=120
    )

    for _,row in df.sample(min(40,len(df))).iterrows():

        plt.text(
            row["Vertical"]+0.02,
            row["Horizontal"]+0.02,
            str(row["course_name"])[:25],
            fontsize=7
        )

    plt.axvline(df["Vertical"].mean(), linestyle="--", color="grey")
    plt.axhline(df["Horizontal"].mean(), linestyle="--", color="grey")

    plt.xlabel("Technical Depth")
    plt.ylabel("Interdisciplinary Breadth")

    plt.title("T-Shape Curriculum Map")

    save_fig("fig_tshape_curriculum_map.png")


# ------------------------------------------------
# CURRICULUM TRAJECTORY
# ------------------------------------------------

def plot_curriculum_trajectory(df):

    trajectory = df.groupby("academic_degree")[["Vertical","Horizontal"]].mean()

    plt.figure(figsize=FIG_SIZE)

    plt.plot(
        trajectory["Vertical"],
        trajectory["Horizontal"],
        marker="o",
        linewidth=2
    )

    for degree,row in trajectory.iterrows():

        plt.text(
            row["Vertical"]+0.02,
            row["Horizontal"]+0.02,
            degree
        )

    plt.xlabel("Vertical Competency")
    plt.ylabel("Horizontal Competency")

    plt.title("Curriculum Development Trajectory")

    plt.grid(True)

    save_fig("fig_curriculum_trajectory.png")


# ------------------------------------------------
# T-SHAPE LANDSCAPE
# ------------------------------------------------

def plot_tshape_landscape(df):

    plt.figure(figsize=FIG_SIZE)

    sns.kdeplot(
        data=df,
        x="Vertical",
        y="Horizontal",
        fill=True,
        cmap="viridis",
        thresh=0.05,
        levels=50
    )

    plt.axvline(df["Vertical"].mean(), linestyle="--")
    plt.axhline(df["Horizontal"].mean(), linestyle="--")

    plt.xlabel("Technical Depth")
    plt.ylabel("Interdisciplinary Breadth")

    plt.title("Curriculum T-Shape Landscape")

    save_fig("fig_tshape_landscape.png")


# ------------------------------------------------
# T-SHAPE PROGRESSION
# ------------------------------------------------

def plot_tshape_progression(df):

    degree_scores = df.groupby("academic_degree")[[
        "Vertical","Horizontal","TShapeIndex"
    ]].mean()

    plt.figure(figsize=FIG_SIZE)

    degree_scores.plot(kind="bar", ax=plt.gca())

    plt.title("T-Shape Competency Progression Across Academic Degrees")

    plt.ylabel("Average Competency Score")

    save_fig("fig_tshape_progression_by_degree.png")


# ------------------------------------------------
# HORIZONTAL COMPETENCY BOXPLOT
# ------------------------------------------------

def plot_horizontal_boxplot(df):

    plt.figure(figsize=FIG_SIZE)

    sns.boxplot(
        data=df,
        x="academic_degree",
        y="Horizontal"
    )

    plt.title("Distribution of Horizontal Competencies by Degree")

    save_fig("fig_horizontal_by_degree_boxplot.png")


# ------------------------------------------------
# COMPETENCY HEATMAP
# ------------------------------------------------

def plot_competency_heatmap(df):

    plt.figure(figsize=(12,10))

    sns.heatmap(
        df[["V1","V2","V3","H1","H2","H3","H4","H5"]],
        cmap="viridis"
    )

    plt.title("Competency Coverage Matrix")

    save_fig("fig_competency_coverage_matrix.png")


# ------------------------------------------------
# PROGRAM BALANCE
# ------------------------------------------------

def plot_program_balance(df):

    program_balance = df.groupby("study_programme")[["Vertical","Horizontal"]].mean()

    plt.figure(figsize=FIG_SIZE)

    sns.scatterplot(
        data=program_balance,
        x="Vertical",
        y="Horizontal",
        s=120
    )

    for program,row in program_balance.iterrows():

        plt.text(
            row["Vertical"]+0.02,
            row["Horizontal"]+0.02,
            program,
            fontsize=9
        )

    plt.axvline(program_balance["Vertical"].mean(), linestyle="--")
    plt.axhline(program_balance["Horizontal"].mean(), linestyle="--")

    plt.xlabel("Technical Depth")
    plt.ylabel("Interdisciplinary Breadth")

    plt.title("Program-Level T-Shape Balance")

    save_fig("fig_program_tshape_balance.png")


# ------------------------------------------------
# COMPETENCY CORRELATION NETWORK
# ------------------------------------------------

def competency_network(df):

    competencies=["V1","V2","V3","H1","H2","H3","H4","H5"]

    corr=df[competencies].corr()

    G=nx.Graph()

    for c in competencies:
        G.add_node(c)

    for i in competencies:
        for j in competencies:
            if i!=j and abs(corr.loc[i,j])>0.3:
                G.add_edge(i,j,weight=corr.loc[i,j])

    plt.figure(figsize=FIG_SIZE)

    pos=nx.spring_layout(G,seed=42)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2000,
        node_color="lightblue",
        font_size=10
    )

    plt.title("Competency Correlation Network")

    save_fig("fig_competency_network.png")


# ------------------------------------------------
# MASTER FUNCTION
# ------------------------------------------------

def generate_all_visualizations(df):

    plot_course_distribution(df)

    plot_competency_frequency(df)

    plot_vertical_horizontal(df)

    plot_scores_by_degree(df)

    plot_scores_by_course_type(df)

    plot_faculty_competency_radar(df)

    plot_interdisciplinary_gap(df)

    plot_tshape_map(df)

    plot_tshape_curriculum_map(df)

    plot_curriculum_trajectory(df)

    plot_tshape_landscape(df)

    plot_tshape_progression(df)

    plot_horizontal_boxplot(df)

    plot_competency_heatmap(df)

    plot_program_balance(df)

    competency_network(df)