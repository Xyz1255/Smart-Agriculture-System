import streamlit as st
import pickle
import pandas as pd

def main():
    # Load the trained model and encoders
    with open(r"C:\\Users\\Maitri Chitania\\OneDrive\\Desktop\\CODE UNNATI\\Crop Fertilizer\\fertilizer_model.pkl", "rb") as f:
        data = pickle.load(f)  # ✅ This should be inside the function properly

    model = data["model"]
    fertilizer_encoder = data["fertilizer_encoder"]
    label_encoders = data["label_encoders"]

    # Streamlit UI
    st.title("🌱 Fertilizer Recommendation System")

    # Set background image
    def set_bg(image_url):
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url("https://static.vecteezy.com/system/resources/thumbnails/006/359/341/small_2x/growth-trees-concept-coffee-bean-seedlings-nature-background-photo.jpg") no-repeat center center fixed;
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    # Call the function with the image URL
    set_bg("https://static.vecteezy.com/system/resources/thumbnails/006/359/341/small_2x/growth-trees-concept-coffee-bean-seedlings-nature-background-photo.jpg")

    st.write("Enter the soil and crop details to get the best fertilizer recommendation.")

    # Input fields
    temperature = st.number_input("🌡 Temperature (°C)", min_value=-10, max_value=50, value=25)
    humidity = st.number_input("💧 Humidity (%)", min_value=0, max_value=100, value=60)
    moisture = st.number_input("🌊 Moisture (%)", min_value=0, max_value=100, value=40)

    soil_type = st.selectbox("🪵 Soil Type", label_encoders["Soil_Type"].classes_)
    crop_type = st.selectbox("🌾 Crop Type", label_encoders["Crop_Type"].classes_)

    nitrogen = st.number_input("🧪 Nitrogen (mg/kg)", min_value=0, max_value=100, value=50)
    potassium = st.number_input("🔬 Potassium (mg/kg)", min_value=0, max_value=100, value=30)
    phosphorous = st.number_input("🧪 Phosphorous (mg/kg)", min_value=0, max_value=100, value=20)

    # Predict button
    if st.button("🔍 Predict Fertilizer"):
        # Convert categorical inputs using LabelEncoders
        soil_encoded = label_encoders["Soil_Type"].transform([soil_type])[0]
        crop_encoded = label_encoders["Crop_Type"].transform([crop_type])[0]

        # Create DataFrame for prediction
        input_data = pd.DataFrame([{
            "Temparature": temperature,
            "Humidity": humidity,
            "Moisture": moisture,
            "Soil_Type": soil_encoded,
            "Crop_Type": crop_encoded,
            "Nitrogen": nitrogen,
            "Potassium": potassium,
            "Phosphorous": phosphorous
        }])

        # Make prediction
        prediction = model.predict(input_data)
        fertilizer_name = fertilizer_encoder.inverse_transform(prediction)[0]

        # Display result
        st.success(f"✅ Recommended Fertilizer: **{fertilizer_name}**")

if __name__ == '__main__':
    main()

