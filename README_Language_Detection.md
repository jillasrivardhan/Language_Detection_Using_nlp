# Language Detection Using NLP

A web-based language identification system that predicts the language of user-provided text using Natural Language Processing (NLP) and machine learning. The project combines a Django web application with a trained text-classification model to provide language predictions through a simple interface.

## Overview

Language identification is a common NLP task used in multilingual applications, content processing, translation workflows, and text analytics. This project converts text into numerical features using character-level TF-IDF n-grams and classifies it using a Multinomial Naive Bayes model.

The repository also includes user registration/login flows, an administrator interface for managing registered users, dataset viewing, and a model-training page that displays evaluation results.

## Features

- **Language prediction:** Enter text and receive a predicted language.
- **Character-level TF-IDF:** Uses character n-grams (1–3) to represent text.
- **Multinomial Naive Bayes:** Trained classifier for language classification.
- **Web application:** Django-based interface for accessing project functionality.
- **User registration and login:** Registration and login pages backed by the application's database.
- **Admin workflow:** Administrator login, registered-user viewing, and user activation workflow.
- **Dataset preview:** Displays a sample of the dataset in the web interface.
- **Training/evaluation page:** Trains a model from the cleaned dataset and displays accuracy, confusion matrix, and classification report.

## Machine Learning Workflow

```text
Input text
    │
    ▼
Character-level TF-IDF vectorization
(analyzer="char", n-gram range 1–3)
    │
    ▼
Multinomial Naive Bayes classifier
    │
    ▼
Predicted language
    │
    ▼
Display prediction in Django web interface
```

### Model details

| Component | Implementation |
|---|---|
| Task | Text language classification |
| Feature extraction | `TfidfVectorizer` |
| TF-IDF analyzer | Character |
| Character n-grams | 1 to 3 |
| Classifier | `MultinomialNB` |
| Model serialization | Pickle (`model.pkl`, `vectorizer.pkl`) |
| Web framework | Django |

The model and vectorizer are loaded from the saved pickle files when the prediction view is initialized.

## Tech Stack

- **Python**
- **Django**
- **Pandas**
- **NumPy**
- **Scikit-learn**
- **TF-IDF**
- **Multinomial Naive Bayes**
- **HTML, CSS**
- **SQLite**
- **Pickle**

## Project Structure

```text
Language_Detection_Using_nlp/
├── Admin/                         # Admin views and app configuration
├── users/                         # Registration, login, dataset and prediction views
├── language_detaction/             # Django project settings, URLs and WSGI/ASGI
├── templates/                      # HTML templates
│   ├── admins/                    # Admin pages
│   └── users/                     # User pages and prediction form
├── static/                         # CSS, images and frontend assets
├── media/
│   └── balanced_language_dataset_clean.csv
├── model.pkl                       # Trained classifier
├── vectorizer.pkl                  # Fitted TF-IDF vectorizer
├── train_model.py                  # Model training and serialization
├── clean_dataset.py                # Dataset-cleaning script
├── manage.py                       # Django management script
└── db.sqlite3                      # Local SQLite database (included in repo)
```

## Dataset

The cleaned dataset is stored at:

`media/balanced_language_dataset_clean.csv`

It contains two columns:

- `Text` — input text samples
- `Language` — target language labels

The dataset file currently contains 903 rows and 18 distinct label values. Dataset labels should be reviewed and standardized before retraining (for example, spelling consistency and any unintended label values).

> Dataset provenance, licensing, and the exact collection methodology should be documented if you redistribute or use this project beyond academic purposes.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repository>.git
cd Language_Detection_Using_nlp
```

Replace the repository URL with your own GitHub repository URL.

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

The repository does not currently include a `requirements.txt`. Install the main dependencies:

```bash
pip install django pandas numpy scikit-learn matplotlib seaborn
```

If you encounter a dependency/version issue, use a compatible Python and Django/scikit-learn version, then freeze the working environment:

```bash
pip freeze > requirements.txt
```

### 4. Verify model files

Ensure the following files exist in the project root:

```text
model.pkl
vectorizer.pkl
```

These are included in the repository. If you retrain the model, regenerate both files together so that the classifier and vectorizer correspond to the same training process.

### 5. Run database migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open the local server URL shown in the terminal (usually `http://127.0.0.1:8000/`).

## Usage

1. Start the Django server.
2. Open the project homepage.
3. Register a user account, if required.
4. Sign in through the user login page.
5. Navigate to the language prediction page.
6. Enter text and submit it.
7. View the predicted language displayed by the application.

The repository also provides routes/pages for dataset preview and model training/evaluation.

## Retraining the Model

The training script reads the cleaned CSV, extracts character-level TF-IDF features, trains a Multinomial Naive Bayes classifier, and saves the classifier and vectorizer as pickle files.

```bash
python train_model.py
```

The script expects the dataset at:

```text
media/balanced_language_dataset_clean.csv
```

It writes:

```text
model.pkl
vectorizer.pkl
```

**Important:** Keep the model and vectorizer paired. Do not replace one file without regenerating the other.

## Evaluation

The Django training page includes an evaluation workflow that splits the dataset into training and testing portions and displays:

- Accuracy
- Confusion matrix
- Classification report (precision, recall, and F1-score)

The model-training script and the training page currently use different classifier/vectorization configurations. For reproducible evaluation, standardize both workflows so they evaluate the same pipeline and data split.

## Application Routes

| Route | Purpose |
|---|---|
| `/` | Homepage |
| `/UserRegister/` | Registration page |
| `/UserLogin/` | User login page |
| `/AdminLogin/` | Admin login page |
| `/UserHome/` | User home page |
| `/prediction/` | Language prediction |
| `/training/` | Model training and evaluation results |
| `/DatasetView/` | Dataset preview |
| `/AdminHome/` | Admin home |
| `/RegisterUsersView/` | View registered users |
| `/ActivaUsers/` | User activation workflow |

Routes may require login or admin access depending on the application's flow.

## Limitations & Future Improvements

- Improve dataset quality and verify all language labels.
- Add a consistent preprocessing pipeline for training and prediction.
- Use a shared train/test split and model configuration for evaluation.
- Add automated tests for prediction, registration, and authentication flows.
- Improve authentication security by using Django's built-in password hashing and authentication system instead of storing/checking raw passwords.
- Add input validation, clearer error handling, and user-friendly feedback.
- Add confidence scores or top-k predictions, with calibration and evaluation before exposing them.
- Track per-language precision, recall, and F1 to identify weak classes.
- Add API endpoints for integration with other applications.
- Add deployment configuration, environment-based settings, and production security configuration.
- Add a reproducible `requirements.txt`, screenshots, and dataset/model documentation.

## Security Notes

This repository is configured as a development project. Before deploying publicly:

- Set `DEBUG = False`.
- Move the Django secret key to an environment variable and rotate the exposed development key.
- Configure `ALLOWED_HOSTS`.
- Use HTTPS and secure session/cookie settings.
- Review the authentication implementation and avoid storing plaintext passwords.
- Do not expose development databases or sensitive user data.
- Only load pickle files from trusted sources, since pickle deserialization can execute arbitrary code.

## Academic Project

**Project:** Language Detection Using NLP  
**Objective:** Identify the language of a text sample using machine learning and NLP techniques.  
**Core approach:** Character-level TF-IDF features with Multinomial Naive Bayes classification.  
**Web application:** Django.

## Contributing

Contributions, bug reports, and suggestions are welcome. Fork the repository, create a feature branch, make your changes, and open a pull request.

## License

See the [`LICENSE`](LICENSE) file for license details.
