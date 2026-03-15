from ast import alias
from concurrent.futures import process
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse
from django.contrib import messages

import language_detaction

from .forms import UserRegistrationForm
from .models import UserRegistrationModel
from django.conf import settings
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import datetime as dt
from sklearn import preprocessing, metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.metrics import classification_report


# Create your views here.

def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})

def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(
                loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})



def UserHome(request):
    return render(request, 'users/UserHomePage.html', {})

def DatasetView(request):
    path = settings.MEDIA_ROOT + "//" + 'balanced_language_dataset.csv'
    df = pd.read_csv(path, nrows=200)
    # df = df.to_html()
    table = df.to_html(index=False,classes="table table-bordered")
    print("data set view called")
    print(type(table))
    # return render(request, 'users/viewdataset.html', {'data': df})
    return render(request, 'users/viewdataset.html', {'data': table})
    



#=============================================================================================================

from django.shortcuts import render
import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Global variable for the model and vectorizer to be reused between views
# classifier = None
# vectorizer = None
# Load trained model and vectorizer

BASE_DIR = settings.BASE_DIR

model_path = os.path.join(BASE_DIR,"model.pkl")
vectorizer_path = os.path.join(BASE_DIR,"vectorizer.pkl")

classifier = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))

# temp debug
print("model path:", model_path)
print("vectorizer path:", vectorizer_path)

# Training View
def training(request):
    global classifier, vectorizer
    
    # Load the dataset
    # data = pd.read_csv(r'C:\Users\chund\Desktop\New folder (3)\language_detac\language_detaction\media\balanced_language_dataset.csv')
    path = os.path.join(settings.MEDIA_ROOT, 'balanced_language_dataset_clean.csv')
    data = pd.read_csv(path)
    X = data['Text']  # Text data
    y = data['Language']  # Labels (target)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Convert text data into numerical features using TF-IDF
    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Initialize and train the classifier (Logistic Regression)
    classifier = LogisticRegression()
    classifier.fit(X_train_tfidf, y_train)

    # Make predictions on the testing set
    y_pred = classifier.predict(X_test_tfidf)

    # Evaluate the model's performance
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred)

    # Render the training results to the HTML template
    return render(request, "users/training.html",{
        'accuracy': accuracy, 
        'conf_matrix': conf_matrix,
        'class_report': class_report
    })

#=======================================================================================================================


# Prediction View
def prediction(request):
    global classifier, vectorizer

    if request.method == 'POST':
        # Get the text input from the form
        # input_text = request.POST.get('input_text')
        input_text = request.POST.get('text')

        if not input_text:
            messages.error(request, "Please enter some text for prediction.")
            return render(request, 'users/predictForm.html',{'output':'please enter some text for prediction','entered_text':""})
        input_text = input_text.strip()
        

        # Convert input text into TF-IDF format using the trained vectorizer
        input_tfidf = vectorizer.transform([input_text])

        # Predict the language or label using the trained classifier
        single_prediction = classifier.predict(input_tfidf)[0]

        # Render the result to the HTML template
        return render(request, 'users/predictForm.html', {'output': single_prediction,'entered_text': input_text})

    # If not POST request, just render the form page
    return render(request, 'users/predictForm.html')
