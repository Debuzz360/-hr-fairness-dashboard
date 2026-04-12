import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from theme import ARCTIC_CSS, INDIGO

st.set_page_config(page_title="Overview", page_icon="📋", layout="wide")
st.markdown(ARCTIC_CSS, unsafe_allow_html=True)

st.title("📋 Overview & Research Framework")
st.markdown("<div class='ac-section'>Research Progress</div>", unsafe_allow_html=True)

progress_data = [
    ("Data Collection",    "✅ Complete",    100),
    ("Model Training",     "✅ Complete",    100),
    ("Fairness Analysis",  "✅ Complete",    100),
    ("Mitigation Testing", "✅ Complete",    100),
    ("Streamlit App",      "✅ Complete",    100),
    ("Chapter 5 Write-up", "🔄 In Progress", 60),
]
for phase, status, pct in progress_data:
    c1, c2, c3 = st.columns([2, 2, 6])
    with c1: st.write(phase)
    with c2: st.write(status)
    with c3: st.progress(pct / 100, text=f"{pct}%")

st.markdown("<div class='ac-section'>Research Context</div>", unsafe_allow_html=True)
st.markdown("""
This dissertation examines **algorithmic bias in machine learning systems used for HR recruitment**
within UK financial services. The UK Equality Act 2010 prohibits discrimination on protected
characteristics including gender, race/ethnicity, and age. A Disparate Impact Ratio (DIR) below
**0.8** signals potential legal exposure — the so-called *four-fifths rule*.
""")

st.markdown("<div class='ac-section'>Five-Metric Fairness Framework</div>", unsafe_allow_html=True)
st.markdown("Five complementary metrics were used — no single metric captures the full picture of fairness.")
metrics = {
    "Metric": ["SPD", "DIR", "EOD", "PPV Parity", "FPR Parity"],
    "Full Name": ["Statistical Parity Difference", "Disparate Impact Ratio",
                  "Equal Opportunity Difference", "Positive Predictive Value Parity",
                  "False Positive Rate Parity"],
    "Ideal Value": ["0", "1.0 (legal ≥ 0.8)", "0", "0", "0"],
    "What it captures": [
        "Overall selection rate gap",
        "Ratio of selection rates — legal indicator",
        "Whether qualified candidates are equally hired",
        "Whether hire predictions are equally reliable",
        "Whether rejection errors fall equally"
    ]
}
st.dataframe(pd.DataFrame(metrics), use_container_width=True, hide_index=True)

st.markdown("<div class='ac-section'>Socio-Technical Governance Schema</div>", unsafe_allow_html=True)
layers = {
    "Layer": ["1 — Technical", "2 — Organisational", "3 — Regulatory", "4 — Human Oversight"],
    "Focus": ["Algorithm design, fairness constraints, mitigation",
               "HR policy, diversity strategy, data governance",
               "Equality Act 2010, GDPR, FCA conduct standards",
               "Human-in-the-loop review, explainability, appeals"],
    "Key Tools": ["Reweighting, ExponentiatedGradient, ThresholdOptimizer, SHAP",
                  "Bias auditing schedules, diverse training data mandates",
                  "DIR ≥ 0.8 threshold, data minimisation, right to explanation",
                  "Recruiter review triggers, candidate transparency, audit trails"]
}
st.dataframe(pd.DataFrame(layers), use_container_width=True, hide_index=True)

st.markdown("<div class='ac-section'>Models Evaluated</div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""<div class="ac-card"><div class="ac-val" style="font-size:1.2rem;">Logistic Regression</div>
    <div class="ac-lbl">Baseline Model</div>
    <div style="font-size:0.82rem;color:#64748B;margin-top:6px;">Interpretable baseline. Linear decision boundary. Best for coefficient-level bias inspection.</div></div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="ac-card"><div class="ac-val" style="font-size:1.2rem;">Random Forest</div>
    <div class="ac-lbl">Ensemble Model</div>
    <div style="font-size:0.82rem;color:#64748B;margin-top:6px;">Ensemble of decision trees. Used with ThresholdOptimizer for best DIR compliance result.</div></div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class="ac-card"><div class="ac-val" style="font-size:1.2rem;">XGBoost</div>
    <div class="ac-lbl">Best Performer</div>
    <div style="font-size:0.82rem;color:#64748B;margin-top:6px;">Gradient boosted trees. Best predictive F1 (~86%). SHAP-compatible for proxy feature analysis.</div></div>""", unsafe_allow_html=True)
