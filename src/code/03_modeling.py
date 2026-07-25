# =============================================================================================================
# MACHINE LEARNING TRAINING PREPARATION & MULTI-MODAL PREPROCESSING PIPELINE
# Resolves internal project paths, establishes data preprocessing architectures, splits clean bug data into
# stratified train/test verification vectors, and structures text vectorization alongside categorical encoding.
# =============================================================================================================

# =====================================================================
# Core System & Data Processing Libraries
# =====================================================================
import os
import sys
import pandas as pd
import numpy as np

# =====================================================================
# Model Training & Pipeline Infrastructure
# =====================================================================
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# =====================================================================
# Scikit-Learn Feature Extraction & Data Preprocessing
# =====================================================================
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# =====================================================================
# Model Evaluation Metrics
# =====================================================================
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

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
# Data Loading Logic
# =====================================================================
if getattr(config, "bug_data", None) is not None:
        print("Bug data already loaded.")
else:
    config.bug_data_filled = pd.read_csv(os.path.join(config.PROCESSED_DATA_DIR, 'normalized_dataset_bugs.csv'))

# =====================================================================
# Relational Dimension Remapping & Column Normalization
# =====================================================================
# Load dimension metadata lookup tables
dim_environments = pd.read_csv(os.path.join(config.PROCESSED_DATA_DIR, 'dim_environments.csv'))
dim_domains = pd.read_csv(os.path.join(config.PROCESSED_DATA_DIR, 'dim_domains.csv'))
dim_categories = pd.read_csv(os.path.join(config.PROCESSED_DATA_DIR, 'dim_categories.csv'))
dim_tech_stack = pd.read_csv(os.path.join(config.PROCESSED_DATA_DIR, 'dim_tech_stacks.csv'))
dim_severities = pd.read_csv(os.path.join(config.PROCESSED_DATA_DIR, 'dim_severities.csv'))
dim_priorities = pd.read_csv(os.path.join(config.PROCESSED_DATA_DIR, 'dim_priorities.csv'))

# Translate IDs to names using map lookups
env_map = dict(zip(dim_environments['environment_id'], dim_environments['environment_name']))
dmn_map = dict(zip(dim_domains['domain_id'], dim_domains['domain_name']))
cat_map = dict(zip(dim_categories['category_id'], dim_categories['category_name']))
tes_map = dict(zip(dim_tech_stack['tech_stack_id'], dim_tech_stack['tech_stack_name']))
sev_map = dict(zip(dim_severities['severity_id'], dim_severities['severity_name']))
pri_map = dict(zip(dim_priorities['priority_id'], dim_priorities['priority_name']))

# Convert numerical IDs into human-readable categorical string headers
config.bug_data_filled["environment"] = config.bug_data_filled["environment_id"].map(env_map)
config.bug_data_filled["bug_domain"] = config.bug_data_filled["domain_id"].map(dmn_map)
config.bug_data_filled["bug_category"] = config.bug_data_filled["category_id"].map(cat_map)
config.bug_data_filled["tech_stack"] = config.bug_data_filled["tech_stack_id"].map(tes_map)
config.bug_data_filled["severity"] = config.bug_data_filled["severity_id"].map(sev_map)
config.bug_data_filled["priority"] = config.bug_data_filled["priority_id"].map(pri_map)

# =====================================================================
# Console Preparation
# =====================================================================
# Flush out previous command terminal print artifacts to make the report readable
utils.clear_console()

# =============================================================================================================
# Feature Engineering & Composite Metrics
# =============================================================================================================
# Calculate unified balanced index scale value using uniform integer divisions (floor division)
config.bug_data_filled["severity_priority"] = (config.bug_data_filled["severity_id"] + config.bug_data_filled["priority_id"]) // 2

# =====================================================================
# Feature Extraction Synthesis (NLP Text Synthesis)
# =====================================================================
# Concatenate unstructured summary components into a singular text array block
config.bug_data_filled["text"] = (
    config.bug_data_filled["title"].fillna("") +
    " " +
    config.bug_data_filled["description"].fillna("")
)

# =====================================================================
# Array Isolations (Independent & Dependent Matrices)
# =====================================================================
# Filter specific multivariable data elements intended for training inputs
x = config.bug_data_filled[
    [
        "text",
        "error_code",
        "bug_domain",
        "bug_category",
        "environment",
        "tech_stack"
    ]
]

# Set the combined label value array as the dependent target output variable
y = config.bug_data_filled["severity_priority"]

# =====================================================================
# Data Dimension Verification Logs
# =====================================================================
# Audit row counts representing distinct output targets
print(f"\n{utils.color_text('[Target class distributions]', utils.CYAN + utils.BOLD)}")
print(config.bug_data_filled["severity_priority"].value_counts().to_frame(name="Count"))

# Verify multi-modal dataset row and column shapes prior to splitting
print(f"\n{utils.color_text('[Feature matrix shape]', utils.CYAN + utils.BOLD)}")
print(config.bug_data_filled.shape)


# =====================================================================
# Stratified Dataset Partitioning
# =====================================================================
# Allocate an 80/20 train-test division split, maintaining matching target category densities
x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size = 0.2, #80/20 split
    random_state = 42,
    stratify = y
)

# =====================================================================
# Preprocessing Data Pipeline Architecture
# =====================================================================
# Build automatic transformations matching input data structural formats
preprocessor = ColumnTransformer(
    transformers = [
         # Sub-Pipeline A: Numerical Text Vectorization via TF-IDF
        (
          "text",
         TfidfVectorizer(
             stop_words = 'english', #Remove common words
             max_features = 3000, #Keeps 3000 most informative words
             ngram_range = (1, 2), #Uses single and two-word phrases
             min_df = 2 #Ignores words that only appear once)
         ),
         "text"
        ),
        # Sub-Pipeline B: Discrete Categorical One-Hot Conversion Encoding
        (
            "categorical",
            # Convert text values into numeric dummy flag arrays, ignoring runtime mismatches
            OneHotEncoder(handle_unknown="ignore"),
            [
                "error_code",           # Core Fix: Swapped out "text" column for missing error_code item
                "bug_domain",
                "bug_category",
                "environment",
                "tech_stack",
            ]
        )
    ]
)

# =====================================================================
# Logistic Regression Model Architecture
# =====================================================================
# Construct an end-to-end execution pipeline binding preprocessing stages to a linear classifier
lr_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000, random_state=42))
])

# Fit the underlying feature matrices and optimization parameters to training vectors
lr_pipeline.fit(x_train, y_train)

# Generate category predictions against the isolated test dataset split
lr_predictions = lr_pipeline.predict(x_test)

# =====================================================================
# Logistic Regression Metrics Evaluation Logs
# =====================================================================
# Output descriptive, colorized performance report headings for the linear architecture
print(f"\n{utils.color_text('=== LOGISTIC REGRESSION BENCHMARK REPORT ===', utils.CYAN + utils.BOLD)}")

# Log raw categorical accuracy calculation score results
print(f"\n{utils.color_text('[Model Accuracy]', utils.BOLD)}")
print(f"{accuracy_score(y_test, lr_predictions):.4f}")

# Output localized precision, recall, and f1-score evaluations per label class
print(f"\n{utils.color_text('[Classification Metrics Detail]', utils.BOLD)}")
print(classification_report(y_test, lr_predictions))

# Output raw frequency matrix mappings detailing correct classifications vs false indicators
print(f"\n{utils.color_text('[Confusion Matrix Contingency Table]', utils.BOLD)}")
print(confusion_matrix(y_test, lr_predictions))


# =====================================================================
# Random Forest Model Architecture
# =====================================================================
# Construct an ensemble tree pipeline utilizing identical preprocessing transformations
rf_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=200,      # Generate a forest ensemble of 200 distinct decision tree branches
        random_state=42,       # Establish an execution state seed variable to replicate findings
        max_depth=None          # Expand leaf nodes dynamically until elements are completely homogeneous
    ))
])

# Train ensemble estimators utilizing uniform random bootstrap samples from historical records
rf_pipeline.fit(x_train, y_train)

# Generate category predictions from majority voting calculations across the tree nodes
rf_predictions = rf_pipeline.predict(x_test)

# =====================================================================
# Random Forest Metrics Evaluation Logs
# =====================================================================
# Output descriptive, colorized performance report headings for the ensemble tree architecture
print(f"\n{utils.color_text('=== RANDOM FOREST BENCHMARK REPORT ===', utils.GREEN + utils.BOLD)}")

# Log raw categorical accuracy calculation score results
print(f"\n{utils.color_text('[Model Accuracy]', utils.BOLD)}")
print(f"{accuracy_score(y_test, rf_predictions):.4f}")

# Output localized precision, recall, and f1-score evaluations per label class
print(f"\n{utils.color_text('[Classification Metrics Detail]', utils.BOLD)}")
print(classification_report(y_test, rf_predictions))

# Output raw frequency matrix mappings detailing correct classifications vs false indicators
print(f"\n{utils.color_text('[Confusion Matrix Contingency Table]', utils.BOLD)}")
print(confusion_matrix(y_test, rf_predictions))