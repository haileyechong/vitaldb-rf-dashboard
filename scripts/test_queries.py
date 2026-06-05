import os
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


# ============================================================
# Project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "sql_results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Load environment variables
# ============================================================

load_dotenv(PROJECT_ROOT / ".env", override=True)

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "vitaldb_project")

if not MYSQL_USER or not MYSQL_PASSWORD:
    raise ValueError("Missing MYSQL_USER or MYSQL_PASSWORD. Check your .env file.")

encoded_password = quote_plus(MYSQL_PASSWORD)

engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{encoded_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)


# ============================================================
# SQL queries
# ============================================================

queries = {
    "01_overall_kpis": """
        SELECT
            COUNT(*) AS total_cases,
            ROUND(AVG(in_hospital_death) * 100, 2) AS mortality_rate_pct,
            ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
            ROUND(AVG(prolonged_hospital_stay) * 100, 2) AS prolonged_hospital_stay_rate_pct,
            ROUND(AVG(icu_days), 2) AS avg_icu_days,
            ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
        FROM surgery_cases;
    """,

    "02_case_volume_by_department": """
        SELECT
            department,
            COUNT(*) AS case_count
        FROM surgery_cases
        GROUP BY department
        ORDER BY case_count DESC;
    """,

    "03_outcomes_by_department": """
        SELECT
            department,
            COUNT(*) AS case_count,
            ROUND(AVG(in_hospital_death) * 100, 2) AS mortality_rate_pct,
            ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
            ROUND(AVG(prolonged_hospital_stay) * 100, 2) AS prolonged_hospital_stay_rate_pct,
            ROUND(AVG(icu_days), 2) AS avg_icu_days,
            ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
        FROM surgery_cases
        GROUP BY department
        ORDER BY case_count DESC;
    """,

    "04_case_volume_by_operation_type": """
        SELECT
            operation_type,
            COUNT(*) AS case_count
        FROM surgery_cases
        GROUP BY operation_type
        ORDER BY case_count DESC;
    """,

    "05_outcomes_by_operation_type": """
        SELECT
            operation_type,
            COUNT(*) AS case_count,
            ROUND(AVG(in_hospital_death) * 100, 2) AS mortality_rate_pct,
            ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
            ROUND(AVG(prolonged_hospital_stay) * 100, 2) AS prolonged_hospital_stay_rate_pct,
            ROUND(AVG(icu_days), 2) AS avg_icu_days,
            ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
        FROM surgery_cases
        GROUP BY operation_type
        ORDER BY case_count DESC;
    """,

    "06_outcomes_by_asa_class": """
        SELECT
            asa_class,
            COUNT(*) AS case_count,
            ROUND(AVG(in_hospital_death) * 100, 2) AS mortality_rate_pct,
            ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
            ROUND(AVG(prolonged_hospital_stay) * 100, 2) AS prolonged_hospital_stay_rate_pct,
            ROUND(AVG(icu_days), 2) AS avg_icu_days,
            ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
        FROM surgery_cases
        GROUP BY asa_class
        ORDER BY asa_class;
    """,

    "07_emergency_vs_non_emergency_outcomes": """
        SELECT
            emergency_operation_label,
            COUNT(*) AS case_count,
            ROUND(AVG(in_hospital_death) * 100, 2) AS mortality_rate_pct,
            ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
            ROUND(AVG(prolonged_hospital_stay) * 100, 2) AS prolonged_hospital_stay_rate_pct,
            ROUND(AVG(icu_days), 2) AS avg_icu_days,
            ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
        FROM surgery_cases
        GROUP BY emergency_operation_label
        ORDER BY case_count DESC;
    """,

    "08_highest_prolonged_stay_by_operation_type": """
        SELECT
            operation_type,
            COUNT(*) AS case_count,
            ROUND(AVG(prolonged_hospital_stay) * 100, 2) AS prolonged_hospital_stay_rate_pct,
            ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
        FROM surgery_cases
        GROUP BY operation_type
        HAVING COUNT(*) >= 50
        ORDER BY prolonged_hospital_stay_rate_pct DESC;
    """,

    "09_highest_icu_stay_by_operation_type": """
        SELECT
            operation_type,
            COUNT(*) AS case_count,
            ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
            ROUND(AVG(icu_days), 2) AS avg_icu_days
        FROM surgery_cases
        GROUP BY operation_type
        HAVING COUNT(*) >= 50
        ORDER BY icu_stay_rate_pct DESC;
    """,

    "10_patient_characteristics_by_prolonged_stay": """
        SELECT
            prolonged_hospital_stay_label,
            COUNT(*) AS case_count,
            ROUND(AVG(age_numeric), 2) AS avg_age,
            ROUND(AVG(asa_class), 2) AS avg_asa_class,
            ROUND(AVG(emergency_operation) * 100, 2) AS emergency_case_rate_pct,
            ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
            ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
        FROM surgery_cases
        GROUP BY prolonged_hospital_stay_label;
    """
}


# ============================================================
# Run and save query results
# ============================================================

for name, query in queries.items():
    print("\n" + "=" * 90)
    print(name)
    print("=" * 90)

    result = pd.read_sql(query, con=engine)

    print(result)

    output_path = OUTPUT_DIR / f"{name}.csv"
    result.to_csv(output_path, index=False)

    print(f"Saved to: {output_path}")

print("\nAll core SQL dashboard query results saved.")