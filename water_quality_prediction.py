"""
=========================================================
Water Quality Prediction using Machine Learning

M.Tech Final Year Project

Author : Your Name
Guide : Your Guide Name

Dataset:
water_potability.csv

=========================================================
"""

# ==========================================================
# Import Required Libraries
# ==========================================================

import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# ==========================================================
# Create Output Folders
# ==========================================================

os.makedirs("outputs", exist_ok=True)
os.makedirs("models", exist_ok=True)

# ==========================================================
# Load Dataset
# ==========================================================

print("="*70)
print("Loading Dataset...")
print("="*70)

DATA_PATH = "water_potability.csv"

df = pd.read_csv(DATA_PATH)

print("\nDataset Loaded Successfully.\n")

# ==========================================================
# Dataset Information
# ==========================================================

print("="*70)
print("Dataset Shape")
print("="*70)

print(df.shape)

print("\n")

print("="*70)
print("Dataset Information")
print("="*70)

print(df.info())

print("\n")

print("="*70)
print("First Five Records")
print("="*70)

print(df.head())

print("\n")

print("="*70)
print("Statistical Summary")
print("="*70)

print(df.describe())

# ==========================================================
# Missing Values
# ==========================================================

print("\n")
print("="*70)
print("Missing Values")
print("="*70)

print(df.isnull().sum())

# ==========================================================
# Missing Value Visualization
# ==========================================================

plt.figure(figsize=(8,5))

sns.heatmap(df.isnull(),
            cbar=False,
            cmap="viridis")

plt.title("Missing Values")

plt.savefig("outputs/missing_values.png")

plt.show()

# ==========================================================
# Handle Missing Values
# ==========================================================

print("\n")
print("="*70)
print("Replacing Missing Values using Median")
print("="*70)

imputer = SimpleImputer(strategy="median")

df[df.columns] = imputer.fit_transform(df)

print(df.isnull().sum())

# ==========================================================
# Check Duplicate Rows
# ==========================================================

print("\n")
print("="*70)
print("Duplicate Rows")
print("="*70)

duplicates = df.duplicated().sum()

print("Duplicate Records :", duplicates)

if duplicates > 0:

    df.drop_duplicates(inplace=True)

# ==========================================================
# Class Distribution
# ==========================================================

plt.figure(figsize=(6,5))

sns.countplot(
    x="Potability",
    data=df,
    palette="Set2"
)

plt.title("Class Distribution")

plt.savefig("outputs/class_distribution.png")

plt.show()

# ==========================================================
# Correlation Heatmap
# ==========================================================

plt.figure(figsize=(10,8))

sns.heatmap(
    df.corr(),
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")

plt.savefig("outputs/correlation_heatmap.png")

plt.show()

# ==========================================================
# Distribution Plots
# ==========================================================

numerical_columns = df.columns[:-1]

for column in numerical_columns:

    plt.figure(figsize=(6,4))

    sns.histplot(
        df[column],
        kde=True,
        color="steelblue"
    )

    plt.title(column)

    plt.savefig(f"outputs/{column}_distribution.png")

    plt.close()

print("Distribution plots saved.")

# ==========================================================
# Boxplots
# ==========================================================

plt.figure(figsize=(15,8))

df.boxplot()

plt.xticks(rotation=45)

plt.title("Boxplots of Features")

plt.savefig("outputs/boxplots.png")

plt.show()

# ==========================================================
# Outlier Detection using IQR
# ==========================================================

print("\n")
print("="*70)
print("Outlier Detection")
print("="*70)

for column in numerical_columns:

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower) |
        (df[column] > upper)
    ]

    print(f"{column:20s} : {len(outliers)}")

# ==========================================================
# Feature Matrix
# ==========================================================

X = df.drop("Potability", axis=1)

y = df["Potability"]

print("\n")
print("="*70)
print("Features")
print("="*70)

print(X.columns)

# ==========================================================
# Feature Scaling
# ==========================================================

print("\nApplying StandardScaler...")

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print("Scaling Completed.")

# ==========================================================
# Train Test Split
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\n")

print("="*70)
print("Training Samples :", X_train.shape)
print("Testing Samples  :", X_test.shape)
print("="*70)

# ==========================================================
# Ready for Model Building
# ==========================================================

print("\n")
print("="*70)
print("Preprocessing Completed Successfully")
print("Ready for Model Training...")
print("="*70)

# ==========================================================
# PART 2B : MODEL TRAINING AND EVALUATION
# ==========================================================

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay,
    RocCurveDisplay
)

import joblib

# ==========================================================
# Try importing XGBoost
# ==========================================================

try:
    from xgboost import XGBClassifier
    xgb_available = True
except ImportError:
    print("\nXGBoost not installed. Skipping...")
    xgb_available = False

# ==========================================================
# Dictionary to Store Results
# ==========================================================

results = {}

# ==========================================================
# Evaluation Function
# ==========================================================

def evaluate_model(model, name):

    print("\n" + "=" * 70)
    print(f"Training : {name}")
    print("=" * 70)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X_test)[:, 1]
    else:
        probabilities = model.decision_function(X_test)

    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(y_test, predictions)

    recall = recall_score(y_test, predictions)

    f1 = f1_score(y_test, predictions)

    roc = roc_auc_score(y_test, probabilities)

    print("\nAccuracy :", round(accuracy,4))
    print("Precision:", round(precision,4))
    print("Recall   :", round(recall,4))
    print("F1 Score :", round(f1,4))
    print("ROC AUC  :", round(roc,4))

    print("\nClassification Report\n")

    print(classification_report(y_test, predictions))

    # Store Results

    results[name] = {
        "Model": model,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1": f1,
        "ROC": roc
    }

    # Confusion Matrix

    cm = confusion_matrix(y_test, predictions)

    disp = ConfusionMatrixDisplay(cm)

    disp.plot()

    plt.title(name + " Confusion Matrix")

    plt.savefig(f"outputs/{name}_confusion_matrix.png")

    plt.close()

    # ROC Curve

    RocCurveDisplay.from_estimator(model, X_test, y_test)

    plt.title(name + " ROC Curve")

    plt.savefig(f"outputs/{name}_roc_curve.png")

    plt.close()

    return model

# ==========================================================
# Logistic Regression
# ==========================================================

logistic = LogisticRegression(max_iter=1000)

evaluate_model(logistic, "Logistic_Regression")

# ==========================================================
# Decision Tree
# ==========================================================

decision_tree = DecisionTreeClassifier(
    max_depth=6,
    random_state=42
)

evaluate_model(decision_tree, "Decision_Tree")

# ==========================================================
# KNN
# ==========================================================

knn = KNeighborsClassifier(
    n_neighbors=7
)

evaluate_model(knn, "KNN")

# ==========================================================
# Support Vector Machine
# ==========================================================

svm = SVC(
    probability=True,
    kernel="rbf",
    random_state=42
)

evaluate_model(svm, "SVM")

# ==========================================================
# Random Forest
# ==========================================================

random_forest = RandomForestClassifier(

    n_estimators=200,

    random_state=42,

    max_depth=10
)

evaluate_model(random_forest, "Random_Forest")

# ==========================================================
# Gradient Boosting
# ==========================================================

gradient_boost = GradientBoostingClassifier(

    random_state=42

)

evaluate_model(gradient_boost, "Gradient_Boosting")

# ==========================================================
# XGBoost
# ==========================================================

if xgb_available:

    xgb = XGBClassifier(

        random_state=42,

        eval_metric="logloss"

    )

    evaluate_model(xgb, "XGBoost")

# ==========================================================
# Deep Learning (Artificial Neural Network)
# ==========================================================

mlp = MLPClassifier(
    hidden_layer_sizes=(64, 32, 16),
    max_iter=1000,
    random_state=42
)

evaluate_model(mlp, "Neural_Network")

# ==========================================================
# Model Comparison Table
# ==========================================================

comparison = pd.DataFrame({

    model: {

        "Accuracy": results[model]["Accuracy"],

        "Precision": results[model]["Precision"],

        "Recall": results[model]["Recall"],

        "F1 Score": results[model]["F1"],

        "ROC AUC": results[model]["ROC"]

    }

    for model in results

}).T

comparison = comparison.sort_values(

    by="Accuracy",

    ascending=False

)

print("\n")

print("="*70)

print("MODEL COMPARISON")

print("="*70)

print(comparison)

comparison.to_csv(

    "outputs/model_comparison.csv"

)

# ==========================================================
# Accuracy Comparison Plot
# ==========================================================

plt.figure(figsize=(10,6))

comparison["Accuracy"].plot(

    kind="bar"

)

plt.ylabel("Accuracy")

plt.title("Model Comparison")

plt.tight_layout()

plt.savefig(

    "outputs/model_comparison.png"

)

plt.show()

# ==========================================================
# Best Model Selection
# ==========================================================

best_model_name = comparison.index[0]

best_model = results[best_model_name]["Model"]

print("\n")

print("="*70)

print("BEST MODEL")

print("="*70)

print(best_model_name)

print("Accuracy :", results[best_model_name]["Accuracy"])

# ==========================================================
# Save Best Model
# ==========================================================

joblib.dump(

    best_model,

    "models/best_model.pkl"

)

joblib.dump(

    scaler,

    "models/scaler.pkl"

)

print("\nBest model saved successfully.")

# ==========================================================
# PART 2C : HYPERPARAMETER TUNING & CROSS VALIDATION
# ==========================================================

from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold,
    cross_val_score,
    learning_curve,
    validation_curve
)

from sklearn.inspection import permutation_importance

# ==========================================================
# CROSS VALIDATION
# ==========================================================

print("\n" + "="*70)
print("10-FOLD STRATIFIED CROSS VALIDATION")
print("="*70)

cv = StratifiedKFold(
    n_splits=10,
    shuffle=True,
    random_state=42
)

for name, value in results.items():

    model = value["Model"]

    scores = cross_val_score(
        model,
        X_scaled,
        y,
        cv=cv,
        scoring="accuracy"
    )

    print(f"\n{name}")

    print("Fold Accuracy :", np.round(scores,4))

    print("Mean Accuracy :", round(scores.mean(),4))

    print("Std Deviation :", round(scores.std(),4))

# ==========================================================
# RANDOM FOREST GRID SEARCH
# ==========================================================

print("\n")
print("="*70)
print("GRID SEARCH : RANDOM FOREST")
print("="*70)

rf_parameters = {

    "n_estimators":[100,200,300],

    "max_depth":[5,10,15,None],

    "min_samples_split":[2,5,10],

    "min_samples_leaf":[1,2,4]

}

rf_grid = GridSearchCV(

    estimator=RandomForestClassifier(random_state=42),

    param_grid=rf_parameters,

    cv=5,

    scoring="accuracy",

    n_jobs=-1

)

rf_grid.fit(X_train,y_train)

print("\nBest Parameters")

print(rf_grid.best_params_)

print("\nBest Accuracy")

print(round(rf_grid.best_score_,4))

best_rf = rf_grid.best_estimator_

# ==========================================================
# RANDOM FOREST FEATURE IMPORTANCE
# ==========================================================

print("\n")
print("="*70)
print("FEATURE IMPORTANCE")
print("="*70)

importance = pd.DataFrame({

    "Feature":X.columns,

    "Importance":best_rf.feature_importances_

})

importance = importance.sort_values(

    by="Importance",

    ascending=False

)

print(importance)

plt.figure(figsize=(10,6))

plt.barh(

    importance["Feature"],

    importance["Importance"]
)

plt.gca().invert_yaxis()

plt.title("Random Forest Feature Importance")

plt.tight_layout()

plt.savefig("outputs/feature_importance.png")

plt.show()

# ==========================================================
# PERMUTATION IMPORTANCE
# ==========================================================

print("\n")
print("="*70)
print("PERMUTATION IMPORTANCE")
print("="*70)

perm = permutation_importance(

    best_rf,

    X_test,

    y_test,

    n_repeats=10,

    random_state=42

)

perm_df = pd.DataFrame({

    "Feature":X.columns,

    "Importance":perm.importances_mean

})

perm_df = perm_df.sort_values(

    by="Importance",

    ascending=False

)

print(perm_df)

plt.figure(figsize=(10,6))

plt.barh(

    perm_df["Feature"],

    perm_df["Importance"]

)

plt.gca().invert_yaxis()

plt.title("Permutation Importance")

plt.tight_layout()

plt.savefig("outputs/permutation_importance.png")

plt.show()

# ==========================================================
# LEARNING CURVE
# ==========================================================

print("\n")
print("="*70)
print("LEARNING CURVE")
print("="*70)

train_sizes, train_scores, test_scores = learning_curve(

    best_rf,

    X_scaled,

    y,

    cv=5,

    scoring="accuracy",

    train_sizes=np.linspace(0.1,1.0,10),

    random_state=42

)

train_mean = np.mean(train_scores,axis=1)

test_mean = np.mean(test_scores,axis=1)

plt.figure(figsize=(8,6))

plt.plot(train_sizes,train_mean,label="Training Accuracy")

plt.plot(train_sizes,test_mean,label="Validation Accuracy")

plt.xlabel("Training Samples")

plt.ylabel("Accuracy")

plt.title("Learning Curve")

plt.legend()

plt.grid(True)

plt.savefig("outputs/learning_curve.png")

plt.show()

# ==========================================================
# VALIDATION CURVE
# ==========================================================

print("\n")
print("="*70)
print("VALIDATION CURVE")
print("="*70)

param_range = [50,100,150,200,250,300]

train_scores,test_scores = validation_curve(

    RandomForestClassifier(random_state=42),

    X_scaled,

    y,

    param_name="n_estimators",

    param_range=param_range,

    cv=5,

    scoring="accuracy"

)

train_mean = np.mean(train_scores,axis=1)

test_mean = np.mean(test_scores,axis=1)

plt.figure(figsize=(8,6))

plt.plot(param_range,train_mean,label="Training")

plt.plot(param_range,test_mean,label="Validation")

plt.xlabel("Number of Trees")

plt.ylabel("Accuracy")

plt.title("Validation Curve")

plt.legend()

plt.grid(True)

plt.savefig("outputs/validation_curve.png")

plt.show()

# ==========================================================
# SAVE TUNED RANDOM FOREST
# ==========================================================

joblib.dump(

    best_rf,

    "models/tuned_random_forest.pkl"

)

print("\n")
print("="*70)
print("TUNED RANDOM FOREST SAVED")
print("="*70)

# ==========================================================
# PART 2D : EXPLAINABILITY, PREDICTION & MODEL SAVING
# ==========================================================

from sklearn.metrics import PrecisionRecallDisplay
import joblib

# ==========================================================
# SHAP Explainability (Optional)
# ==========================================================

print("\n" + "=" * 70)
print("SHAP EXPLAINABILITY")
print("=" * 70)

try:
    import shap

    explainer = shap.TreeExplainer(best_rf)

    shap_values = explainer.shap_values(X_test)

    plt.figure(figsize=(10,6))

    shap.summary_plot(
        shap_values,
        X_test,
        feature_names=X.columns,
        show=False
    )

    plt.tight_layout()

    plt.savefig("outputs/shap_summary.png")

    plt.close()

    print("SHAP Summary saved.")

except Exception as e:

    print("SHAP skipped.")

    print(e)

# ==========================================================
# Precision Recall Curve
# ==========================================================

print("\nGenerating Precision Recall Curve...")

PrecisionRecallDisplay.from_estimator(

    best_rf,

    X_test,

    y_test

)

plt.title("Precision Recall Curve")

plt.savefig("outputs/precision_recall_curve.png")

plt.close()

# ==========================================================
# Load Saved Model
# ==========================================================

print("\nLoading Saved Model...")

loaded_model = joblib.load("models/best_model.pkl")

loaded_scaler = joblib.load("models/scaler.pkl")

print("Model Loaded Successfully.")

# ==========================================================
# Predict Example Sample
# ==========================================================

sample = pd.DataFrame({

    "ph":[7.2],

    "Hardness":[205],

    "Solids":[20791],

    "Chloramines":[7.3],

    "Sulfate":[330],

    "Conductivity":[420],

    "Organic_carbon":[10.4],

    "Trihalomethanes":[78],

    "Turbidity":[4.5]

})

sample_scaled = loaded_scaler.transform(sample)

prediction = loaded_model.predict(sample_scaled)[0]

probability = loaded_model.predict_proba(sample_scaled)[0][1]

print("\n")

print("="*70)

print("PREDICTION")

print("="*70)

if prediction==1:

    print("Water is POTABLE")

else:

    print("Water is NOT POTABLE")

print("Probability :",round(probability,4))

# ==========================================================
# Interactive Prediction
# ==========================================================

print("\n")
print("="*70)
print("INTERACTIVE PREDICTION")
print("="*70)

choice = input("Do you want to test your own sample? (y/n): ")

if choice.lower()=="y":

    ph=float(input("pH : "))

    hardness=float(input("Hardness : "))

    solids=float(input("Solids : "))

    chloramines=float(input("Chloramines : "))

    sulfate=float(input("Sulfate : "))

    conductivity=float(input("Conductivity : "))

    organic=float(input("Organic Carbon : "))

    thm=float(input("Trihalomethanes : "))

    turbidity=float(input("Turbidity : "))

    new_data=pd.DataFrame({

        "ph":[ph],

        "Hardness":[hardness],

        "Solids":[solids],

        "Chloramines":[chloramines],

        "Sulfate":[sulfate],

        "Conductivity":[conductivity],

        "Organic_carbon":[organic],

        "Trihalomethanes":[thm],

        "Turbidity":[turbidity]

    })

    new_scaled=loaded_scaler.transform(new_data)

    pred=loaded_model.predict(new_scaled)[0]

    prob=loaded_model.predict_proba(new_scaled)[0][1]

    print("\n")

    if pred==1:

        print("Prediction : POTABLE")

    else:

        print("Prediction : NOT POTABLE")

    print("Probability :",round(prob,4))

# ==========================================================
# Save Prediction
# ==========================================================

prediction_df=pd.DataFrame({

    "Prediction":[prediction],

    "Probability":[probability]

})

prediction_df.to_csv(

    "outputs/final_prediction.csv",

    index=False

)

# ==========================================================
# Final Summary
# ==========================================================

print("\n")
print("="*70)
print("PROJECT SUMMARY")
print("="*70)

print("Dataset Shape :",df.shape)

print("Training Samples :",len(X_train))

print("Testing Samples :",len(X_test))

print("Number of Features :",X.shape[1])

print("Best Model :",best_model_name)

print("Best Accuracy :",round(results[best_model_name]["Accuracy"],4))

print("Outputs saved in outputs/ folder")

print("Models saved in models/ folder")

print("="*70)

print("PROJECT COMPLETED SUCCESSFULLY")

print("="*70)
