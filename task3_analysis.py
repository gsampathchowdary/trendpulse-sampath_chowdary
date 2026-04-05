import pandas as pd
import numpy as np
import os

def analyze_data():
    #1: Load and Explore
    file_path = 'data/trends_clean.csv'
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Please run Task 2 first.")
        return

# Loading csv file into dataframe
    df = pd.read_csv(file_path)
    
    # Printing dataframe shape
    print(f"Loaded data: {df.shape}")
    print(f"\nFirst 5 rows: \n {df.head()}")
    
    
    avg_score = df['score'].mean()
    avg_comments = df['num_comments'].mean()
    
    print(f"\nAverage score   : {avg_score:.2f}")
    print(f"Average comments: {avg_comments:.2f}")

    # 2: Basic Analysis with NumPy 
    print("\n" + "-"*10 + " NumPy Stats " + "-"*10)
    
    # Converting columns to NumPy arrays for calculations
    scores = df['score'].to_numpy()
    
    print(f"Mean score   : {np.mean(scores):.2f}")
    print(f"Median score : {np.median(scores):.2f}")
    print(f"Standard deviation: {np.std(scores):.2f}")
    print(f"Max score    : {np.max(scores)}")
    print(f"Min score    : {np.min(scores)}")
    
    # Finding category with most stories
    # value_counts() is Pandas, but we can use idxmax() to find the label
    mode_category = df['category'].value_counts()
    print(f"Most stories in: {mode_category.idxmax()} ({mode_category.max()} stories)")
    
    # Finding the most commented story
    max_comments_idx = df['num_comments'].idxmax()
    top_story = df.loc[max_comments_idx]
    print(f"Most commented story: \"{top_story['title']}\" — {top_story['num_comments']} comments")

    # 3: Adding New Columns 
    # (score + 1) to avoid division by zero
    df['engagement'] = df['num_comments'] / (df['score'] + 1)
    
    # is_popular = True if score > average, else False
    df['is_popular'] = df['score'] > avg_score

    # 4: Save the Result
    output_path = 'data/trends_analysed.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\nAnalysis complete. Saved to {output_path}")

if __name__ == "__main__":
    analyze_data()