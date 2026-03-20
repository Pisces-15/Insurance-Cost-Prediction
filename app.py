import streamlit as st
import pickle
import numpy as np

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Insurance App", layout="wide")

# ------------------ CUSTOM CSS ------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1588776814546-1ffcf47267a5");
    background-size: cover;
    background-position: center;
}

/* Light transparent overlay */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.6); /* LIGHT transparency */
    z-index: 0;
}

/* Keep content above overlay */
.main {
    position: relative;
    z-index: 1;
}

/* Heading styling */
h1 {
    color: #1a1a1a;
    font-weight: 800;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.85);
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# Load model
model = pickle.load(open("Insurance.pkl", "rb"))

# ------------------ SIDEBAR ------------------
st.sidebar.title("👩‍💻 About Me")

st.sidebar.write("### Personal Information")
st.sidebar.write("Name: Sakshi Patil")
st.sidebar.write("Stream: IT Engineering")

st.sidebar.write("### 📞 Contact")
st.sidebar.write("Email: patilsakshi1554@email.com")


# ------------------ MAIN PAGE ------------------
st.title("🏥 Insurance Cost Prediction App")

st.write("Enter details below to predict insurance charges:")

# Input fields
age = st.number_input("Age", min_value=1, max_value=100, value=25)
bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=22.0)
children = st.number_input("Number of Children", min_value=0, max_value=10, value=0)

smoker = st.selectbox("Smoker", ["No", "Yes"])
smoker = 1 if smoker == "Yes" else 0

region = st.selectbox("Region", ["Southwest", "Southeast", "Northwest", "Northeast"])

# Encode region manually (example encoding)
region_dict = {
    "Southwest": 0,
    "Southeast": 1,
    "Northwest": 2,
    "Northeast": 3
}
region = region_dict[region]

# ------------------ PREDICTION ------------------
if st.button("Predict 💡"):
    input_data = np.array([[age, bmi, children, smoker, region]])
    
    prediction = model.predict(input_data)

    st.success(f"💰 Estimated Insurance Cost: ₹ {round(prediction[0], 2)}")
