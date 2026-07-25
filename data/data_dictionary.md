# Data Dictionary

## Overview

This project contains a synthetic bug tracking dataset designed for learning, analytics, SQL practice, machine learning, and business intelligence.

The project includes:

- A raw dataset
- A cleaned/corrected dataset
- A fully normalized relational database structure
- Dimension tables
- A Python script that performs the normalization process

The normalized structure follows database normalization principles (3NF) and is ready for SQL databases such as SQL Server, PostgreSQL, MySQL, or SQLite.

---

# Project Structure

```
data/
│
├── raw/
│   ├── bug_dataset_with_priority_and_severity.csv
│   └── bug_dataset_with_priority_and_severity_corrected.csv
│
├── processed/
│   ├── normalized_dataset_bugs.csv
│   ├── dim_priorities.csv
│   ├── dim_severities.csv
│   ├── dim_categories.csv
│   ├── dim_domains.csv
│   ├── dim_environments.csv
│   ├── dim_tech_stacks.csv
│   └── dim_developer_roles.csv
│
└── scripts/
    └── normalize_bugs.py
```

---

# File Descriptions

---

## bug_dataset_with_priority_and_severity.csv

### Description

The original synthetic bug dataset.

Every record represents a single software bug reported by a tester or user.

This dataset contains descriptive values such as:

- Priority names
- Severity names
- Environment names
- Technology stack names
- Bug category names

These values are stored directly inside every row, making the dataset suitable for analysis but not ideal for relational databases.

### Typical Uses

- Data exploration
- Data cleaning exercises
- Machine Learning
- Feature engineering
- Pandas practice
- CSV analysis

---

## bug_dataset_with_priority_and_severity_corrected.csv

### Description

An improved version of the original dataset.

It contains corrected values, standardized categories, cleaned formatting, and validated data.

Use this file whenever possible.

### Typical Uses

- Production analytics
- ML model training
- SQL import
- Visualization
- Dashboard creation

---

## normalize_bugs.py

### Description

This Python script converts the raw dataset into a normalized relational model.

The script automatically:

- Loads the raw dataset
- Cleans the date column
- Creates all lookup (dimension) tables
- Generates numeric IDs
- Replaces text values with foreign keys
- Produces the normalized fact table
- Saves every generated CSV file

### Generated Files

Running this script creates:

- normalized_dataset_bugs.csv
- dim_priorities.csv
- dim_severities.csv
- dim_categories.csv
- dim_domains.csv
- dim_environments.csv
- dim_tech_stacks.csv
- dim_developer_roles.csv

### Skills You Can Learn

- Pandas
- Data Cleaning
- ETL
- Database Normalization
- Foreign Keys
- Dimension Tables
- Data Engineering

---

# Processed Dataset

---

## normalized_dataset_bugs.csv

### Description

This is the central fact table.

It contains one row for every bug.

Instead of storing descriptive text, it stores foreign key IDs pointing to the corresponding dimension tables.

### Example

Instead of

```
Priority = High
```

it stores

```
priority_id = 3
```

This dramatically reduces duplicated data and improves database performance.

### Relationships

The table references:

- Priority
- Severity
- Category
- Domain
- Environment
- Technology Stack
- Developer Role

### Typical Uses

- SQL joins
- Power BI
- Tableau
- Star Schema
- Machine Learning
- Reporting

---

# Dimension Tables

Dimension tables store unique values only once.

They eliminate duplicated text and create relationships inside the database.

---

## dim_priorities.csv

### Description

Contains all possible bug priorities.

Columns

| Column | Description |
|---------|-------------|
| priority_id | Primary Key |
| priority_name | Low, Normal, High, Urgent |

Example

| priority_id | priority_name |
|-------------|---------------|
|1|Low|
|2|Normal|
|3|High|
|4|Urgent|

---

## dim_severities.csv

### Description

Contains all bug severity levels.

Columns

- severity_id
- severity_name

Possible values

- Low
- Medium
- High
- Critical

---

## dim_categories.csv

### Description

Stores software bug categories.

Examples

- UI
- Backend
- API
- Database
- Performance
- Authentication

Purpose

Categorizing bugs for reporting and analytics.

---

## dim_domains.csv

### Description

Stores business domains where bugs occurred.

Examples

- Finance
- Healthcare
- E-Commerce
- Education
- Government

Purpose

Business intelligence and reporting.

---

## dim_environments.csv

### Description

Stores execution environments.

Examples

- Development
- QA
- Staging
- Production

Purpose

Environment-specific analytics.

---

## dim_tech_stacks.csv

### Description

Stores technologies associated with the bug.

Examples

- React
- Angular
- Vue
- .NET
- Java
- Python
- Node.js

Purpose

Technology trend analysis.

---

## dim_developer_roles.csv

### Description

Stores the developer role responsible for resolving the issue.

Examples

- Frontend Developer
- Backend Developer
- Full Stack Developer
- DevOps Engineer
- QA Engineer
- Database Developer

Purpose

Resource planning and workload analysis.

---

# Database Relationships

```
                dim_priorities
                       |
                priority_id
                       |
                       |
dim_severities --- normalized_dataset_bugs --- dim_categories
                       |
                       |
                 dim_domains
                       |
                 dim_environments
                       |
                dim_tech_stacks
                       |
             dim_developer_roles
```

---

# Recommended Learning Path

Beginners should explore the project in the following order:

1. Open the original dataset.
2. Explore all columns.
3. Understand duplicated values.
4. Study database normalization.
5. Review the Python normalization script.
6. Examine each generated dimension table.
7. Understand primary keys.
8. Understand foreign keys.
9. Study the normalized fact table.
10. Import the tables into SQL Server or PostgreSQL.
11. Write JOIN queries.
12. Build dashboards using Power BI.
13. Train Machine Learning models using the normalized data.

---

# Suggested SQL Exercises

Practice writing queries such as:

- Count bugs by severity
- Count bugs by priority
- Top bug categories
- Bugs by technology stack
- Bugs by developer role
- Bugs by environment
- Average resolution time
- Critical bugs in Production
- Monthly bug trends
- Priority vs Severity analysis

---

# Suggested Machine Learning Projects

This dataset can be used to build models that predict:

- Bug priority
- Bug severity
- Estimated resolution time
- Assigned developer role
- Bug category
- Production risk
- Root cause prediction

---

# Business Intelligence Ideas

Build dashboards showing:

- Total bugs
- Open vs Closed bugs
- Bugs by month
- Bugs by category
- Bugs by technology
- Bugs by developer
- Bugs by environment
- Critical production issues
- Average fix time
- Severity distribution

---

# Summary

This project demonstrates a complete real-world data engineering workflow:

- Raw data collection
- Data cleaning
- ETL processing
- Database normalization
- Relational modeling
- SQL-ready datasets
- Business Intelligence preparation
- Machine Learning feature preparation

It provides an excellent foundation for learning Data Engineering, SQL, Python, Power BI, Database Design, and Machine Learning using a realistic software bug tracking scenario.