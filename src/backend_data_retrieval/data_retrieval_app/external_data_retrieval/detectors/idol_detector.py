import pandas as pd

from data_retrieval_app.external_data_retrieval.detectors.base import DetectorBase


class IdolDetector(DetectorBase):
    def _specialized_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        if "rarity" not in df.columns:
            return pd.DataFrame(columns=df.columns)

        df = df.loc[(df["extended.category"] == "idol") & df["identified"]]
        df = df.loc[df["baseType"] != "Minor Idol"]

        return df

    def __str__(self):
        return "Idol detector"
