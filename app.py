import streamlit as st
import pickle
import numpy as np

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Insurance Predictor", layout="centered")

# ------------------ SIMPLE CLEAN CSS ------------------
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1556742049-0cfed4f6a45d");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Light overlay */
.main {
    background-color: rgba(255, 255, 255, 0.75);
    padding: 20px;
    border-radius: 10px;
}

/* Black text everywhere */
html, body, [class*="css"] {
    color: black !important;
}

/* Button styling */
.stButton>button {
    background-color: black;
    color: white;
    border-radius: 6px;
    height: 40px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ------------------ LOAD MODEL ------------------
try:
    model = pickle.load(open("Insurance.pkl", "rb"))
except:
    st.error("Model file not found!")
    st.stop()

# ------------------ SIDEBAR ------------------
st.sidebar.title("About Me")
st.sidebar.write("**Name:** Sakshi Patil")
st.sidebar.write("**Stream:** IT Engineering")
st.sidebar.write("**Email:** patilsakshi1554@email.com")

# ------------------ MAIN ------------------
st.title("🏥 Insurance Cost Prediction")

st.write("Enter details:")

# Inputs (ONLY required features)
age = st.number_input("Age", 1, 100, 25)
bmi = st.number_input("BMI", 10.0, 50.0, 22.0)
children = st.number_input("Children", 0, 10, 0)

smoker = st.selectbox("Smoker", ["No", "Yes"])
smoker = 1 if smoker == "Yes" else 0

# ------------------ PREDICTION ------------------
if st.button("Predict"):
    input_data = np.array([[age, bmi, children, smoker]])
    prediction = model.predict(input_data)

    st.success(f"Estimated Insurance Cost: ₹ {round(prediction[0], 2)}")
