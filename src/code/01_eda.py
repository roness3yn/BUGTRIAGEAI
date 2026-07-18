# =============================================================================================================
# MACHINE LEARNING MODEL PIPELINE & EXPLORATORY DATA ANALYSIS (EDA)
# Initializes environment paths, imports scientific and ML libraries, configures plotting states,
# and performs a detailed structural audit of the incoming bug dataset to terminal console.
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
from src.utils import utils

# =====================================================================
# Visual Plotting Configuration
# =====================================================================
# Apply a clean, structured canvas style for generated graphs
plt.style.use('seaborn-v0_8-whitegrid')

# Establish a default aspect ratio size (10 inches wide by 6 inches high) for standard plots
plt.rcParams['figure.figsize'] = [10, 6]

# =====================================================================
# Console Preparation
# =====================================================================
# Flush out previous command terminal print artifacts to make the report readable
utils.clear_console()

# =====================================================================
# Data Loading Engine
# =====================================================================
# Load the cleaned tracking dataset from the designated processed file repository
config.bug_data = pd.read_csv(os.path.join(config.PROCESSED_DATA_DIR, 'normalized_dataset_bugs.csv'))

# Log data loading success confirmation
print(f"\n{utils.color_text('Data loaded successfully!', utils.GREEN + utils.BOLD)}")

# =====================================================================
# Exploratory Data Analysis (EDA) Console Output
# =====================================================================

# Output dataframe dimensions (rows, columns)
print(f"\n{utils.color_text('[Data shape]', utils.CYAN + utils.BOLD)}")
print(config.bug_data.shape)

# Output all structural column feature headers
print(f"\n{utils.color_text('[Data columns]', utils.CYAN + utils.BOLD)}")
print(config.bug_data.columns)

# Output datatype schemas wrapped in a clean dataframe container
print(f"\n{utils.color_text('[Data types]', utils.CYAN + utils.BOLD)}")
print(config.bug_data.dtypes.to_frame(name='Data Type'))

# Output cumulative missing value metrics categorized per column field
print(f"\n{utils.color_text('[Missing values]', utils.CYAN + utils.BOLD)}")
print(config.bug_data.isnull().sum().to_frame(name='Missing Values'))

# Output complete numerical percentile distributions and categorical statistics summary
print(f"\n{utils.color_text('[Data description]', utils.CYAN + utils.BOLD)}")
print(config.bug_data.describe(include='all'))

# Output the initial 5 structural entry records
print(f"\n{utils.color_text('[First 5 rows of the data]', utils.CYAN + utils.BOLD)}")
print(config.bug_data.head())

# Output the absolute concluding 5 structural entry records
print(f"\n{utils.color_text('[Last 5 rows of the data]', utils.CYAN + utils.BOLD)}")
print(config.bug_data.tail())

# Output comprehensive memory usage, indexing metrics, and explicit row limits details
print(f"\n{utils.color_text('[Data info]', utils.CYAN + utils.BOLD)}")
print(config.bug_data.info())

# Output a randomized distribution sample of 5 items to audit random variance
print(f"\n{utils.color_text('[Data sample]', utils.CYAN + utils.BOLD)}")
print(config.bug_data.sample(5))