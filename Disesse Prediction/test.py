import streamlit as st
import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import base64
import os  # Import os to check file existence

# 🎨 Function to set background image
def set_bg_image(image_file):
    if not os.path.exists(image_file):
        st.error(f"🚨 Background image not found: {image_file}")
        return
    
    with open(image_file, "rb") as file:
        img_data = base64.b64encode(file.read()).decode()
    
    bg_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{img_data}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

def main():
    # ✅ Define absolute paths for files
    BASE_DIR = r"C:\\Users\\Maitri Chitania\\OneDrive\\Desktop\\CODE UNNATI\\Disesse Prediction"
    BACKGROUND_IMAGE_PATH = os.path.join(BASE_DIR, "background.jpeg")
    MODEL_PATH = os.path.join(BASE_DIR, "plant-disease-model.pth")

    # ✅ Set background image
    set_bg_image(BACKGROUND_IMAGE_PATH)

    # ✅ Define class labels for diseases
    CLASS_LABELS = [
        "Healthy", "Powdery Mildew", "Leaf Spot", "Rust", "Blight",
        "Bacterial Wilt", "Yellow Leaf Curl", "Downy Mildew", "Anthracnose", "Mosaic Virus"
    ]

    # ✅ Load trained model
    @st.cache_resource
    def load_model():
        if not os.path.exists(MODEL_PATH):
            st.error(f"🚨 Model file not found: {MODEL_PATH}")
            return None  # Return None if model file doesn't exist
        
        NUM_CLASSES = len(CLASS_LABELS)
        model = models.vgg16(pretrained=False)  # Adjust based on your trained model
        model.classifier[6] = nn.Linear(model.classifier[6].in_features, NUM_CLASSES)  # Adjust classifier
        
        model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')), strict=False)
        model.eval()
        return model

    model = load_model()
    if model is None:
        return  # Stop execution if model is not found

    # ✅ Image transformations
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

    # ✅ Streamlit app interface
    st.markdown(
        "<h1 style='text-align: center; color: green;'>🌿Plant Disease Image Recognition🌿</h1>",
        unsafe_allow_html=True
    )

    st.markdown("<h4 style='color: blue;'>📤 Upload an Image of a Plant Leaf</h4>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

    # ✅ Get predictions
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="🖼 Uploaded Image", use_column_width=True)

        if st.button("🔍 Predict Disease"):
            try:
                # Preprocess the image
                image_tensor = transform(image).unsqueeze(0)

                # Get prediction
                with torch.no_grad():
                    outputs = model(image_tensor)
                    _, predicted = torch.max(outputs, 1)
                    disease_name = CLASS_LABELS[predicted.item()]

                # 🎯 Display result
                st.success(f"🌱 **Predicted Disease:** {disease_name} ✅")
            except Exception as e:
                st.error(f"🚨 Prediction failed: {e}")

if __name__ == '__main__':
    main()







