import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from PIL import Image

try:
    from tavily import TavilyClient
    import google.generativeai as genai
    
    tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-3.5-flash')
    rag_enabled = True
except Exception as e:
    st.error(f"RAG initialization failed: {e}")
    rag_enabled = False

# ==========================================================
# Page Configuration
# ==========================================================
st.set_page_config(
    page_title="AI Water Quality Predictor",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# Custom CSS for Premium Look
# ==========================================================
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-title {
        font-size: 1.5rem;
        color: #3B82F6;
        text-align: center;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# Caching Model Loading
# ==========================================================
@st.cache_resource
def load_models():
    try:
        model = joblib.load("models/best_model.pkl")
        scaler = joblib.load("models/scaler.pkl")
        return model, scaler
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None

best_model, scaler = load_models()

# ==========================================================
# Title Section
# ==========================================================
st.markdown("<div class='main-title'>💧 AI-Based Water Quality Prediction System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Predicting Water Potability using Machine Learning</div>", unsafe_allow_html=True)

# ==========================================================
# Layout Tabs
# ==========================================================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Project Overview & Data", "📈 Model Performance & AI Explainability", "🤖 Interactive AI Predictor", "💬 AI Chatbot Assistant"])

# ==========================================================
# TAB 1: Project Overview & Data
# ==========================================================
with tab1:
    st.header("Project Objective")
    st.write("""
    > **To develop an intelligent system that predicts whether a water sample is safe (potable) or unsafe (non-potable) based on its physicochemical properties, enabling faster and more reliable water quality assessment.**
    
    Instead of manually testing water in a laboratory every time, this AI model can predict potability instantly using measured parameters.
    """)
    
    st.markdown("---")
    st.header("Data Exploratory Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Class Distribution")
        if os.path.exists("outputs/class_distribution.png"):
            st.image(Image.open("outputs/class_distribution.png"), use_container_width=True)
        else:
            st.warning("Image not found.")
            
        st.subheader("Missing Values Heatmap")
        if os.path.exists("outputs/missing_values.png"):
            st.image(Image.open("outputs/missing_values.png"), use_container_width=True)
    
    with col2:
        st.subheader("Correlation Heatmap")
        if os.path.exists("outputs/correlation_heatmap.png"):
            st.image(Image.open("outputs/correlation_heatmap.png"), use_container_width=True)
            
    st.subheader("Feature Boxplots (Outlier Detection)")
    if os.path.exists("outputs/boxplots.png"):
        st.image(Image.open("outputs/boxplots.png"), use_container_width=True)

# ==========================================================
# TAB 2: Model Performance & Explainability
# ==========================================================
with tab2:
    st.header("Base Model Comparison")
    if os.path.exists("outputs/model_comparison.csv"):
        df_comp = pd.read_csv("outputs/model_comparison.csv")
        st.dataframe(df_comp.style.highlight_max(axis=0, subset=['Accuracy', 'Precision', 'Recall', 'F1 Score', 'ROC AUC'], color='lightgreen'))
    
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists("outputs/model_comparison.png"):
            st.image(Image.open("outputs/model_comparison.png"), use_container_width=True, caption="Model Accuracy Comparison")
    with col2:
        if os.path.exists("outputs/roc_curve.png"): # ROC of best model
            st.image(Image.open("outputs/roc_curve.png"), use_container_width=True, caption="Best Model ROC Curve")
            
    st.markdown("---")
    st.header("Explainable AI (XAI)")
    st.write("These plots show exactly how the Artificial Intelligence is making its decisions, making the 'black box' model completely transparent.")
    
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Feature Importance")
        if os.path.exists("outputs/feature_importance.png"):
            st.image(Image.open("outputs/feature_importance.png"), use_container_width=True)
        
        st.subheader("Learning Curve")
        if os.path.exists("outputs/learning_curve.png"):
            st.image(Image.open("outputs/learning_curve.png"), use_container_width=True)
            
    with col4:
        st.subheader("SHAP Summary Plot")
        if os.path.exists("outputs/shap_summary.png"):
            st.image(Image.open("outputs/shap_summary.png"), use_container_width=True)
            
        st.subheader("Validation Curve")
        if os.path.exists("outputs/validation_curve.png"):
            st.image(Image.open("outputs/validation_curve.png"), use_container_width=True)


# ==========================================================
# TAB 3: Interactive AI Predictor
# ==========================================================
with tab3:
    st.header("🤖 Test a Custom Water Sample")
    st.write("Adjust the physicochemical parameters below to get an instant AI prediction.")
    
    if best_model is None or scaler is None:
        st.error("Models failed to load. Please ensure the machine learning script has been executed successfully.")
    else:
        # Form for input
        with st.form("prediction_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                ph = st.slider("pH Level", min_value=0.0, max_value=14.0, value=7.0, step=0.1)
                hardness = st.slider("Hardness (mg/L)", min_value=0.0, max_value=350.0, value=196.0, step=1.0)
                solids = st.slider("Solids (TDS) (ppm)", min_value=0.0, max_value=65000.0, value=21000.0, step=100.0)
            
            with col2:
                chloramines = st.slider("Chloramines (ppm)", min_value=0.0, max_value=15.0, value=7.1, step=0.1)
                sulfate = st.slider("Sulfate (mg/L)", min_value=0.0, max_value=500.0, value=333.0, step=1.0)
                conductivity = st.slider("Conductivity (μS/cm)", min_value=0.0, max_value=800.0, value=426.0, step=1.0)
                
            with col3:
                organic_carbon = st.slider("Organic Carbon (ppm)", min_value=0.0, max_value=30.0, value=14.2, step=0.1)
                trihalomethanes = st.slider("Trihalomethanes (μg/L)", min_value=0.0, max_value=130.0, value=66.0, step=1.0)
                turbidity = st.slider("Turbidity (NTU)", min_value=0.0, max_value=8.0, value=3.96, step=0.01)
                
            submit_button = st.form_submit_button(label="🔮 Predict Potability")
            
        if submit_button:
            # Prepare data
            input_data = pd.DataFrame({
                "ph": [ph],
                "Hardness": [hardness],
                "Solids": [solids],
                "Chloramines": [chloramines],
                "Sulfate": [sulfate],
                "Conductivity": [conductivity],
                "Organic_carbon": [organic_carbon],
                "Trihalomethanes": [trihalomethanes],
                "Turbidity": [turbidity]
            })
            
            # Scale
            input_scaled = scaler.transform(input_data)
            
            # Predict
            pred = best_model.predict(input_scaled)[0]
            prob = best_model.predict_proba(input_scaled)[0]
            
            st.markdown("---")
            st.header("Prediction Results")
            
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                if pred == 1:
                    st.success("## 🚰 Water is POTABLE (Safe)")
                    st.write("The AI model has determined this water sample meets safety standards.")
                else:
                    st.error("## ☠️ Water is NOT POTABLE (Unsafe)")
                    st.write("The AI model has determined this water sample is unsafe for consumption.")
                    
            with res_col2:
                st.info(f"### Confidence Score: {np.max(prob)*100:.2f}%")
                
                # Dynamic recommendations
                st.write("### AI Recommendation:")
                if pred == 1:
                    st.write("✓ Suitable for drinking after routine filtration.")
                else:
                    recs = []
                    if sulfate > 250: recs.append("- High Sulfate detected. Consider Reverse Osmosis.")
                    if solids > 1000: recs.append("- High TDS detected. Needs intense filtration.")
                    if chloramines > 4: recs.append("- High Chloramines. Use Activated Carbon Filter.")
                    if not recs: recs.append("- General contamination detected. Advanced purification required.")
                    
                    for r in recs:
                        st.write(r)
                        
            st.balloons() if pred == 1 else None
            
            # Save context for RAG Chatbot
            st.session_state.current_sample = input_data.to_dict(orient="records")[0]
            st.session_state.current_prediction = "Potable" if pred == 1 else "Not Potable"

# ==========================================================
# TAB 4: AI Chatbot Assistant (RAG Enabled)
# ==========================================================
def ai_search_answer(user_question):
    if not rag_enabled:
        return "RAG features are currently disabled due to missing API keys or libraries."
        
    try:
        # 1. Search the web
        search_results = tavily.search(query=user_question, max_results=5)
        context = "\n".join([r["content"] for r in search_results.get("results", [])])
    except Exception as e:
        context = f"Web search failed: {e}"

    # 2. Add local context
    local_context = "No water sample currently being tested."
    if "current_sample" in st.session_state:
        sample_str = ", ".join([f"{k}: {v}" for k,v in st.session_state.current_sample.items()])
        local_context = f"The user is currently testing a water sample with these parameters: {sample_str}. The ML model predicted it as: {st.session_state.current_prediction}."

    # 3. Ask the LLM to answer using that context
    prompt = f"""You are an elite water quality expert assistant.
Use the following live search results to answer the user's question accurately.
If the results are irrelevant, use your own knowledge instead.

Live Search Results:
{context}

Current User Context:
{local_context}

User question: {user_question}

Give a clear, practical answer with treatment recommendations if relevant. Acknowledge the user's specific water parameters if they are relevant to the question."""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"LLM Generation failed: {e}"

with tab4:
    st.header("💬 AI Water Quality Assistant (RAG)")
    st.write("Ask me questions! I am powered by live web search and state-of-the-art LLMs, and I am aware of the water sample you are testing in Tab 3.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your RAG-powered AI Water Quality Assistant. How can I help you today?"}
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if user_input := st.chat_input("E.g. What is the best way to lower high TDS levels?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(user_input)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Searching the web and analyzing..."):
                answer = ai_search_answer(user_input)
            st.markdown(answer)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer})
