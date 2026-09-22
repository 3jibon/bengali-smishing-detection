from datasets import load_dataset
import pandas as pd

# ডেটাসেট লোড
dataset = load_dataset("shariul-islam/bengali-sms-smishing-dataset")

print("=" * 50)
print("Dataset Splits:")
print(dataset)
print("=" * 50)

# প্রতিটি split এর তথ্য
for split in dataset.keys():
    df = dataset[split].to_pandas()
    print(f"\n--- {split.upper()} ---")
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nLabel distribution:")
    print(df['label'].value_counts())
    print(f"\nSource distribution:")
    if 'source' in df.columns:
        print(df['source'].value_counts())
    print(f"\nSample rows:")
    print(df.head(3))

    import os
os.makedirs("data/raw", exist_ok=True)

for split in dataset.keys():
    df = dataset[split].to_pandas()
    df.to_csv(f"data/raw/{split}.csv", index=False)
    print(f"Saved data/raw/{split}.csv")

# সম্পূর্ণ ডেটা একসাথে
full_df = pd.concat([dataset[s].to_pandas() for s in dataset.keys()], ignore_index=True)
full_df.to_csv("data/raw/full_dataset.csv", index=False)
print(f"\nFull dataset saved: {full_df.shape}")