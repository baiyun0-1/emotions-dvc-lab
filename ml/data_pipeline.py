import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/sample.csv")

def load_raw_dataset(path=DATA_PATH):
    """读取 csv 数据集，默认读 v2 干净版。"""
    df = pd.read_csv(path)
    return df

def split_features_label(df):
    """把 DataFrame 拆成 X(特征) 和 y(标签)。"""
    X = df[["id"]].values
    y = df["value"].values
    return X, y
