import os
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.types import BigInteger, Float, Integer, String, Text


# ============================================================
# Load environment variables from .env
# ============================================================

load_dotenv(override=True)

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "vitaldb_project")

if not MYSQL_USER or not MYSQL_PASSWORD:
    raise ValueError("Missing MYSQL_USER or MYSQL_PASSWORD. Check your .env file.")

encoded_password = quote_plus(MYSQL_PASSWORD)

print("Using MySQL user:", MYSQL_USER)
print("Using MySQL database:", MYSQL_DATABASE)


# ============================================================
# Load cleaned dataset
# ============================================================

csv_path = "data/processed/vitaldb_cleaned.csv"

df = pd.read_csv(csv_path)

print("Loaded cleaned dataset:")
print(df.shape)
print(df.head())


# ============================================================
# Connect directly to existing MySQL database
# ============================================================

db_engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{encoded_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)


# ============================================================
# Define MySQL column types
# ============================================================

dtype_mapping = {
    "case_id": BigInteger(),
    "patient_id": BigInteger(),

    "admission_time_from_case_start_sec": BigInteger(),
    "discharge_time_from_case_start_sec": BigInteger(),

    "icu_days": Integer(),
    "in_hospital_death": Integer(),
    "emergency_operation": Integer(),
    "preoperative_hypertension": Integer(),
    "preoperative_diabetes": Integer(),
    "intraoperative_red_blood_cell_transfusion": Integer(),
    "intraoperative_fresh_frozen_plasma_transfusion": Integer(),
    "intraoperative_colloid": Integer(),
    "intraoperative_propofol": Integer(),
    "intraoperative_fentanyl": Integer(),
    "had_icu_stay": Integer(),
    "prolonged_hospital_stay": Integer(),

    "height": Float(),
    "weight": Float(),
    "bmi": Float(),
    "asa_class": Float(),
    "preoperative_hemoglobin": Float(),
    "preoperative_platelet_count": Float(),
    "preoperative_creatinine": Float(),
    "intraoperative_estimated_blood_loss": Float(),
    "intraoperative_urine_output": Float(),
    "intraoperative_crystalloid": Float(),
    "intraoperative_midazolam": Float(),
    "hospital_length_of_stay": Float(),
    "age_numeric": Float(),

    "age": String(20),
    "sex": String(20),
    "department": String(100),
    "operation_type": String(100),
    "surgical_approach": String(100),
    "patient_position": String(100),
    "anesthesia_type": String(100),
    "emergency_operation_label": String(50),
    "in_hospital_death_label": String(50),
    "icu_stay_label": String(50),
    "prolonged_hospital_stay_label": String(50),

    "diagnosis": Text(),
    "operation_name": Text(),
}


# ============================================================
# Load dataframe into MySQL
# ============================================================

df.to_sql(
    name="surgery_cases",
    con=db_engine,
    if_exists="replace",
    index=False,
    dtype=dtype_mapping
)

print("Loaded cleaned data into MySQL table: surgery_cases")


# ============================================================
# Add useful indexes for reporting queries
# ============================================================

index_queries = [
    "ALTER TABLE surgery_cases ADD PRIMARY KEY (case_id);",
    "CREATE INDEX idx_department ON surgery_cases (department);",
    "CREATE INDEX idx_operation_type ON surgery_cases (operation_type);",
    "CREATE INDEX idx_asa_class ON surgery_cases (asa_class);",
    "CREATE INDEX idx_emergency_operation ON surgery_cases (emergency_operation);",
    "CREATE INDEX idx_prolonged_hospital_stay ON surgery_cases (prolonged_hospital_stay);",
    "CREATE INDEX idx_in_hospital_death ON surgery_cases (in_hospital_death);",
    "CREATE INDEX idx_had_icu_stay ON surgery_cases (had_icu_stay);"
]

with db_engine.connect() as conn:
    for query in index_queries:
        try:
            conn.execute(text(query))
            conn.commit()
            print("Ran:", query)
        except Exception as e:
            print("Skipped or failed:", query)
            print(e)


# ============================================================
# Verify table loaded correctly
# ============================================================

with db_engine.connect() as conn:
    row_count = conn.execute(
        text("SELECT COUNT(*) FROM surgery_cases;")
    ).scalar()

    kpi_result = conn.execute(
        text("""
            SELECT
                COUNT(*) AS total_cases,
                ROUND(AVG(in_hospital_death) * 100, 2) AS mortality_rate_pct,
                ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
                ROUND(AVG(prolonged_hospital_stay) * 100, 2) AS prolonged_hospital_stay_rate_pct,
                ROUND(AVG(icu_days), 2) AS avg_icu_days,
                ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
            FROM surgery_cases;
        """)
    ).fetchone()

print(f"surgery_cases row count: {row_count}")
print("Overall KPI check:")
print(kpi_result)

print("Database setup complete.")