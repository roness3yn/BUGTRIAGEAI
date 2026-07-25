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
from sklearn.model_selection import cross_val_score

# =====================================================================
# Scikit-Learn Feature Extraction & Data Preprocessing
# =====================================================================
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from mord import LogisticAT
from lightgbm import LGBMClassifier

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
from src.features.CONSTANS import CRASH_KEYWORDS, FEATURE_COLUMNS, TARGET_COLUMN, CUSTOM_STOP_WORDS

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

# =====================================================================
# Array Isolations (Independent & Dependent Matrices)
# =====================================================================
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

x = config.bug_data[FEATURE_COLUMNS].copy()
y = config.bug_data[TARGET_COLUMN].copy()

x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size = 0.2, #80/20 split
    random_state = 42,
    stratify = y
)

#Pipelines per feature type (includes imputation to prevent NaN crashes)
text_transformer = TfidfVectorizer(
    stop_words=list(CUSTOM_STOP_WORDS),
    max_features=3000,
    ngram_range=(1, 2),
    min_df=10,
    max_df=0.7,
)

categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="constant", fill_value="unknown")),
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=True)),
])

numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

#Master Preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ("text_tf_idf", text_transformer, "text"),
        ("categorical", categorical_transformer, ["product_name", "component_name"]),
        ("numeric", numeric_transformer, ["text_length", "exclamation_count", "has_crash_keyword"]),
    ]
)

#Ordinal Logistic Regression
lr_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticAT(max_iter = 5000))
])

lgb_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LGBMClassifier(
        objective = "multiclass",
        class_weight = 'balanced',
        n_estimators = 300,
        learning_rate = 0.04,
        max_depth = 6,
        min_child_samples = 25,
        num_leaves = 31,
        random_state = 42,
        n_jobs = -1,
        verbose = -1
    ))
])

# =====================================================================
# Logistic Regression Cross-Validation
# =====================================================================
# Output descriptive, colorized performance report headings for the ensemble tree architecture
print(f"\n{utils.color_text('=== Logistic Regression Cross-validation ===', utils.GREEN + utils.BOLD)}")

#Calculate cross validation based on Logistic Regression execution
lr_scores = cross_val_score(
    lr_pipeline,
    x,
    y,
    cv = 5,
    scoring = "accuracy"
)

#Print cross validation scores
print(f"\n{utils.color_text('[Logistic Regression Cross-validation accuracy:]', utils.CYAN + utils.BOLD)}")
print(lr_scores)
print(f"\n{utils.color_text('[Mean accuracy:]', utils.CYAN + utils.BOLD)}")
print(lr_scores.mean())


# =====================================================================
# Random Forest Cross-Validation
# =====================================================================
# Output descriptive, colorized performance report headings for the ensemble tree architecture
print(f"\n{utils.color_text('=== Random Forest Cross-validation ===', utils.GREEN + utils.BOLD)}")

#Calculate cross validation based on Random Forest execution
scores = cross_val_score(
    lgb_pipeline,
    x,
    y,
    cv = 5,
    scoring = "accuracy"
)

#Print cross validation scores
print(f"\n{utils.color_text('[LGBM Cross-validation accuracy:]', utils.CYAN + utils.BOLD)}")
print(scores)
print(f"\n{utils.color_text('[Mean accuracy:]', utils.CYAN + utils.BOLD)}")
print(scores.mean())