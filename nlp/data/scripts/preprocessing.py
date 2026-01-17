import pandas as pd
import re
from sklearn.model_selection import train_test_split
import os

CSV_PATH = r"C:\Users\ayoub\Github\projet3-chatbot\project3-chatbot\nlp\data\raw\medquad.csv"

# -------- Nettoyage texte -------- #
def normalize_text(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
    return text

# -------- Charger dataset -------- #
def load_medquad_csv(csv_path):
    df = pd.read_csv(csv_path)
    df = df[["question", "answer", "focus_area"]].copy()
    return df

# -------- Preprocessing pipeline -------- #
def preprocess(csv_path):

    os.makedirs("nlp/data/raw", exist_ok=True)
    os.makedirs("nlp/data/processed", exist_ok=True)

    df = load_medquad_csv(csv_path)

    # Sauvegarde brute (3 colonnes seulement)
    df.to_csv("nlp/data/raw/medquad_raw.csv", index=False)

    # Nettoyage interne
    df["question"] = df["question"].apply(normalize_text)
    df["answer"] = df["answer"].apply(normalize_text)
    df["focus_area"] = df["focus_area"].apply(normalize_text)

    # Split
    train_df, test_df = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        shuffle=True
    )

    # Sauvegarde finale (3 colonnes uniquement)
    train_df.to_csv("nlp/data/processed/train.csv", index=False)
    test_df.to_csv("nlp/data/processed/test.csv", index=False)
    df.to_csv("nlp/data/processed/processed.csv", index=False)

    print("✔ Final dataset ready with columns: question, answer, focus_area")

if __name__ == "__main__":
    preprocess(CSV_PATH)
