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
import numpy as np

# =====================================================================
# Data Visualization Libraries
# =====================================================================
import matplotlib.pyplot as plt
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
from src.features import transformers
from src.visualization import plots
from src.utils import utils

# =====================================================================
# Data Loading Logic
# =====================================================================
if getattr(config, "bug_data", None) is not None:
        print("Bug data already loaded.")
else:
    config.bug_data = pd.read_csv(os.path.join(config.PROCESSED_DATA_DIR, 'normalized_dataset_bugs.csv'))
#==================================================
# Business Rule Transformations
#==================================================
# Calculate the raw severity score for each row based on business rules
config.bug_data["severity_score"] = config.bug_data.apply(transformers.calculate_severity_score, axis=1)
# Map the numerical severity score to a discrete severity class (1-4)
config.bug_data["severity"] = config.bug_data["severity_score"].apply(transformers.severity_class)
# Recode priority based on underlying categorical impact mappings
config.bug_data["priority"] = config.bug_data.apply(transformers.priority_class,axis=1)

#===========================
#   Terminal Console Reset
#===========================
# Clear previous log artifacts before presenting analytics reports
utils.clear_console()

#===========================
# Persistent Export Setup
#===========================
# Reference and save the enriched dataset containing calculated operational values
config.bug_data_corrected = config.bug_data
config.bug_data_corrected.to_csv(
   os.path.join(config.PROCESSED_DATA_DIR, 'bug_dataset_with_priority_and_severity_corrected.csv'), 
   index=False
)

# =============================================================================================================
#   Relational Dimension Table Loading & Mapping Dictionaries
#===============================================================
config.dim_environments = pd.read_csv(os.path.join(config.PROCESSED_DATA_DIR, 'dim_environments.csv'))
config.dim_domains = pd.read_csv(os.path.join(config.PROCESSED_DATA_DIR, 'dim_domains.csv'))
config.dim_categories = pd.read_csv(os.path.join(config.PROCESSED_DATA_DIR, 'dim_categories.csv'))

# Create mapping lookups using zip compression schemas
env_map = dict(zip(config.dim_environments['environment_id'], config.dim_environments['environment_name']))
dmn_map = dict(zip(config.dim_domains['domain_id'], config.dim_domains['domain_name']))
cat_map = dict(zip(config.dim_categories['category_id'], config.dim_categories['category_name']))

# Static manual mappings for core rating scales
severity_map = {1: 'Low', 2: 'Medium', 3: 'High', 4: 'Critical'}
priority_map = {1: 'Low', 2: 'Normal', 3: 'High', 4: 'Urgent'}
environment = {1: 'Development', 2: 'Production', 3: 'Staging'}

# =============================================================================================================
# Descriptive Statistics & Data Distribution Reports
# =============================================================================================================

# Volume metrics reporting
print(f"\n{utils.color_text('[Number of bugs]', utils.CYAN + utils.BOLD)}")
print(len(config.bug_data))

print(f"\n{utils.color_text('[Number of errors per error_code]', utils.CYAN + utils.BOLD)}")
print(config.bug_data["error_code"].value_counts().to_frame(name="Count").sort_index())

# Severity metric distribution
print("\n[Number of errors per severity]")
print(config.bug_data["severity"].value_counts().rename(index=severity_map).to_frame(name="Count").sort_index())

# Priority metric distribution
print(f"\n{utils.color_text('[Number of errors per priority rating]', utils.CYAN + utils.BOLD)}")
print(config.bug_data["priority"].value_counts().rename(index=priority_map).to_frame(name="Count").sort_index())

# Environment metric distribution
print(f"\n{utils.color_text('[Number of errors per environment]', utils.CYAN + utils.BOLD)}")
print(config.bug_data["environment_id"].value_counts().rename(index=environment).to_frame(name="Count").sort_index())

# =============================================================================================================
# Cross-Tabulation & Categorical Aggregations
# =============================================================================================================

# Aggregations grouped by operational Bug Category
print(f"\n{utils.color_text('[Mean Priority by Category]', utils.CYAN + utils.BOLD)}")
print(config.bug_data.groupby("category_id")["priority"].mean().rename(index=cat_map).to_frame(name="Avg Priority"))

print(f"\n{utils.color_text('[Mean Severity by Category]', utils.CYAN + utils.BOLD)}")
print(config.bug_data.groupby("category_id")["severity"].mean().rename(index=cat_map).to_frame(name="Avg Severity"))

# Aggregations grouped by Runtime Environment
print(f"\n{utils.color_text('[Mean Priority by Environment]', utils.CYAN + utils.BOLD)}")
print(config.bug_data.groupby("environment_id")["priority"].mean().rename(index=env_map).to_frame(name="Avg Priority"))

print(f"\n{utils.color_text('[Mean Severity by Environment]', utils.CYAN + utils.BOLD)}")
print(config.bug_data.groupby("environment_id")["severity"].mean().rename(index=env_map).to_frame(name="Avg Severity"))

# Aggregations grouped by Technical System Domain
print(f"\n{utils.color_text('[Mean Priority by Domain]', utils.CYAN + utils.BOLD)}")
print(config.bug_data.groupby("domain_id")["priority"].mean().rename(index=dmn_map).to_frame(name="Avg Priority"))

print(f"\n{utils.color_text('[Mean Severity by Domain]', utils.CYAN + utils.BOLD)}")
print(config.bug_data.groupby("domain_id")["severity"].mean().rename(index=dmn_map).to_frame(name="Avg Severity"))

# =============================================================================================================
# Data Visualization Pipeline
# =============================================================================================================
# Render distribution metrics charts to graphic engines
plots.plot_mean_severity_by_category(config.bug_data, cat_map)
plots.plot_median_metric_by_environment(config.bug_data, "severity", "Median Severity by Environment", env_map)
plots.plot_median_metric_by_environment(config.bug_data, "priority", "Median Priority by Environment", env_map)

# Render bivariate statistical matrix showing cross-correlation profiles
plots.plot_severity_priority_correlation(config.bug_data)

# =============================================================================================================
# Data Integrity Audit & Missing Value Imputation
# =============================================================================================================
# Verify structural data consistency profile
if config.bug_data.isna().values.any():
    print(f"\n{utils.color_text('[Summary of missing values before imputation]', utils.YELLOW + utils.BOLD)}")
    print(config.bug_data.isna().sum().to_frame(name="Missing Count").sort_values(by="Missing Count", ascending=False))
else:
    print(utils.color_text("There are no missing values in the dataset", utils.GREEN))

# Impute text category tags to isolate unpopulated feature spaces
config.bug_data_filled = config.bug_data.fillna("Unknown")

# Final verification audit check on feature gaps
print(f"\n{utils.color_text('[Summary of missing values after imputation]', utils.GREEN + utils.BOLD)}")
print(config.bug_data_filled.isna().sum().to_frame(name="Missing Count").sort_values(by="Missing Count", ascending=False))

# =============================================================================================================
# Data Deduplication Audit
# =============================================================================================================
# Execute complete transaction uniqueness tests
if config.bug_data_filled.duplicated().any():
    print(f"\n{utils.color_text('[Summary of duplicate values after imputation]', utils.RED + utils.BOLD)}")
    print(config.bug_data_filled.duplicated().sum())
else:
    print(f"\n{utils.color_text('There are no duplicate values in the dataset', utils.GREEN)}")