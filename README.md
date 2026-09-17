# 💧 MizuBuddy: AI-Powered Water Quality & Potability Intelligence System

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-F7931E.svg)](https://scikit-learn.org/)
[![Explainable AI](https://img.shields.io/badge/XAI-SHAP%20%26%20Feature%20Importance-7B1FA2.svg)](https://shap.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Executive Summary

**MizuBuddy** is an end-to-end artificial intelligence platform designed for real-time **Water Quality Prediction, Potability Assessment, and Risk Remediation**. 

Water contamination poses severe global public health challenges. Traditional laboratory water quality testing requires manual sampling, expensive chemical assays, and significant delay. **MizuBuddy** addresses this by employing **Ensemble Machine Learning algorithms, Deep Artificial Neural Networks (ANN), and Explainable AI (XAI)** to predict water potability instantly based on **9 key physicochemical parameters**. 

The platform features:
- **FastAPI Microservice REST API Backend** for high-throughput prediction and AI chatbot interaction.
- **MizuAgent 2.0 Autonomous AI Assistant** powered by Google Gemini RAG for automated water filtration advice and live web control.
- **Streamlit Analytics Dashboard** for exploratory data analysis, SHAP explainability, and model benchmarking.
- **Modern Responsive Web Application** featuring real-time input sliders, WQI gauges, parameter safety status indicators, and targeted remediation tips.

---

## ✨ Key System Features

- **📊 Comprehensive Machine Learning Pipeline:**
  - Median-based missing data imputation (pH, Sulfate, Trihalomethanes).
  - Outlier detection and feature distribution analysis.
  - StandardScaler feature normalization.
  - Benchmarks **8 Classification Models** (SVM, Random Forest, Gradient Boosting, Decision Tree, XGBoost, MLP Neural Network, Logistic Regression, KNN).
- **🔬 Explainable AI (XAI):**
  - **SHAP (SHapley Additive exPlanations)** summary plots for feature contribution.
  - Feature Importance ranking, Permutation Importance, and Learning Curves.
  - ROC-AUC and Precision-Recall evaluation curves.
- **💧 Custom Water Quality Index (WQI):**
  - Computes a normalized WQI score (0–100) based on weighted WHO/EPA standard safety tolerances.
- **🛡️ Parameter Safety & Remediation Engine:**
  - Detects threshold violations across all 9 physicochemical parameters.
  - Generates custom, multi-stage water treatment strategies (e.g., Calcite Neutralizers, Reverse Osmosis, Granular Activated Carbon, UV Disinfection).
- **🤖 MizuAgent 2.0 AI Research Assistant:**
  - Embedded AI Agent integrated with Google Gemini API to analyze active water samples, provide water safety advice, and trigger live UI actions.
- **🌐 Dual User Interfaces:**
  - **Streamlit Interactive Dashboard** (`app.py`) for data scientists and analysts.
  - **Interactive Frontend Web App** (`frontend/index.html`) for end-users and field personnel.

---

## 🧪 Dataset Architecture & Physicochemical Features

The system utilizes the **Water Potability Dataset** containing **3,276 water samples** evaluated against international drinking water guidelines (WHO / EPA).

| Parameter | Full Name | Unit | WHO / EPA Safe Range | Health Impact / Description |
| :--- | :--- | :--- | :--- | :--- |
| **pH** | Hydrogen Ion Concentration | pH units | 6.5 – 8.5 | Indicates acidity or alkalinity. Low pH causes pipe corrosion; high pH leads to mineral scaling. |
| **Hardness** | Water Hardness | mg/L | < 300 mg/L | Concentration of Calcium & Magnesium. High hardness causes scale buildup in pipes and appliances. |
| **Solids** | Total Dissolved Solids (TDS) | ppm / mg/L | < 500 ppm | Total mineral and organic content. High TDS imparts bad taste and indicates mineral contamination. |
| **Chloramines** | Chloramine Residual | ppm / mg/L | < 4.0 ppm | Disinfectant agent added to municipal water. Excess levels cause taste issues and mucous membrane irritation. |
| **Sulfate** | Sulfate Content | mg/L | < 250 mg/L | Naturally occurring mineral. High concentrations (>250 mg/L) cause laxative effects and gastrointestinal distress. |
| **Conductivity** | Electrical Conductivity | μS/cm | < 800 μS/cm | Measures ionic concentration and salinity of water. High conductivity indicates dissolved salts. |
| **Organic Carbon** | Total Organic Carbon (TOC) | ppm / mg/L | < 15 ppm | Organic matter content. High TOC promotes bacterial growth and disinfectant byproduct formation. |
| **Trihalomethanes** | Trihalomethanes (THMs) | μg/L | < 80 μg/L | Chemical byproducts of chlorine disinfection. High levels are linked to carcinogenicity. |
| **Turbidity** | Water Turbidity / Clarity | NTU | < 1.0 NTU | Cloudiness caused by suspended particles. High turbidity shelters pathogens and reduces filtration efficacy. |

**Target Variable:**
- `Potability = 1`: Water is safe and drinkable.
- `Potability = 0`: Water is contaminated and non-potable.

---

## 📈 Model Comparison & Benchmark Performance

Eight machine learning and deep learning models were trained, tuned, and evaluated on a held-out test dataset:

| Model Name | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Support Vector Machine (SVM)** | **67.07%** | **70.41%** | 26.95% | 38.98% | **0.6487** | 🏆 **Best Model** |
| **Random Forest** | 66.46% | 74.32% | 21.48% | 33.33% | 0.6711 | 🥈 Runner-Up |
| **Gradient Boosting** | 65.24% | 64.29% | 24.61% | 35.59% | 0.6281 | Evaluated |
| **Decision Tree** | 64.18% | 59.46% | 25.78% | 35.97% | 0.6083 | Evaluated |
| **XGBoost** | 64.18% | 55.74% | 39.84% | 46.47% | 0.6256 | Evaluated |
| **Artificial Neural Network (MLP)** | 62.65% | 52.30% | **48.83%** | **50.51%** | 0.6378 | Deep Learning |
| **Logistic Regression** | 60.98% | 0.00% | 0.00% | 0.00% | 0.5485 | Baseline |
| **K-Nearest Neighbors (KNN)** | 58.54% | 44.87% | 27.34% | 33.98% | 0.5992 | Evaluated |

*Note: Models are saved in `models/best_model.pkl` and `models/scaler.pkl` for API inference.*

---

## 📁 Repository Structure

```gfm
Mtech Project/
├── api.py                        # FastAPI REST API Backend & MizuAgent 2.0 Endpoint
├── app.py                        # Streamlit Interactive Analytics Dashboard
├── water_quality_prediction.py   # Full Machine Learning & Deep Learning Pipeline
├── water_potability.csv          # Benchmark Water Quality Dataset (3,276 samples)
├── requirements.txt              # Project Python Dependencies
├── README.md                     # Quickstart & System README
├── PROJECT_DOCUMENTATION.md      # Detailed Technical Project Documentation & Report
├── .env                          # Environment Configuration (API Keys)
├── frontend/                     # Interactive Web Application Frontend
│   ├── index.html                # Single Page Web App Interface
│   ├── style.css                 # Custom Styling & Glassmorphism System
│   └── script.js                 # API Integration & UI Interactivity Logic
├── models/                       # Trained Serialized Machine Learning Artifacts
│   ├── best_model.pkl            # Trained Top-Performing Classifier Model (SVM/RF)
│   ├── scaler.pkl                # Trained StandardScaler Object
│   └── tuned_random_forest.pkl   # Hyperparameter-Tuned Random Forest Artifact
└── outputs/                      # Saved Analytical Visualizations & Benchmark CSVs
    ├── model_comparison.csv      # Model Performance Metrics Matrix
    ├── model_comparison.png      # Comparative Accuracy Chart
    ├── feature_importance.png    # Feature Importance Visualization
    ├── shap_summary.png          # SHAP Summary Explainability Plot
    ├── roc_curve.png             # Best Model Receiver Operating Characteristic
    └── missing_values.png        # Dataset Missing Values Heatmap
```

---

## 🛠️ Technology Stack

- **Programming Language:** Python 3.9+
- **Machine Learning & DL:** Scikit-Learn, XGBoost, LightGBM, SHAP, SciPy
- **Data Manipulation & Viz:** Pandas, NumPy, Matplotlib, Seaborn
- **Backend API Framework:** FastAPI, Uvicorn, Pydantic, Joblib
- **Dashboard Framework:** Streamlit
- **Generative AI & RAG:** Google Gemini API (`gemini-3.5-flash`), Tavily Search
- **Frontend Stack:** HTML5, Modern CSS (Glassmorphism, CSS Variables), Vanilla JavaScript (ES6+), Canvas API

---

## ⚡ Quickstart & Installation Guide

### 1. Prerequisites & Virtual Environment Setup
```bash
# Clone or navigate to project workspace
cd "c:\Users\kanch\OneDrive\Documents\Mtech Project"

# Create a virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
pip install fastapi uvicorn streamlit google-generativeai pydantic
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 4. Execute Machine Learning Pipeline
Train all 8 models, evaluate metrics, generate SHAP plots, and export serialized model files:
```bash
python water_quality_prediction.py
```

### 5. Launch FastAPI Backend Server
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```
- API Swagger Documentation: `http://localhost:8000/docs`
- Redoc API Documentation: `http://localhost:8000/redoc`

### 6. Launch Streamlit Analytics Dashboard
```bash
streamlit run app.py
```
- Local URL: `http://localhost:8501`

### 7. Run Web Frontend
Open `frontend/index.html` directly in any web browser, or serve via any static HTTP server.

---

## 🔌 API Endpoints Reference

### `POST /predict`
Analyzes input water sample metrics and returns potability prediction, confidence score, Water Quality Index (WQI), threshold violations, and remediation recommendations.

**Request Body:**
```json
{
  "ph": 6.1,
  "Hardness": 320.0,
  "Solids": 650.0,
  "Chloramines": 4.5,
  "Sulfate": 280.0,
  "Conductivity": 850.0,
  "Organic_carbon": 18.0,
  "Trihalomethanes": 90.0,
  "Turbidity": 1.5
}
```

**Response Output:**
```json
{
  "potability_class": 0,
  "potable": false,
  "confidence_score": 0.8425,
  "wqi": 52.3,
  "violations": [
    {"param": "pH", "val": 6.1, "issue": "Acidic Water", "limit": "6.5 - 8.5"},
    {"param": "Hardness", "val": 320.0, "issue": "High Hardness", "limit": "< 300 mg/L"},
    {"param": "Solids (TDS)", "val": 650.0, "issue": "High TDS", "limit": "< 500 ppm"}
  ],
  "remediation_tips": [
    "💧 **Acidic Water Fix (pH < 6.5):** Install a Calcite neutralizer filter or Soda Ash injection system.",
    "🧪 **Hardness Fix (>300 mg/L):** Install an Ion-Exchange Water Softener.",
    "🏭 **High TDS Fix (>500 ppm):** Install a Reverse Osmosis (RO) Membrane System."
  ],
  "status": "Success"
}
```

### `POST /chat`
MizuAgent 2.0 AI Assistant endpoint powered by Gemini RAG.

---

## 📜 Project Documentation

For full academic and technical details, refer to [PROJECT_DOCUMENTATION.md](file:///c:/Users/kanch/OneDrive/Documents/Mtech%20Project/PROJECT_DOCUMENTATION.md).

---

## 📄 License
This project is released under the **MIT License**.
