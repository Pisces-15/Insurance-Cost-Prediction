import streamlit as st
import pickle
import numpy as np

# Load model
model = pickle.load(open("Insurance.pkl", "rb"))

# Page config
st.set_page_config(page_title="Insurance Predictor", page_icon="💰", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to right, #74ebd5, #ACB6E5);
    }
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 20px;
    }
    .card {
        background-color: rgba(255,255,255,0.9);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    }
    .result {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        color: green;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">💰 Insurance Cost Predictor</div>', unsafe_allow_html=True)

# Card container
st.markdown('<div class="card">', unsafe_allow_html=True)

# Layout with columns
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 1, 100, 25)
    bmi = st.number_input("BMI", 10.0, 50.0, 22.0)
    children = st.number_input("Children", 0, 10, 0)

with col2:
    sex = st.selectbox("Gender", ["Male", "Female"])
    smoker = st.selectbox("Smoker", ["Yes", "No"])
    region = st.selectbox("Region", ["Northeast", "Northwest", "Southeast", "Southwest"])

# Encoding
sex = 1 if sex == "Male" else 0
smoker = 1 if smoker == "Yes" else 0

region_northeast = 1 if region == "Northeast" else 0
region_northwest = 1 if region == "Northwest" else 0
region_southeast = 1 if region == "Southeast" else 0
region_southwest = 1 if region == "Southwest" else 0

# Button centered
st.markdown("<br>", unsafe_allow_html=True)
predict_btn = st.button("🚀 Predict Cost")

# Prediction
if predict_btn:
    input_data = np.array([[age, sex, bmi, children, smoker,
                            region_northeast, region_northwest,
                            region_southeast, region_southwest]])

    prediction = model.predict(input_data)

    st.markdown(f"""
        <div class="result">
            💰 Estimated Insurance Cost: ₹ {round(prediction[0], 2)}
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
