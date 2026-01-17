import pandas as pd
import re
from sklearn.model_selection import train_test_split
import os

# ----- Chemin dataset local (WINDOWS) ----- #
CSV_PATH = r"C:\Users\ayoub\Github\projet3-chatbot\project3-chatbot\nlp\data\raw\medquad.csv"

# ---------- Texte cleaning ----------- #
def normalize_text(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
    return text

# --------- Load MedQuAD CSV -------- #
def load_medquad_csv(csv_path):
    df = pd.read_csv(csv_path)

    # On garde seulement question + answer
    df = df[["question", "answer"]].copy()

    return df

# -------- Preprocess ----------- #
def preprocess(csv_path):

    os.makedirs("nlp/data/raw", exist_ok=True)
    os.makedirs("nlp/data/processed", exist_ok=True)

    df = load_medquad_csv(csv_path)
    df.to_csv("nlp/data/raw/medquad_raw.csv", index=False)

    # Nettoyage textes
    df["clean_question"] = df["question"].apply(normalize_text)
    df["clean_answer"] = df["answer"].apply(normalize_text)

    # Merge QA dans un seul champ si tu veux un seul jeu de texte
    df["text"] = df["clean_question"] + " " + df["clean_answer"]

    # Train / Test split
    train_df, test_df = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        shuffle=True
    )

    train_df.to_csv("nlp/data/processed/train.csv", index=False)
    test_df.to_csv("nlp/data/processed/test.csv", index=False)
    df.to_csv("nlp/data/processed/processed.csv", index=False)

    print("✔ MedQuAD dataset preprocessing done!")

if __name__ == "__main__":
    preprocess(CSV_PATH)
