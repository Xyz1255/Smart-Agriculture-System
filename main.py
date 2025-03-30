import streamlit as st
import importlib.util
import os
import base64

# ---------------------------------------------------
# 1. PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Agriculture Prediction Dashboard",
    page_icon=":seedling:",
    layout="wide"
)

# ---------------------------------------------------
# 2. IMAGE PATHS & UTILITY FUNCTION
# ---------------------------------------------------
DASHBOARD_BG = r"C:\Users\Maitri Chitania\OneDrive\Desktop\CODE UNNATI\Images\Dashboard_bg.jpg"
CARD1_BG = r"C:\Users\Maitri Chitania\OneDrive\Desktop\CODE UNNATI\Images\Crop Recommedation.jpg"
CARD2_BG = r"C:\Users\Maitri Chitania\OneDrive\Desktop\CODE UNNATI\Images\Crop Feritilizer.jpg"
CARD3_BG = r"C:\Users\Maitri Chitania\OneDrive\Desktop\CODE UNNATI\Images\Disease Prediction.png"

def image_to_base64(path):
    if not os.path.exists(path):
        st.write("File does NOT exist:", path)
        return ""
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Convert images to base64 strings
bg_dashboard = image_to_base64(DASHBOARD_BG)
bg_card1 = image_to_base64(CARD1_BG)
bg_card2 = image_to_base64(CARD2_BG)
bg_card3 = image_to_base64(CARD3_BG)

# ---------------------------------------------------
# 3. CONDITIONAL GLOBAL CSS INJECTION
# ---------------------------------------------------
def set_dashboard_background(bg_b64):
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/png;base64,{bg_b64}") no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """, unsafe_allow_html=True)

def remove_dashboard_background():
    # Inject CSS that resets the background so sub-app backgrounds are not overridden
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# 4. CUSTOM CSS FOR CARDS & HEADINGS
# ---------------------------------------------------
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        color: #2E8B57;
        margin-top: 0.2em;
        margin-bottom: 0.2em;
        font-weight: 700;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #555;
        margin-bottom: 2em;
    }
    .card {
        position: relative;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        padding: 1.5em;
        margin: 1em;
        text-align: center;
        color: #fff;
        min-height: 300px;
        background-size: cover;
        background-position: center;
    }
    .card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.4);
        border-radius: 10px;
    }
    .card > * {
        position: relative;
        z-index: 2;
    }
    .card-title {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.5em;
    }
    .card-text {
        font-size: 1rem;
        margin-bottom: 1.5em;
        min-height: 3em;
    }
    .card-button {
        background-color: #2E8B57;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.6em 1.2em;
        cursor: pointer;
        font-weight: 600;
        font-size: 1rem;
    }
    .card-button:hover {
        background-color: #3CB371;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# 5. HELPER FUNCTIONS TO LOAD OTHER APPS
# ---------------------------------------------------
def load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def load_crop_recommendation():
    crop_app = load_module("crop_recommendation_app", 
                           r"C:\Users\Maitri Chitania\OneDrive\Desktop\CODE UNNATI\Crop Recommendation\app.py")
    if hasattr(crop_app, "main"):
        crop_app.main()
    else:
        st.error("Error: 'main()' function not found in Crop Recommendation app.")

def load_crop_fertilizer():
    fert_app = load_module("crop_fertilizer_app", 
                           r"C:\Users\Maitri Chitania\OneDrive\Desktop\CODE UNNATI\Crop Fertilizer\app17.py")
    if hasattr(fert_app, "main"):
        fert_app.main()
    else:
        st.error("Error: 'main()' function not found in Crop Fertilizer app.")

def load_disease_prediction():
    disease_app = load_module("disease_prediction_app", 
                              r"C:\Users\Maitri Chitania\OneDrive\Desktop\CODE UNNATI\Disesse Prediction\test.py")
    if hasattr(disease_app, "main"):
        disease_app.main()
    else:
        st.error("Error: 'main()' function not found in Disease Prediction app.")

# ---------------------------------------------------
# 6. HOME PAGE LAYOUT
# ---------------------------------------------------
def show_home():
    # Apply the dashboard background only on home page
    set_dashboard_background(bg_dashboard)
    
    st.markdown("<h1 class='main-title'>Agriculture Prediction Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Select one of the following models to get started:</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    # Card 1 - Crop Recommendation
    with col1:
        st.markdown(f"""
        <div class="card" style="background-image: url('data:image/png;base64,{bg_card1}');">
            <div class="card-title">Crop Recommendation</div>
            <div class="card-text">
                Find the best crop to grow based on soil nutrients, weather, and more!
            </div>
            <form action="" method="get">
                <button class="card-button" type="submit">Explore</button>
            </form>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Crop Recommendation", key="crop_reco_btn"):
            st.session_state.page = "crop_recommendation"

    # Card 2 - Crop Fertilizer
    with col2:
        st.markdown(f"""
        <div class="card" style="background-image: url('data:image/png;base64,{bg_card2}');">
            <div class="card-title">Crop Fertilizer</div>
            <div class="card-text">
                Determine the ideal fertilizer to maximize yield and keep your soil healthy.
            </div>
            <form action="" method="get">
                <button class="card-button" type="submit">Explore</button>
            </form>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Crop Fertilizer", key="fert_btn"):
            st.session_state.page = "crop_fertilizer"

    # Card 3 - Disease Prediction
    with col3:
        st.markdown(f"""
        <div class="card" style="background-image: url('data:image/png;base64,{bg_card3}');">
            <div class="card-title">Disease Prediction</div>
            <div class="card-text">
                Upload a plant leaf image and detect possible diseases for better crop health.
            </div>
            <form action="" method="get">
                <button class="card-button" type="submit">Explore</button>
            </form>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Disease Prediction", key="disease_btn"):
            st.session_state.page = "disease_prediction"

# ---------------------------------------------------
# 7. SESSION STATE NAVIGATION & PAGE ROUTING
# ---------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# When not on home page, remove the dashboard background
if st.session_state.page != "home":
    remove_dashboard_background()

# "Back to Home" button for sub-pages
if st.session_state.page != "home":
    if st.button("← Back to Home", key="back_home_btn"):
        st.session_state.page = "home"
        st.rerun()

# Route to the selected page
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "crop_recommendation":
    load_crop_recommendation()
elif st.session_state.page == "crop_fertilizer":
    load_crop_fertilizer()
elif st.session_state.page == "disease_prediction":
    load_disease_prediction()
