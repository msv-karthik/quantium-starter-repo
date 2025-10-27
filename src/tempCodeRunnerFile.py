# Quick check
check_df = pd.read_csv(output_path)
print("\n✅ Output file preview:")
print(check_df.head())
print("\nColumns:", list(check_df.columns))
print("Number of rows:", len(check_df))