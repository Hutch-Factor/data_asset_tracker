import pandas as pd

def load_assets(path="data_assets.csv"):
    return pd.read_csv(path)

def save_assets(new_asset, path="data_assets.csv"):
    df = load_assets(path)
    df = df.append(new_asset, ignore_index=True)
    df.to_csv(path, index=False)