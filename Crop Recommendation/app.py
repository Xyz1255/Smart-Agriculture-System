import streamlit as st
import pickle
import xgboost
import numpy as np
import os

# ✅ Define the dictionary mapping numeric values to crop names
crop_dict = {
    0: "Rice", 1: "Maize", 2: "Jute", 3: "Cotton", 4: "Coconut",
    5: "Papaya", 6: "Orange", 7: "Apple", 8: "Muskmelon", 9: "Watermelon",
    10: "Grapes", 11: "Mango", 12: "Banana", 13: "Pomegranate", 14: "Lentil",
    15: "Blackgram", 16: "Mungbean", 17: "Mothbeans", 18: "Pigeonpeas",
    19: "Kidneybeans", 20: "Chickpea", 21: "Coffee"
}

# ✅ Define model file paths at the top (Avoid redefining inside `main()`)
model_files = {
    "Decision Tree": "C:\\Users\\Maitri Chitania\\OneDrive\\Desktop\\CODE UNNATI\\Models\\DecisionTree.pkl",
    "Naive Bayes": "C:\\Users\\Maitri Chitania\\OneDrive\\Desktop\\CODE UNNATI\\Models\\NBClassifier.pkl",
    "Random Forest": "C:\\Users\\Maitri Chitania\\OneDrive\\Desktop\\CODE UNNATI\\Models\\RandomForest.pkl",
    "XGBoost": "C:\\Users\\Maitri Chitania\\OneDrive\\Desktop\\CODE UNNATI\\Models\\XGBoost.pkl"
}

models = {}  # ✅ Dictionary to store loaded models

# ✅ Load models at the start
st.write("🔍 Checking model files...")  
for name, file in model_files.items():
    if os.path.exists(file):
        st.write(f"✅ Found: {file}")  
        with open(file, "rb") as f:
            models[name] = pickle.load(f)
    else:
        st.warning(f"⚠️ Model file not found: {file}")  

if not models:
    st.error("❌ No models loaded! Please check the file paths.")
    
def main():
    # ✅ Page config and background styling
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] { background-size: cover; background-position: center; }
        [data-testid="stHeader"], [data-testid="stSidebar"] { background: rgba(0,0,0,0); }
        .stTextInput, .stNumberInput { background-color: white; border-radius: 5px; color: black; }
        .stButton > button { background-color: #228B22; color: white; font-size: 16px; font-weight: bold; padding: 10px; border-radius: 5px; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ✅ App title
    st.markdown("<h2 style='text-align: center; color: gold;'>Crop Recommendation System</h2>", unsafe_allow_html=True)

    # ✅ Ensure models are available before selection
    if models:
        selected_model = st.selectbox("Choose Model", list(models.keys()), key="model_selection")
    else:
        st.error("🚨 No models available for selection.")
        return  # Stop execution if no models are loaded

    # ✅ Form for user inputs
    with st.form("prediction_form"):
        nitrogen = st.number_input("Nitrogen", min_value=0.0, step=1.0)
        phosphorus = st.number_input("Phosphorus", min_value=0.0, step=1.0)
        potassium = st.number_input("Potassium", min_value=0.0, step=1.0)
        temperature = st.number_input("Temperature", min_value=-10.0, step=0.1)
        humidity = st.number_input("Humidity", min_value=0.0, step=0.1)
        ph = st.number_input("pH", min_value=0.0, step=0.1)
        rainfall = st.number_input("Rainfall", min_value=0.0, step=0.1)

        # ✅ Submit button inside the form
        submit = st.form_submit_button("Predict")

    # ✅ Handle prediction logic
    if submit:
        try:
            input_features = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
            model = models[selected_model]  # Fetch selected model
            prediction_numeric = model.predict(input_features)[0]  # Get numeric prediction
            predicted_crop = crop_dict.get(prediction_numeric, "Unknown Crop")  # Convert to crop name
            
            st.success(f"🌱 Recommended Crop: **{predicted_crop}**")
            st.info(f"🔍 Prediction made using the **{selected_model}** model.")
        except Exception as e:
            st.error(f"Error during prediction: {e}")

if __name__ == '__main__':
    main()  # ✅ Ensure `main()` runs when script is executed
