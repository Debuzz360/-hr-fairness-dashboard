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
    ("Data Collection",        "✅ Complete", 100),
    ("Model Training",         "✅ Complete", 100),
    ("Fairness Analysis",      "✅ Complete", 100),
    ("Mitigation Testing",     "✅ Complete", 100),
    ("Streamlit App",          "✅ Complete", 100),
    ("Chapter 5 & 6 Write-up", "✅ Complete", 100),
    ("Dissertation Submission","✅ Complete", 100),
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
**0.8** signals potential adverse impact — the so-called *four-fifths rule*, drawn from the US EEOC
Uniform Guidelines on Employee Selection Procedures and used throughout as a **practical benchmark**.
""")

st.markdown("""<div class="ac-warn-box">
⚠️ <strong>Legal Note:</strong> The 0.80 DIR threshold is a practical benchmark drawn from the US EEOC
four-fifths rule — it is <strong>not a statutory threshold</strong> under the Equality Act 2010.
Exceeding 0.80 does not automatically negate an indirect discrimination claim under Section 19.
Organisations must also demonstrate that any potentially discriminatory practice is a proportionate
means of achieving a legitimate aim. Additionally, the <strong>Data (Use and Access) Act 2025</strong>
has reformed the UK automated decision-making framework, replacing the original UK GDPR Article 22
with updated provisions on "significant decisions" taken solely by automated means. HR teams should
ensure compliance with these latest requirements.
</div>""", unsafe_allow_html=True)

st.markdown("<div class='ac-section'>Five-Metric Fairness Framework</div>", unsafe_allow_html=True)
st.markdown("Five complementary metrics were used — no single metric captures the full picture of fairness.")
metrics = {
    "Metric": ["SPD", "DIR", "EOD", "PPV Parity", "FPR Parity"],
    "Full Name": ["Statistical Parity Difference", "Disparate Impact Ratio",
                  "Equal Opportunity Difference", "Positive Predictive Value Parity",
                  "False Positive Rate Parity"],
    "Ideal Value": ["0", "1.0 (benchmark ≥ 0.8)", "0", "0", "0"],
    "What it captures": [
        "Overall selection rate gap",
        "Ratio of selection rates — four-fifths rule benchmark",
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
                  "DIR ≥ 0.8 four-fifths rule benchmark, data minimisation, right to explanation",
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
