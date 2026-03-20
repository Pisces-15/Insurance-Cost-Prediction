import streamlit as st
import pickle
import numpy as np

# Load model
model = pickle.load(open("Insurance.pkl", "rb"))

# Page config
st.set_page_config(page_title="Insurance Predictor", page_icon="💰")

# Title
st.title("💰 Insurance Cost Prediction")

st.write("Predict your insurance cost using ML model")

# Sidebar
st.sidebar.header("📝 Enter Your Details")

age = st.sidebar.number_input("Age", 1, 100, 25)
sex = st.sidebar.selectbox("Gender", ["Male", "Female"])
bmi = st.sidebar.number_input("BMI", 10.0, 50.0, 22.0)
children = st.sidebar.number_input("Children", 0, 10, 0)
smoker = st.sidebar.selectbox("Smoker", ["Yes", "No"])
region = st.sidebar.selectbox("Region", ["Northeast", "Northwest", "Southeast", "Southwest"])

# Encoding
sex = 1 if sex == "Male" else 0
smoker = 1 if smoker == "Yes" else 0

region_map = {
    "Northeast": 0,
    "Northwest": 1,
    "Southeast": 2,
    "Southwest": 3
}
region_encoded = region_map[region]

# One-hot encoding
region_northeast = 1 if region == "Northeast" else 0
region_northwest = 1 if region == "Northwest" else 0
region_southeast = 1 if region == "Southeast" else 0

# Button
if st.sidebar.button("🚀 Predict"):

    try:
        expected = model.n_features_in_

        # CASE 1: 6 features
        if expected == 6:
            input_data = np.array([[age, sex, bmi, children, smoker, region_encoded]])

        # CASE 2: 8 features (drop one dummy)
        elif expected == 8:
            input_data = np.array([[age, sex, bmi, children, smoker,
                                    region_northeast, region_northwest, region_southeast]])

        # CASE 3: 9 features (all dummies)
        elif expected == 9:
            region_southwest = 1 if region == "Southwest" else 0
            input_data = np.array([[age, sex, bmi, children, smoker,
                                    region_northeast, region_northwest,
                                    region_southeast, region_southwest]])

        else:
            st.error("⚠️ Model feature mismatch. Please check training data.")
            st.stop()

        # Prediction
        prediction = model.predict(input_data)

        st.success(f"💰 Estimated Insurance Cost: ₹ {round(prediction[0], 2)}")

    except Exception as e:
        st.error("⚠️ Error occurred while prediction")
        st.write(e)

# Debug info (optional remove later)
st.write("Model expects features:", model.n_features_in_)
