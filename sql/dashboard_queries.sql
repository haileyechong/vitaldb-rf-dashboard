-- Dashboard Queries
-- VitalDB Perioperative Surgical Outcomes Project


USE vitaldb_project;



-- 1. Overall KPI cards


SELECT
    COUNT(*) AS total_cases,
    ROUND(AVG(in_hospital_death) * 100, 2) AS mortality_rate_pct,
    ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
    ROUND(AVG(prolonged_hospital_stay) * 100, 2) AS prolonged_hospital_stay_rate_pct,
    ROUND(AVG(icu_days), 2) AS avg_icu_days,
    ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
FROM surgery_cases;



-- 2. Case volume by department


SELECT
    department,
    COUNT(*) AS case_count
FROM surgery_cases
GROUP BY department
ORDER BY case_count DESC;



-- 3. Outcomes by department


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



-- 4. Case volume by operation type


SELECT
    operation_type,
    COUNT(*) AS case_count
FROM surgery_cases
GROUP BY operation_type
ORDER BY case_count DESC;



-- 5. Outcomes by operation type


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



-- 6. Outcomes by ASA class


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



-- 7. Emergency vs non-emergency outcomes


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



-- 8. Operation types with highest prolonged hospital stay rate
-- Only includes groups with at least 50 cases


SELECT
    operation_type,
    COUNT(*) AS case_count,
    ROUND(AVG(prolonged_hospital_stay) * 100, 2) AS prolonged_hospital_stay_rate_pct,
    ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
FROM surgery_cases
GROUP BY operation_type
HAVING COUNT(*) >= 50
ORDER BY prolonged_hospital_stay_rate_pct DESC;



-- 9. Operation types with highest ICU stay rate
-- Only includes groups with at least 50 cases


SELECT
    operation_type,
    COUNT(*) AS case_count,
    ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
    ROUND(AVG(icu_days), 2) AS avg_icu_days
FROM surgery_cases
GROUP BY operation_type
HAVING COUNT(*) >= 50
ORDER BY icu_stay_rate_pct DESC;



-- 10. Mortality by operation type
-- Only includes groups with at least 50 cases


SELECT
    operation_type,
    COUNT(*) AS case_count,
    SUM(in_hospital_death) AS death_count,
    ROUND(AVG(in_hospital_death) * 100, 2) AS mortality_rate_pct
FROM surgery_cases
GROUP BY operation_type
HAVING COUNT(*) >= 50
ORDER BY mortality_rate_pct DESC;



-- 11. Patient characteristics by prolonged hospital stay status
-- Useful for connecting SQL reporting to the ML target


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



-- 12. Intraoperative factors by prolonged hospital stay status


SELECT
    prolonged_hospital_stay_label,
    COUNT(*) AS case_count,
    ROUND(AVG(intraoperative_estimated_blood_loss), 2) AS avg_estimated_blood_loss,
    ROUND(AVG(intraoperative_urine_output), 2) AS avg_urine_output,
    ROUND(AVG(intraoperative_red_blood_cell_transfusion), 2) AS avg_rbc_transfusion,
    ROUND(AVG(intraoperative_fresh_frozen_plasma_transfusion), 2) AS avg_ffp_transfusion,
    ROUND(AVG(intraoperative_crystalloid), 2) AS avg_crystalloid
FROM surgery_cases
GROUP BY prolonged_hospital_stay_label;



-- 13. Outcomes by sex


SELECT
    sex,
    COUNT(*) AS case_count,
    ROUND(AVG(in_hospital_death) * 100, 2) AS mortality_rate_pct,
    ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
    ROUND(AVG(prolonged_hospital_stay) * 100, 2) AS prolonged_hospital_stay_rate_pct,
    ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
FROM surgery_cases
GROUP BY sex
ORDER BY case_count DESC;



-- 14. Age group outcomes


SELECT
    CASE
        WHEN age_numeric < 18 THEN 'Under 18'
        WHEN age_numeric BETWEEN 18 AND 39 THEN '18-39'
        WHEN age_numeric BETWEEN 40 AND 59 THEN '40-59'
        WHEN age_numeric BETWEEN 60 AND 79 THEN '60-79'
        WHEN age_numeric >= 80 THEN '80+'
        ELSE 'Unknown'
    END AS age_group,
    COUNT(*) AS case_count,
    ROUND(AVG(in_hospital_death) * 100, 2) AS mortality_rate_pct,
    ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
    ROUND(AVG(prolonged_hospital_stay) * 100, 2) AS prolonged_hospital_stay_rate_pct,
    ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
FROM surgery_cases
GROUP BY age_group
ORDER BY
    CASE age_group
        WHEN 'Under 18' THEN 1
        WHEN '18-39' THEN 2
        WHEN '40-59' THEN 3
        WHEN '60-79' THEN 4
        WHEN '80+' THEN 5
        ELSE 6
    END;



-- 15. Top individual cases by hospital length of stay
-- Useful for checking outliers


SELECT
    case_id,
    patient_id,
    department,
    operation_type,
    operation_name,
    age_numeric,
    asa_class,
    emergency_operation_label,
    hospital_length_of_stay,
    icu_days,
    in_hospital_death_label,
    prolonged_hospital_stay_label
FROM surgery_cases
ORDER BY hospital_length_of_stay DESC
LIMIT 20;