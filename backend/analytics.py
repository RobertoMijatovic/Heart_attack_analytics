import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "dataset", "heart_attack_dataset.csv")
ART_DIR = os.path.join(BASE_DIR, "artifacts")

os.makedirs(ART_DIR, exist_ok=True)

def load_data():
    df = pd.read_csv(DATA_PATH)
    return df

def save_json(data, filename):

    path = os.path.join(ART_DIR, filename)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Saved: {filename}")

def save_plot(filename):

    path = os.path.join(ART_DIR, filename)

    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    print(f"Saved plot: {filename}")

def generate_kpis():

    df = load_data()

    kpis = {
        "total_patients": int(df.shape[0]),
        "average_age": float(df["age"].mean()),
        "average_cholesterol": float(df["cholesterol"].mean()),
        "average_resting_bp": float(df["resting_bp"].mean()),
        "average_bmi": float(df["bmi"].mean())
    }

    save_json(kpis, "kpis.json")

    return kpis

def generate_plots():

    df = load_data()

    # Age distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(
        data=df,
        x="age",
        bins=20,
        kde=True
    )
    plt.title("Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Count")
    save_plot("eda_age_distribution.png")


    # Cholesterol vs Heart Attack Risk
    plt.figure(figsize=(7, 4))
    sns.boxplot(
        data=df,
        x="heart_attack_risk",
        y="cholesterol"
    )
    plt.title("Cholesterol by Heart Attack Risk")
    plt.xlabel("Heart Attack Risk")
    plt.ylabel("Cholesterol")
    save_plot("eda_cholesterol_vs_risk.png")


    # Correlation Heatmap
    correlation = df.select_dtypes(include=np.number).corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )

    plt.title("Correlation Heatmap")
    save_plot("eda_correlation_heatmap.png")

if __name__ == "__main__":
    generate_kpis()
    generate_plots()