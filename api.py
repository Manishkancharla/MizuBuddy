from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import json
import urllib.request
import joblib
import numpy as np
import pandas as pd

app = FastAPI(
    title="Water Quality AI API",
    description="REST API for predicting water potability using a trained ML model.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try loading the model globally
try:
    best_model = joblib.load("models/best_model.pkl")
    scaler = joblib.load("models/scaler.pkl")
except Exception as e:
    best_model, scaler = None, None
    print(f"Warning: Could not load models. Ensure they exist in the models/ directory. {e}")

class WaterSample(BaseModel):
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float

@app.get("/")
def home():
    return {"message": "Welcome to the Water Quality Prediction API. Use the /predict endpoint."}

@app.post("/predict")
def predict_potability(sample: WaterSample):
    if best_model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Machine Learning model is not loaded.")
        
    try:
        # Convert input to DataFrame for the scaler
        input_data = pd.DataFrame([{
            "ph": sample.ph,
            "Hardness": sample.Hardness,
            "Solids": sample.Solids,
            "Chloramines": sample.Chloramines,
            "Sulfate": sample.Sulfate,
            "Conductivity": sample.Conductivity,
            "Organic_carbon": sample.Organic_carbon,
            "Trihalomethanes": sample.Trihalomethanes,
            "Turbidity": sample.Turbidity
        }])
        
        # Scale
        input_scaled = scaler.transform(input_data)
        
        # Predict
        prediction = int(best_model.predict(input_scaled)[0])
        probability = float(np.max(best_model.predict_proba(input_scaled)[0]))
        
        # Parameter safety threshold checks and remediation tips generator
        violations = []
        remediation_tips = []
        
        if sample.ph < 6.5:
            violations.append({"param": "pH", "val": sample.ph, "issue": "Acidic Water", "limit": "6.5 - 8.5"})
            remediation_tips.append("💧 **Acidic Water Fix (pH < 6.5):** Install a Calcite neutralizer filter or Soda Ash injection system to elevate pH and prevent pipe corrosion.")
        elif sample.ph > 8.5:
            violations.append({"param": "pH", "val": sample.ph, "issue": "Alkaline Water", "limit": "6.5 - 8.5"})
            remediation_tips.append("💧 **Alkaline Water Fix (pH > 8.5):** Install a Reverse Osmosis (RO) system or acid-injection unit to reduce alkaline mineral scaling.")
            
        if sample.Hardness > 300:
            violations.append({"param": "Hardness", "val": sample.Hardness, "issue": "High Hardness", "limit": "< 300 mg/L"})
            remediation_tips.append("🧪 **Hardness Fix (>300 mg/L):** Install an Ion-Exchange Water Softener to remove excess Calcium and Magnesium.")
            
        if sample.Solids > 500:
            violations.append({"param": "Solids (TDS)", "val": sample.Solids, "issue": "High TDS", "limit": "< 500 ppm"})
            remediation_tips.append("🏭 **High TDS Fix (>500 ppm):** Install a Reverse Osmosis (RO) Membrane System or Deionization unit.")
            
        if sample.Chloramines > 4.0:
            violations.append({"param": "Chloramines", "val": sample.Chloramines, "issue": "High Disinfectant Residual", "limit": "< 4.0 ppm"})
            remediation_tips.append("🔬 **Chloramines Fix (>4.0 ppm):** Use a Catalytic Carbon Filter to neutralize excess chlorine-ammonia residuals.")
            
        if sample.Sulfate > 250:
            violations.append({"param": "Sulfate", "val": sample.Sulfate, "issue": "High Sulfate", "limit": "< 250 mg/L"})
            remediation_tips.append("🚰 **Sulfate Fix (>250 mg/L):** Install a Reverse Osmosis system or Anion Exchange Resin to reduce laxative mineral content.")
            
        if sample.Conductivity > 800:
            violations.append({"param": "Conductivity", "val": sample.Conductivity, "issue": "High Electrical Conductivity", "limit": "< 800 μS/cm"})
            remediation_tips.append("⚡ **High Conductivity Fix (>800 μS/cm):** RO filtration effectively strips dissolved conductive ionic salts.")
            
        if sample.Organic_carbon > 15:
            violations.append({"param": "Organic Carbon", "val": sample.Organic_carbon, "issue": "High Organic Load", "limit": "< 15 ppm"})
            remediation_tips.append("🌿 **Organic Carbon Fix (>15 ppm):** Install Granular Activated Carbon (GAC) + UV Disinfection.")
            
        if sample.Trihalomethanes > 80:
            violations.append({"param": "Trihalomethanes", "val": sample.Trihalomethanes, "issue": "High Disinfection Byproducts", "limit": "< 80 μg/L"})
            remediation_tips.append("⚠️ **THMs Fix (>80 μg/L):** Use Granular Activated Carbon (GAC) filtration to adsorb toxic chlorination byproducts.")
            
        if sample.Turbidity > 1.0:
            violations.append({"param": "Turbidity", "val": sample.Turbidity, "issue": "High Turbidity / Cloudiness", "limit": "< 1.0 NTU"})
            remediation_tips.append("🌧️ **Turbidity Fix (>1.0 NTU):** Install a 5-Micron Sediment Depth Filter followed by Ultrafiltration (UF).")
            
        # Calculate Water Quality Index (WQI: 0 - 100)
        scores = [
            max(0, 100 - abs(sample.ph - 7.2) * 20),
            100 if sample.Hardness <= 200 else max(0, 100 - (sample.Hardness - 200) * 0.25),
            100 if sample.Solids <= 500 else max(0, 100 - (sample.Solids - 500) * 0.003),
            100 if sample.Chloramines <= 4.0 else max(0, 100 - (sample.Chloramines - 4.0) * 15),
            100 if sample.Sulfate <= 250 else max(0, 100 - (sample.Sulfate - 250) * 0.3),
            100 if sample.Conductivity <= 400 else max(0, 100 - (sample.Conductivity - 400) * 0.1),
            100 if sample.Organic_carbon <= 10 else max(0, 100 - (sample.Organic_carbon - 10) * 5),
            100 if sample.Trihalomethanes <= 60 else max(0, 100 - (sample.Trihalomethanes - 60) * 1.5),
            100 if sample.Turbidity <= 1.0 else max(0, 100 - (sample.Turbidity - 1.0) * 18)
        ]
        wqi = round(float(np.mean(scores)), 1)

        optimal_params = {
            "ph": 7.20,
            "Hardness": 180.00,
            "Solids": 450.00,
            "Chloramines": 2.50,
            "Sulfate": 180.00,
            "Conductivity": 400.00,
            "Organic_carbon": 8.00,
            "Trihalomethanes": 45.00,
            "Turbidity": 0.80
        }

        return {
            "potability_class": prediction,
            "potable": bool(prediction == 1),
            "confidence_score": round(probability, 4),
            "wqi": wqi,
            "violations": violations,
            "remediation_tips": remediation_tips,
            "optimal_params": optimal_params,
            "status": "Success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==========================================
# MIZUAGENT 2.0 AI AGENT ENDPOINT
# ==========================================
class ChatMessage(BaseModel):
    message: str
    sample_data: Optional[dict] = None
    prediction_result: Optional[dict] = None

# Load API Key from environment or .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if not GEMINI_API_KEY and os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                GEMINI_API_KEY = line.split("=", 1)[1].strip()

def call_gemini_api(user_message: str, sample_data: Optional[dict] = None, prediction_result: Optional[dict] = None) -> str:
    if not GEMINI_API_KEY:
        return ""
    
    models_to_try = [
        "gemini-3.5-flash",
        "gemini-flash-latest"
    ]
    
    context_info = ""
    if sample_data:
        context_info += f"\nCurrent Active Water Sample Metrics: {json.dumps(sample_data)}"
    if prediction_result:
        context_info += f"\nCurrent ML Prediction Output: {json.dumps(prediction_result)}"

    system_prompt = (
        "You are MizuAgent 2.0, a Live Autonomous AI Water Quality & Safety Research Agent for MizuBuddy connected directly to this web application.\n"
        "You can read live parameter inputs, analyze prediction outputs, recommend multi-stage filtration strategies, explain ML models & SHAP values, evaluate WHO/EPA standards, AND directly control/update the web page for the user.\n\n"
        "Guidance:\n"
        "- Be authoritative, friendly, highly informative, and structure responses with clear Markdown (bold headers, numbered steps, concise bullet points).\n"
        "- When asked why water is not potable or for filtration solutions, perform a full parameter-by-parameter analysis using the provided metrics, highlight every parameter breaching WHO limits, and provide a clear step-by-step filtration system setup.\n"
        "- If user asks you to change parameters (e.g. 'set pH to 7.2', 'fix pH and predict', 'load contaminated sample'), output the appropriate live control tag:\n"
        "  • [ACTION:FILL_DEMO] (load standard demo sample)\n"
        "  • [ACTION:RUN_PREDICTOR] (execute water potability prediction)\n"
        "  • [ACTION:SET_PARAM:ph=7.2,Hardness=180.5] (update specific form inputs)\n"
        "  • [ACTION:SET_AND_PREDICT:ph=7.4] (update input parameters and run prediction)\n"
        "  • [ACTION:SCROLL:predictor] (scroll browser to predictor section)\n"
        "  • [ACTION:SCROLL:performance] (scroll browser to model performance & SHAP section)\n"
        "  • [ACTION:SCROLL:overview] (scroll browser to project overview section)\n"
        "  • [ACTION:SCROLL:awareness] (scroll browser to safe water awareness section)\n"
        "  • [ACTION:CLEAR_FORM] (clear all inputs)\n"
        f"{context_info}\n\n"
        f"User Query: {user_message}"
    )

    payload = {
        "contents": [{"parts": [{"text": system_prompt}]}]
    }

    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            res = urllib.request.urlopen(req, timeout=5)
            res_data = json.loads(res.read().decode("utf-8"))
            candidates = res_data.get("candidates", [])
            if candidates and "content" in candidates[0]:
                parts = candidates[0]["content"].get("parts", [])
                if parts and parts[0].get("text"):
                    return parts[0].get("text", "")
        except Exception as e:
            print(f"Gemini API Model {model_name} Error: {e}")

    return ""

def get_agent_fallback_reply(message: str, sample_data: Optional[dict] = None, prediction_result: Optional[dict] = None) -> str:
    q = message.lower().strip()

    # Dynamic action triggers
    if "fix ph" in q or "set ph" in q or "change ph" in q:
        return "⚡ **Live Site Action:** Updating pH to safe WHO neutral standard (7.20) and executing real-time ML potability re-evaluation on screen...\n\n[ACTION:SET_AND_PREDICT:ph=7.20]"
    
    if "clear" in q or "reset" in q:
        return "🧹 **Live Site Action:** Clearing all input fields on the predictor form.\n\n[ACTION:CLEAR_FORM]"

    if "scroll to chart" in q or "show performance" in q or "show shap" in q or "show model" in q or "metrics" in q:
        return "📊 **Live Site Action:** Scrolling to model evaluation, accuracy metrics, and SHAP XAI visual charts section...\n\n[ACTION:SCROLL:performance]"

    if "scroll to predictor" in q or "show predictor" in q or "predict section" in q:
        return "🎯 **Live Site Action:** Scrolling to interactive AI predictor form...\n\n[ACTION:SCROLL:predictor]"

    if "scroll to overview" in q or "project info" in q:
        return "📑 **Live Site Action:** Scrolling to Project Overview section...\n\n[ACTION:SCROLL:overview]"

    if "scroll to awareness" in q or "every drop" in q or "safe water" in q:
        return "💙 **Live Site Action:** Scrolling to safe water awareness section...\n\n[ACTION:SCROLL:awareness]"

    if "predict" in q or "evaluate" in q or "test sample" in q or "analyze sample" in q:
        return "⚡ **Live Site Action:** Executing machine learning classification model on active screen inputs...\n\n[ACTION:RUN_PREDICTOR]"

    if "demo" in q or "sample data" in q or "load sample" in q:
        return "🤖 **Live Site Action:** Loading sample physicochemical water metrics directly into form fields...\n\n[ACTION:FILL_DEMO]"
    
    # Check for filtration / non-potable diagnostic request
    if any(w in q for w in ["not potable", "unpotable", "unsafe", "why", "filter", "filtration", "solution", "fix", "remediat", "treat"]):
        breaches = []
        if sample_data:
            ph = sample_data.get("ph")
            if ph is not None and (ph < 6.5 or ph > 8.5):
                breaches.append(f"• **pH ({ph:.2f}):** Outside safe range (6.5 – 8.5). Acidic or overly alkaline water.")
            hardness = sample_data.get("Hardness")
            if hardness is not None and hardness > 300:
                breaches.append(f"• **Hardness ({hardness:.2f} mg/L):** Excessive mineral hardness (limit: <300 mg/L).")
            solids = sample_data.get("Solids")
            if solids is not None and solids > 1000:
                breaches.append(f"• **Solids / TDS ({solids:.2f} ppm):** High total dissolved solids (limit: <500 - 1000 ppm).")
            chloramines = sample_data.get("Chloramines")
            if chloramines is not None and chloramines > 4.0:
                breaches.append(f"• **Chloramines ({chloramines:.2f} ppm):** Exceeds disinfectant safety threshold (<4.0 ppm).")
            sulfate = sample_data.get("Sulfate")
            if sulfate is not None and sulfate > 250:
                breaches.append(f"• **Sulfate ({sulfate:.2f} mg/L):** Exceeds WHO guideline threshold (<250 mg/L).")
            conductivity = sample_data.get("Conductivity")
            if conductivity is not None and conductivity > 800:
                breaches.append(f"• **Conductivity ({conductivity:.2f} μS/cm):** Indicates elevated ionic contaminant concentration.")
            toc = sample_data.get("Organic_carbon")
            if toc is not None and toc > 10.0:
                breaches.append(f"• **Organic Carbon ({toc:.2f} ppm):** Elevated organic matter (<10.0 ppm recommended).")
            thms = sample_data.get("Trihalomethanes")
            if thms is not None and thms > 80.0:
                breaches.append(f"• **Trihalomethanes ({thms:.2f} μg/L):** Exceeds maximum disinfectant by-product limit (<80 μg/L).")
            turbidity = sample_data.get("Turbidity")
            if turbidity is not None and turbidity > 5.0:
                breaches.append(f"• **Turbidity ({turbidity:.2f} NTU):** Excess cloudiness shielding microbial pathogens (<1-5 NTU).")

        breach_summary = "\n".join(breaches) if breaches else "• **Multiple Parameter Violations:** Water sample exceeds safe WHO chemical thresholds."

        return (
            "🚨 **Water Safety Diagnostic & Step-by-Step Treatment Plan**\n\n"
            "### 1. Key Contaminants & Threshold Violations:\n"
            f"{breach_summary}\n\n"
            "### 2. Recommended Step-by-Step Multi-Stage Filtration System:\n\n"
            "1. **Stage 1 — Sediment Pre-Filter (5 Micron):**\n"
            "   • Traps silt, rust, and particulate matter to reduce turbidity and protect downstream membranes.\n\n"
            "2. **Stage 2 — Catalytic Granular Activated Carbon (GAC):**\n"
            "   • Removes chloramines, trihalomethanes (THMs), and dissolved organic carbon compounds.\n\n"
            "3. **Stage 3 — Reverse Osmosis (RO) Membrane (0.0001 Micron):**\n"
            "   • Rejects up to 99% of dissolved solids (TDS), excess sulfates, heavy metals, and ionic salts.\n\n"
            "4. **Stage 4 — Water Softener / Calcite Neutralizer:**\n"
            "   • Neutralizes pH levels to 7.0–7.5 and softens high mineral hardness to prevent scale build-up.\n\n"
            "5. **Stage 5 — UV Disinfection & Post-RO Remineralization:**\n"
            "   • Eradicates 99.99% of biological pathogens and adds balanced Calcium/Magnesium for healthy drinking water."
        )

    if any(w in q for w in ["mineral", "low tds", "less mineral", "soft water", "demineral"]):
        return (
            "💡 **Low Mineral Water (De-mineralization / Soft Water) Remediation:**\n\n"
            "When water contains very low mineral levels (TDS < 100 mg/L or Hardness < 60 mg/L):\n\n"
            "1. **Re-Mineralization Cartridges:** Install a post-RO mineral filter containing natural **Calcium** and **Magnesium** stones to restore essential electrolytes.\n"
            "2. **Calcite Media Filter:** Pass water through a calcite neutralizer bed to elevate pH and balance dissolved minerals.\n"
            "3. **Mineral Drops:** Add food-grade mineral drops (electrolytes) directly to drinking water.\n\n"
            "⚠️ *Note:* De-mineralized water can taste flat and acidic, and may leach metals from metal containers over time."
        )
    if "test" in q or "run" in q or "diagnostic" in q or "demo" in q:
        return "🤖 **MizuAgent 2.0 Action:** Initiating diagnostic workflow. Loading sample water quality values and running potability evaluation...\n\n[ACTION:FILL_DEMO]"
    if "ph" in q:
        return "🔬 **MizuAgent Diagnostic — pH Analysis:**\n\n• **Safe Range:** 6.5 – 8.5 (WHO / EPA Standard)\n• **Low pH (<6.5):** Acidic; corrodes metal pipes and leaches copper/lead.\n• **High pH (>8.5):** Alkaline; causes mineral scaling and reduces chlorination efficiency."
    if "turbid" in q or "cloud" in q:
        return "🌧️ **Turbidity Analysis:**\n\n• **WHO Limit:** <1.0 NTU\n• **Risk:** High turbidity indicates suspended silt or pathogens that shield bacteria from UV/chlorine disinfection.\n• **Fix:** Sediment depth filtration (5 micron) + Ultrafiltration."
    if "who" in q or "standard" in q or "limit" in q:
        return "🏥 **MizuAgent Standards Check — WHO & EPA Guidelines:**\n\n• **pH:** 6.5 – 8.5\n• **TDS (Solids):** <500 ppm\n• **Chloramines:** <4.0 mg/L\n• **Turbidity:** <1.0 NTU\n• **THMs:** <80 μg/L\n• **Sulfate:** <250 mg/L"
    if "shap" in q or "xai" in q or "feature importance" in q:
        return "🔬 **Explainable AI (SHAP) Insights:**\n\nOur pipeline evaluates 7+ ML algorithms (Random Forest, XGBoost, LightGBM, SVM, KNN). SHAP values quantify how much each parameter (e.g. pH or Turbidity) pushes the prediction toward 'Potable' vs. 'Not Potable'."
    
    return "🤖 **MizuAgent 2.0 Active:** I am your MizuBuddy autonomous AI water research agent. Ask me about mineral levels, pH, WHO standards, SHAP explainability, or run a water quality diagnostic!"

@app.post("/chat")
def chat(msg: ChatMessage):
    if not msg.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    
    # Try Live Gemini Multi-Model API
    reply = call_gemini_api(msg.message, msg.sample_data, msg.prediction_result)
    
    # Fallback to intelligent agent knowledge engine
    if not reply:
        reply = get_agent_fallback_reply(msg.message, msg.sample_data, msg.prediction_result)
        
    return {"reply": reply}



