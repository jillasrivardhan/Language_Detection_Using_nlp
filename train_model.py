import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# -------------------------
# Load Dataset
# -------------------------
data = pd.read_csv("media/balanced_language_dataset_clean.csv")   # your dataset name

X = data["Text"]
y = data["Language"]

# -------------------------
# Vectorization
# -------------------------
vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(1, 3))  # character-level n-grams

X_vectorized = vectorizer.fit_transform(X)

# -------------------------
# Train Model
# -------------------------
model = MultinomialNB()
model.fit(X_vectorized, y)

# -------------------------
# Save Files
# -------------------------
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Model and Vectorizer saved successfully!")