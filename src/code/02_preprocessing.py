# =============================================================================================================
# DATA ANALYSIS & TRIAGE METRICS GENERATION ENGINE
# Loads normalized bug tracking data, executes custom business rule transformations for severity and priority,
# maps relational dimension keys to descriptive metadata, audits missing values, and calculates composite features.
# =============================================================================================================

# =====================================================================
# Core System & Data Processing Libraries
# =====================================================================
import os
import sys
import pandas as pd
from pandas.core.indexes import category
import numpy as np

# =====================================================================
# Data Visualization Libraries
# =====================================================================
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# =====================================================================
# Project-Specific Directory Setup
# =====================================================================
# Target the 'BugTriageAI' root directory (one level up from data/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Add root to search path so Python can see the 'src' folder
if project_root not in sys.path:
    sys.path.append(project_root)

# =====================================================================
# Internal Project Configuration & Utilities Import
# =====================================================================
from src.config import config
from src.features.transformers import clean_bug_text
from src.features.CONSTANS import CRASH_KEYWORDS, FEATURE_COLUMNS, TARGET_COLUMN
from src.visualization import plots
from src.utils import utils

# =====================================================================
# Data Loading Logic
# =====================================================================
if getattr(config, "bug_data", None) is not None:
        print("Bug data already loaded.")
else:
    config.bug_data = pd.read_csv(os.path.join(config.PROCESSED_DATA_DIR, 'normalized_dataset_bugs.csv'))

# =====================================================================
# Console Preparation
# =====================================================================
# Flush out previous command terminal print artifacts to make the report readable
utils.clear_console()

# =============================================================================================================
# Data Deduplication Audit
# =============================================================================================================
# Execute complete transaction uniqueness tests
if config.bug_data.duplicated().any():
    print(f"\n{utils.color_text('[Summary of duplicate values after imputation]', utils.RED + utils.BOLD)}")
    print(config.bug_data.duplicated().sum())
else:
    print(f"\n{utils.color_text('There are no duplicate values in the dataset', utils.GREEN)}")


# =============================================================================================================
# Clean text function
# =============================================================================================================
#Create text variable
# Create combined text column cleanly using pandas string concatenation
config.bug_data["text"] = (
    config.bug_data["short_description"].fillna("")
    + " "
    + config.bug_data["long_description"].fillna("")
).str.strip()

#Clean HTML and log noise
print(f"\n{utils.color_text('Cleaning text data... Please wait.', utils.YELLOW + utils.BOLD)}")
config.bug_data["text"] = config.bug_data["text"].astype(str).apply(clean_bug_text)
print(f"\n{utils.color_text('Text cleaning complete!', utils.GREEN + utils.BOLD)}")

#Extra metadata features showing urgency
crash_pattern = r"|".join(CRASH_KEYWORDS)
#Extract metadata features using efficient, vectorized pandas string methods
config.bug_data["text_length"] = config.bug_data["text"].str.len().fillna(0).astype(int)
config.bug_data["exclamation_count"] = (
    config.bug_data["text"].str.count(r"!").fillna(0).astype(int)
)
#Vectorized keyword check (no slow .apply() or python loops)
config.bug_data["has_crash_keyword"] = (
    config.bug_data["text"]
    .str.contains(crash_pattern, case=False, na=False)
    .astype(int)
)

#Define explicit feature lists for scalability and maintenance
#Extract feature set (X) and target vector (y) cleanly
X = config.bug_data[FEATURE_COLUMNS].copy()
y = config.bug_data[TARGET_COLUMN].copy()

# Print target class distribution instead of raw print
print(f"\n{utils.color_text('[Target class distribution]:', utils.CYAN + utils.BOLD)}")
print(y.value_counts(dropna=False))


# =============================================================================================================
# Visualisation
# =============================================================================================================
#Frequency Plot of Severity based on Bug Category
severity_counts = config.bug_data["severity_rating"].value_counts()
plt.figure(figsize=(10, 6))
sns.barplot(x=severity_counts.index, y=severity_counts.values, palette='viridis')
plt.title('Frequency of Severity Categories')
plt.xlabel('Severity Category')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

#Plot of severity by environment
severity_by_environment = config.bug_data.groupby("environment")["severity_rating"].mean().sort_values(ascending=False)

#Bar Plot of Severity by Environment
plt.figure(figsize=(12, 6))
sns.barplot(x=severity_by_environment.index, y=severity_by_environment.values, palette='viridis')
plt.title('Mean Severity Rating by Environment')
plt.xlabel('Environment')
plt.ylabel('Mean Severity Rating')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

#Bar Plot of Priority by Environment
count = config.bug_data.groupby(["priority", "environment"]).size().reset_index(name="count")
count = count.pivot(index="priority", columns="environment", values="count")
print(f"\n{utils.color_text('[Priority by Environment]:', utils.CYAN + utils.BOLD)}")
print(count)
fig = px.bar(count, barmode="stack", title="Priority per Environment")
fig.update_layout(xaxis_title="Priority", yaxis_title="Count", xaxis_tickangle=-45)
category_order = ["critical", "high", "medium", "low"]
fig.update_xaxes(categoryorder="array", categoryarray=category_order)
fig.show()

#Plot of Priority Frequency
priority_counts = config.bug_data["priority"].value_counts()
plt.figure(figsize=(10, 6))
sns.barplot(x=priority_counts.index, y=priority_counts.values, palette='viridis')
plt.title('Frequency of Priority Categories')
plt.xlabel('Severity Category')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

#create chart of target role assignments with bug count ordered by priority
count = config.bug_data.groupby(["priority", "target_role"]).size().reset_index(name="count")
count = count.pivot(index="priority", columns="target_role", values="count")
print(f"\n{utils.color_text('[Target role assignments with bug count ordered by priority]:', utils.CYAN + utils.BOLD)}")
print(count)
fig = px.bar(count, barmode="stack", title="Target Role Assignments by Priority")
fig.update_layout(xaxis_title="Priority", yaxis_title="Count", xaxis_tickangle=-45)
category_order = ["critical", "high", "medium", "low"]
fig.update_xaxes(categoryorder="array", categoryarray=category_order)
fig.show()

environment_role = config.bug_data.groupby(["environment", "target_role"]).size().reset_index(name="count")
environment_role = environment_role.pivot(index="environment", columns="target_role", values="count")
print(f"\n{utils.color_text('[Environment Role]:', utils.CYAN + utils.BOLD)}")
print(environment_role)