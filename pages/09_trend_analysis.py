import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from theme import ARCTIC_CSS, PLOTLY_LAYOUT, INDIGO, GREEN, RED, AMBER, SLATE

st.set_page_config(page_title="Trend Analysis", page_icon="📈", layout="wide")
st.markdown(ARCTIC_CSS, unsafe_allow_html=True)
st.title("📈 Fairness Trend Analysis")
st.markdown("Simulated monitoring dashboard showing how fairness metrics evolve across quarterly audit cycles.")

timeline = pd.DataFrame({
    "Period":        ["Q1 2024","Q2 2024","Q3 2024","Q4 2024","Q1 2025","Q2 2025"],
    "Gender_SPD":    [-0.062,-0.071,-0.083,-0.074,-0.069,-0.059],
    "Education_DIR": [0.68,  0.69,  0.71,  0.72,  0.73,  0.74],
    "F1_Score":      [0.82,  0.84,  0.86,  0.86,  0.86,  0.86],
    "Mitigation":    [False, False, False, True,  True,  True]
})
pre  = timeline[~timeline["Mitigation"]]
post = timeline[timeline["Mitigation"]]
bridge = timeline.iloc[2:4]
layout = dict(PLOTLY_LAYOUT)

def line_chart(y_col, y_title, y_range, h_val, h_label, chart_title=""):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pre["Period"],  y=pre[y_col],
        mode="lines+markers", name="Pre-mitigation",
        line=dict(color=RED, width=3), marker=dict(size=9)))
    fig.add_trace(go.Scatter(x=post["Period"], y=post[y_col],
        mode="lines+markers", name="Post-mitigation",
        line=dict(color=GREEN, width=3), marker=dict(size=9)))
    fig.add_trace(go.Scatter(x=bridge["Period"], y=bridge[y_col],
        mode="lines", showlegend=False,
        line=dict(color=AMBER, width=2, dash="dot")))
    fig.add_hline(y=h_val, line_dash="dot", line_color=RED,
                  annotation_text=h_label, annotation_font_color=RED)
    l = dict(layout); l.update(height=340, yaxis_title=y_title,
        title=chart_title, title_font_size=13,
        legend=dict(bgcolor="#FFFFFF", bordercolor="#E2E8F0", borderwidth=1))
    if y_range: l["yaxis"] = dict(range=y_range, gridcolor="#E2E8F0")
    fig.update_layout(**l)
    return fig

st.markdown("<div class='ac-section'>Gender Fairness Trend (SPD)</div>", unsafe_allow_html=True)
st.caption("Negative SPD = female candidates disadvantaged. Values closer to 0 are fairer.")
st.plotly_chart(line_chart("Gender_SPD","SPD",None,-0.05,"Fairness threshold (−0.05)","Gender SPD Trend: Pre vs Post Mitigation"), use_container_width=True)

st.markdown("<div class='ac-section'>Education Fairness Trend (DIR)</div>", unsafe_allow_html=True)
st.caption("DIR ≥ 0.8 four-fifths rule practical benchmark.")
st.plotly_chart(line_chart("Education_DIR","DIR",[0.5,1.0],0.8,"Legal threshold (0.8)","Education DIR Trend: Pre vs Post Mitigation"), use_container_width=True)

st.markdown("<div class='ac-section'>Model Accuracy Trend (F1)</div>", unsafe_allow_html=True)
st.caption("Fairness improvements should not catastrophically reduce accuracy.")
st.plotly_chart(line_chart("F1_Score","F1 Score",[0.7,1.0],0.8,"Minimum acceptable F1","Model Accuracy (F1) Trend: Pre vs Post Mitigation"), use_container_width=True)

st.markdown("""<div class="ac-info-box">
📈 <strong>Key observations:</strong> Gender fairness improves after mitigation in Q4 2024. Education DIR is 
improving but remains below 0.8. Model accuracy stays stable — mitigation does not significantly degrade 
performance. Quarterly audits are recommended under the socio-technical governance framework.
</div>""", unsafe_allow_html=True)
