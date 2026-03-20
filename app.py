import streamlit as st
import pickle
import numpy as np

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Insurance App", layout="wide")

# ------------------ CUSTOM CSS ------------------
page_bg = """
<style>

/* Background Image */
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1556742049-0cfed4f6a45d");
    background-size: cover;
    background-position: center;
}

/* Light overlay */
.stApp {
    background: rgba(255, 255, 255, 0.7);
}

/* All text black */
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
}

/* Button */
.stButton>button {
    background-color: black;
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 200px;
}

</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ------------------ LOAD MODEL ------------------
try:
    model = pickle.load(open("Insurance.pkl", "rb"))
except:
    st.error("❌ Model file not found!")
    st.stop()

# ------------------ SIDEBAR ------------------
st.sidebar.title("👩‍💻 About Me")

st.sidebar.write("### Personal Information")
st.sidebar.write("**Name:** Sakshi Patil")
st.sidebar.write("**Stream:** IT Engineering")

st.sidebar.write("### 📞 Contact")
st.sidebar.write("Email: patilsakshi1554@email.com")

# ------------------ MAIN PAGE ------------------
st.markdown("<h1>🏥 Insurance Cost Prediction App</h1>", unsafe_allow_html=True)

st.write("### Enter details below:")

# ------------------ INPUTS ------------------
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 1, 100, 25)
    bmi = st.number_input("BMI", 10.0, 50.0, 22.0)
    children = st.number_input("Children", 0, 10, 0)

with col2:
    smoker = st.selectbox("Smoker", ["No", "Yes"])
    region = st.selectbox("Region", ["Southwest", "Southeast", "Northwest", "Northeast"])

# Encoding
smoker = 1 if smoker == "Yes" else 0

# One-hot encoding for region (most common case)
region_sw = 1 if region == "Southwest" else 0
region_se = 1 if region == "Southeast" else 0
region_nw = 1 if region == "Northwest" else 0
region_ne = 1 if region == "Northeast" else 0

# ------------------ PREDICTION ------------------
st.write("")

if st.button("🚀 Predict Insurance Cost"):
    try:
        # Most common feature format (8 features)
        input_data = np.array([[
            age, bmi, children, smoker,
            region_sw, region_se, region_nw, region_ne
        ]])

        prediction = model.predict(input_data)

        st.success(f"💰 Estimated Insurance Cost: ₹ {round(prediction[0], 2)}")

    except Exception as e:
        st.error("⚠️ Feature mismatch! Try this fix:")
        st.code(str(e))
