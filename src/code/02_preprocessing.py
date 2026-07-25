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