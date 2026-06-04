import os
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


# ============================================================
# Load environment variables
# ============================================================

load_dotenv(override=True)

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "vitaldb_project")

encoded_password = quote_plus(MYSQL_PASSWORD)

engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{encoded_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)


# ============================================================
# Test selected SQL queries
# ============================================================

queries = {
    "overall_kpis": """
        SELECT
            COUNT(*) AS total_cases,
            ROUND(AVG(in_hospital_death) * 100, 2) AS mortality_rate_pct,
            ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
            ROUND(AVG(prolonged_hospital_stay) * 100, 2) AS prolonged_hospital_stay_rate_pct,
            ROUND(AVG(icu_days), 2) AS avg_icu_days,
            ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
        FROM surgery_cases;
    """,

    "outcomes_by_department": """
        SELECT
            department,
            COUNT(*) AS case_count,
            ROUND(AVG(in_hospital_death) * 100, 2) AS mortality_rate_pct,
            ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
            ROUND(AVG(prolonged_hospital_stay) * 100, 2) AS prolonged_hospital_stay_rate_pct,
            ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
        FROM surgery_cases
        GROUP BY department
        ORDER BY case_count DESC;
    """,

    "outcomes_by_operation_type": """
        SELECT
            operation_type,
            COUNT(*) AS case_count,
            ROUND(AVG(in_hospital_death) * 100, 2) AS mortality_rate_pct,
            ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
            ROUND(AVG(prolonged_hospital_stay) * 100, 2) AS prolonged_hospital_stay_rate_pct,
            ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
        FROM surgery_cases
        GROUP BY operation_type
        ORDER BY case_count DESC;
    """,

    "outcomes_by_asa_class": """
        SELECT
            asa_class,
            COUNT(*) AS case_count,
            ROUND(AVG(in_hospital_death) * 100, 2) AS mortality_rate_pct,
            ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
            ROUND(AVG(prolonged_hospital_stay) * 100, 2) AS prolonged_hospital_stay_rate_pct,
            ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
        FROM surgery_cases
        GROUP BY asa_class
        ORDER BY asa_class;
    """,

    "emergency_vs_non_emergency": """
        SELECT
            emergency_operation_label,
            COUNT(*) AS case_count,
            ROUND(AVG(in_hospital_death) * 100, 2) AS mortality_rate_pct,
            ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
            ROUND(AVG(prolonged_hospital_stay) * 100, 2) AS prolonged_hospital_stay_rate_pct,
            ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
        FROM surgery_cases
        GROUP BY emergency_operation_label
        ORDER BY case_count DESC;
    """
}


for name, query in queries.items():
    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)

    result = pd.read_sql(query, con=engine)
    print(result)