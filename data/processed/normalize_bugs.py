import os
import pandas as pd

# 1. Setup dynamic paths relative to this script's location
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define input path (pointing to data/raw)
input_file = os.path.abspath(os.path.join(script_dir, "../raw/bug_dataset_with_priority_and_severity.csv"))
#"../../data/raw/bug_dataset_with_priority_and_severity.csv"))

# Define output directory (pointing to data/processed)
output_dir = os.path.abspath(os.path.join(script_dir, "../processed"))
#"../../data/processed"))

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# 2. Load the dataset
print(f"Reading source file from: {input_file}")
df = pd.read_csv(input_file)

# 3. Clean date column (handling mixed date formats)
df['created_at'] = pd.to_datetime(df['created_at'], format='mixed', errors='coerce').dt.strftime('%Y-%m-%d')

# Helper function to create a dimension table
def extract_dimension(df, column_name, id_name, val_name):
    unique_vals = df[column_name].dropna().unique()
    dim_df = pd.DataFrame({
        id_name: range(1, len(unique_vals) + 1),
        val_name: unique_vals
    })
    return dim_df

# 4. Extract dimension dataframes
priorities_df = extract_dimension(df, 'priority', 'priority_id', 'priority_name')
severities_df = extract_dimension(df, 'severity', 'severity_id', 'severity_name')
environments_df = extract_dimension(df, 'environment', 'environment_id', 'environment_name')
categories_df = extract_dimension(df, 'bug_category', 'category_id', 'category_name')
domains_df = extract_dimension(df, 'bug_domain', 'domain_id', 'domain_name')
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
bugs_df.to_csv(os.path.join(output_dir, 'fact_bugs.csv'), index=False)

print("Database normalization and file split complete!")