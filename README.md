# T-Shape Curriculum Analysis Framework

A hybrid curriculum analytics pipeline for evaluating how university courses contribute to the development of **T-shaped professionals**.

The framework combines **keyword-based competency detection** with **LLM-assisted semantic evaluation (Gemini 2.5 Flash)** to identify technical depth and interdisciplinary breadth in course syllabi.

It produces quantitative curriculum indicators and visualizations that reveal competency coverage, curriculum balance, and developmental trajectories across academic programs.

---

# Concept

The concept of **T-shaped professionals** describes individuals who combine:

• **Vertical depth** – strong disciplinary expertise
• **Horizontal breadth** – interdisciplinary collaboration and communication skills

This framework evaluates whether a curriculum supports the development of both dimensions.

---

# Methodological Pipeline

The analysis follows a hybrid scoring workflow.

```
course descriptions
        ↓
section-based keyword scoring
        ↓
variance-based uncertainty detection
        ↓
LLM semantic evaluation (Gemini 2.5 Flash)
        ↓
score replacement
        ↓
T-shape competency metrics
        ↓
curriculum analytics and visualization
```

Keyword scoring ensures **transparent rule-based detection**, while LLM evaluation provides **semantic interpretation for ambiguous cases**.

---

# Competency Framework

The model evaluates eight competencies.

## Vertical (Technical Depth)

| Code | Competency                    |
| ---- | ----------------------------- |
| V1   | Technical expertise           |
| V2   | Analytical problem solving    |
| V3   | Specialized tools and methods |

## Horizontal (Interdisciplinary Breadth)

| Code | Competency                    |
| ---- | ----------------------------- |
| H1   | Teamwork                      |
| H2   | Communication                 |
| H3   | Interdisciplinary integration |
| H4   | Project-based learning        |
| H5   | Industry engagement           |

---

# T-Shape Index

Vertical and horizontal scores are aggregated to compute a **balanced T-shape index**:

```
T = √(Vertical × Horizontal) × (1 − |Vertical − Horizontal| / 3)
```

This formulation rewards **balanced competency development** and penalizes strong asymmetry between depth and breadth.

---

# Repository Structure

```
project/

data/
    final_thesis_data.csv

cache/
    llm_cache.json

tables/
    exported analysis tables

figures/
    generated visualizations

main.py
data.py
scoring.py
analysis.py
visualization.py
```

Module responsibilities:

| Module           | Purpose                                     |
| ---------------- | ------------------------------------------- |
| data.py          | data loading and preprocessing              |
| scoring.py       | keyword scoring and LLM evaluation          |
| analysis.py      | competency metrics and statistical analysis |
| visualization.py | curriculum analytics visualizations         |
| main.py          | pipeline orchestration                      |

---

# Installation

Clone the repository:

```
git clone https://github.com/sisayteferamamo/tshape-curriculum-analysis
cd tshape-curriculum-analysis
```

Create environment:

```
python -m venv .venv
```

Activate environment:

Windows

```
.venv\Scripts\activate
```

Install dependencies:

```
pip install pandas numpy matplotlib seaborn scikit-learn networkx google-generativeai
```

---

# Configuration

Add your Gemini API key in **main.py**:

```
API_KEY = "YOUR_API_KEY"
```

---

# Running the Pipeline

Execute the full analysis:

```
python main.py
```

The script will automatically:

• score competencies
• evaluate uncertain courses using Gemini
• compute T-shape metrics
• generate tables and figures

---

# Output

## Tables

Saved in `/tables`

Examples:

```
table_dataset_summary.csv
table_scores_by_degree.csv
table_tshape_distribution.csv
table_curriculum_balance_index.csv
```

## Figures

Saved in `/figures`

Examples:

```
fig_tshape_competency_map.png
fig_tshape_curriculum_map.png
fig_tshape_landscape.png
fig_program_tshape_balance.png
fig_competency_network.png
fig_interdisciplinary_gap_analysis.png
fig_competency_radar_profile.png
```

---

# Key Visualizations

The framework generates several analytical views of the curriculum.

• **Competency Coverage Matrix** – heatmap of competencies across courses
• **T-Shape Competency Map** – distribution of courses in depth-breadth space
• **Curriculum Trajectory** – competency development across academic degrees
• **Program Balance Plot** – specialization vs interdisciplinarity per program
• **Competency Network** – relationships between competencies
• **Gap Analysis** – underdeveloped competencies

---

# Validation

The framework includes manual validation support.

A random validation sample is exported:

```
validation_sample_for_manual_coding.csv
```

Manual scoring can then be compared to automated results using **Cohen's Kappa**.

---

# Research Applications

This framework can support:

• curriculum evaluation
• program accreditation
• educational policy analysis
• interdisciplinary program design
• learning outcomes assessment

---

# License

MIT License

---

# Author

Curriculum analytics research project on **T-shaped competency development in higher education**.
