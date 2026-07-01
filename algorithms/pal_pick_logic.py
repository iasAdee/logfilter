import pandas as pd
from algorithms.data_processing import DataPreprocessing
import re

def get_results(df:pd.DataFrame):
    # Editing the top column names
    df.columns = (
        df.columns
        .str.strip()                    # remove leading/trailing spaces
        .str.lower()                    # lowercase
        .str.replace(".", "_", regex=False)
        .str.replace(" ", "_", regex=False)
    )

    df.columns = [
        re.sub(r"[^a-z0-9_]", "", col)
        for col in df.columns
    ]

    #print(df.columns)
    int_cols = ["verursach_", "plzwempf", "brutto", "versandbed",
                "offene_mng","material","gelmenge", "best_mg","auftrgeber","warenempf_"]

    for col in int_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )

        df[col] = pd.to_numeric(df[col], errors="coerce")


    data_preprocessor = DataPreprocessing(df)

    #calling tof dascher functions
    data_req, fig = data_preprocessor.clac_2()

    ls2, ls3, data1, data2, fig2, fig3, fig4, fig5, fig6, fig7, fig10, fig20 = data_preprocessor.get_calculated_results(input=False)
    fig8 = data_preprocessor.get_absenders()

    return (data_req,
            fig,
            fig2, 
            fig3,
            fig4,
            fig5,
            fig6,
            fig7,
            fig8,
            fig10,
            fig20, 
            data1, 
            data2
            )
