import pandas as pd
import glob
import os

data_path = os.path.join(os.path.dirname(__file__), "../data")

print("Looking for CSVs in:", os.path.abspath(data_path))

csv_files = glob.glob(os.path.join(data_path, "*.csv"))
print("Found CSV files:", csv_files)


if not csv_files:
    raise FileNotFoundError(f"No CSV files found in {os.path.abspath(data_path)}")


dfs = []

for file in csv_files:
    print(f"Processing {file}...")
    df = pd.read_csv(file)

    
    df["product"] = df["product"].astype(str).str.strip().str.lower()

    
    df = df[df["product"] == "pink morsel"]

    if df.empty:
        print(f"  No Pink Morsel rows in {os.path.basename(file)} — skipping.")
        continue

    df["price"] = df["price"].replace('[\$,]', '', regex=True).astype(float)
    
    df["sales"] = df["quantity"] * df["price"]

    
    df = df[["sales", "date", "region"]]

    dfs.append(df)


if not dfs:
    raise ValueError(" No valid Pink Morsel data found in any CSV files.")

final_df = pd.concat(dfs, ignore_index=True)


output_path = os.path.join(os.path.dirname(__file__), "../pink_morsel_sales.csv")
final_df.to_csv(output_path, index=False)

print(f" Processed data saved to: {os.path.abspath(output_path)}")


# Quick check
check_df = pd.read_csv(output_path)
print("\n Output file preview:")
print(check_df.head())
print("\nColumns:", list(check_df.columns))
print("Number of rows:", len(check_df))
