import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from theme import ARCTIC_CSS, PLOTLY_LAYOUT, INDIGO, GREEN, RED, AMBER, SLATE

st.set_page_config(page_title="Dissertation Results", page_icon="📊", layout="wide")
st.markdown(ARCTIC_CSS, unsafe_allow_html=True)
st.title("📊 Dissertation Results")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "fairness_results.csv")

@st.cache_data
def load():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame({
        "Classifier": ["Logistic Regression","Logistic Regression","Random Forest","Random Forest","XGBoost","XGBoost"],
        "Technique":  ["Baseline","ThresholdOptimizer (Post)","Baseline","ThresholdOptimizer (Post)","Baseline","ThresholdOptimizer (Post)"],
        "SPD_Gender": [-0.0369, 0.0091, -0.0716,-0.0120,-0.0839,-0.0210],
        "F1_Score":   [0.7902,  0.8449, 0.8457, 0.8750, 0.8603, 0.8920],
        "SPD_Delta":  [0.0, 0.0278, 0.0, 0.0596, 0.0, 0.0629],
        "F1_Delta":   [0.0, 0.0547, 0.0, 0.0293, 0.0, 0.0317]
    })

df = load()
if not os.path.exists(DATA_PATH):
    st.warning("⚠️ Using placeholder data — place fairness_results.csv in data/ folder.")

baseline = df[df["Technique"]=="Baseline"] if "Technique" in df.columns else df

st.markdown("<div class='ac-section'>Model Predictive Performance</div>", unsafe_allow_html=True)
cols = st.columns(len(baseline))
for i, (_, row) in enumerate(baseline.iterrows()):
    with cols[i]:
        f1 = float(row["F1_Score"])
        st.metric(row["Classifier"], f"{f1:.1%}" if f1<=1 else f"{f1:.1f}%")

st.markdown("<div class='ac-section'>SPD by Classifier and Technique</div>", unsafe_allow_html=True)

techniques = df["Technique"].unique().tolist() if "Technique" in df.columns else []
sel = st.multiselect("Filter techniques", techniques, default=techniques)
filtered = df[df["Technique"].isin(sel)] if sel else df

layout = dict(PLOTLY_LAYOUT)
layout.update(title='', height=400)

fig = px.bar(filtered, x="Classifier", y="SPD_Gender", color="Technique", barmode="group",
             color_discrete_sequence=[INDIGO, GREEN, AMBER, RED])
fig.add_hline(y=0, line_dash="dash", line_color=SLATE, line_width=1)
fig.add_hline(y=-0.05, line_dash="dot", line_color=RED,
              annotation_text="Fairness threshold (−0.05)", annotation_font_color=RED)
fig.update_layout(**layout)
st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='ac-section'>F1 Score by Classifier and Technique</div>", unsafe_allow_html=True)
fig2 = px.bar(filtered, x="Classifier", y="F1_Score", color="Technique", barmode="group",
              color_discrete_sequence=[INDIGO, GREEN, AMBER, RED])
fig2.update_layout(**layout)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("<div class='ac-section'>Full Results Table</div>", unsafe_allow_html=True)
with st.expander("View complete table"):
    d = df.copy()
    for c in ["SPD_Gender","F1_Score","SPD_Delta","F1_Delta"]:
        if c in d.columns: d[c] = d[c].apply(lambda x: f"{float(x):.4f}")
    st.dataframe(d, use_container_width=True, hide_index=True)

st.markdown("<div class='ac-section'>Figure 4.8: Gender Fairness Metrics Heatmap — Baseline Results</div>", unsafe_allow_html=True)

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np

metrics_hm = ['SPD', 'EOD', 'EqOdds', 'FNRP', 'DIR']
classifiers_hm = ['Logistic\nRegression', 'Random\nForest', 'XGBoost']

data_hm = np.array([
    [-0.0369, -0.0716, -0.0839],
    [-0.0807, -0.1241, -0.1368],
    [ 0.0807,  0.1241,  0.1368],
    [ 0.0807,  0.1241,  0.1368],
    [ 0.9057,  0.7674,  0.7435],
])

import seaborn as sns
fig_hm, ax_hm = plt.subplots(figsize=(10, 7))
cmap_hm = sns.diverging_palette(10, 130, as_cmap=True)
sns.heatmap(data_hm, ax=ax_hm, annot=True, fmt='.4f', cmap=cmap_hm,
    center=0, vmin=-0.20, vmax=0.95, linewidths=0.8, linecolor='white',
    xticklabels=classifiers_hm, yticklabels=metrics_hm,
    cbar_kws={'label': 'Metric Value', 'shrink': 0.75},
    annot_kws={'size': 12, 'weight': 'bold'})
ax_hm.axhline(y=4, color='navy', linewidth=2, linestyle='--', alpha=0.8)
ax_hm.set_title(
    'Figure 4.8: Gender Fairness Metrics Heatmap — Baseline Results\nFemale vs Male | Logistic Regression, Random Forest, XGBoost',
    fontsize=12, fontweight='bold', pad=15)
ax_hm.set_xlabel('Classifier', fontsize=11, labelpad=10)
ax_hm.set_ylabel('Fairness Metric', fontsize=11, labelpad=10)
ax_hm.tick_params(axis='x', rotation=0, labelsize=10)
ax_hm.tick_params(axis='y', rotation=0, labelsize=10)
fig_hm.text(0.5, -0.02,
    'Source: Lawal Adeniyi (2026). Dashed line separates DIR from other metrics.',
    ha='center', fontsize=9, style='italic', color='gray')
plt.tight_layout()
st.pyplot(fig_hm, use_container_width=True)
plt.close()

st.markdown("""<div class="ac-info-box">
♿ <strong>Accessibility note:</strong> The heatmap uses a red-green colour scale. Red cells indicate
negative fairness values (disadvantage to unprivileged group). Green cells indicate positive values
(above benchmark). All numerical values are displayed directly in each cell.
</div>""", unsafe_allow_html=True)

st.markdown("<div class='ac-section'>Key Findings</div>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown("""<div class="ac-info-box">
    <strong>Consistent negative SPD</strong> across all three classifiers and all protected groups —
    unprivileged candidates were systematically less likely to be selected at baseline.
    </div>""", unsafe_allow_html=True)
with c2:
    # Heatmap accessibility note added below
    st.markdown("""<div class="ac-info-box">
    <strong>ThresholdOptimizer</strong> achieved the greatest SPD improvement, with Logistic Regression
    reaching a positive SPD (0.0091) — the unprivileged group slightly favoured post-mitigation.
    </div>""", unsafe_allow_html=True)

st.markdown("""<div class="ac-info-box">
♿ <strong>Accessibility note:</strong> The gender fairness metrics heatmap uses a red-green
colour scale. If you have colour vision deficiency, please refer to the numerical values displayed
in each cell directly. Red cells indicate negative fairness values (disadvantage to unprivileged
group), green cells indicate positive values (above benchmark).
</div>""", unsafe_allow_html=True)
