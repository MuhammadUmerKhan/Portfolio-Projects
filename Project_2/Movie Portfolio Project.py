import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
url = "C:\DATA SCIENCE\Python-git-files\All Files\movies.csv"
df = pd.read_csv(url)

df.shape
df.describe()
df.head()
new_order = ['budget', 'company', 'country', 'director', 'genre', 'gross', 'name', 'rating', 'released', 'runtime', 'score', 'star', 'votes', 'writer', 'year']
df = df[new_order]
df['runtime']
df.head()
df.columns

# Cleaning Data
# Checking if there is any missing data
for col in df.columns:
    missing_data = np.mean(df[col].isnull())
    print('{}\t{}'.format(col, missing_data))

df['budget'].isnull().sum()
mean_budget = df['budget'].mean()
df['budget'].replace(np.NaN, mean_budget, inplace=True)
df['budget'].isnull().sum()

df['gross'].isnull().sum()
gross_mean = df['gross'].mean()
df['gross'].replace(np.NaN, gross_mean, inplace=True)

runtime_mean = df['runtime'].mean()
df['runtime'].isnull().sum()
df['runtime'].replace(np.NaN,runtime_mean, inplace=True)

score_mean = df['score'].mean()
df['score'].isnull().sum()
df['score'].replace(np.NaN,score_mean, inplace=True)

votes_mean = df['votes'].mean()
df['votes'].isnull().sum()
df['votes'].replace(np.NaN,score_mean, inplace=True)

df['writer']
df['released'].isnull().sum()
df['year'].isnull().sum()
df.dtypes
# change data type of columns
df['budget'] = df['budget'].astype('int64')
df['gross'] = df['gross'].astype('int64')
df['runtime'] = df['runtime'].astype('int64')
df['votes'] = df['votes'].astype('int64')
df.dtypes

df = df.sort_values(by=['gross'], inplace=False, ascending=False)
pd.set_option('display.max_rows', None)

df.to_csv('movies.csv')
df = pd.read_csv('movies.csv')
df.drop(columns='Unnamed: 0', inplace=True)
df.head()

# Drop any duplicated
df['company'] = df['company'].drop_duplicates().sort_values(ascending=False)

# Budget high correlation
# company high correlation
# scatter plot with budget with gross
df.columns
fig = px.scatter(df, x='budget', y='gross', title='Budget vs Gross Earning', size_max=20,)
fig.update_layout(xaxis_title='Gross Earning', yaxis_title='Budget for Film')
fig.show()

# plot using seaborn
plt.figure(figsize=(10, 6))
sns.regplot(x='budget', y='gross', data=df, scatter_kws={'color':'red'}, line_kws={'color':'blue'})
plt.xlabel('Gross Earning')
plt.ylabel('Budget for Film')
plt.title('Budget vs Gross Earning')
plt.show()

# For Actual correslation
correlation = df[['budget', 'gross', 'runtime', 'score', 'votes', 'year']]
correlation.corr() # mwthod = pearson, kendall, spearman
# High correlation between bidget and gross is high

correlation_matriix = correlation.corr(method='pearson')
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matriix, annot=True)
plt.xlabel('Movie Features')
plt.ylabel('Movie Features')
plt.title('Correlation Matric For Numeric Features')
plt.show()

df_numerized = df
for col_name in df_numerized.columns:
    if (df_numerized[col_name].dtype == 'object'):
        df_numerized[col_name] = df_numerized[col_name].astype('category')
        df_numerized[col_name] = df_numerized[col_name].cat.codes
        
df_numerized.head()


correlation_matrix = df_numerized.corr(method='pearson')
plt.figure(figsize=(20, 10))
sns.heatmap(correlation_matrix, annot=True)
plt.xlabel('Movie Features')
plt.ylabel('Movie Features')
plt.title('Correlation Matric For Numeric Features')
plt.show()


correlation_matrix = df_numerized.corr(method='pearson')
corr_pairs = correlation_matrix.unstack()
sorted_pairs = corr_pairs.sort_values()

high_corr = sorted_pairs[(sorted_pairs) > 0.5]
high_corr