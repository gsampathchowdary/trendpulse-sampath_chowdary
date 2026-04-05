import pandas as pd
import os
import glob

def clean_data():
    # Load the trends JSON file from the 'data' folder
    json_files = glob.glob('data/trends_*.json')
    if not json_files:
        print("No JSON files found in data/ folder.")
        return
    
    # Sort to get the most recent file
    latest_file = max(json_files, key=os.path.getctime)

    df = pd.read_json(latest_file)
    print(f"Loaded {len(df)} stories from {latest_file}")

    # Task 2: Clean the Data

    # 1. Duplicates: Remove rows with the same post_id
    df = df.drop_duplicates(subset=['post_id'])
    print(f"After removing duplicates: {len(df)}")

    # 2. Missing values: Drop rows where post_id, title, or score is missing
    df = df.dropna(subset=['post_id', 'title', 'score'])
    print(f"After removing nulls: {len(df)}")

    # 3. Data types: Ensure score and num_comments are integers
    # fillna(0) ensures we don't crash if num_comments was missing but row was kept
    df['score'] = df['score'].astype(int)
    df['num_comments'] = df['num_comments'].fillna(0).astype(int)

    # 4. Low quality: Remove stories where score is less than 5
    df = df[df['score'] >= 5]
    print(f"After removing low scores: {len(df)}")

    # 5. Whitespace: Strip extra spaces from the title column
    df['title'] = df['title'].str.strip()

    # Task 3: Save as CSV file
    output_path = 'data/trends_clean.csv'
    df.to_csv(output_path, index=False)

    print("==" * 30)
    print(f"Saved {len(df)} rows to {output_path}")

    # Quick Summary: Stories per category
    print("\nStories per category:")
    print(df['category'].value_counts())

if __name__ == "__main__":
    clean_data()