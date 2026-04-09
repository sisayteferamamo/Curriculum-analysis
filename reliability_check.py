import pandas as pd
from sklearn.metrics import cohen_kappa_score

def reliability_check():

    try:

        validation=pd.read_csv("validation_sample_scored.csv")

        competencies=["V1","V2","V3","H1","H2","H3","H4","H5"]

        results=[]

        for c in competencies:

            agreement=(validation[c]==validation[c+"_manual"]).mean()

            kappa=cohen_kappa_score(
                validation[c],
                validation[c+"_manual"]
            )

            results.append({
                "Competency":c,
                "Agreement":round(agreement,3),
                "Cohen_Kappa":round(kappa,3)
            })

        pd.DataFrame(results).to_csv(
            "table_llm_validation_results.csv",
            index=False
        )

    except FileNotFoundError:

        print("Manual validation file not found.")