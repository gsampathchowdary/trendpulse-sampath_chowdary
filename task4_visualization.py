import pandas as pd
import matplotlib.pyplot as plt
import os

def create_visualizations():
    # 1: Setup 
    file_path = 'data/trends_analysed.csv'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Please run Task 3 first.")
        return
    # Loading csv file to dataframe
    df = pd.read_csv(file_path)

    # Create outputs folder if doesnot exist
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    # 2: Chart 1 - Top 10 Stories by Score
    plt.figure(figsize=(10, 6))
    # Sort stories by score and take top 10
    top_10 = df.sort_values(by='score', ascending=False).head(10)
    # Shorten titles for readability
    titles = [t[:47] + "..." if len(t) > 50 else t for t in top_10['title']]

    plt.barh(titles, top_10['score'], color='skyblue')
    plt.xlabel('Upvote Score')
    plt.title('Top 10 HackerNews Stories by Score')
    plt.gca().invert_yaxis() # Highest score at the top
    plt.tight_layout()
    plt.savefig('outputs/chart1_top_stories.png')
    plt.show()
    plt.close()

    # 3: Chart 2 - Stories per Category
    plt.figure(figsize=(8, 6))
    # Calculate number of stories in each category
    cat_counts = df['category'].value_counts()
    colors = ['gold', 'lightgreen', 'red', 'skyblue', 'pink']

    cat_counts.plot(kind='bar', color=colors[:len(cat_counts)])
    plt.title('Distribution of Stories by Category')
    plt.xlabel('Category')
    plt.ylabel('Number of Stories')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('outputs/chart2_categories.png')
    plt.show()
    plt.close()

    # 4: Chart 3 - Score vs Comments
    plt.figure(figsize=(8, 6))
    # Separating stories into popular and not_popular
    popular = df[df['is_popular'] == True]
    not_popular = df[df['is_popular'] == False]

    plt.scatter(not_popular['score'], not_popular['num_comments'], alpha=0.5, label='Standard', c='blue')
    plt.scatter(popular['score'], popular['num_comments'], alpha=0.7, label='Popular', c='red', edgecolors='black')

    plt.title('Correlation: Score vs. Number of Comments')
    plt.xlabel('Score (Upvotes)')
    plt.ylabel('Number of Comments')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('outputs/chart3_scatter.png')
    plt.show()
    plt.close()

    # Bonus: Dashboard
    # Creating a 2x2 grid (bottom right will be used for Output text)
    fig, axes = plt.subplots(2, 2, figsize=(24, 16))
    fig.suptitle('TrendPulse Dashboard', fontsize=24, fontweight='bold')

    # Subplot 1: Top Stories
    axes[0, 0].barh(titles, top_10['score'], color='skyblue')
    axes[0, 0].set_title('Top 10 Stories')
    axes[0, 0].invert_yaxis()

    # Subplot 2: Categories
    cat_counts.plot(kind='bar', color=colors[:len(cat_counts)], ax=axes[0, 1])
    axes[0, 1].set_title('Stories per Category')

    # Subplot 3: Scatter Plot
    axes[1, 0].scatter(not_popular['score'], not_popular['num_comments'], alpha=0.5, c='blue', label='Standard')
    axes[1, 0].scatter(popular['score'], popular['num_comments'], alpha=0.7, c='red', label='Popular', edgecolors='black')
    axes[1, 0].set_title('Score vs Comments')
    axes[1, 0].set_xlabel('Score')
    axes[1, 0].set_ylabel('Comments')
    axes[1, 0].legend()

    # Subplot 4: We do not have any subplot so we are removing all visual elements here
    axes[1, 1].axis('off')
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig('outputs/dashboard.png')
    plt.show()
    plt.close()

    print("All charts and the dashboard have been saved to the 'outputs/' folder.")

if __name__ == "__main__":
    create_visualizations()