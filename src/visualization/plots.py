import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_mean_severity_by_category(df: pd.DataFrame, cat_map: dict):
    severity_by_domain = df.groupby("category_id")["severity"].mean().rename(index=cat_map).sort_values()
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=severity_by_domain.index, y=severity_by_domain.values, palette='viridis')
    plt.title('Mean Severity Rating by Bug Category')
    plt.xlabel('Bug Domain')
    plt.ylabel('Mean Severity Rating')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_median_metric_by_environment(df: pd.DataFrame, target_col: str, title: str, env_map: dict):
    data_grouped = df.groupby("environment_id")[target_col].median().rename(index=env_map).sort_values()
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=data_grouped.index, y=data_grouped.values, palette='viridis')
    plt.title(title)
    plt.xlabel('Environment')
    plt.ylabel(f'Median {target_col.capitalize()} Rating')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_severity_priority_correlation(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(df["priority"], df["severity"])
    sns.regplot(x=df['priority'], y=df['severity'], ax=ax)
    plt.suptitle('Correlation Between Severity and Priority', y=1.02)
    plt.xlabel('Priority Rating')
    plt.ylabel('Severity Rating')
    plt.tight_layout()
    plt.show()