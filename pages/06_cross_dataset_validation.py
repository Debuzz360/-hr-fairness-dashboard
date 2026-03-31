import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from theme import ARCTIC_CSS, PLOTLY_LAYOUT, INDIGO, GREEN, RED, AMBER, SLATE

st.set_page_config(page_title="Cross-Dataset Validation", page_icon="🔄", layout="wide")
st.markdown(ARCTIC_CSS, unsafe_allow_html=True)
st.title("🔄 Cross-Dataset Validation")

st.markdown("<div class='ac-section'>Dataset Characteristics</div>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown("""<div class="ac-card">
    <div class="ac-val">Primary Dataset</div><div class="ac-lbl">Main Analysis</div>
    <div style="margin-top:12px;">
        <div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #E2E8F0;"><span style="color:#64748B;font-size:0.85rem;">Records</span><strong>1,500</strong></div>
        <div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #E2E8F0;"><span style="color:#64748B;font-size:0.85rem;">Hire Rate</span><strong>31%</strong></div>
        <div style="display:flex;justify-content:space-between;padding:4px 0;"><span style="color:#64748B;font-size:0.85rem;">Features</span><strong>31 columns</strong></div>
    </div></div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="ac-card">
    <div class="ac-val">Secondary Dataset</div><div class="ac-lbl">Validation</div>
    <div style="margin-top:12px;">
        <div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #E2E8F0;"><span style="color:#64748B;font-size:0.85rem;">Records</span><strong>225</strong></div>
        <div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #E2E8F0;"><span style="color:#64748B;font-size:0.85rem;">Hire Rate</span><strong>33%</strong></div>
        <div style="display:flex;justify-content:space-between;padding:4px 0;"><span style="color:#64748B;font-size:0.85rem;">Features</span><strong>Matched subset</strong></div>
    </div></div>""", unsafe_allow_html=True)

st.markdown("<div class='ac-section'>SPD Comparison: Primary vs Secondary</div>", unsafe_allow_html=True)
cross = pd.DataFrame({
    "Model":   ["LR","RF","XGB"]*2,
    "Dataset": ["Primary"]*3 + ["Secondary"]*3,
    "SPD_Gender": [-0.082,-0.091,-0.087, -0.078,-0.085,-0.081]
})
layout = dict(PLOTLY_LAYOUT); layout.update(height=380)
fig = go.Figure()
for dataset, colour in [("Primary", INDIGO), ("Secondary", AMBER)]:
    d = cross[cross["Dataset"]==dataset]
    fig.add_trace(go.Bar(name=dataset, x=d["Model"], y=d["SPD_Gender"],
        marker_color=colour, text=[f"{v:.3f}" for v in d["SPD_Gender"]], textposition="outside"))
fig.add_hline(y=0, line_dash="dash", line_color=SLATE, line_width=1)
fig.update_layout(**layout, barmode="group", yaxis_title="SPD (Gender)")
st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='ac-section'>Validation Summary</div>", unsafe_allow_html=True)
summary = pd.DataFrame({
    "Finding": ["Negative gender SPD", "DIR below 0.8", "Education bias most severe", "RecruitmentStrategy proxy"],
    "Primary (n=1,500)": ["✅ Confirmed"]*4,
    "Secondary (n=225)": ["✅ Confirmed","✅ Confirmed","⚠️ Partial","⚠️ Partial"],
    "Generalises?": ["✅ Yes","✅ Yes","⚠️ Partially","⚠️ Partially"]
})
st.dataframe(summary, use_container_width=True, hide_index=True)

st.markdown("""<div class="ac-info-box">
<strong>RQ4 answered:</strong> Consistent negative SPD direction across both datasets confirms bias
patterns are not artefacts of a single dataset, strengthening the generalisability of the findings.
</div>""", unsafe_allow_html=True)
