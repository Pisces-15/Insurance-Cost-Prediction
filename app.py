import streamlit as st
import pickle
import numpy as np

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Insurance App", layout="wide")

# ------------------ CSS ------------------
# ------------------ CUSTOM CSS ------------------
page_bg = """
<style>

/* Background Image (new one) */
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1556742049-0cfed4f6a45d");
    background-size: cover;
    background-position: center;
}

/* Light overlay so text is visible */
.stApp {
    background: rgba(255, 255, 255, 0.7);
}

/* Make ALL text black */
html, body, [class*="css"]  {
    color: black !important;
}

/* Headings */
h1, h2, h3 {
    color: black !important;
    font-weight: bold;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.9);
    color: black;
}

/* Buttons */
.stButton>button {
    background-color: #000000;
    color: white;
    border-radius: 8px;
}

</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)
# ------------------ LOAD MODEL ------------------
model = pickle.load(open("Insurance.pkl", "rb"))

# ------------------ SIDEBAR ------------------
st.sidebar.title("👩‍💻 About Me")

st.sidebar.write("### Personal Information")
st.sidebar.write("**Name:** Sakshi Patil")
st.sidebar.write("**Stream:** IT Engineering")

st.sidebar.write("### 📞 Contact")
st.sidebar.write("Email: sakshi@email.com")
st.sidebar.write("Phone: 1234567890")

# ------------------ MAIN PAGE ------------------
st.markdown("<h1>🏥 Insurance Cost Prediction App</h1>", unsafe_allow_html=True)

st.write("### Enter details below to predict insurance charges:")

# Input fields
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 1, 100, 25)
    bmi = st.number_input("BMI", 10.0, 50.0, 22.0)

with col2:
    children = st.number_input("Children", 0, 10, 0)
    smoker = st.selectbox("Smoker", ["No", "Yes"])

smoker = 1 if smoker == "Yes" else 0

region = st.selectbox("Region", ["Southwest", "Southeast", "Northwest", "Northeast"])

region_dict = {
    "Southwest": 0,
    "Southeast": 1,
    "Northwest": 2,
    "Northeast": 3
}
region = region_dict[region]

# ------------------ PREDICTION ------------------
st.write("")

if st.button("🚀 Predict Insurance Cost"):
    input_data = np.array([[age, bmi, children, smoker, region]])
    prediction = model.predict(input_data)

    st.success(f"💰 Estimated Insurance Cost: ₹ {round(prediction[0], 2)}")
