from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RESULTS_DIR = PROJECT_ROOT / "outputs" / "sql_results"
CHARTS_DIR = PROJECT_ROOT / "outputs" / "figures"

CHARTS_DIR.mkdir(parents=True, exist_ok=True)


def save_chart(filename):
    output_path = CHARTS_DIR / filename
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved chart: {output_path}")


def load_result(filename):
    path = RESULTS_DIR / filename
    if not path.exists():
        print(f"Missing file: {path}")
        return None
    return pd.read_csv(path)


def add_value_labels_bar(values, offset=0.5, suffix=""):
    for i, v in enumerate(values):
        plt.text(i, v + offset, f"{v:.2f}{suffix}", ha="center", fontsize=9)


def add_value_labels_barh(values, offset=0.5, suffix=""):
    for i, v in enumerate(values):
        plt.text(v + offset, i, f"{v:.2f}{suffix}", va="center", fontsize=9)


# 1. Overall KPIs

df = load_result("01_overall_kpis.csv")

if df is not None:
    kpi = df.iloc[0]

    outcome_rates = pd.DataFrame({
        "metric": [
            "Mortality Rate",
            "ICU Stay Rate",
            "Prolonged Stay Rate"
        ],
        "value": [
            kpi["mortality_rate_pct"],
            kpi["icu_stay_rate_pct"],
            kpi["prolonged_hospital_stay_rate_pct"]
        ]
    })

    plt.figure(figsize=(10, 5.625))
    plt.bar(outcome_rates["metric"], outcome_rates["value"])
    plt.title("Overall Surgical Outcome Rates", fontsize=16, fontweight="bold")
    plt.ylabel("Percent of Cases (%)")
    plt.ylim(0, outcome_rates["value"].max() + 8)

    add_value_labels_bar(outcome_rates["value"], suffix="%")

    save_chart("01_overall_surgical_outcome_rates.png")



# 2. Case Volume by Department


df = load_result("02_case_volume_by_department.csv")

if df is not None:
    df = df.sort_values("case_count", ascending=True)

    plt.figure(figsize=(10, 5.625))
    plt.barh(df["department"], df["case_count"])
    plt.title("Case Volume by Department", fontsize=16, fontweight="bold")
    plt.xlabel("Number of Cases")
    plt.ylabel("Department")

    for i, v in enumerate(df["case_count"]):
        plt.text(v + 50, i, f"{int(v):,}", va="center", fontsize=9)

    save_chart("02_case_volume_by_department.png")



# 3. Outcomes by Department


df = load_result("03_outcomes_by_department.csv")

if df is not None:
    df = df.sort_values("prolonged_hospital_stay_rate_pct", ascending=True)

    y = np.arange(len(df))
    width = 0.25

    plt.figure(figsize=(10, 5.625))
    plt.barh(y - width, df["mortality_rate_pct"], width, label="Mortality")
    plt.barh(y, df["icu_stay_rate_pct"], width, label="ICU Stay")
    plt.barh(y + width, df["prolonged_hospital_stay_rate_pct"], width, label="Prolonged Stay")

    plt.yticks(y, df["department"])
    plt.title("Outcome Rates by Department", fontsize=16, fontweight="bold")
    plt.xlabel("Outcome Rate (%)")
    plt.ylabel("Department")
    plt.legend()

    save_chart("03_outcome_rates_by_department.png")



# 4. Case Volume by Operation Type


df = load_result("04_case_volume_by_operation_type.csv")

if df is not None:
    df = df.sort_values("case_count", ascending=True)

    plt.figure(figsize=(10, 5.625))
    plt.barh(df["operation_type"], df["case_count"])
    plt.title("Case Volume by Operation Type", fontsize=16, fontweight="bold")
    plt.xlabel("Number of Cases")
    plt.ylabel("Operation Type")

    for i, v in enumerate(df["case_count"]):
        plt.text(v + 25, i, f"{int(v):,}", va="center", fontsize=8)

    save_chart("04_case_volume_by_operation_type.png")



# 5. Outcomes by Operation Type


df = load_result("05_outcomes_by_operation_type.csv")

if df is not None:
    df = df.sort_values("prolonged_hospital_stay_rate_pct", ascending=True)

    plt.figure(figsize=(10, 5.625))
    plt.barh(df["operation_type"], df["prolonged_hospital_stay_rate_pct"])
    plt.title("Prolonged Hospital Stay Rate by Operation Type", fontsize=16, fontweight="bold")
    plt.xlabel("Prolonged Hospital Stay Rate (%)")
    plt.ylabel("Operation Type")

    add_value_labels_barh(df["prolonged_hospital_stay_rate_pct"], suffix="%")

    save_chart("05_prolonged_stay_by_operation_type.png")



# 6. Outcomes by ASA Class


df = load_result("06_outcomes_by_asa_class.csv")

if df is not None:
    df = df.dropna(subset=["asa_class"]).copy()
    df["asa_class"] = df["asa_class"].astype(int).astype(str)

    plt.figure(figsize=(10, 5.625))
    plt.bar(df["asa_class"], df["prolonged_hospital_stay_rate_pct"])
    plt.title("Prolonged Hospital Stay Rate by ASA Class", fontsize=16, fontweight="bold")
    plt.xlabel("ASA Class")
    plt.ylabel("Prolonged Hospital Stay Rate (%)")
    plt.ylim(0, 100)

    add_value_labels_bar(df["prolonged_hospital_stay_rate_pct"], offset=2, suffix="%")

    save_chart("06_prolonged_stay_by_asa_class.png")



# 7. Emergency vs Non-Emergency Outcomes


df = load_result("07_emergency_vs_non_emergency_outcomes.csv")

if df is not None:
    x = np.arange(len(df))
    width = 0.25

    plt.figure(figsize=(10, 5.625))
    plt.bar(x - width, df["mortality_rate_pct"], width, label="Mortality")
    plt.bar(x, df["icu_stay_rate_pct"], width, label="ICU Stay")
    plt.bar(x + width, df["prolonged_hospital_stay_rate_pct"], width, label="Prolonged Stay")

    plt.xticks(x, df["emergency_operation_label"])
    plt.title("Emergency vs Non-Emergency Surgical Outcomes", fontsize=16, fontweight="bold")
    plt.ylabel("Outcome Rate (%)")
    plt.xlabel("Emergency Status")
    plt.ylim(0, 55)
    plt.legend()

    save_chart("07_emergency_vs_non_emergency_outcomes.png")



# 8. Highest Prolonged Stay by Operation Type


df = load_result("08_highest_prolonged_stay_by_operation_type.csv")

if df is not None:
    df = df.sort_values("prolonged_hospital_stay_rate_pct", ascending=True)

    plt.figure(figsize=(10, 5.625))
    plt.barh(df["operation_type"], df["prolonged_hospital_stay_rate_pct"])
    plt.title("Highest Prolonged Stay Rates by Operation Type", fontsize=16, fontweight="bold")
    plt.xlabel("Prolonged Hospital Stay Rate (%)")
    plt.ylabel("Operation Type")

    add_value_labels_barh(df["prolonged_hospital_stay_rate_pct"], suffix="%")

    save_chart("08_highest_prolonged_stay_by_operation_type.png")



# 9. Highest ICU Stay by Operation Type


df = load_result("09_highest_icu_stay_by_operation_type.csv")

if df is not None:
    df = df.sort_values("icu_stay_rate_pct", ascending=True)

    plt.figure(figsize=(10, 5.625))
    plt.barh(df["operation_type"], df["icu_stay_rate_pct"])
    plt.title("Highest ICU Stay Rates by Operation Type", fontsize=16, fontweight="bold")
    plt.xlabel("ICU Stay Rate (%)")
    plt.ylabel("Operation Type")

    add_value_labels_barh(df["icu_stay_rate_pct"], suffix="%")

    save_chart("09_highest_icu_stay_by_operation_type.png")



# 10. Patient Characteristics by Prolonged Stay Status


df = load_result("10_patient_characteristics_by_prolonged_stay.csv")

if df is not None:
    x = np.arange(len(df))
    width = 0.25

    plt.figure(figsize=(10, 5.625))
    plt.bar(x - width, df["emergency_case_rate_pct"], width, label="Emergency Case Rate")
    plt.bar(x, df["icu_stay_rate_pct"], width, label="ICU Stay Rate")
    plt.bar(x + width, df["avg_asa_class"] * 10, width, label="Avg ASA Class × 10")

    plt.xticks(x, df["prolonged_hospital_stay_label"])
    plt.title("Patient Characteristics by Prolonged Stay Status", fontsize=16, fontweight="bold")
    plt.ylabel("Value")
    plt.xlabel("Prolonged Hospital Stay Status")
    plt.legend()

    save_chart("10_patient_characteristics_by_prolonged_stay.png")


print("\nAll SQL visualizations created.")