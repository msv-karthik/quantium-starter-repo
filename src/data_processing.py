import pandas as pd
import glob
import os

# --- Find CSV files safely ---
# Build the full absolute path to the data folder
data_path = os.path.join(os.path.dirname(__file__), "../data")

print("Looking for CSVs in:", os.path.abspath(data_path))

# Grab all CSV files in that folder
csv_files = glob.glob(os.path.join(data_path, "*.csv"))
print("Found CSV files:", csv_files)

# If no CSVs found, stop early
if not csv_files:
    raise FileNotFoundError(f"No CSV files found in {os.path.abspath(data_path)}")

# --- Process each file ---
dfs = []

for file in csv_files:
    print(f"Processing {file}...")
    df = pd.read_csv(file)

    # Normalize product names (case & whitespace)
    df["product"] = df["product"].astype(str).str.strip().str.lower()

    # Filter for Pink Morsel only
    df = df[df["product"] == "pink morsel"]

    if df.empty:
        print(f"⚠️  No Pink Morsel rows in {os.path.basename(file)} — skipping.")
        continue

    # Compute sales
    df["sales"] = df["quantity"] * df["price"]

    # Keep only the required columns
    df = df[["sales", "date", "region"]]

    dfs.append(df)

# --- Combine all filtered dataframes ---
if not dfs:
    raise ValueError("❌ No valid Pink Morsel data found in any CSV files.")

final_df = pd.concat(dfs, ignore_index=True)

# --- Save output ---
output_path = os.path.join(os.path.dirname(__file__), "../pink_morsel_sales.csv")
final_df.to_csv(output_path, index=False)

print(f"✅ Processed data saved to: {os.path.abspath(output_path)}")


# Quick check
check_df = pd.read_csv(output_path)
print("\n✅ Output file preview:")
print(check_df.head())
print("\nColumns:", list(check_df.columns))
print("Number of rows:", len(check_df))