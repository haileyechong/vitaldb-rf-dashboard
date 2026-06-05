# VitalDB Surgical Outcomes Dashboard

## Project Overview

This project is a short data science project with surgical quality reporting, dashboards, databases, and risk prediction.

Since real adult cardiac surgery registry data is restricted, we used the open-access VitalDB `clinical_data.csv` file as a public perioperative surgical dataset.

The project includes:

* Cleaning the VitalDB clinical data
* Doing exploratory data analysis
* Loading the cleaned data into MySQL
* Writing SQL queries for outcome reporting
* Building a Streamlit dashboard
* Adding model results from Random Forest and XGBoost
* Creating a simple risk explorer for prolonged hospital stay

## Dataset

We used the VitalDB `clinical_data.csv` file only.

The raw file should be placed here:

```text
data/raw/clinical_data.csv
```

We did not use the huge waveform files from VitalDB.

Each row in the dataset represents one surgical case. The data includes patient information, surgery details, preoperative lab values, intraoperative variables, and outcomes.

Important note: VitalDB is perioperative surgical data, not adult cardiac surgery registry data. We used it because it is public and de-identified, while real registry data is not available for this project.

## Project Structure

```text
vitaldb-rf-dashboard/
│
├── data/
│   ├── raw/
│   │   └── clinical_data.csv
│   └── processed/
│       └── vitaldb_cleaned.csv
│
├── notebooks/
│   └── eda.ipynb
|   └── random_forest.ipynb
│
├── outputs/
│   ├── figures/
│   └── model_results/
|   └── sql_results/
│
├── scripts/
│   ├── database_setup.py
│   └── test_queries.py
|   └── create_sql_visualizations.py
│
├── sql/
│   ├── create_tables.sql
│   └── dashboard_queries.sql
│
|── streamlit_app/
|   └── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Data Cleaning

The original VitalDB columns had a lot of shortened names, so I renamed the important columns into more readable snake_case names.

Some columns I added:

| Column                    | What it means                                |
| ------------------------- | -------------------------------------------- |
| `age_numeric`             | Numeric version of age                       |
| `hospital_length_of_stay` | Hospital stay in days                        |
| `had_icu_stay`            | Whether the patient had any ICU stay         |
| `prolonged_hospital_stay` | Whether the patient stayed longer than usual |
| Label columns             | More readable labels for dashboard display   |

The main outcome we focused on was:

```text
prolonged_hospital_stay
```

I defined prolonged hospital stay as cases where the hospital length of stay was above the 75th percentile.

## SQL Database

After cleaning the data, I loaded it into a MySQL database.

Database name:

```text
vitaldb_project
```

Main table:

```text
surgery_cases
```

The SQL queries were used to create dashboard-ready summaries, such as:

* Overall KPI cards
* Case volume by department
* Outcomes by department
* Outcomes by operation type
* Outcomes by ASA class
* Emergency vs non-emergency outcomes
* Highest prolonged stay rates by operation type
* Highest ICU stay rates by operation type

## Machine Learning

The modeling part tested Random Forest and XGBoost models on:

* In-hospital death
* Prolonged hospital stay
* ICU stay

## Streamlit Dashboard

The Streamlit dashboard shows:

* Overall KPIs
* Case volume by department and operation type
* Department-level outcomes
* Operation-type outcomes
* ASA and emergency status risk patterns
* Model results
* A simple prolonged hospital stay risk explorer

The risk explorer is not the actual Random Forest or XGBoost model. It is a simple rules-based prototype based on EDA findings, SQL results, and non-leakage feature importance.

The risk explorer uses inputs like:

* Age
* BMI
* ASA class
* Emergency operation status
* Operation type
* Preoperative creatinine
* Preoperative hemoglobin
* Preoperative platelet count
* Estimated blood loss
* Intraoperative crystalloid

It classifies cases into low, moderate, high, or very high risk for prolonged hospital stay. This is just for demonstration and is not a real clinical tool.

## How to Run the Project

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd vitaldb-rf-dashboard
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install packages

```bash
pip install -r requirements.txt
```

### 4. Add the dataset

Place the VitalDB clinical CSV here:

```text
data/raw/clinical_data.csv
```

### 5. Set up the `.env` file

Copy the example file:

```bash
cp .env.example .env
```

Then fill in your MySQL information:

```env
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=vitaldb_project
```

Do not push your real `.env` file to GitHub.

### 6. Load the data into MySQL

```bash
python scripts/database_setup.py
```

### 7. Run SQL queries

```bash
python scripts/test_queries.py
```

### 8. Launch the dashboard

```bash
streamlit run app.py
```

## Reproducibility

The project is meant to be reproducible from the same raw CSV.

Basic workflow:

```text
1. Download VitalDB clinical_data.csv
2. Place it in data/raw/
3. Run the cleaning workflow
4. Save the cleaned dataset
5. Load the cleaned data into MySQL
6. Run the SQL queries
7. Launch the Streamlit dashboard
```

The model uses `random_state=42` where possible so results are easier to reproduce.

Database passwords are not included in the repo. Each person should create their own local `.env` file.

## Limitations

Some important limitations:

* VitalDB is not adult cardiac surgery registry data.
* This is a prototype, not a clinical decision tool.
* The data comes from a specific surgical dataset and may not generalize to other hospitals.
* Mortality was rare, which made death prediction difficult.
* Some smaller groups, like ASA 4 or ASA 6, had small sample sizes.
* Prolonged hospital stay was defined using the 75th percentile, so a different cutoff could change the results.
* Some model results may be inflated if leakage variables are included.
* The risk explorer is rules-based and not clinically validated.
* The analysis shows associations, not causation.

## Contributors

| Team Member | Role                                                                       |
| ----------- | -------------------------------------------------------------------------- |
| Hailey      | Data cleaning, EDA, MySQL database setup, SQL queries, Streamlit dashboard |
| Aniqa       | Random Forest / XGBoost modeling, model metrics, feature importance        |

## Final Note

Overall, this project shows how a public perioperative surgical dataset can be cleaned, stored in a database, queried with SQL, visualized in a dashboard, and connected to machine learning results. It is not meant for clinical use, but it demonstrates the type of workflow that could be used for surgical quality reporting.
