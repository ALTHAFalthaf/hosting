from datetime import datetime
from .models import VaccineSchedule


def calculate_age(date_of_birth):
    today = datetime.now().date()
    age_in_months = (today - date_of_birth).days / 30
    return age_in_months

def get_vaccines_for_age(age):
    return VaccineSchedule.objects.filter(age=age).values_list('vaccine_name', flat=True)



# # Importing necessary libraries
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load the dataset from CSV file with correct column names
# data = pd.read_csv('dataset1.csv', names=['BMDSTATS', 'RIAGENDR', 'RIDAGEYR', 'BMXWT', 'BHXHT', 'BMXLEG', 'BOXARML', 'BMXARMC', 'BMXWAIST', 'BMXHIP', 'OUTMAL'])

# # Drop the first row if it contains data instead of column names
# data = data.drop(index=0).reset_index(drop=True)

# # Split dataset into features (X) and target variable (y)
# X = data.drop(columns=['OUTMAL'])
# y = data['OUTMAL']

# # Train-test split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Add separation between Random Forest and Decision Tree metrics
# print("\n------------------------------------------\n")

# # Ensemble Learning with Random Forest
# rf_model = RandomForestClassifier(random_state=42)
# rf_model.fit(X_train, y_train)
# rf_pred = rf_model.predict(X_test)

# # Evaluate Random Forest model
# rf_accuracy = accuracy_score(y_test, rf_pred)
# rf_precision = precision_score(y_test, rf_pred)
# rf_recall = recall_score(y_test, rf_pred)
# rf_f1 = f1_score(y_test, rf_pred)
# print("Random Forest Metrics:")
# print("Accuracy:", rf_accuracy)
# print("Precision:", rf_precision)
# print("Recall:", rf_recall)
# print("F1-score:", rf_f1)



# # Ensemble Learning with Decision Tree
# dt_model = DecisionTreeClassifier(random_state=42)
# dt_model.fit(X_train, y_train)
# dt_pred = dt_model.predict(X_test)

# # Evaluate Decision Tree model
# dt_accuracy = accuracy_score(y_test, dt_pred)
# dt_precision = precision_score(y_test, dt_pred)
# dt_recall = recall_score(y_test, dt_pred)
# dt_f1 = f1_score(y_test, dt_pred)
# print("Decision Tree Metrics:")
# print("Accuracy:", dt_accuracy)
# print("Precision:", dt_precision)
# print("Recall:", dt_recall)
# print("F1-score:", dt_f1)

# # Confusion matrix for Decision Tree



# # Ensemble Learning with Random Forest
# rf_model = RandomForestClassifier(random_state=42)
# rf_model.fit(X_train, y_train)

# # Get feature importances from Random Forest model
# rf_feature_importances = rf_model.feature_importances_



# # Ensemble Learning with Decision Tree
# dt_model = DecisionTreeClassifier(random_state=42)
# dt_model.fit(X_train, y_train)

# # Get feature importances from Decision Tree model
# dt_feature_importances = dt_model.feature_importances_



# # Function to calculate BMI
# def calculate_bmi(weight_kg, height_cm):
#     height_m = height_cm / 100
#     bmi = weight_kg / (height_m ** 2)
#     return bmi

# def calculate_z_score(measurement, mean, std_dev):
#     z_score = (measurement - mean) / std_dev
#     return z_score

# def calculate_weight_gain_rate(weight_initial, weight_final, time_period):
#     weight_gain_rate = (weight_final - weight_initial) / time_period
#     return weight_gain_rate

# def calculate_weight_status(bmi, age, gender):
#     # Define BMI percentile thresholds for different weight statuses
#     underweight_threshold = 5
#     normal_weight_threshold = 85
#     overweight_threshold = 95
    
#     # Use BMI percentile charts to determine weight status based on age and gender
#     if bmi < underweight_threshold:
#         return "Underweight"
#     elif underweight_threshold <= bmi < normal_weight_threshold:
#         return "Normal weight"
#     elif normal_weight_threshold <= bmi < overweight_threshold:
#         return "Overweight"
#     else:
#         return "Obese"

