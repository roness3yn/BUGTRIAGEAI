# Data Dictionary

This document provides an overview of the datasets included in the project. Each dataset is described with its file path, purpose, and schema.

---

## Project Structure
data/ 
       ├── data_dictionary.md 
       ├── code/ 
       │ └── normalize_bugs.py 
       ├── processed/ 
       │ ├── dim_products.csv 
       │ ├── dim_severities.csv 
       │ ├── dim_roles.csv 
       │ ├── dim_environments.csv 
       │ ├── normalized_dataset_bugs.csv 
       │ ├── normalized_dataset_bugs.zip 
       │ └── dim_priorities.csv └── raw/ 
       ├── winehq_bug_report_data.csv 
       ├── freedesktop_bug_report_data.csv 
       ├── bug_dataset.csv 
       ├── eclipse_bug_report_data.csv 
       ├── gcc_bug_report_data.csv 
       ├── mozilla_bug_report_data.csv └── gnome_bug_report_data.csv

---

## Raw Data Files

### 1. `data/raw/winehq_bug_report_data.csv`
- **Description**: Raw bug report data from the WineHQ project.
- **Columns**:
  | Column Name           | Description                          |
  |-----------------------|--------------------------------------|
  | `bug_id`              | Unique identifier for the bug.       |
  | `creation_date`       | Date the bug was created.            |
  | `component_name`      | Component associated with the bug.   |
  | `product_name`        | Product associated with the bug.     |
  | `short_description`   | Short description of the bug.        |
  | `long_description`    | Detailed description of the bug.     |
  | `assignee_name`       | Name of the person assigned to fix.  |
  | `reporter_name`       | Name of the person who reported it.  |
  | `resolution_category` | Category of the resolution.          |
  | `resolution_code`     | Code representing the resolution.    |
  | `status_category`     | Category of the bug's status.        |
  | `status_code`         | Code representing the status.        |
  | `update_date`         | Date the bug was last updated.       |
  | `quantity_of_votes`   | Number of votes the bug received.    |
  | `quantity_of_comments`| Number of comments on the bug.       |
  | `resolution_date`     | Date the bug was resolved.           |
  | `bug_fix_time`        | Time taken to fix the bug.           |
  | `severity_category`   | Category of the bug's severity.      |
  | `severity_code`       | Code representing the severity.      |

### 2. `data/raw/freedesktop_bug_report_data.csv`
- **Description**: Raw bug report data from the FreeDesktop project.
- **Columns**: Same as `winehq_bug_report_data.csv`.

### 3. `data/raw/bug_dataset.csv`
- **Description**: Consolidated raw bug report dataset.
- **Columns**: Same as `winehq_bug_report_data.csv`.

### 4. `data/raw/eclipse_bug_report_data.csv`
- **Description**: Raw bug report data from the Eclipse project.
- **Columns**: Same as `winehq_bug_report_data.csv`.

### 5. `data/raw/gcc_bug_report_data.csv`
- **Description**: Raw bug report data from the GCC project.
- **Columns**: Same as `winehq_bug_report_data.csv`.

### 6. `data/raw/mozilla_bug_report_data.csv`
- **Description**: Raw bug report data from the Mozilla project.
- **Columns**: Same as `winehq_bug_report_data.csv`.

### 7. `data/raw/gnome_bug_report_data.csv`
- **Description**: Raw bug report data from the GNOME project.
- **Columns**: Same as `winehq_bug_report_data.csv`.

---

## Processed Data Files

### 1. `data/processed/normalized_dataset_bugs.csv`
- **Description**: Normalized dataset containing bug reports with relational references to dimension tables.
- **Columns**:
  | Column Name           | Description                          |
  |-----------------------|--------------------------------------|
  | `bug_id`              | Unique identifier for the bug.       |
  | `creation_date`       | Date the bug was created.            |
  | `component_name`      | Component associated with the bug.   |
  | `product_name`        | Product associated with the bug.     |
  | `short_description`   | Short description of the bug.        |
  | `long_description`    | Detailed description of the bug.     |
  | `assignee_name`       | Name of the person assigned to fix.  |
  | `reporter_name`       | Name of the person who reported it.  |
  | `resolution_category` | Category of the resolution.          |
  | `resolution_code`     | Code representing the resolution.    |
  | `status_category`     | Category of the bug's status.        |
  | `status_code`         | Code representing the status.        |
  | `update_date`         | Date the bug was last updated.       |
  | `quantity_of_votes`   | Number of votes the bug received.    |
  | `quantity_of_comments`| Number of comments on the bug.       |
  | `resolution_date`     | Date the bug was resolved.           |
  | `bug_fix_time`        | Time taken to fix the bug.           |
  | `severity_category`   | Category of the bug's severity.      |
  | `severity_code`       | Code representing the severity.      |
  | `severity_rating`     | Rating of the bug's severity.        |
  | `text`                | Additional text information.         |
  | `environment`         | Environment where the bug occurred.  |
  | `priority`            | Priority of the bug.                 |
  | `target_role`         | Role targeted for fixing the bug.    |

### 2. `data/processed/dim_products.csv`
- **Description**: Dimension table for products.
- **Columns**:
  | Column Name   | Description                          |
  |---------------|--------------------------------------|
  | `product_id`  | Unique identifier for the product.   |
  | `product_name`| Name of the product.                |

### 3. `data/processed/dim_severities.csv`
- **Description**: Dimension table for severities.
- **Columns**:
  | Column Name    | Description                          |
  |----------------|--------------------------------------|
  | `severity_id`  | Unique identifier for the severity.  |
  | `severity_name`| Name of the severity.               |

### 4. `data/processed/dim_roles.csv`
- **Description**: Dimension table for roles.
- **Columns**:
  | Column Name | Description                          |
  |-------------|--------------------------------------|
  | `role_id`   | Unique identifier for the role.      |
  | `role_name` | Name of the role.                   |

### 5. `data/processed/dim_environments.csv`
- **Description**: Dimension table for environments.
- **Columns**:
  | Column Name       | Description                          |
  |-------------------|--------------------------------------|
  | `environment_id`  | Unique identifier for the environment. |
  | `environment_name`| Name of the environment.            |

### 6. `data/processed/dim_priorities.csv`
- **Description**: Dimension table for priorities.
- **Columns**:
  | Column Name    | Description                          |
  |----------------|--------------------------------------|
  | `priority_id`  | Unique identifier for the priority.  |
  | `priority_name`| Name of the priority.               |

---

Let me know if further adjustments are needed!
---

## Raw Data Files

### 1. `data/raw/winehq_bug_report_data.csv`
- **Description**: Raw bug report data from the WineHQ project.
- **Columns**:
  | Column Name           | Description                          |
  |-----------------------|--------------------------------------|
  | `bug_id`              | Unique identifier for the bug.       |
  | `creation_date`       | Date the bug was created.            |
  | `component_name`      | Component associated with the bug.   |
  | `product_name`        | Product associated with the bug.     |
  | `short_description`   | Short description of the bug.        |
  | `long_description`    | Detailed description of the bug.     |
  | `assignee_name`       | Name of the person assigned to fix.  |
  | `reporter_name`       | Name of the person who reported it.  |
  | `resolution_category` | Category of the resolution.          |
  | `resolution_code`     | Code representing the resolution.    |
  | `status_category`     | Category of the bug's status.        |
  | `status_code`         | Code representing the status.        |
  | `update_date`         | Date the bug was last updated.       |
  | `quantity_of_votes`   | Number of votes the bug received.    |
  | `quantity_of_comments`| Number of comments on the bug.       |
  | `resolution_date`     | Date the bug was resolved.           |
  | `bug_fix_time`        | Time taken to fix the bug.           |
  | `severity_category`   | Category of the bug's severity.      |
  | `severity_code`       | Code representing the severity.      |

### 2. `data/raw/freedesktop_bug_report_data.csv`
- **Description**: Raw bug report data from the FreeDesktop project.
- **Columns**: Same as `winehq_bug_report_data.csv`.

### 3. `data/raw/bug_dataset.csv`
- **Description**: Consolidated raw bug report dataset.
- **Columns**: Same as `winehq_bug_report_data.csv`.

### 4. `data/raw/eclipse_bug_report_data.csv`
- **Description**: Raw bug report data from the Eclipse project.
- **Columns**: Same as `winehq_bug_report_data.csv`.

### 5. `data/raw/gcc_bug_report_data.csv`
- **Description**: Raw bug report data from the GCC project.
- **Columns**: Same as `winehq_bug_report_data.csv`.

### 6. `data/raw/mozilla_bug_report_data.csv`
- **Description**: Raw bug report data from the Mozilla project.
- **Columns**: Same as `winehq_bug_report_data.csv`.

### 7. `data/raw/gnome_bug_report_data.csv`
- **Description**: Raw bug report data from the GNOME project.
- **Columns**: Same as `winehq_bug_report_data.csv`.

---

## Processed Data Files

### 1. `data/processed/normalized_dataset_bugs.csv`
- **Description**: Normalized dataset containing bug reports with relational references to dimension tables.
- **Columns**:
  | Column Name           | Description                          |
  |-----------------------|--------------------------------------|
  | `bug_id`              | Unique identifier for the bug.       |
  | `creation_date`       | Date the bug was created.            |
  | `component_name`      | Component associated with the bug.   |
  | `product_name`        | Product associated with the bug.     |
  | `short_description`   | Short description of the bug.        |
  | `long_description`    | Detailed description of the bug.     |
  | `assignee_name`       | Name of the person assigned to fix.  |
  | `reporter_name`       | Name of the person who reported it.  |
  | `resolution_category` | Category of the resolution.          |
  | `resolution_code`     | Code representing the resolution.    |
  | `status_category`     | Category of the bug's status.        |
  | `status_code`         | Code representing the status.        |
  | `update_date`         | Date the bug was last updated.       |
  | `quantity_of_votes`   | Number of votes the bug received.    |
  | `quantity_of_comments`| Number of comments on the bug.       |
  | `resolution_date`     | Date the bug was resolved.           |
  | `bug_fix_time`        | Time taken to fix the bug.           |
  | `severity_category`   | Category of the bug's severity.      |
  | `severity_code`       | Code representing the severity.      |
  | `severity_rating`     | Rating of the bug's severity.        |
  | `text`                | Additional text information.         |
  | `environment`         | Environment where the bug occurred.  |
  | `priority`            | Priority of the bug.                 |
  | `target_role`         | Role targeted for fixing the bug.    |

### 2. `data/processed/dim_products.csv`
- **Description**: Dimension table for products.
- **Columns**:
  | Column Name   | Description                          |
  |---------------|--------------------------------------|
  | `product_id`  | Unique identifier for the product.   |
  | `product_name`| Name of the product.                |

### 3. `data/processed/dim_severities.csv`
- **Description**: Dimension table for severities.
- **Columns**:
  | Column Name    | Description                          |
  |----------------|--------------------------------------|
  | `severity_id`  | Unique identifier for the severity.  |
  | `severity_name`| Name of the severity.               |

### 4. `data/processed/dim_roles.csv`
- **Description**: Dimension table for roles.
- **Columns**:
  | Column Name | Description                          |
  |-------------|--------------------------------------|
  | `role_id`   | Unique identifier for the role.      |
  | `role_name` | Name of the role.                   |

### 5. `data/processed/dim_environments.csv`
- **Description**: Dimension table for environments.
- **Columns**:
  | Column Name       | Description                          |
  |-------------------|--------------------------------------|
  | `environment_id`  | Unique identifier for the environment. |
  | `environment_name`| Name of the environment.            |

### 6. `data/processed/dim_priorities.csv`
- **Description**: Dimension table for priorities.
- **Columns**:
  | Column Name    | Description                          |
  |----------------|--------------------------------------|
  | `priority_id`  | Unique identifier for the priority.  |
  | `priority_name`| Name of the priority.               |

---