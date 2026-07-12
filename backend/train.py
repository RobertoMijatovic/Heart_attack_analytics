import os
import json
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from analytics import generate_kpis, generate_plots


# =========================================================
# Putanje i osnovne postavke
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "heart_attack_dataset.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

ART_DIR = os.path.join(
    BASE_DIR,
    "artifacts"
)

TARGET = "heart_attack_risk"
SEED = 42

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(ART_DIR, exist_ok=True)

np.random.seed(SEED)
tf.random.set_seed(SEED)


# =========================================================
# Učitavanje i priprema dataseta
# =========================================================

def load_data():
    """
    Učitava CSV datoteku i uklanja stupce koji se ne koriste
    za treniranje modela.
    """

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Dataset nije pronađen: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    # Uklanjanje praznih razmaka iz naziva stupaca
    df.columns = [
        column.strip()
        for column in df.columns
    ]

    # Uklanjanje praznog stupca koji se ponekad pojavi
    # zbog zareza na kraju CSV retka
    unnamed_columns = [
        column
        for column in df.columns
        if column.lower().startswith("unnamed")
        or column == ""
    ]

    if unnamed_columns:
        df = df.drop(columns=unnamed_columns)

    if TARGET not in df.columns:
        raise ValueError(
            f"Target stupac '{TARGET}' ne postoji u datasetu."
        )

    return df


def prepare_features(df):
    """
    Razdvaja ulazne značajke X i ciljnu varijablu y.
    """

    columns_to_drop = [TARGET]

    # patient_id je samo identifikator i ne koristi se
    # za predikciju
    if "patient_id" in df.columns:
        columns_to_drop.append("patient_id")

    X = df.drop(columns=columns_to_drop)
    y = df[TARGET].astype(int)

    return X, y


# =========================================================
# Preprocessing
# =========================================================

def create_preprocessor(X):
    """
    Kreira preprocessing za numeričke i kategorijske stupce.
    """

    numeric_features = (
        X.select_dtypes(include=np.number)
        .columns
        .tolist()
    )

    categorical_features = (
        X.select_dtypes(exclude=np.number)
        .columns
        .tolist()
    )

    numeric_transformer = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median")
            ),
            (
                "scaler",
                StandardScaler()
            )
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent")
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                numeric_transformer,
                numeric_features
            ),
            (
                "cat",
                categorical_transformer,
                categorical_features
            )
        ]
    )

    return preprocessor


# =========================================================
# Pomoćne funkcije
# =========================================================

def calculate_metrics(y_true, y_pred):
    """
    Računa evaluacijske metrike klasifikacijskog modela.
    """

    return {
        "accuracy": float(
            accuracy_score(y_true, y_pred)
        ),
        "precision": float(
            precision_score(
                y_true,
                y_pred,
                zero_division=0
            )
        ),
        "recall": float(
            recall_score(
                y_true,
                y_pred,
                zero_division=0
            )
        ),
        "f1": float(
            f1_score(
                y_true,
                y_pred,
                zero_division=0
            )
        )
    }


def save_json(data, filename):
    """
    Sprema Python dictionary u JSON datoteku.
    """

    path = os.path.join(
        ART_DIR,
        filename
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=4
        )

    print(f"Spremljeno: {path}")


# =========================================================
# Random Forest
# =========================================================

def train_random_forest(
    X_train,
    X_test,
    y_train,
    y_test,
    base_preprocessor
):
    """
    Trenira Random Forest pipeline i sprema model.
    """

    print("\nTreniranje Random Forest modela...")

    random_forest = RandomForestClassifier(
        n_estimators=300,
        random_state=SEED,
        n_jobs=-1
    )

    # Clone stvara zasebnu kopiju preprocessora
    rf_preprocessor = clone(base_preprocessor)

    rf_model = Pipeline(
        steps=[
            (
                "preprocessor",
                rf_preprocessor
            ),
            (
                "classifier",
                random_forest
            )
        ]
    )

    rf_model.fit(
        X_train,
        y_train
    )

    rf_predictions = rf_model.predict(
        X_test
    )

    rf_metrics = calculate_metrics(
        y_test,
        rf_predictions
    )

    rf_path = os.path.join(
        MODEL_DIR,
        "rf_model.joblib"
    )

    joblib.dump(
        rf_model,
        rf_path
    )

    print(f"Random Forest spremljen: {rf_path}")
    print("Random Forest metrike:")

    for metric, value in rf_metrics.items():
        print(f"{metric}: {value:.4f}")

    return rf_model, rf_metrics


# =========================================================
# Deep Learning
# =========================================================

def build_deep_learning_model(input_dim):
    """
    Kreira neuronsku mrežu za binarnu klasifikaciju.
    """

    model = keras.Sequential(
        [
            layers.Input(
                shape=(input_dim,)
            ),
            layers.Dense(
                64,
                activation="relu"
            ),
            layers.Dropout(0.2),
            layers.Dense(
                32,
                activation="relu"
            ),
            layers.Dense(
                1,
                activation="sigmoid"
            )
        ]
    )

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    return model


def train_deep_learning(
    X_train,
    X_test,
    y_train,
    y_test,
    base_preprocessor
):
    """
    Priprema podatke, trenira neuronsku mrežu
    i sprema model i preprocessor.
    """

    print("\nPriprema podataka za Deep Learning...")

    dl_preprocessor = clone(
        base_preprocessor
    )

    X_train_prepared = (
        dl_preprocessor.fit_transform(
            X_train
        )
    )

    X_test_prepared = (
        dl_preprocessor.transform(
            X_test
        )
    )

    # OneHotEncoder može vratiti sparse matricu.
    # TensorFlowu šaljemo običan NumPy array.
    if hasattr(
        X_train_prepared,
        "toarray"
    ):
        X_train_prepared = (
            X_train_prepared.toarray()
        )

    if hasattr(
        X_test_prepared,
        "toarray"
    ):
        X_test_prepared = (
            X_test_prepared.toarray()
        )

    X_train_prepared = np.asarray(
        X_train_prepared,
        dtype=np.float32
    )

    X_test_prepared = np.asarray(
        X_test_prepared,
        dtype=np.float32
    )

    input_dim = X_train_prepared.shape[1]

    print(
        f"Broj ulaznih značajki nakon obrade: "
        f"{input_dim}"
    )

    dl_model = build_deep_learning_model(
        input_dim
    )

    print("\nTreniranje Deep Learning modela...")

    dl_model.fit(
        X_train_prepared,
        y_train.to_numpy(),
        validation_split=0.2,
        epochs=30,
        batch_size=32,
        verbose=1
    )

    dl_probabilities = dl_model.predict(
        X_test_prepared,
        verbose=0
    ).ravel()

    dl_predictions = (
        dl_probabilities >= 0.5
    ).astype(int)

    dl_metrics = calculate_metrics(
        y_test,
        dl_predictions
    )

    dl_model_path = os.path.join(
        MODEL_DIR,
        "dl_model.keras"
    )

    preprocessor_path = os.path.join(
        MODEL_DIR,
        "preprocessor.joblib"
    )

    dl_model.save(
        dl_model_path
    )

    joblib.dump(
        dl_preprocessor,
        preprocessor_path
    )

    print(
        f"Deep Learning model spremljen: "
        f"{dl_model_path}"
    )

    print(
        f"Preprocessor spremljen: "
        f"{preprocessor_path}"
    )

    print("Deep Learning metrike:")

    for metric, value in dl_metrics.items():
        print(f"{metric}: {value:.4f}")

    return dl_model, dl_preprocessor, dl_metrics


# =========================================================
# Glavna funkcija za treniranje
# =========================================================

def main():
    """
    Pokreće cijeli proces:
    1. učitavanje podataka
    2. preprocessing
    3. treniranje Random Foresta
    4. treniranje Deep Learning modela
    5. spremanje metrika
    6. ponovno generiranje KPI-ja i EDA grafova
    """

    print("=" * 60)
    print("POČETAK TRENIRANJA MODELA")
    print("=" * 60)

    df = load_data()

    print(
        f"Dataset učitan. Broj redaka: "
        f"{df.shape[0]}"
    )

    X, y = prepare_features(df)

    base_preprocessor = create_preprocessor(
        X
    )

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=SEED,
            stratify=y
        )
    )

    print(
        f"Trening skup: {X_train.shape[0]} redaka"
    )

    print(
        f"Testni skup: {X_test.shape[0]} redaka"
    )

    _, rf_metrics = train_random_forest(
        X_train,
        X_test,
        y_train,
        y_test,
        base_preprocessor
    )

    _, _, dl_metrics = train_deep_learning(
        X_train,
        X_test,
        y_train,
        y_test,
        base_preprocessor
    )

    metrics = {
        "random_forest": rf_metrics,
        "deep_learning": dl_metrics
    }

    save_json(
        metrics,
        "metrics.json"
    )

    print("\nPonovno računanje KPI pokazatelja...")

    generate_kpis()

    print("\nPonovno generiranje EDA grafova...")

    generate_plots()

    print("\n" + "=" * 60)
    print("TRENIRANJE USPJEŠNO ZAVRŠENO")
    print("=" * 60)

    return {
        "status": "success",
        "message": (
            "Modeli, metrike, KPI pokazatelji "
            "i grafovi uspješno su ažurirani."
        ),
        "metrics": metrics
    }


# =========================================================
# Pokretanje train.py iz terminala
# =========================================================

if __name__ == "__main__":
    main()