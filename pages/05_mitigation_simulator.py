import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from theme import ARCTIC_CSS, PLOTLY_LAYOUT, INDIGO, GREEN, RED, AMBER, SLATE

st.set_page_config(page_title="Mitigation Simulator", page_icon="⚖️", layout="wide")
st.markdown(ARCTIC_CSS, unsafe_allow_html=True)
st.title("⚖️ Mitigation Strategy Simulator")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "fairness_results.csv")

@st.cache_data
def load():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame({
        "Classifier": ["Logistic Regression"]*3 + ["Random Forest"]*3 + ["XGBoost"]*3,
        "Technique":  ["Baseline","Reweighting (Pre)","ThresholdOptimizer (Post)"]*3,
        "SPD_Gender": [-0.0369,-0.0433,0.0091, -0.0716,-0.0580,-0.0120, -0.0839,-0.0690,-0.0210],
        "F1_Score":   [0.7902,0.7864,0.8449,   0.8457,0.8310,0.8750,   0.8603,0.8460,0.8920],
        "SPD_Delta":  [0,-.0064,.0278,           0,.0136,.0596,           0,.0149,.0629],
        "F1_Delta":   [0,-.0038,.0547,           0,-.0147,.0293,          0,-.0143,.0317]
    })

df = load()
if not os.path.exists(DATA_PATH):
    st.warning("⚠️ Using placeholder data.")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""<div class="ac-card"><div class="ac-lbl">Pre-processing</div>
    <div style="font-size:1rem;font-weight:600;color:#0F172A;margin-top:4px;">Reweighting</div>
    <div style="font-size:0.8rem;color:#64748B;margin-top:4px;">Assigns higher training weights to underrepresented group–outcome combinations.</div></div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="ac-card"><div class="ac-lbl">In-processing</div>
    <div style="font-size:1rem;font-weight:600;color:#0F172A;margin-top:4px;">ExponentiatedGradient</div>
    <div style="font-size:0.8rem;color:#64748B;margin-top:4px;">Applies fairness constraints during training via Lagrangian optimisation (Fairlearn).</div></div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class="ac-card"><div class="ac-lbl">Post-processing</div>
    <div style="font-size:1rem;font-weight:600;color:#0F172A;margin-top:4px;">ThresholdOptimizer</div>
    <div style="font-size:0.8rem;color:#64748B;margin-top:4px;">Adjusts prediction thresholds per group after training. Best SPD result in dissertation.</div></div>""", unsafe_allow_html=True)

clf = st.selectbox("Select classifier", df["Classifier"].unique().tolist())
filtered = df[df["Classifier"]==clf].reset_index(drop=True)

layout = dict(PLOTLY_LAYOUT); layout.update(title='', height=360)

spd_colours = [GREEN if abs(float(v))<=0.05 else (AMBER if abs(float(v))<=0.1 else RED)
               for v in filtered["SPD_Gender"]]

fig = go.Figure(go.Bar(x=filtered["Technique"], y=filtered["SPD_Gender"].astype(float),
    marker_color=spd_colours,
    text=[f"{float(v):.4f}" for v in filtered["SPD_Gender"]], textposition="outside"))
fig.add_hline(y=0, line_dash="dash", line_color=SLATE, line_width=1)
fig.add_hline(y=-0.05, line_dash="dot", line_color=RED,
              annotation_text="Fairness threshold", annotation_font_color=RED)
fig.update_layout(**layout, yaxis_title="SPD (Gender)")
st.plotly_chart(fig, use_container_width=True)
st.caption("🟢 Green = fair  |  🟡 Amber = moderate  |  🔴 Red = significant bias")

fig2 = go.Figure(go.Bar(x=filtered["Technique"], y=filtered["F1_Score"].astype(float),
    marker_color=INDIGO,
    text=[f"{float(v):.4f}" for v in filtered["F1_Score"]], textposition="outside"))
fig2.update_layout(**layout, yaxis_title="F1 Score")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("<div class='ac-section'>Fairness–Accuracy Trade-off</div>", unsafe_allow_html=True)
fig3 = go.Figure()
colours_s = [INDIGO, AMBER, GREEN, RED]
for i, (_, row) in enumerate(filtered.iterrows()):
    fig3.add_trace(go.Scatter(x=[abs(float(row["SPD_Gender"]))], y=[float(row["F1_Score"])],
        mode="markers+text", text=[row["Technique"]], textposition="top center",
        marker=dict(size=18, color=colours_s[i%4], line=dict(color="#fff", width=2)),
        name=row["Technique"]))
fig3.add_vline(x=0.05, line_dash="dash", line_color=RED,
               annotation_text="|SPD| threshold", annotation_font_color=RED)
layout3 = dict(PLOTLY_LAYOUT); layout3.update(title='', height=380, showlegend=False,
    xaxis_title="|SPD| (lower = fairer)", yaxis_title="F1 Score (higher = better)")
fig3.update_layout(**layout3)
st.plotly_chart(fig3, use_container_width=True)

with st.expander("Full Results Table"):
    d = df.copy()
    for c in ["SPD_Gender","F1_Score","SPD_Delta","F1_Delta"]:
        if c in d.columns: d[c] = d[c].apply(lambda x: f"{float(x):.4f}")
    d["SPD Improved?"] = df["SPD_Delta"].astype(float).apply(
        lambda x: "✅ Yes" if x>0 else ("➡️ Same" if x==0 else "⬇️ Worse"))
    st.dataframe(d, use_container_width=True, hide_index=True)

st.markdown("""<div class="ac-info-box">
<strong>Key finding:</strong> ThresholdOptimizer achieved the greatest SPD improvement across all classifiers,
directly answering RQ3. For Logistic Regression it produced a positive SPD (0.0091) — confirming
post-processing techniques can achieve legal compliance in UK financial services recruitment systems.
</div>""", unsafe_allow_html=True)
