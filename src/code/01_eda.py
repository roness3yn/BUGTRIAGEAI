import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# If config.py is two levels up, add it to the path so python can find it
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../config")))
import config
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

#Settings
plt.style.use('seaborn-v0_8-whitegrid')

plt.rcParams['figure.figsize'] = [10, 6]

#Load data
config.bug_data = pd.read_csv(os.path.join(config.PROCESSED_DATA_DIR, 'fact_bugs.csv'))
print("\n\nData loaded successfully.")
print("==================================\n\n")
print("Data shape:", config.bug_data.shape)
print("==================================\n\n")
print("Data columns:", config.bug_data.columns)
print("==================================\n\n")
print("Data types:\n", config.bug_data.dtypes)
print("==================================\n\n")
print("Missing values:\n", config.bug_data.isnull().sum())
print("==================================\n\n")
print("Data description:\n", config.bug_data.describe(include='all'))
print("==================================\n\n")
print("First 5 rows of the data:\n", config.bug_data.head())
print("==================================\n\n")
print("Last 5 rows of the data:\n", config.bug_data.tail())
print("==================================\n\n")
print("Data info:\n", config.bug_data.info())
print("==================================\n\n")
print("Data sample:\n", config.bug_data.sample(5))