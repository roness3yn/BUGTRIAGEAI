import os
import pandas as pd

# 1. Setup dynamic paths relative to this script's location
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define input path (pointing to data/raw)
input_file = os.path.abspath(os.path.join(script_dir, "../raw/bug_dataset_with_priority_and_severity.csv"))

# Define output directory (pointing to data/processed)
output_dir = os.path.abspath(os.path.join(script_dir, "../processed"))

bug_data = pd.read_csv(os.path.join(output_dir, 'bug_dataset_with_priority_and_severity.csv"'))  
#Replace string with int ratings
bug_data["severity"] = bug_data["severity"].replace({"Low": 1, "Medium": 2, "High": 3, "Critical": 4})
bug_data["priority"] = bug_data["priority"].replace({"Low": 1, "Normal": 2, "High": 3, "Urgent": 4})

#Recode severity
def calculate_severity(row):
    score = 0
    # Environment
    if row["environment"] == "Production":
        score += 2
    elif row["environment"] == "Staging":
        score += 1
    # Bug Category
    if row["bug_category"] == "Security Vulnerability":
        score += 4
    elif row["bug_category"] in [
        "Memory Leak",
        "Database Bug",
        "Concurrency Bug",
        "Authentication Bug",
        "Authorization Bug"
    ]:
        score += 3
    elif row["bug_category"] in [
        "Backend Logic Bug",
        "Performance Bug",
        "API Bug",
        "Deployment Bug",
        "Cloud Configuration Bug"
    ]:
        score += 2
    else:
        score += 1
    # Error Code
    if row["error_code"] >= 500:
        score += 2
    elif row["error_code"] >= 400:
        score += 1
    return score

#Apply recode
bug_data["severity_score"] = bug_data.apply(
    calculate_severity,
    axis=1
)

def severity_class(score):
    if score <= 2:
        return 1      # Low
    elif score <= 4:
        return 2      # Medium
    elif score <= 6:
        return 3      # High
    else:
        return 4      # Critical

bug_data["severity"] = bug_data["severity_score"].apply(severity_class)

#Recode priority
def priority_class(row):
    score = row["severity"]
    if row["environment"] == "Production":
        score += 1
    if score >= 5:
        return 4      # P1 Critical
    elif score == 4:
        return 3      # P2 High
    elif score == 3:
        return 2      # P3 Normal
    else:
        return 1      # P4 Low

#Apply recode
bug_data["priority"] = bug_data.apply(
    priority_class,
    axis=1
)

#Export new file
bug_data_corrected = bug_data
bug_data_corrected.to_csv(Data_Path + "bug_dataset_with_priority_and_severity_corrected.csv", index=False)