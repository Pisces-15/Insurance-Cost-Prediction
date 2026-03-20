import streamlit as st
import pickle
import numpy as np
import base64
from pathlib import Path

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Insurance Claim Predictor",
    page_icon="🏥",
    layout="wide",
)

# ── Load model ──────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("Insurance.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Google Font ---- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ---- Full-page faint insurance background ---- */
.stApp {
    background-image:
        linear-gradient(rgba(240, 248, 255, 0.92), rgba(240, 248, 255, 0.92)),
        url("https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=1600&q=80");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0a1f44 0%, #1a3a6b 60%, #1e4d8c 100%);
    border-right: 2px solid #2a5298;
}

[data-testid="stSidebar"] * {
    color: #e8f0fe !important;
}

.sidebar-card {
    background: rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 14px;
    border: 1px solid rgba(255,255,255,0.15);
}

.sidebar-card h3 {
    color: #90caf9 !important;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
}

.sidebar-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 8px;
    font-size: 0.88rem;
}

.sidebar-icon {
    font-size: 1.1rem;
    min-width: 20px;
    margin-top: 1px;
}

.sidebar-link a {
    color: #64b5f6 !important;
    text-decoration: none;
}

.sidebar-link a:hover {
    color: #90caf9 !important;
    text-decoration: underline;
}

.profile-avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1565c0, #42a5f5);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    margin: 0 auto 12px auto;
    border: 3px solid rgba(255,255,255,0.3);
}

/* ---- App heading ---- */
.app-heading {
    text-align: center;
    padding: 22px 30px 14px 30px;
    margin-bottom: 28px;
}

.app-heading h1 {
    font-size: 2.2rem;
    font-weight: 700;
    color: #0a1f44;
    background: white;
    display: inline-block;
    padding: 10px 36px;
    border: 1.5px solid #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(10, 31, 68, 0.15);
    letter-spacing: 0.5px;
}

.app-heading p {
    color: #374151;
    font-size: 1rem;
    margin-top: 8px;
    font-weight: 400;
}

/* ---- Form card ---- */
.form-card {
    background: rgba(255, 255, 255, 0.82);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 28px 32px;
    border: 1px solid rgba(255,255,255,0.9);
    box-shadow: 0 8px 32px rgba(10, 31, 68, 0.10);
    margin-bottom: 24px;
}

.section-label {
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.4px;
    color: #1a3a6b;
    margin-bottom: 6px;
    border-left: 3px solid #2a5298;
    padding-left: 8px;
}

/* ---- Streamlit widgets ---- */
label[data-testid="stWidgetLabel"] p,
.stSlider label,
.stSelectbox label,
.stNumberInput label {
    color: #111827 !important;
    font-weight: 600 !important;
    font-size: 0.93rem !important;
}

.stSlider [data-testid="stThumbValue"],
.stSlider [data-testid="stTickBar"] {
    color: #111827 !important;
}

/* ---- Result box ---- */
.result-box {
    background: linear-gradient(135deg, #0a1f44 0%, #1e4d8c 100%);
    border-radius: 14px;
    padding: 28px 32px;
    text-align: center;
    color: white;
    box-shadow: 0 8px 30px rgba(10, 31, 68, 0.35);
    margin-top: 10px;
}

.result-box .amount {
    font-size: 2.8rem;
    font-weight: 700;
    color: #64b5f6;
    letter-spacing: 1px;
}

.result-box .label {
    font-size: 1rem;
    opacity: 0.85;
    margin-bottom: 6px;
}

.result-box .subtitle {
    font-size: 0.85rem;
    opacity: 0.65;
    margin-top: 8px;
}

/* ---- Info metric ---- */
.metric-row {
    display: flex;
    gap: 14px;
    margin-top: 18px;
}

.metric-chip {
    background: rgba(255,255,255,0.80);
    border-radius: 10px;
    padding: 10px 16px;
    flex: 1;
    text-align: center;
    border: 1px solid rgba(10,31,68,0.10);
}

.metric-chip .val {
    font-size: 1.3rem;
    font-weight: 700;
    color: #0a1f44;
}

.metric-chip .key {
    font-size: 0.75rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ---- Predict button ---- */
.stButton button {
    background: linear-gradient(135deg, #0a1f44, #1e4d8c) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 14px 0 !important;
    width: 100% !important;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 16px rgba(10,31,68,0.3) !important;
    transition: all 0.2s ease !important;
}

.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(10,31,68,0.4) !important;
}

/* ---- Divider ---- */
.divider {
    height: 1px;
    background: linear-gradient(to right, transparent, #2a5298, transparent);
    margin: 20px 0;
    opacity: 0.3;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR  — Personal Details
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 10px 0;">
        <div class="profile-avatar">👤</div>
        <div style="font-size:1.2rem; font-weight:700; color:#e3f2fd;">Your Name</div>
        <div style="font-size:0.82rem; color:#90caf9; margin-top:4px;">Data Scientist</div>
    </div>
    <div class="divider"></div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-card">
        <h3>📋 Contact Info</h3>
        <div class="sidebar-item">
            <span class="sidebar-icon">📧</span>
            <span>yourname@email.com</span>
        </div>
        <div class="sidebar-item">
            <span class="sidebar-icon">📞</span>
            <span>+91 98765 43210</span>
        </div>
        <div class="sidebar-item">
            <span class="sidebar-icon">📍</span>
            <span>Pune, Maharashtra, India</span>
        </div>
    </div>

    <div class="sidebar-card">
        <h3>🔗 Links</h3>
        <div class="sidebar-item sidebar-link">
            <span class="sidebar-icon">💼</span>
            <a href="https://linkedin.com/in/yourprofile" target="_blank">LinkedIn Profile</a>
        </div>
        <div class="sidebar-item sidebar-link">
            <span class="sidebar-icon">🐙</span>
            <a href="https://github.com/yourgithub" target="_blank">GitHub Portfolio</a>
        </div>
        <div class="sidebar-item sidebar-link">
            <span class="sidebar-icon">🌐</span>
            <a href="https://yourportfolio.com" target="_blank">Portfolio Website</a>
        </div>
        <div class="sidebar-item sidebar-link">
            <span class="sidebar-icon">🐦</span>
            <a href="https://twitter.com/yourhandle" target="_blank">Twitter / X</a>
        </div>
    </div>

    <div class="sidebar-card">
        <h3>🎓 Education</h3>
        <div class="sidebar-item">
            <span class="sidebar-icon">🏛️</span>
            <div>
                <div style="font-weight:600;">B.Tech / M.Tech</div>
                <div style="font-size:0.78rem; opacity:0.75;">Your University · 2024</div>
            </div>
        </div>
    </div>

    <div class="sidebar-card">
        <h3>🛠 Skills</h3>
        <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:4px;">
            <span style="background:rgba(255,255,255,0.15); border-radius:20px; padding:3px 10px; font-size:0.78rem;">Python</span>
            <span style="background:rgba(255,255,255,0.15); border-radius:20px; padding:3px 10px; font-size:0.78rem;">ML</span>
            <span style="background:rgba(255,255,255,0.15); border-radius:20px; padding:3px 10px; font-size:0.78rem;">Streamlit</span>
            <span style="background:rgba(255,255,255,0.15); border-radius:20px; padding:3px 10px; font-size:0.78rem;">Sklearn</span>
            <span style="background:rgba(255,255,255,0.15); border-radius:20px; padding:3px 10px; font-size:0.78rem;">Pandas</span>
            <span style="background:rgba(255,255,255,0.15); border-radius:20px; padding:3px 10px; font-size:0.78rem;">SQL</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════════

# ── Heading ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-heading">
    <h1>🏥 Insurance Claim Predictor</h1>
    <p>Enter patient details below to estimate the medical insurance charge</p>
</div>
""", unsafe_allow_html=True)


# ── Input Parameters ─────────────────────────────────────────────────────────
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Patient Parameters</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    age = st.slider(
        "🎂  Age (years)",
        min_value=18,
        max_value=100,
        value=35,
        step=1,
        help="Age of the primary insurance holder"
    )

    bmi = st.number_input(
        "⚖️  BMI — Body Mass Index",
        min_value=10.0,
        max_value=60.0,
        value=26.5,
        step=0.1,
        format="%.1f",
        help="Body Mass Index = weight(kg) / height(m)²"
    )

with col2:
    children = st.selectbox(
        "👶  Number of Dependents / Children",
        options=[0, 1, 2, 3, 4, 5],
        index=0,
        help="Number of children/dependents covered by the insurance"
    )

    smoker = st.radio(
        "🚬  Smoking Status",
        options=["Non-Smoker", "Smoker"],
        index=0,
        horizontal=True,
        help="Whether the insurance holder smokes or not"
    )

st.markdown('</div>', unsafe_allow_html=True)  # close form-card


# ── Summary chips ────────────────────────────────────────────────────────────
smoker_val = 1 if smoker == "Smoker" else 0
bmi_category = (
    "Underweight" if bmi < 18.5 else
    "Normal" if bmi < 25 else
    "Overweight" if bmi < 30 else
    "Obese"
)

st.markdown(f"""
<div class="metric-row">
    <div class="metric-chip">
        <div class="val">{age}</div>
        <div class="key">Age</div>
    </div>
    <div class="metric-chip">
        <div class="val">{bmi:.1f}</div>
        <div class="key">BMI · {bmi_category}</div>
    </div>
    <div class="metric-chip">
        <div class="val">{children}</div>
        <div class="key">Dependents</div>
    </div>
    <div class="metric-chip">
        <div class="val">{"🚬 Yes" if smoker_val else "✅ No"}</div>
        <div class="key">Smoker</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Predict Button + Result ───────────────────────────────────────────────────
if st.button("🔍  Predict Insurance Charge", use_container_width=True):
    features = np.array([[age, bmi, children, smoker_val]])
    prediction = model.predict(features)[0]
    prediction = max(prediction, 0)

    risk_level = "🟢 Low Risk" if prediction < 8000 else "🟡 Medium Risk" if prediction < 20000 else "🔴 High Risk"

    st.markdown(f"""
    <div class="result-box">
        <div class="label">Estimated Annual Insurance Charge</div>
        <div class="amount">$ {prediction:,.2f}</div>
        <div class="subtitle">
            Risk Level: {risk_level} &nbsp;|&nbsp;
            Model: Linear Regression &nbsp;|&nbsp;
            Features: Age · BMI · Children · Smoker
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("📊 How was this calculated?", expanded=False):
        coefs = model.coef_
        intercept = model.intercept_
        feature_names = ["Age", "BMI", "Children", "Smoker"]
        input_vals = [age, bmi, children, smoker_val]

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Model Coefficients**")
            for name, coef, val in zip(feature_names, coefs, input_vals):
                contribution = coef * val
                st.markdown(
                    f"<span style='color:#111827'><b>{name}</b>: {coef:.2f} × {val} = <b>{contribution:.2f}</b></span>",
                    unsafe_allow_html=True
                )
        with col_b:
            st.markdown("**Intercept (Base Charge)**")
            st.markdown(
                f"<span style='color:#111827'>Base: <b>${intercept:.2f}</b></span>",
                unsafe_allow_html=True
            )
            st.markdown("**Formula**")
            st.code(
                "charge = intercept\n"
                "       + age × coef_age\n"
                "       + bmi × coef_bmi\n"
                "       + children × coef_children\n"
                "       + smoker × coef_smoker",
                language="text"
            )

else:
    st.markdown("""
    <div style="text-align:center; padding:30px; color:#6b7280; font-size:0.95rem;">
        ☝️ Fill in the parameters above and click <b>Predict Insurance Charge</b>
    </div>
    """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; font-size:0.78rem; color:#9ca3af; padding:10px 0;">
    Built with ❤️ using Streamlit · Linear Regression Model · Insurance Dataset
</div>
""", unsafe_allow_html=True)
