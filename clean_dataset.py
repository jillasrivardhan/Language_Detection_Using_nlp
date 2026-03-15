import pandas as pd

data = pd.read_csv("media/balanced_language_dataset.csv", on_bad_lines='skip')

data.columns = ['Text', 'Language']

data = data.dropna()

data = data.drop_duplicates()

data.to_csv("media/balanced_language_dataset_clean.csv", index=False)

print("Dataset cleaned successfully")