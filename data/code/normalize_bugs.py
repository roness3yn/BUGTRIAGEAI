import os
import sys
import pandas as pd
# 1. Get the directory of dataTune.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Get the absolute path to the 'src/config' folder
#    (Goes up one level to root, then down into src/config)
config_dir = os.path.abspath(os.path.join(current_dir, "../../src/config"))

# 3. Add the config directory to Python's search path
if config_dir not in sys.path:
    sys.path.append(config_dir)

# 4. Now you can import it directly
import config

# Define input path (pointing to data/raw)
input_file = os.path.join(config.RAW_DATA_DIR, "bug_dataset_with_priority_and_severity.csv")

# Define output directory (pointing to data/processed)
output_dir = config.PROCESSED_DATA_DIR


# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# 2. Load the dataset
print(f"Reading source file from: {input_file}")
df = pd.read_csv(input_file)

# 3. Clean date column (handling mixed date formats)
df['created_at'] = pd.to_datetime(df['created_at'], format='mixed', errors='coerce').dt.strftime('%Y-%m-%d')

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

# 4. Extract dimension dataframes
# 1. Define your custom order lists
severity_order = ['Low', 'Medium', 'High', 'Critical']
priority_order = ['Low', 'Normal', 'High', 'Urgent']

# 2. Extract with custom order (Low will be 1, Critical/Urgent will be 4)
severities_df = extract_dimension(df, 'severity', 'severity_id', 'severity_name', custom_order=severity_order)
priorities_df = extract_dimension(df, 'priority', 'priority_id', 'priority_name', custom_order=priority_order)

# 3. Extract standard columns without custom order (keeps original behavior)
categories_df = extract_dimension(df, 'bug_category', 'category_id', 'category_name')
domains_df = extract_dimension(df, 'bug_domain', 'domain_id', 'domain_name')
environments_df = extract_dimension(df, 'environment', 'environment_id', 'environment_name')
tech_stacks_df = extract_dimension(df, 'tech_stack', 'tech_stack_id', 'tech_stack_name')
roles_df = extract_dimension(df, 'developer_role', 'role_id', 'role_name')

# 5. Map original dataframe values to foreign key IDs
bugs_df = df.copy()

bugs_df = bugs_df.merge(priorities_df, left_on='priority', right_on='priority_name', how='left')
bugs_df = bugs_df.merge(severities_df, left_on='severity', right_on='severity_name', how='left')
bugs_df = bugs_df.merge(environments_df, left_on='environment', right_on='environment_name', how='left')
bugs_df = bugs_df.merge(categories_df, left_on='bug_category', right_on='category_name', how='left')
bugs_df = bugs_df.merge(domains_df, left_on='bug_domain', right_on='domain_name', how='left')
bugs_df = bugs_df.merge(tech_stacks_df, left_on='tech_stack', right_on='tech_stack_name', how='left')
bugs_df = bugs_df.merge(roles_df, left_on='developer_role', right_on='role_name', how='left')

# Drop the descriptive columns that are now in dimension tables
columns_to_drop = [
    'priority', 'priority_name',
    'severity', 'severity_name',
    'environment', 'environment_name',
    'bug_category', 'category_name',
    'bug_domain', 'domain_name',
    'tech_stack', 'tech_stack_name',
    'developer_role', 'role_name'
]
bugs_df = bugs_df.drop(columns=columns_to_drop)

# 6. Save split tables to the 'data/processed' directory
print(f"Saving processed tables to: {output_dir}")

priorities_df.to_csv(os.path.join(output_dir, 'dim_priorities.csv'), index=False)
severities_df.to_csv(os.path.join(output_dir, 'dim_severities.csv'), index=False)
environments_df.to_csv(os.path.join(output_dir, 'dim_environments.csv'), index=False)
categories_df.to_csv(os.path.join(output_dir, 'dim_categories.csv'), index=False)
domains_df.to_csv(os.path.join(output_dir, 'dim_domains.csv'), index=False)
tech_stacks_df.to_csv(os.path.join(output_dir, 'dim_tech_stacks.csv'), index=False)
roles_df.to_csv(os.path.join(output_dir, 'dim_developer_roles.csv'), index=False)
bugs_df.to_csv(os.path.join(output_dir, 'normalized_dataset_bugs.csv'), index=False)

print("Database normalization and file split complete!")