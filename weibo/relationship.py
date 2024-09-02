import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the transformed CSV file
transformed_file_path_uploaded = '春晚新_hot02_transformed.csv'
data_transformed = pd.read_csv(transformed_file_path_uploaded)

# Convert '_reposts', '_comments', and '_likes' to numeric, handling any errors by coercing to NaN
data_transformed['_reposts'] = pd.to_numeric(data_transformed['_reposts'], errors='coerce')
data_transformed['_comments'] = pd.to_numeric(data_transformed['_comments'], errors='coerce')
data_transformed['_likes'] = pd.to_numeric(data_transformed['_likes'], errors='coerce')

# Drop rows with NaN values in relevant columns to clean the dataset
data_transformed.dropna(subset=['_followers', '_reposts', '_comments', '_likes'], inplace=True)

# Set the aesthetic style of the plots
sns.set_style("whitegrid")

# Create a figure with 3 subplots
fig, axes = plt.subplots(1, 3, figsize=(14, 5))

# Plot the relationship between '_followers' and '_reposts'
sns.scatterplot(ax=axes[0], x='_followers', y='_reposts', data=data_transformed)
axes[0].set_title('Followers vs Reposts')
axes[0].set_xlabel('Number of Followers')
axes[0].set_ylabel('Number of Reposts')
axes[0].set_xscale('log')
axes[0].set_yscale('log')

# Plot the relationship between '_followers' and '_comments'
sns.scatterplot(ax=axes[1], x='_followers', y='_comments', data=data_transformed)
axes[1].set_title('Followers vs Comments')
axes[1].set_xlabel('Number of Followers')
axes[1].set_ylabel('Number of Comments')
axes[1].set_xscale('log')
axes[1].set_yscale('log')

# Plot the relationship between '_followers' and '_likes'
sns.scatterplot(ax=axes[2], x='_followers', y='_likes', data=data_transformed)
axes[2].set_title('Followers vs Likes')
axes[2].set_xlabel('Number of Followers')
axes[2].set_ylabel('Number of Likes')
axes[2].set_xscale('log')
axes[2].set_yscale('log')

plt.tight_layout()
plt.show()


