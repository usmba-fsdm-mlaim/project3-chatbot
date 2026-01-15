from datasets import load_dataset
import pandas as pd
import re
from sklearn.model_selection import train_test_split

def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_medqa():
    dataset = load_dataset("pubmed_qa", "pqa_labeled")

    data = dataset["train"]

    pairs = []

    for record in data:
        question = record["question"]
        answer_text = record["final_decision"]

        pairs.append({
            "role": "question",
            "text": question
        })
        pairs.append({
            "role": "answer",
            "text": answer_text
        })

    return pd.DataFrame(pairs)


def preprocess():
    df = load_medqa()
    df.to_csv("nlp/data/raw/Dataset_pubmedqa.csv", index=False)
    
    df["clean_text"] = df["text"].apply(normalize_text)

    train_df, test_df = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        shuffle=True
    )
    
    train_df.to_csv("nlp/data/processed/train.csv", index=False)
    test_df.to_csv("nlp/data/processed/test.csv", index=False)
    df.to_csv("nlp/data/processed/processed.csv", index=False)

    print("✓ MedQA dataset processed & saved successfully")

if __name__ == "__main__":
    preprocess()
