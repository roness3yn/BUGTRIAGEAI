# BugTriageAI

## Team Members
- Erin Schaverien  
- Ron Ness

## Project Goal
The goal of BugTriageAI is to automate the process of bug triage by leveraging machine 
learning models to classify and assign bugs to the appropriate teams or developers efficiently.

## Problem Statement
Bug triage is a critical yet time-consuming process in software development. 
Misclassification or delays in assigning bugs can lead to increased development costs and slower release cycles. 
Automating this process ensures faster resolution times and improved productivity.

## Data Description
The dataset used for this project includes historical bug reports sourced from open-source repositories. 
It contains fields such as bug description, severity, priority, assigned team, and resolution status. 
The data was preprocessed to remove duplicates, irrelevant fields, and missing values.

## Approach and Methodology
1. **Data Preprocessing**: Cleaning, tokenization, and vectorization of textual data.  
2. **Exploratory Data Analysis (EDA)**: Understanding patterns and distributions in the data.  
3. **Model Training**: Testing multiple machine learning models for classification.  
els for classification, including Logistic Regression, Random Forest, Support Vector Machines (SVM), and Neural Networks. Each model was evaluated to determine its suitability for the task.  
4. **Evaluation**: Comparing models based on accuracy, precision, recall, and F1-score.  

## Work Process
The project was divided into the following phases:  
1. Data collection and preprocessing.  
2. Exploratory data analysis.  
3. Model selection and training.  
4. Evaluation and optimization.  
5. Deployment and testing.  

## Models Tested
- Logistic Regression  
- Random Forest  
- Support Vector Machines (SVM)  
- Neural Networks  

## Key Results
- Random Forest achieved the highest accuracy of 85%.  
- Neural Networks showed potential but required more computational resources.  

## Conclusions
Automating bug triage using machine learning significantly reduces manual effort and improves efficiency. Random Forest was identified as the most suitable model for this task.

## Running Instructions
### Requirements
- Python 3.8+  
- Libraries: `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `seaborn`, `tensorflow`  

### Setup
1. Clone the repository:  
    ```bash
    git clone https://github.com/yourusername/BugTriageAI.git
    cd BugTriageAI
    ```  
2. Install dependencies:  
    ```bash
    pip install -r requirements.txt
    ```  
3. Run the main script:  
    ```bash
    python main.py
    ```  

## Repository Structure
- `data/`: Contains the dataset and preprocessing scripts.  
- `notebooks/`: Jupyter notebooks for EDA and model experimentation.  
- `src/`: Source code for data processing, model training, and evaluation.  
- `results/`: Contains evaluation metrics and visualizations.  
- `README.md`: Project overview and instructions.  

## Next Steps
- Fine-tune the Neural Network model for better performance.  
- Integrate the model into a web-based bug tracking system.  
- Collect more diverse datasets to improve generalization.  
