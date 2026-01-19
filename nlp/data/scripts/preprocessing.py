import pandas as pd
import re
from sklearn.model_selection import train_test_split
import os

# 📌 chemin relatif (portable)
CSV_PATH = "nlp/data/raw/medquad.csv"

def normalize_text(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
    return text

def load_medquad_csv(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Dataset not found at {csv_path}. "
            f"Please place medquad.csv inside nlp/data/raw/"
        )

    df = pd.read_csv(csv_path)
    df = df[["question", "answer", "focus_area"]].copy()
    return df

def preprocess(csv_path):

    os.makedirs("nlp/data/raw", exist_ok=True)
    os.makedirs("nlp/data/processed", exist_ok=True)

    df = load_medquad_csv(csv_path)

    df.to_csv("nlp/data/raw/medquad_raw.csv", index=False)

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

    print("✔ Dataset ready for all team members")

if __name__ == "__main__":
    preprocess(CSV_PATH)
    print("✓ MedQA dataset processed & saved successfully")

if __name__ == "__main__":
    preprocess()
