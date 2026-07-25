# =====================================================================
# Core System & Data Processing Libraries
# =====================================================================
import os
import sys
import pandas as pd
import zipfile

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
from src.features.transformers import severity_rating, classify_environment, assign_target_role
from src.features.CONSTANS import PRIORITY_MAP

# =====================================================================
# Console Preparation
# =====================================================================
# Flush out previous command terminal print artifacts to make the report readable
utils.clear_console()

# 1. Get the directory of dataTune.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Get the absolute path to the 'src/config' folder
#    (Goes up one level to root, then down into src/config)
config_dir = os.path.abspath(os.path.join(current_dir, "../../src/config"))

# Define input path (pointing to data/raw)
input_file_eclipse = os.path.join(config.RAW_DATA_DIR,"eclipse_bug_report_data.csv")
input_file_freedesktop = os.path.join(config.RAW_DATA_DIR,"freedesktop_bug_report_data.csv")
input_file_gcc = os.path.join(config.RAW_DATA_DIR,"gcc_bug_report_data.csv")
input_file_gnome = os.path.join(config.RAW_DATA_DIR,"gnome_bug_report_data.csv")
input_file_mozilla = os.path.join(config.RAW_DATA_DIR,"mozilla_bug_report_data.csv")
input_file_winehq = os.path.join(config.RAW_DATA_DIR,"winehq_bug_report_data.csv")

# Define output directory (pointing to data/processed)
output_dir = config.PROCESSED_DATA_DIR


# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# =============================================================
# Load the dataset
# =============================================================
# Join the items into a nicely formatted string
file_list_str = "\n  - ".join(str(f) for f in [input_file_eclipse, input_file_freedesktop, input_file_gcc, input_file_gnome, input_file_mozilla, input_file_winehq])
print(f"\n{utils.color_text('Reading source files from:', utils.CYAN + utils.BOLD)}")
print(f"  - {file_list_str}")

df_eclipse = pd.read_csv(input_file_eclipse)
df_freedesktop = pd.read_csv(input_file_freedesktop)
df_gcc = pd.read_csv(input_file_gcc)
df_gnome = pd.read_csv(input_file_gnome)
df_mozilla = pd.read_csv(input_file_mozilla)
df_winehq = pd.read_csv(input_file_winehq)

# ============================================================================
# Combine dataframes into a single DataFrame and store it in the config module
# ============================================================================
config.bug_data = pd.concat([df_eclipse, df_freedesktop, df_gcc, df_gnome, df_mozilla, df_winehq], ignore_index=True)
config.bug_data.to_csv(os.path.join(config.RAW_DATA_DIR,"bug_dataset.csv"), index=False)
#show distribution of new values
print(f"\n{utils.color_text('[Shape]', utils.CYAN + utils.BOLD)}")
print(config.bug_data.shape)

# =============================================================
# In-place drop (Cleaner & No Re-assignment)
# =============================================================
config.bug_data.dropna(inplace=True)

# =============================================================
# Apply recode
# =============================================================
config.bug_data["severity_rating"] = config.bug_data.apply(
    severity_rating,
    axis=1
)

# =============================================================
# Remove severity_category not set value
# =============================================================
config.bug_data = config.bug_data.query("severity_category != 'not set'")

# =============================================================
# Show distribution of new values
# =============================================================
print(f"\n{utils.color_text('[Severity Rating]', utils.CYAN + utils.BOLD)}")
print(config.bug_data["severity_rating"].value_counts().sort_index().reset_index())

# =============================================================
# Displays as percentages (e.g., 0.45 -> 45%)
# =============================================================
print(f"\n{utils.color_text('[Severity Rating percentages]', utils.CYAN + utils.BOLD)}")
# 1. Get percentages sorted by severity ID
prec = config.bug_data["severity_rating"].value_counts(normalize=True).sort_index().reset_index()
# 2. Multiply only the proportion column by 100 and add '%'
value_col = "proportion" if "proportion" in prec.columns else "severity_rating"
# (In older pandas, the column name is 'severity_rating'; in pandas 2.0+, it's 'proportion')
prec[value_col] = (prec[value_col] * 100).map("{:.1f}%".format)
# 3. Rename columns cleanly
prec.columns = ["Severity Rateing", "Percentage"]
print(prec.to_string(index=False))

# =============================================================
# include Missing / NaN Values
# =============================================================
print(f"\n{utils.color_text('[Include Missing / NaN Values]', utils.CYAN + utils.BOLD)}")
print(config.bug_data["severity_rating"].value_counts(dropna=False))

# =============================================================
# Clean table layout with headers
# =============================================================
summary = config.bug_data["severity_rating"].value_counts().sort_index().reset_index()
summary.columns = ["Severity", "Count"]
print(f"\n{utils.color_text('[Clean table]', utils.CYAN + utils.BOLD)}")
print(summary.to_string(index=False))

print(f"\n{utils.color_text('[Data shape]', utils.CYAN + utils.BOLD)}")
print(config.bug_data.shape)

# =============================================================
# Reassign products with less than 100 reports
# =============================================================
product_counts = config.bug_data["product_name"].value_counts()
rare_products = product_counts[product_counts < 100].index
config.bug_data["product_name"] = config.bug_data["product_name"].apply(lambda x: "Other" if x in rare_products else x)
print(f"\n{utils.color_text('[Product Name]', utils.CYAN + utils.BOLD)}")
print(config.bug_data["product_name"].value_counts().rename("Count").reset_index().rename(columns={"product_name": "Product Name"}).to_string(index=False))

# =============================================================
# Combine both description columns
# =============================================================
config.bug_data["text"] = (
    config.bug_data["short_description"]
    .str.cat(config.bug_data["long_description"], sep=" ", na_rep="")
    .str.lower()
    .str.strip()
)

# =============================================================
# Combine both description columns
# =============================================================
config.bug_data["environment"] = config.bug_data["text"].apply(classify_environment)
#check distribution
print(f"\n{utils.color_text('[Environment]', utils.CYAN + utils.BOLD)}")
print(config.bug_data["environment"].value_counts())


# =============================================================
# Combine both description columns
# =============================================================
config.bug_data["priority"] = [
    PRIORITY_MAP.get((sev, env), "low")  # "low" acts as default fallback
    for sev, env in zip(config.bug_data["severity_rating"], config.bug_data["environment"])
]
print(f"\n{utils.color_text('[Priority]', utils.CYAN + utils.BOLD)}")
print(config.bug_data["priority"].value_counts().rename("Count").sort_index().reset_index().rename(columns={"priority": "Priority"}).to_string(index=False))

# =============================================================
# Combine both description columns
# =============================================================
config.bug_data["target_role"] = config.bug_data.apply(assign_target_role, axis=1)
print(f"\n{utils.color_text('[Target Role]', utils.CYAN + utils.BOLD)}")
print(config.bug_data["target_role"].value_counts().rename("Count").sort_index().reset_index().rename(columns={"target_role": "Role"}).to_string(index=False))



# Helper function to create a dimension table
def extract_dimension(df, column_name, id_name, val_name, custom_order=None):
    if custom_order is not None:
        # Filter the custom order to only include values that actually exist in the data
        unique_vals = [val for val in custom_order if val in df[column_name].dropna().unique()]
    else:
        # Fallback to the original behavior (order of appearance)
        unique_vals = df[column_name].dropna().unique()
        
    dim_df = pd.DataFrame({
        id_name: range(1, len(unique_vals) + 1),
        val_name: unique_vals
    })
    return dim_df



priority_order = ["low", "medium", "high", "critical"]
env_order = ["development", "staging", "production", "unknown"]
severity_order = ["trivial", "minor", "normal", "major", "critical", "blocker"]

# =============================================================
# Extract Dimension DataFrames
# =============================================================
# Priority Dimension
dim_priority = extract_dimension(df=config.bug_data,column_name="priority",id_name="priority_id",val_name="priority_name",custom_order=priority_order)
# Environment Dimension
dim_environment = extract_dimension(df=config.bug_data,column_name="environment",id_name="environment_id",val_name="environment_name",custom_order=env_order)
# Target Role Dimension
dim_roles = extract_dimension(df=config.bug_data,column_name="target_role",id_name="role_id",val_name="role_name")
# Product Dimension
dim_products = extract_dimension(df=config.bug_data,column_name="product_name",id_name="product_id",val_name="product_name")
# Severity Category Dimension
dim_severity = extract_dimension(df=config.bug_data,column_name="severity_category",id_name="severity_id",val_name="severity_name",custom_order=severity_order)

# =============================================================
# Map Foreign Keys Back to Fact Table
# =============================================================
# Convert text columns in main dataset into foreign key IDs
fact_bugs = config.bug_data.copy()
# =============================================================
# Merge Severity Category Dimension
# =============================================================
fact_bugs = fact_bugs.merge(dim_severity, left_on="severity_category", right_on="severity_name", how="left").drop(columns=["severity_category", "severity_name"])
fact_bugs = fact_bugs.merge(dim_products, left_on="product_name", right_on="product_name", how="left")
fact_bugs = fact_bugs.merge(dim_roles, left_on="target_role", right_on="role_name", how="left").drop(columns=["target_role", "role_name"])
fact_bugs = fact_bugs.merge(dim_priority, left_on="priority", right_on="priority_name", how="left").drop(columns=["priority", "priority_name"])
fact_bugs = fact_bugs.merge(dim_environment, left_on="environment", right_on="environment_name", how="left").drop(columns=["environment", "environment_name"])

# =============================================================
# Save split tables to the 'data/processed' directory
# =============================================================
print(f"\n{utils.color_text(f'[Saving processed tables to: {output_dir}]', utils.CYAN + utils.BOLD)}")
dim_priority.to_csv(os.path.join(output_dir, 'dim_priorities.csv'), index=False)
dim_environment.to_csv(os.path.join(output_dir, 'dim_environments.csv'), index=False)
dim_roles.to_csv(os.path.join(output_dir, 'dim_roles.csv'), index=False)
dim_products.to_csv(os.path.join(output_dir, 'dim_products.csv'), index=False)
dim_severity.to_csv(os.path.join(output_dir, 'dim_severities.csv'), index=False)
config.bug_data.to_csv(os.path.join(output_dir, 'normalized_dataset_bugs.csv'), index=False)

print(f"\n{utils.color_text('Database normalization and file split complete!', utils.GREEN + utils.BOLD)}")


# =============================================================
# Compress the large CSV into a zip file
# =============================================================
with zipfile.ZipFile("data/processed/normalized_dataset_bugs.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write("data/processed/normalized_dataset_bugs.csv", arcname="normalized_dataset_bugs.csv")


print(f"\n{utils.color_text(f'File compressed successfully!', utils.GREEN + utils.BOLD)}")

