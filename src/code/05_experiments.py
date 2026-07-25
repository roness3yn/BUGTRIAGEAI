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
from sklearn.utils.class_weight import compute_sample_weight

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
from src.features.transformers import classify_environment, assign_priority, assign_target_role, assign_escalation_level,clean_bug_text

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


config.bug_data["escalation_level"] = config.bug_data.apply(assign_escalation_level, axis=1)
print(config.bug_data["escalation_level"].value_counts())

config.bug_data["environment"] = config.bug_data.apply(classify_environment, axis = 1)
# 1. Define explicit priority lookup matrix
PRIORITY_MAP = {
    # Severity 3 (High)
    (3, "production"): "critical",
    (3, "staging"):    "critical",
    (3, "development"): "high",
    
    # Severity 2 (Medium)
    (2, "production"): "medium",
    (2, "staging"):    "medium",
    (2, "development"): "low",
    
    # Severity 1 (Low)
    (1, "production"): "medium",
    (1, "staging"):    "low",
    (1, "development"): "low",
}

# 2. Fast mapping across rows using zip
config.bug_data["priority"] = [
    PRIORITY_MAP.get((sev, env), "low")  # "low" acts as default fallback
    for sev, env in zip(config.bug_data["severity_rating"], config.bug_data["environment"])
]
config.bug_data["target_role"] = config.bug_data.apply(assign_target_role, axis = 1)
config.bug_data["escalation_level"] = config.bug_data.apply(assign_escalation_level, axis=1)
config.bug_data["confidence_score"] = lr_pipeline.predict_proba(x).max(axis=1)

#Generate bug assignment report
report_columns = [
    "bug_id",
    "creation_date",
    "product_name",
    "component_name",
    "environment",
    "severity_rating",
    "priority",
    "target_role",
    "escalation_level",
    "confidence_score"
]

bug_triage_report = config.bug_data[report_columns].copy()

print(bug_triage_report.head(10))

bug_triage_report.to_csv(
    "future_bug_triage_report.csv",
    index=False
)

def bug_report(new_bug):
  """
  Generates a bug triage report for incoming bugs
  Parameters
  new_bug: pd.DataFrame
    DataFrame containing one new bug
  Returns
    triage_report: pd.DataFrame
      DataFrame containing the triage report for the incoming bug
  """
  defaults = {
    "product_name": "Unknown Product",
    "component_name": "General",
    "environment": "Unknown Environment",
    "short_description": "",
    "long_description": ""
  }

  for column, default in defaults.items():
      if column not in new_bug.columns:
          new_bug[column] = default

  #Create combined text description
  new_bug["text"] = (
    new_bug["short_description"].fillna("") +
    " " + new_bug["long_description"].fillna("")
  )

  #Clean HTML and log noise
  print("Cleaning text data... Please wait.")
  new_bug["text"] = new_bug["text"].apply(clean_bug_text)
  print("Text cleaning complete!")

  #Extra metadata features showing urgency
  new_bug['text_length'] = new_bug['text'].str.len()
  new_bug['exclamation_count'] = new_bug['text'].str.count('!')
  crash_words = ['crash', 'blocker', 'nullpointer', 'down', 'broken', 'fatal']
  new_bug['has_crash_keyword'] = new_bug['text'].str.lower().apply(
    lambda x: 1 if any(w in x for w in crash_words) else 0
  )

  x = new_bug[
      [
        "text",
        "product_name",
        "text_length",
        "exclamation_count",
        "has_crash_keyword",
        "component_name"
      ]
    ]

  #Predict severity
  new_bug["severity_rating"] = lr_pipeline.predict(x)

  #confidence score
  new_bug["confidence_score"] = lr_pipeline.predict_proba(x).max(axis=1)

  #Assign Environment
  new_bug["environment"] = new_bug.apply(classify_environment, axis = 1)

  #Generate Priority
  new_bug["priority"] = [
    PRIORITY_MAP.get((sev, env), "low")  # "low" acts as default fallback
    for sev, env in zip(new_bug["severity_rating"], new_bug["environment"])
]
  #new_bug.apply(assign_priority, axis = 1)

  #Generate Target Role
  new_bug["target_role"] = new_bug.apply(assign_target_role, axis = 1)

  #Assign Escalation Level
  new_bug["escalation_level"] = new_bug.apply(assign_escalation_level, axis=1)

  #Final report
  report_columns = [
        "bug_id",
        "short_description",
        "component_name",
        "severity_rating",
        "environment",
        "priority",
        "target_role",
        "escalation_level",
        "confidence_score"
  ]

  #do not return empty columns
  report_columns = [
      column for column in report_columns
      if column in new_bug.columns
  ]

  return new_bug[report_columns]

#Generate report for incoming bug
new_bug = pd.DataFrame({
    "product_name": ["Customer Portal"],
    "component_name": ["Database"],
    "environment": ["production"],
    "short_description": ["Database queries timing out"],
    "long_description": ["Customers experience major delays during checkout because several database queries exceed the timeout threshold."],
})

report = bug_report(new_bug)

print(f"\n{utils.color_text('[Bug Report:]', utils.CYAN + utils.BOLD)}")
print(report)