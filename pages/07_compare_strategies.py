import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from theme import ARCTIC_CSS, INDIGO, GREEN, RED, AMBER

st.set_page_config(page_title="Compare Strategies", page_icon="📊", layout="wide")
st.markdown(ARCTIC_CSS, unsafe_allow_html=True)
st.title("📊 Recruitment Strategy Comparison")

c1, c2 = st.columns(2)
with c1:
    st.markdown("<div class='ac-section'>Strategy 1 — Baseline (No Mitigation)</div>", unsafe_allow_html=True)
    st.metric("Selection Rate","31%")
    st.metric("Gender SPD","-0.0839",help="Negative: female candidates selected less often")
    st.metric("Education DIR","0.727",help="Below 0.80 four-fifths rule benchmark")
    st.metric("XGBoost F1","86.0%")
    st.markdown("""<div class="ac-danger-box">
    ❌ Gender bias (SPD = −0.0839)<br>
    ❌ Education bias (DIR = 0.727, below the 0.80 four-fifths rule benchmark)<br>
    ❌ RecruitmentStrategy_1 dominates SHAP predictions<br>
    ❌ All models fail DIR ≥ 0.8 for at least one group
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='ac-section'>Strategy 2 — With Mitigation</div>", unsafe_allow_html=True)
    mit = st.selectbox("Select mitigation technique", ["ThresholdOptimizer","ExponentiatedGradient","Reweighting"])
    if mit == "ThresholdOptimizer":
        st.metric("Selection Rate","32%",delta="+1%")
        st.metric("Gender SPD","-0.0689",delta="Improved")
        st.metric("Education DIR","0.795",delta="+0.068")
        st.metric("F1 Score","84.7%",delta="-1.0%", delta_color="inverse")
        st.markdown("""<div class="ac-info-box">✅ <strong>Recommended:</strong> Best DIR compliance. Closest to the 0.80 four-fifths rule benchmark.</div>""", unsafe_allow_html=True)
        st.progress(0.795, text="DIR toward 0.8 threshold: 99.4%")
    elif mit == "ExponentiatedGradient":
        st.metric("Selection Rate","31%",delta="No change")
        st.metric("Gender SPD","-0.0187",delta="Best SPD improvement")
        st.metric("Education DIR","0.517",delta="-0.210", delta_color="inverse")
        st.metric("F1 Score","78.9%",delta="-1.3%", delta_color="inverse")
        st.markdown("""<div class="ac-warn-box">⚠️ Best SPD for gender but worsens education DIR. Best suited to Logistic Regression.</div>""", unsafe_allow_html=True)
        st.progress(0.517, text="DIR toward 0.8 threshold: 64.6%")
    else:
        st.metric("Selection Rate","31%",delta="No change")
        st.metric("Gender SPD","-0.0716",delta="Slight improvement")
        st.metric("Education DIR","0.769",delta="+0.042")
        st.metric("F1 Score","85.4%",delta="-0.6%", delta_color="inverse")
        st.markdown("""<div class="ac-warn-box">⚠️ Modest improvement. Useful pre-processing step but insufficient alone.</div>""", unsafe_allow_html=True)
        st.progress(0.769, text="DIR toward 0.8 threshold: 96.1%")

st.markdown("<div class='ac-section'>Summary Comparison Table</div>", unsafe_allow_html=True)
st.dataframe(pd.DataFrame({
    "Technique":       ["Baseline","Reweighting","ExponentiatedGradient","ThresholdOptimizer"],
    "Gender SPD":      ["-0.0839","-0.0716","-0.0187","-0.0689"],
    "Education DIR":   ["0.727","0.769","0.517","0.795"],
    "DIR ≥ 0.8?":      ["🚨 No","🚨 No","🚨 No","⚠️ Near"],
    "F1 Score":        ["86.0%","85.4%","78.9%","84.7%"],
    "Recommendation":  ["Baseline only","Pre-processing step","Gender priority","✅ Best compliance"]
}), use_container_width=True, hide_index=True)
