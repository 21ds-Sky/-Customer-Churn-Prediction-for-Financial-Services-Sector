# -*- coding: utf-8 -*-
"""telco_customer_churn_prediction .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RRRmKQmJYSedAJ-LmcKZe75hC5JmNSwf

# Problem Description :
The Telco Customer Churn dataset consists of data from a telecommunications company.
The objective of this project is to predict customer churn, which is when a customer cancels their service or stops doing business with a company. The dataset contains information about customer demographics, account information, services used, and whether or not the customer churned.
The goal of this project is to build a model that can accurately predict which customers are likely to churn, so that the company
can take steps to prevent it.
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('Telco-Customer-Churn.csv')

# Get information about the dataset
df.info()

# Check for missing values
df.isnull().sum()

# Data cleaning and preprocessing
df.drop(['customerID'], axis=1, inplace=True)

# Convert categorical variables to dummy variables
cat_vars = ['gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'InternetService',
            'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
            'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod']
df = pd.get_dummies(df, columns=cat_vars, drop_first=True)

cat_cols = df.select_dtypes(include=['object']).columns.tolist()
from sklearn.preprocessing import LabelEncoder

# Extract categorical column names
cat_cols = df.select_dtypes(include=['object']).columns.tolist()

# Encode categorical variables
for col in cat_cols:
    label_encoder = LabelEncoder()
    df[col] = label_encoder.fit_transform(df[col])

# Plot distribution of target variable
sns.countplot(x='Churn', data=df)

# Separate features and target variable
X = df.drop(['Churn'], axis=1)
y = df['Churn']

df.info()

df.dtypes

# Convert 'TotalCharges' column to numeric, coercing errors to NaN
X['TotalCharges'] = pd.to_numeric(X['TotalCharges'], errors='coerce')

# Drop rows with NaN values in 'TotalCharges' column
X = X.dropna(subset=['TotalCharges'])

# Convert 'TotalCharges' column to numeric, coercing errors to NaN
X['TotalCharges'] = pd.to_numeric(X['TotalCharges'], errors='coerce')

# Drop rows with NaN values in 'TotalCharges' column
X = X.dropna(subset=['TotalCharges'])

# Drop corresponding rows from y
y = y[X.index]

# Apply feature selection
selector = SelectKBest(chi2, k=20)
X_selected = selector.fit_transform(X, y)

# Split data into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Import the classifier and fit the model on the training data
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression()
clf.fit(X_train, y_train)

# Make predictions on the testing data
y_pred = clf.predict(X_test)
print(y_pred)

# Evaluate the model
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
print("Accuracy Score: ", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

from sklearn.ensemble import RandomForestClassifier

rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)

rf_clf.fit(X_train, y_train)

rf_y_pred = rf_clf.predict(X_test)

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

print("Random Forest Accuracy Score: ", accuracy_score(y_test, rf_y_pred))
print("\nRandom Forest Confusion Matrix:\n", confusion_matrix(y_test, rf_y_pred))
print("\nRandom Forest Classification Report:\n", classification_report(y_test, rf_y_pred))

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Apply SMOTE to handle class imbalance
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# Initialize Random Forest Classifier
rf_clf = RandomForestClassifier(random_state=42)

# Hyperparameter tuning using GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(estimator=rf_clf, param_grid=param_grid, cv=5, n_jobs=-1)

# Fit the grid search to find the best parameters
grid_search.fit(X_train_resampled, y_train_resampled)

# Get the best parameters
best_params = grid_search.best_params_

# Initialize Random Forest Classifier with best parameters
best_rf_clf = RandomForestClassifier(**best_params, random_state=42)

# Train the model
best_rf_clf.fit(X_train_resampled, y_train_resampled)

# Make predictions
rf_y_pred = best_rf_clf.predict(X_test)

# Make predictions
rf_y_pred = best_rf_clf.predict(X_test)

# Evaluate the model
print("Random Forest Accuracy Score: ", accuracy_score(y_test, rf_y_pred))
print("\nRandom Forest Confusion Matrix:\n", confusion_matrix(y_test, rf_y_pred))
print("\nRandom Forest Classification Report:\n", classification_report(y_test, rf_y_pred))

# Summary of Achievements
print("\nSummary:")
print("1. Explored and cleaned the Telco Customer Churn dataset.")
print("2. Preprocessed the data by encoding categorical variables and handling missing values.")
print("3. Built and evaluated a Logistic Regression model with an accuracy of {:.2f}%.".format(accuracy_score(y_test, y_pred) * 100))
print("4. Built and evaluated a Random Forest model with an accuracy of {:.2f}%.".format(accuracy_score(y_test, rf_y_pred) * 100))
print("5. Handled class imbalance using SMOTE technique.")
print("6. Tuned the hyperparameters of the Random Forest model using GridSearchCV.")
print("7. Achieved a final accuracy of {:.2f}% with the tuned Random Forest model.".format(accuracy_score(y_test, rf_y_pred) * 100))