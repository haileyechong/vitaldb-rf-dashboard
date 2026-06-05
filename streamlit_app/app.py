import os
from urllib.parse import quote_plus

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine


st.set_page_config(
    page_title="VitalDB Surgical Outcomes Dashboard",
    page_icon="🏥",
    layout="wide"
)

st.title("VitalDB Perioperative Surgical Outcomes Dashboard")

st.markdown(
    """
    This dashboard uses the open-access VitalDB clinical dataset as a public,
    de-identified proxy for an AQG-style surgical quality reporting workflow.
    The dashboard reports perioperative surgical outcomes including mortality,
    ICU utilization, and prolonged hospital length of stay.
    """
)



# Database connection

load_dotenv(override=True)

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "vitaldb_project")

encoded_password = quote_plus(MYSQL_PASSWORD)

DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{encoded_password}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)


@st.cache_resource
def get_engine():
    return create_engine(DATABASE_URL)


engine = get_engine()


@st.cache_data
def run_query(query):
    return pd.read_sql(query, con=engine)



# SQL queries

overall_kpi_query = """
SELECT
    COUNT(*) AS total_cases,
    ROUND(AVG(in_hospital_death) * 100, 2) AS mortality_rate_pct,
    ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
    ROUND(AVG(prolonged_hospital_stay) * 100, 2) AS prolonged_hospital_stay_rate_pct,
    ROUND(AVG(icu_days), 2) AS avg_icu_days,
    ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
FROM surgery_cases;
"""

department_outcomes_query = """
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
"""

operation_type_outcomes_query = """
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
"""

asa_outcomes_query = """
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
"""

emergency_outcomes_query = """
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
"""

prolonged_stay_operation_query = """
SELECT
    operation_type,
    COUNT(*) AS case_count,
    ROUND(AVG(prolonged_hospital_stay) * 100, 2) AS prolonged_hospital_stay_rate_pct,
    ROUND(AVG(hospital_length_of_stay), 2) AS avg_hospital_length_of_stay
FROM surgery_cases
GROUP BY operation_type
HAVING COUNT(*) >= 50
ORDER BY prolonged_hospital_stay_rate_pct DESC;
"""

icu_operation_query = """
SELECT
    operation_type,
    COUNT(*) AS case_count,
    ROUND(AVG(had_icu_stay) * 100, 2) AS icu_stay_rate_pct,
    ROUND(AVG(icu_days), 2) AS avg_icu_days
FROM surgery_cases
GROUP BY operation_type
HAVING COUNT(*) >= 50
ORDER BY icu_stay_rate_pct DESC;
"""

prolonged_group_query = """
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



# Load data

kpis = run_query(overall_kpi_query)
department_outcomes = run_query(department_outcomes_query)
operation_type_outcomes = run_query(operation_type_outcomes_query)
asa_outcomes = run_query(asa_outcomes_query)
emergency_outcomes = run_query(emergency_outcomes_query)
prolonged_stay_operation = run_query(prolonged_stay_operation_query)
icu_operation = run_query(icu_operation_query)
prolonged_group = run_query(prolonged_group_query)



# KPI cards

st.header("Overview KPIs")

kpi = kpis.iloc[0]

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Total Cases", f"{int(kpi['total_cases']):,}")
col2.metric("Mortality Rate", f"{kpi['mortality_rate_pct']}%")
col3.metric("ICU Stay Rate", f"{kpi['icu_stay_rate_pct']}%")
col4.metric("Prolonged Stay Rate", f"{kpi['prolonged_hospital_stay_rate_pct']}%")
col5.metric("Avg ICU Days", f"{kpi['avg_icu_days']}")
col6.metric("Avg Hospital LOS", f"{kpi['avg_hospital_length_of_stay']} days")



# Tabs

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Case Volume",
        "Department Outcomes",
        "Operation Type Outcomes",
        "Risk Factors",
        "Model Results",
        "Risk Explorer"
    ]
)



# Tab 1: Case Volume

with tab1:
    st.subheader("Case Volume by Department")

    fig_dept_volume = px.bar(
        department_outcomes,
        x="case_count",
        y="department",
        orientation="h",
        title="Case Volume by Department",
        labels={"case_count": "Number of Cases", "department": "Department"}
    )
    fig_dept_volume.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_dept_volume, use_container_width=True)

    st.dataframe(department_outcomes)

    st.subheader("Case Volume by Operation Type")

    fig_op_volume = px.bar(
        operation_type_outcomes,
        x="case_count",
        y="operation_type",
        orientation="h",
        title="Case Volume by Operation Type",
        labels={"case_count": "Number of Cases", "operation_type": "Operation Type"}
    )
    fig_op_volume.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_op_volume, use_container_width=True)

    st.dataframe(operation_type_outcomes)



# Tab 2: Department Outcomes

with tab2:
    st.subheader("Department-Level Outcome Reporting")

    col1, col2 = st.columns(2)

    with col1:
        fig_dept_prolonged = px.bar(
            department_outcomes,
            x="prolonged_hospital_stay_rate_pct",
            y="department",
            orientation="h",
            title="Prolonged Hospital Stay Rate by Department",
            labels={
                "prolonged_hospital_stay_rate_pct": "Prolonged Stay Rate (%)",
                "department": "Department"
            }
        )
        fig_dept_prolonged.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_dept_prolonged, use_container_width=True)

    with col2:
        fig_dept_icu = px.bar(
            department_outcomes,
            x="icu_stay_rate_pct",
            y="department",
            orientation="h",
            title="ICU Stay Rate by Department",
            labels={
                "icu_stay_rate_pct": "ICU Stay Rate (%)",
                "department": "Department"
            }
        )
        fig_dept_icu.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_dept_icu, use_container_width=True)

    st.subheader("Department Outcomes Table")
    st.dataframe(department_outcomes)


# Tab 3: Operation Type Outcomes

with tab3:
    st.subheader("Operation Type Outcome Reporting")

    col1, col2 = st.columns(2)

    with col1:
        fig_op_prolonged = px.bar(
            prolonged_stay_operation,
            x="prolonged_hospital_stay_rate_pct",
            y="operation_type",
            orientation="h",
            title="Highest Prolonged Stay Rates by Operation Type",
            labels={
                "prolonged_hospital_stay_rate_pct": "Prolonged Stay Rate (%)",
                "operation_type": "Operation Type"
            }
        )
        fig_op_prolonged.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_op_prolonged, use_container_width=True)

    with col2:
        fig_op_icu = px.bar(
            icu_operation,
            x="icu_stay_rate_pct",
            y="operation_type",
            orientation="h",
            title="Highest ICU Stay Rates by Operation Type",
            labels={
                "icu_stay_rate_pct": "ICU Stay Rate (%)",
                "operation_type": "Operation Type"
            }
        )
        fig_op_icu.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_op_icu, use_container_width=True)

    st.subheader("Operation Type Outcomes Table")
    st.dataframe(operation_type_outcomes)


# Tab 4: Risk Factors

with tab4:
    st.subheader("ASA Class and Emergency Status")

    asa_clean = asa_outcomes.dropna(subset=["asa_class"]).copy()
    asa_clean["asa_class"] = asa_clean["asa_class"].astype(str)

    col1, col2 = st.columns(2)

    with col1:
        fig_asa = px.bar(
            asa_clean,
            x="asa_class",
            y="prolonged_hospital_stay_rate_pct",
            title="Prolonged Hospital Stay Rate by ASA Class",
            labels={
                "asa_class": "ASA Class",
                "prolonged_hospital_stay_rate_pct": "Prolonged Stay Rate (%)"
            }
        )
        st.plotly_chart(fig_asa, use_container_width=True)

    fig_asa.update_xaxes(type="category")
    st.caption(
        "Note: ASA 4 and ASA 6 have small sample sizes, so their rates should be interpreted cautiously."
    )
    with col2:
        fig_emergency = px.bar(
            emergency_outcomes,
            x="emergency_operation_label",
            y="prolonged_hospital_stay_rate_pct",
            title="Prolonged Hospital Stay: Emergency vs Non-Emergency",
            labels={
                "emergency_operation_label": "Emergency Status",
                "prolonged_hospital_stay_rate_pct": "Prolonged Stay Rate (%)"
            }
        )
        st.plotly_chart(fig_emergency, use_container_width=True)

    st.subheader("Emergency vs Non-Emergency Outcomes")
    st.dataframe(emergency_outcomes)

    st.subheader("Prolonged Stay Group Comparison")
    st.dataframe(prolonged_group)



# Tab 5: Model Results

with tab5:
    st.subheader("Machine Learning Model Results")

    st.markdown(
        """
        The modeling portion tested Random Forest and XGBoost models on three surgical outcome targets:
        in-hospital mortality, prolonged hospital stay, and ICU stay. The main final target was
        `prolonged_hospital_stay`, because mortality was highly imbalanced.
        """
    )

    
    # Model metrics from Aniqa's notebook
    

    model_results = pd.DataFrame({
        "Target": [
            "In-Hospital Death", "In-Hospital Death",
            "Prolonged Hospital Stay", "Prolonged Hospital Stay",
            "ICU Stay", "ICU Stay"
        ],
        "Model": [
            "Random Forest", "XGBoost",
            "Random Forest", "XGBoost",
            "Random Forest", "XGBoost"
        ],
        "Accuracy": [
            0.984346, 0.993738,
            0.984972, 0.998121,
            0.897934, 0.906700
        ],
        "Precision": [
            0.260870, 0.833333,
            0.943787, 0.993846,
            0.683511, 0.731707
        ],
        "Recall": [
            0.428571, 0.357143,
            0.984568, 0.996914,
            0.853821, 0.797342
        ],
        "F1 Score": [
            0.324324, 0.500000,
            0.963746, 0.995378,
            0.759232, 0.763116
        ]
    })

    st.subheader("Test Set Model Performance")
    st.dataframe(model_results, use_container_width=True)

    
    # F1 score comparison
    

    fig_f1 = px.bar(
        model_results,
        x="Target",
        y="F1 Score",
        color="Model",
        barmode="group",
        title="Model F1 Score by Prediction Target",
        labels={
            "F1 Score": "F1 Score",
            "Target": "Prediction Target"
        }
    )

    st.plotly_chart(fig_f1, use_container_width=True)

    
    # Precision / Recall comparison
    

    metric_long = model_results.melt(
        id_vars=["Target", "Model"],
        value_vars=["Precision", "Recall", "F1 Score"],
        var_name="Metric",
        value_name="Score"
    )

    fig_metrics = px.bar(
        metric_long,
        x="Target",
        y="Score",
        color="Metric",
        facet_col="Model",
        barmode="group",
        title="Precision, Recall, and F1 Score by Model",
        labels={
            "Score": "Score",
            "Target": "Prediction Target"
        }
    )

    st.plotly_chart(fig_metrics, use_container_width=True)

    
    # Key interpretation
    

    st.subheader("Model Interpretation")

    st.markdown(
        """
        **In-hospital death was difficult to predict reliably** because mortality was rare in the dataset.
        The models achieved high accuracy, but recall and F1 score were much weaker, showing that accuracy
        alone is misleading for imbalanced outcomes.

        **Prolonged hospital stay performed much better as a prediction target.** It had more positive cases
        than mortality and better represented recovery burden and hospital resource use.

        **ICU stay prediction showed moderate-to-strong performance.** Random Forest had slightly higher recall,
        while XGBoost had slightly higher accuracy and precision.
        """
    )

    st.warning(
        """
        Important modeling caveat: The prolonged hospital stay models may be inflated because some predictors
        are closely related to the outcome, including hospital_length_of_stay, admission/discharge time offsets,
        ICU days, and ICU stay status. For a true preoperative or early-risk prediction model, these leakage
        variables should be removed before final model evaluation.
        """
    )

    
    # Prolonged hospital stay feature importance
    

    st.subheader("Random Forest Feature Importance: Prolonged Hospital Stay")

    st.markdown(
        """
        The original feature importance ranking included variables directly related to hospital length of stay,
        such as admission/discharge time and hospital length of stay itself. Since those variables would leak
        the target outcome, this chart focuses on the top non-leakage clinical features.
        """
    )

    phs_feature_importance = pd.DataFrame({
        "Feature": [
            "preoperative_hemoglobin",
            "height",
            "preoperative_creatinine",
            "preoperative_platelet_count",
            "intraoperative_estimated_blood_loss",
            "bmi",
            "asa_class",
            "intraoperative_crystalloid",
            "age_numeric",
            "weight"
        ],
        "Importance": [
            0.053728,
            0.053300,
            0.051209,
            0.043581,
            0.036937,
            0.029033,
            0.023465,
            0.018583,
            0.016898,
            0.016644
        ]
    })

    fig_phs_importance = px.bar(
        phs_feature_importance.sort_values("Importance", ascending=True),
        x="Importance",
        y="Feature",
        orientation="h",
        title="Top 10 Non-Leakage Features for Prolonged Hospital Stay",
        labels={
            "Importance": "Feature Importance",
            "Feature": "Feature"
        },
        hover_data={
            "Feature": True,
            "Importance": ":.4f"
        }
    )

    st.plotly_chart(fig_phs_importance, use_container_width=True)

    st.caption(
        "This chart excludes identifiers and length-of-stay-derived variables to avoid target leakage."
    )
    
# Tab 6: Risk Explorer / Risk Stratification

with tab6:
    st.subheader("Interactive Prolonged Hospital Stay Risk Explorer")

    st.markdown(
        """
        This page uses a simple rules-based risk score to estimate whether a surgical case may be at
        higher risk for prolonged hospital stay. The score is based on the most interpretable non-leakage
        features from the model results, plus strong patterns found in the EDA and SQL reporting results.

        **Important:** This is a project prototype and is not intended for clinical decision-making.
        """
    )

    st.caption(
        "This risk score is a rules-based prototype informed by EDA, SQL findings, and model feature importance. "
        "It is not the trained Random Forest/XGBoost model."
    )

    
    # Helper function: risk scoring system
    

    def calculate_risk_score(
        age,
        bmi,
        asa_class,
        emergency_operation,
        operation_type,
        creatinine,
        hemoglobin,
        platelet_count,
        estimated_blood_loss,
        crystalloid
    ):
        score = 0
        reasons = []

        # Age
        if age >= 80:
            score += 2
            reasons.append(("Age ≥ 80", 2))
        elif age >= 60:
            score += 1
            reasons.append(("Age 60–79", 1))

        # BMI
        if bmi >= 30:
            score += 2
            reasons.append(("BMI ≥ 30", 2))
        elif bmi < 18.5:
            score += 2
            reasons.append(("BMI < 18.5", 2))

        # ASA class
        if asa_class >= 4:
            score += 5
            reasons.append(("ASA class ≥ 4", 5))
        elif asa_class == 3:
            score += 3
            reasons.append(("ASA class 3", 3))
        elif asa_class == 2:
            score += 1
            reasons.append(("ASA class 2", 1))

        # Emergency operation
        if emergency_operation == "Emergency":
            score += 3
            reasons.append(("Emergency operation", 3))

        # Operation type
        very_high_risk_ops = ["Transplantation"]
        high_risk_ops = ["Others", "Stomach", "Hepatic", "Vascular"]
        moderate_risk_ops = ["Biliary/Pancreas", "Colorectal", "Major resection"]

        if operation_type in very_high_risk_ops:
            score += 4
            reasons.append((f"High-risk operation type: {operation_type}", 4))
        elif operation_type in high_risk_ops:
            score += 3
            reasons.append((f"Higher-risk operation type: {operation_type}", 3))
        elif operation_type in moderate_risk_ops:
            score += 1
            reasons.append((f"Moderate-risk operation type: {operation_type}", 1))

        # Creatinine
        if creatinine >= 2.0:
            score += 3
            reasons.append(("Creatinine ≥ 2.0", 3))
        elif creatinine >= 1.2:
            score += 2
            reasons.append(("Creatinine 1.2–1.99", 2))

        # Hemoglobin
        if hemoglobin < 10:
            score += 3
            reasons.append(("Hemoglobin < 10", 3))
        elif hemoglobin < 12:
            score += 2
            reasons.append(("Hemoglobin 10–11.9", 2))

        # Platelet count
        if platelet_count < 100:
            score += 3
            reasons.append(("Platelet count < 100", 3))
        elif platelet_count < 150:
            score += 2
            reasons.append(("Platelet count 100–149", 2))

        # Estimated blood loss
        if estimated_blood_loss >= 1000:
            score += 2
            reasons.append(("Estimated blood loss ≥ 1000", 2))
        elif estimated_blood_loss >= 500:
            score += 1
            reasons.append(("Estimated blood loss 500–999", 1))

        # Crystalloid
        if crystalloid >= 4000:
            score += 2
            reasons.append(("Crystalloid ≥ 4000", 2))
        elif crystalloid >= 2000:
            score += 1
            reasons.append(("Crystalloid 2000–3999", 1))

        # Risk category
        if score <= 4:
            category = "Low Risk"
            estimated_range = "Lower than average"
            interpretation = "This case has relatively few risk factors for prolonged hospital stay."
        elif score <= 9:
            category = "Moderate Risk"
            estimated_range = "Around average to moderately elevated"
            interpretation = "This case has some risk factors associated with longer recovery."
        elif score <= 14:
            category = "High Risk"
            estimated_range = "Elevated"
            interpretation = "This case has multiple risk factors associated with prolonged hospital stay."
        else:
            category = "Very High Risk"
            estimated_range = "Strongly elevated"
            interpretation = "This case has several strong risk factors and should be considered high-risk in this prototype."

        return score, category, estimated_range, interpretation, reasons

    
    # User inputs
    

       # User inputs
    

    st.subheader("Patient and Surgical Inputs")
    with st.expander("What do these risk factors mean?"):
            st.markdown(
            """
            **Age**  
            Patient age at the time of surgery. Older age may be associated with slower recovery or more complications.  
            **In this prototype, age 60+ begins adding risk points.**

            **BMI**  
            Body Mass Index, based on height and weight. Very high or very low BMI may indicate higher surgical risk.  
            **General adult range:** BMI 18.5–24.9 is usually considered a healthy/normal range; 25–29.9 is overweight; 30+ is obese. 

            **ASA Class**  
            A preoperative physical status score used by anesthesia teams. Higher ASA class generally means the patient is sicker before surgery.  
            **General context:** ASA 1 means a healthy patient; ASA 2 means mild systemic disease; ASA 3+ indicates more serious disease burden.

            **Emergency Operation Status**  
            Whether the surgery was an emergency or non-emergency case. Emergency cases had higher prolonged hospital stay rates in our SQL analysis.  
            **General context:** Non-emergency is lower risk in this prototype; emergency status adds risk points.

            **Operation Type**  
            The broad surgery category, such as colorectal, transplantation, stomach, hepatic, or thyroid. Different operation types had different recovery patterns.  
            **General context:** In our dataset, transplantation, “Others,” stomach, hepatic, and vascular cases had higher prolonged-stay patterns.

            **Preoperative Creatinine**  
            A blood marker related to kidney function. Higher creatinine can suggest worse kidney function, which may increase recovery risk.  
            **Approximate adult reference range:** Around 0.7–1.2 mg/dL for men and 0.5–1.0 mg/dL for women, though this varies by lab, age, sex, and muscle mass.

            **Preoperative Hemoglobin**  
            A blood marker related to oxygen-carrying capacity. Lower hemoglobin can suggest anemia or reduced blood reserve before surgery.  
            **Approximate adult reference range:** Around 13.5–17.5 g/dL for men and 12.0–15.5 g/dL for women, though ranges vary by lab.

            **Preoperative Platelet Count**  
            Platelets help blood clot. A low platelet count may suggest higher bleeding risk or worse overall condition before surgery.  
            **Approximate adult reference range:** Around 150–450 thousand platelets per microliter of blood.

            **Estimated Blood Loss**  
            The estimated amount of blood lost during surgery. Higher blood loss can indicate a more complex or stressful operation.  
            **In this prototype, 500+ adds some risk and 1000+ adds more risk.**

            **Intraoperative Crystalloid**  
            IV fluid given during surgery. Higher fluid volume can reflect longer or more complex intraoperative management.  
            **In this prototype, 2000+ adds some risk and 4000+ adds more risk.**
            """
        )

    col1, col2, col3 = st.columns(3)

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.slider("Age", min_value=0, max_value=95, value=60)
        bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0, step=0.1)
        asa_class = st.selectbox("ASA Class", options=[1, 2, 3, 4, 6], index=1)

    with col2:
        emergency_operation = st.selectbox(
            "Emergency Operation Status",
            options=["Non-emergency", "Emergency"]
        )

        operation_options = sorted(operation_type_outcomes["operation_type"].dropna().unique())
        operation_type = st.selectbox(
            "Operation Type",
            options=operation_options
        )

        creatinine = st.number_input(
            "Preoperative Creatinine (mg/dL)",
            min_value=0.0,
            max_value=10.0,
            value=0.9,
            step=0.1
        )

    with col3:
        hemoglobin = st.number_input(
            "Preoperative Hemoglobin (g/dL)",
            min_value=0.0,
            max_value=25.0,
            value=13.0,
            step=0.1
        )

        platelet_count = st.number_input(
            "Preoperative Platelet Count (10³/µL)",
            min_value=0.0,
            max_value=1000.0,
            value=250.0,
            step=10.0
        )

        estimated_blood_loss = st.number_input(
            "Estimated Blood Loss (mL)",
            min_value=0.0,
            max_value=10000.0,
            value=200.0,
            step=50.0
        )

        crystalloid = st.number_input(
            "Intraoperative Crystalloid (mL)",
            min_value=0.0,
            max_value=20000.0,
            value=1000.0,
            step=100.0
        )

    
    # Calculate score
    

    score, category, estimated_range, interpretation, reasons = calculate_risk_score(
        age=age,
        bmi=bmi,
        asa_class=asa_class,
        emergency_operation=emergency_operation,
        operation_type=operation_type,
        creatinine=creatinine,
        hemoglobin=hemoglobin,
        platelet_count=platelet_count,
        estimated_blood_loss=estimated_blood_loss,
        crystalloid=crystalloid
    )

    st.subheader("Risk Stratification Result")

    col1, col2, col3 = st.columns(3)

    col1.metric("Risk Score", f"{score} points")
    col2.metric("Risk Category", category)
    col3.metric("Estimated Risk Level", estimated_range)

    st.info(interpretation)

    
    # Risk score explanation
    

    st.subheader("Risk Factor Breakdown")

    if reasons:
        reasons_df = pd.DataFrame(reasons, columns=["Risk Factor", "Points Added"])
        st.dataframe(reasons_df, use_container_width=True)

        reasons_chart = reasons_df.set_index("Risk Factor")

        st.bar_chart(
            reasons_chart,
            y="Points Added"
        )
    else:
        st.success("No additional risk points were added based on the selected inputs.")

    
    # Compare to historical SQL rates
    

    st.subheader("Comparison to Historical Dataset Rates")

    overall_rate = float(kpi["prolonged_hospital_stay_rate_pct"])

    selected_operation_row = operation_type_outcomes[
        operation_type_outcomes["operation_type"] == operation_type
    ]

    selected_asa_row = asa_outcomes[
        asa_outcomes["asa_class"] == float(asa_class)
    ]

    selected_emergency_row = emergency_outcomes[
        emergency_outcomes["emergency_operation_label"] == emergency_operation
    ]

    comparison_rows = [
        {
            "Group": "Overall Dataset",
            "Case Count": int(kpi["total_cases"]),
            "Prolonged Stay Rate (%)": overall_rate
        }
    ]

    if not selected_operation_row.empty:
        comparison_rows.append({
            "Group": f"Operation Type: {operation_type}",
            "Case Count": int(selected_operation_row["case_count"].iloc[0]),
            "Prolonged Stay Rate (%)": float(selected_operation_row["prolonged_hospital_stay_rate_pct"].iloc[0])
        })

    if not selected_asa_row.empty:
        comparison_rows.append({
            "Group": f"ASA Class: {asa_class}",
            "Case Count": int(selected_asa_row["case_count"].iloc[0]),
            "Prolonged Stay Rate (%)": float(selected_asa_row["prolonged_hospital_stay_rate_pct"].iloc[0])
        })

    if not selected_emergency_row.empty:
        comparison_rows.append({
            "Group": f"Emergency Status: {emergency_operation}",
            "Case Count": int(selected_emergency_row["case_count"].iloc[0]),
            "Prolonged Stay Rate (%)": float(selected_emergency_row["prolonged_hospital_stay_rate_pct"].iloc[0])
        })

    comparison_df = pd.DataFrame(comparison_rows)

    st.dataframe(comparison_df, use_container_width=True)

    comparison_chart = comparison_df.set_index("Group")

    st.bar_chart(
        comparison_chart,
        y="Prolonged Stay Rate (%)"
    )

    st.caption(
        "The risk score is a simplified educational prototype based on observed dataset patterns, "
        "non-leakage model feature importance, and SQL outcome summaries. It is not a validated clinical risk calculator."
    )