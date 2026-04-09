import pandas as pd

def load_data(path):

    df = pd.read_csv(path)

    for col in ["keywords","abstract","objectives"]:
        df[col] = df[col].fillna("").astype(str)

    df["text"] = (
        "Keywords: " + df["keywords"] +
        "\nAbstract: " + df["abstract"] +
        "\nObjectives: " + df["objectives"]
    ).str.lower()

    df["text"] = df["text"].str.slice(0,3000)

    return df