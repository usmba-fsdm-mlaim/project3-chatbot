import pandas as pd
import re
from sklearn.model_selection import train_test_split
from pathlib import Path
import os, kagglehub, shutil

DATASET_PATH = Path(kagglehub.dataset_download("pythonafroz/medquad-medical-question-answer-for-ai-research"))
DESTINATION_PATH = Path("nlp/data/raw")
DESTINATION_PATH.mkdir(parents=True, exist_ok=True)
shutil.copytree(DATASET_PATH, DESTINATION_PATH, dirs_exist_ok=True)
print(f"Dataset downloaded to: {DATASET_PATH}")
print(f"Dataset copied to: {DESTINATION_PATH}")
CSV_PATH = DESTINATION_PATH / "medquad.csv"
print(f"CSV Path: {CSV_PATH}")
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
    df = df.dropna(subset=["question", "answer", "focus_area"])
    df = df[["question", "answer", "focus_area"]].copy()
    return df

# -------- Preprocessing pipeline -------- #
def preprocess(csv_path):

    os.makedirs("nlp/data/raw", exist_ok=True)
    os.makedirs("nlp/data/processed", exist_ok=True)

    df = load_medquad_csv(csv_path)

    # Nettoyage interne
    df["question"] = df["question"].apply(normalize_text)
    df["answer"] = df["answer"].apply(normalize_text)
    df["focus_area"] = df["focus_area"].apply(normalize_text)
    
    # Split train/test
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    train_df.to_csv("nlp/data/processed/medquad_train.csv", index=False)
    test_df.to_csv("nlp/data/processed/medquad_validation.csv", index=False)

if __name__ == "__main__":
    preprocess(CSV_PATH)
    print("✓ MedQA dataset processed & saved successfully")
