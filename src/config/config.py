# config.py
import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../data"))
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

# App configurations
DEBUG_MODE = True
DATABASE_URL = "sqlite:///bug_triage.db"

#Global variables
bug_data = None
bug_data_corrected = None
bug_data_filled = None