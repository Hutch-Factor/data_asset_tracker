import pandas as pd

def load_assets(path="data_assets.csv"):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip() #Removes spaces around column names
    return df

def save_assets(new_asset, path="data_assets.csv"):
    df = load_assets(path)
    df = df.append(new_asset, ignore_index=True)
    df.to_csv(path, index=False)
