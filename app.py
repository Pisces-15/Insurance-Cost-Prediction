import streamlit as st
import pickle
import numpy as np

# Load model
model = pickle.load(open("Insurance.pkl", "rb"))

# Page config
st.set_page_config(page_title="Insurance Predictor", page_icon="💰", layout="wide")

# ---------------- BACKGROUND ---------------- #
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1588776814546-ec7e7c7c4c6c");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Overlay to make background faint */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background-color: rgba(255,255,255,0.85);
        z-index: -1;
    }

    /* Input labels */
    label {
        color: black !important;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #
st.sidebar.markdown("## 👩‍💻 Personal Details")

st.sidebar.write("**Name:** Sakshi Patil")
st.sidebar.write("**Email:** sakshi@email.com")
st.sidebar.write("**Contact:** +91-XXXXXXXXXX")
st.sidebar.write("[LinkedIn](https://linkedin.com)")
st.sidebar.write("[GitHub](https://github.com)")

st.sidebar.markdown("---")
st.sidebar.write("Made with ❤️ using Streamlit")

# ---------------- MAIN HEADING ---------------- #
st.markdown("""
    <div style='
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        color: darkblue;
        border: 2px solid white;
        padding: 10px;
        border-radius: 10px;
        width: fit-content;
        margin: auto;
        background-color: rgba(255,255,255,0.6);
    '>
        💰 Insurance Cost Prediction System
    </div>
""", unsafe_allow_html=True)

st.write("")  # spacing

# ---------------- INPUT FORM ---------------- #
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.markdown("### Enter Details")

    age = st.number_input("Age", 18, 100, 25)
    sex = st.selectbox("Gender", ["Male", "Female"])
    bmi = st.number_input("BMI", 10.0, 50.0, 22.0)
    children = st.number_input("Children", 0, 5, 0)
    smoker = st.selectbox("Smoker", ["Yes", "No"])
    region = st.selectbox("Region", ["Northeast", "Northwest", "Southeast", "Southwest"])

    st.write("")
    predict_btn = st.button("🚀 Predict Insurance Cost")

# ---------------- ENCODING ---------------- #
sex = 1 if sex == "Male" else 0
smoker = 1 if smoker == "Yes" else 0

region_map = {
    "Northeast": 0,
    "Northwest": 1,
    "Southeast": 2,
    "Southwest": 3
}
region = region_map[region]

# ---------------- PREDICTION ---------------- #
if predict_btn:
    try:
        input_data = np.array([[age, sex, bmi, children, smoker, region]])
        prediction = model.predict(input_data)

       st.markdown(f"""
    <div style='
        background-color: rgba(255,255,255,0.9);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        color: black;
        font-weight: bold;
        width: 50%;
        margin: auto;
    '>
        💰 Estimated Insurance Cost: ₹ {round(prediction[0], 2)}
    </div>
""", unsafe_allow_html=True)
    except Exception as e:
        st.error("⚠️ Model input mismatch")
        st.write(e)
