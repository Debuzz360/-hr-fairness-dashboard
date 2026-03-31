import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from theme import ARCTIC_CSS, INDIGO, GREEN, RED, AMBER

st.set_page_config(page_title="Predict & Assess", page_icon="🔮", layout="wide")
st.markdown(ARCTIC_CSS, unsafe_allow_html=True)
st.title("🔮 Candidate Assessment Tool")
st.markdown("Simulate a hiring prediction and receive a real-time fairness assessment based on dissertation findings.")
st.divider()

c1, c2 = st.columns([1,1], gap="large")

with c1:
    st.markdown("<div class='ac-section'>Candidate Information</div>", unsafe_allow_html=True)
    with st.expander("👤 Personal Details", expanded=True):
        age    = st.slider("Age", 20, 50, 35)
        gender = st.radio("Gender", ["Female","Male"], horizontal=True)
        g_code = 0 if gender=="Female" else 1
        edu    = st.selectbox("Education Level",
                              ["Below Bachelor's","Bachelor's Type 1","Bachelor's Type 2","Master's","PhD"])
        e_map  = {"Below Bachelor's":0,"Bachelor's Type 1":1,"Bachelor's Type 2":2,"Master's":3,"PhD":4}
        e_code = e_map[edu]
    with st.expander("💼 Experience", expanded=True):
        exp       = st.slider("Years of Experience", 0, 15, 5)
        prev_cos  = st.slider("Previous Companies", 1, 5, 2)
        distance  = st.slider("Distance from Company (km)", 1.0, 50.0, 25.0)
    with st.expander("📊 Assessment Scores", expanded=True):
        interview = st.slider("Interview Score", 0, 100, 50)
        skill     = st.slider("Skill Score", 0, 100, 50)
        persona   = st.slider("Personality Score", 0, 100, 50)
    with st.expander("🏢 Recruitment Context", expanded=True):
        strategy = st.selectbox("Recruitment Strategy", ["Strategy 1","Strategy 2","Strategy 3"],
                                help="Strategy 1 = dominant SHAP proxy feature in dissertation analysis")
        s_code = {"Strategy 1":1,"Strategy 2":2,"Strategy 3":3}[strategy]

with c2:
    st.markdown("<div class='ac-section'>Prediction & Fairness Assessment</div>", unsafe_allow_html=True)

    score = (exp*0.5 + interview*0.2 + skill*0.2 + persona*0.1) / 100
    score = min(score, 1.0)
    original = score

    penalties = []
    if g_code == 0:
        score *= 0.92; penalties.append(("Gender (female)", "−8%", "SPD = −0.0839"))
    if e_code == 0:
        score *= 0.70; penalties.append(("Below Bachelor's", "−30%", "DIR = 0.536"))
    elif e_code == 1:
        score *= 0.85; penalties.append(("Bachelor's Type 1", "−15%", "DIR = 0.700"))
    if s_code == 1:
        score *= 0.85; penalties.append(("RecruitmentStrategy_1", "−15%", "Dominant SHAP feature"))
    if distance > 30:
        score *= 0.95; penalties.append(("Distance >30km", "−5%", "Proxy correlation"))

    total_penalty = round((1 - score/original)*100, 1) if original > 0 else 0
    prediction = score > 0.35

    if prediction:
        st.markdown("""<div style="background:#DCFCE7;border:2px solid #16A34A;border-radius:14px;
        padding:1.5rem;text-align:center;margin-bottom:1rem;">
        <div style="font-size:2.5rem;">✅</div>
        <div style="font-size:1.5rem;font-weight:700;color:#14532D;">PREDICTION: HIRED</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style="background:#FEE2E2;border:2px solid #DC2626;border-radius:14px;
        padding:1.5rem;text-align:center;margin-bottom:1rem;">
        <div style="font-size:2.5rem;">❌</div>
        <div style="font-size:1.5rem;font-weight:700;color:#7F1D1D;">PREDICTION: NOT HIRED</div>
        </div>""", unsafe_allow_html=True)

    ca, cb = st.columns(2)
    with ca: st.metric("Qualification Score", f"{original:.1%}", help="Score from skills/experience only")
    with cb: st.metric("Adjusted Score",      f"{score:.1%}",
                       delta=f"−{total_penalty}% bias penalty" if total_penalty>0 else "No penalty",
                       delta_color="inverse" if total_penalty>0 else "off")
    st.progress(min(score,1.0), text=f"Score: {score:.1%}  |  Hire threshold: 35%")

    if penalties:
        st.markdown("<div class='ac-section'>Bias Adjustments Applied</div>", unsafe_allow_html=True)
        pen_df = pd.DataFrame(penalties, columns=["Factor","Adjustment","Dissertation Basis"])
        st.dataframe(pen_df, use_container_width=True, hide_index=True)

    st.markdown("<div class='ac-section'>Benchmark</div>", unsafe_allow_html=True)
    bench = pd.DataFrame({
        "Metric":              ["Gender SPD","Education DIR"],
        "Acceptable":          ["−0.05 to +0.05","≥ 0.80"],
        "This Candidate":      ["⚠️ At risk" if g_code==0 else "✅ Low risk",
                                "🚨 High risk" if e_code==0 else ("⚠️ Moderate" if e_code==1 else "✅ Low")],
        "Dissertation Result": ["SPD = −0.0839","DIR = 0.536–0.727"]
    })
    st.dataframe(bench, use_container_width=True, hide_index=True)

    if not prediction and score > 0.30:
        st.markdown("""<div class="ac-warn-box">💡 <strong>Borderline:</strong> Score is in the 30–35% range.
        Under ThresholdOptimizer mitigation this candidate may have received a different outcome.</div>""", unsafe_allow_html=True)
    st.caption("⚠️ Demonstration model only — actual hiring must follow fair and lawful HR practices.")
