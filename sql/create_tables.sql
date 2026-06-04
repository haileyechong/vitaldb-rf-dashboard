-- Create database and surgery_cases table
-- VitalDB Perioperative Surgical Outcomes Project


CREATE DATABASE IF NOT EXISTS vitaldb_project;

USE vitaldb_project;

DROP TABLE IF EXISTS surgery_cases;

CREATE TABLE surgery_cases (
    case_id BIGINT PRIMARY KEY,
    patient_id BIGINT,

    admission_time_from_case_start_sec BIGINT,
    discharge_time_from_case_start_sec BIGINT,

    icu_days INT,
    in_hospital_death INT,

    age VARCHAR(20),
    sex VARCHAR(20),
    height FLOAT,
    weight FLOAT,
    bmi FLOAT,
    asa_class FLOAT,
    emergency_operation INT,

    department VARCHAR(100),
    operation_type VARCHAR(100),
    diagnosis TEXT,
    operation_name TEXT,
    surgical_approach VARCHAR(100),
    patient_position VARCHAR(100),
    anesthesia_type VARCHAR(100),

    preoperative_hypertension INT,
    preoperative_diabetes INT,
    preoperative_hemoglobin FLOAT,
    preoperative_platelet_count FLOAT,
    preoperative_creatinine FLOAT,

    intraoperative_estimated_blood_loss FLOAT,
    intraoperative_urine_output FLOAT,
    intraoperative_red_blood_cell_transfusion INT,
    intraoperative_fresh_frozen_plasma_transfusion INT,
    intraoperative_crystalloid FLOAT,
    intraoperative_colloid INT,
    intraoperative_propofol INT,
    intraoperative_midazolam FLOAT,
    intraoperative_fentanyl INT,

    had_icu_stay INT,
    hospital_length_of_stay FLOAT,
    prolonged_hospital_stay INT,
    age_numeric FLOAT,

    emergency_operation_label VARCHAR(50),
    in_hospital_death_label VARCHAR(50),
    icu_stay_label VARCHAR(50),
    prolonged_hospital_stay_label VARCHAR(50)
);

-- ============================================================
-- Indexes for faster reporting/dashboard queries
-- ============================================================

CREATE INDEX idx_department 
ON surgery_cases (department);

CREATE INDEX idx_operation_type 
ON surgery_cases (operation_type);

CREATE INDEX idx_asa_class 
ON surgery_cases (asa_class);

CREATE INDEX idx_emergency_operation 
ON surgery_cases (emergency_operation);

CREATE INDEX idx_in_hospital_death 
ON surgery_cases (in_hospital_death);

CREATE INDEX idx_had_icu_stay 
ON surgery_cases (had_icu_stay);

CREATE INDEX idx_prolonged_hospital_stay 
ON surgery_cases (prolonged_hospital_stay);