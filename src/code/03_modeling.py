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
from mord import LogisticAT
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from lightgbm import LGBMClassifier

# =====================================================================
# Scikit-Learn Feature Extraction & Data Preprocessing
# =====================================================================
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

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
from src.features.CONSTANS import CRASH_KEYWORDS, FEATURE_COLUMNS, TARGET_COLUMN, CUSTOM_STOP_WORDS

# =====================================================================
# Data Loading Logic
# =====================================================================
if getattr(config, "bug_data", None) is not None:
        print(f"\n{utils.color_text('normalized_dataset_bugs.csv already loaded...', utils.YELLOW)}")
else:
    config.bug_data = pd.read_csv(os.path.join(config.PROCESSED_DATA_DIR, 'normalized_dataset_bugs.csv'))

# =====================================================================
# Console Preparation
# =====================================================================
# Flush out previous command terminal print artifacts to make the report readable
utils.clear_console()


# =====================================================================
# Define test/train split
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

# =====================================================================
# Add "description" to standard English stop words
# =====================================================================
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


# =====================================================================
# Logistic Regression Model Architecture
# =====================================================================
#set class weights
custom_weights = {
    "1": 1.5,
    "2": 1,
    "3": 1.5
    }
#Ordinal Logistic Regression
lr_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticAT(max_iter = 5000))
])

#apply weights
sample_weights = compute_sample_weight(
    class_weight = 'balanced',
    y = y_train
)

#sample_weights = y_train.map(custom_weights).values

#Train Model
lr_pipeline.fit(x_train, y_train, classifier__sample_weight = sample_weights)

#Test Model
lr_predictions = lr_pipeline.predict(x_test)

#Evaluate Model
print(f"\n{utils.color_text('[Ordinal Logistic Regression]', utils.CYAN + utils.BOLD)}")
print(f"{utils.color_text('[Accuracy:]', utils.CYAN + utils.BOLD)}")
print(accuracy_score(y_test, lr_predictions))
print(classification_report(y_test, lr_predictions))
print(confusion_matrix(y_test, lr_predictions))
#confidence score
print(lr_pipeline.predict_proba(x_test))

# =====================================================================
# Random Forest Model Architecture
# =====================================================================
#Random Forest
rf_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        class_weight = 'balanced_subsample',
        n_estimators = 100,
        random_state = 42,
        max_depth = 20,
        n_jobs = -1
    ))
])

#Train
rf_pipeline.fit(x_train, y_train)

#Test
rf_predictions = rf_pipeline.predict(x_test)

#Evaluate
print(f"\n{utils.color_text('[Random Forest]', utils.CYAN + utils.BOLD)}")
print(f"{utils.color_text('[Accuracy]', utils.CYAN + utils.BOLD)}")
print(accuracy_score(y_test, rf_predictions))
print(classification_report(y_test, rf_predictions))
print(confusion_matrix(y_test, rf_predictions))


calibrated_weights = {
    1: 9,
    2: 1,
    3: 6
}

# =====================================================================
# LightGBM pipeline
# =====================================================================
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

#Train model
lgb_pipeline.fit(x_train, y_train)

#Test model
lgb_predictions = lgb_pipeline.predict(x_test)

#Evaluate
print(f"\n{utils.color_text('[LightGBM]', utils.CYAN + utils.BOLD)}")
print(f"{utils.color_text('[Accuracy]', utils.CYAN + utils.BOLD)}")
print(accuracy_score(y_test, lgb_predictions))
print(classification_report(y_test, lgb_predictions))
print(confusion_matrix(y_test, lgb_predictions))

# 1. Extract feature names from the preprocessor steps in the exact order generated
text_features = lr_pipeline.named_steps['preprocessor'] \
                          .named_transformers_['text_tf_idf'] \
                          .get_feature_names_out()

cat_features = lr_pipeline.named_steps['preprocessor'] \
                         .named_transformers_['categorical'] \
                         .get_feature_names_out()

num_features = lr_pipeline.named_steps['preprocessor'] \
                         .named_transformers_['numeric'] \
                         .get_feature_names_out()

all_feature_names = np.concatenate([text_features, cat_features, num_features])

#Extract linear coefficients from the LogisticAT classifier
# mord stores coefficients in .coef_ (1D array matching feature space)
coefficients = lr_pipeline.named_steps['classifier'].coef_

#Create a DataFrame mapping features to their directional impact
feature_impact_df = pd.DataFrame({
    'Feature': all_feature_names,
    'Coefficient': coefficients,
    'Absolute_Impact': np.abs(coefficients) # Measure overall strength regardless of direction
}).sort_values(by='Absolute_Impact', ascending=False)

#Separate into top drivers for High and Low severity
print(f"\n{utils.color_text('=== TOP 15 MOST INFLUENTIAL FEATURES (ORDINAL LOGISTIC) ===', utils.CYAN + utils.BOLD)}")
print(feature_impact_df.head(50)[['Feature', 'Coefficient']].to_string(index=False))