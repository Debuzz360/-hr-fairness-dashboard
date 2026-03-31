import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from theme import ARCTIC_CSS, PLOTLY_LAYOUT, INDIGO, GREEN, RED, AMBER, SLATE

st.set_page_config(page_title="SHAP Analysis", page_icon="🤖", layout="wide")
st.markdown(ARCTIC_CSS, unsafe_allow_html=True)
st.title("🤖 SHAP Proxy Feature Analysis")

SHAP_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "shap_values.csv")

@st.cache_data
def load():
    if os.path.exists(SHAP_PATH):
        return pd.read_csv(SHAP_PATH)
    return pd.DataFrame({
        "Feature":      ["RecruitmentStrategy_1","SkillScore","PersonalityScore","InterviewScore","ExperienceYears","EducationLevel","Age","Gender"],
        "LR_SHAP":      [1.022,0.720,0.580,0.430,0.310,0.210,0.120,0.063],
        "RF_SHAP":      [0.160,0.070,0.055,0.042,0.031,0.021,0.012,0.006],
        "XGB_SHAP":     [1.821,0.893,0.712,0.534,0.389,0.289,0.145,0.072],
        "Average_SHAP": [1.001,0.561,0.449,0.335,0.243,0.173,0.092,0.047]
    })

df = load()
if not os.path.exists(SHAP_PATH):
    st.warning("⚠️ Using placeholder data — place shap_values.csv in data/ folder.")

PROXY = ["RecruitmentStrategy_1","EducationLevel","Age","Gender","Race"]

model_col = st.selectbox("Select model", ["Average_SHAP","LR_SHAP","RF_SHAP","XGB_SHAP"],
    format_func=lambda x: {"Average_SHAP":"Average (all models)","LR_SHAP":"Logistic Regression",
                            "RF_SHAP":"Random Forest","XGB_SHAP":"XGBoost"}[x])

sorted_df = df.sort_values(model_col, ascending=True).reset_index(drop=True)
colours = [RED if f in PROXY else INDIGO for f in sorted_df["Feature"]]

layout = dict(PLOTLY_LAYOUT)
layout.update(height=max(380, len(sorted_df)*42), margin=dict(l=20,r=60,t=20,b=20), showlegend=False)

fig = go.Figure(go.Bar(
    x=sorted_df[model_col], y=sorted_df["Feature"], orientation="h",
    marker_color=colours,
    text=[f"{v:.4f}" for v in sorted_df[model_col]],
    textposition="outside"
))
fig.update_layout(**layout)
st.plotly_chart(fig, use_container_width=True)

c1, c2 = st.columns(2)
with c1: st.markdown("🔵 **Indigo** — job-relevant feature")
with c2: st.markdown("🔴 **Red** — potential proxy feature")

st.markdown("<div class='ac-section'>Key Finding</div>", unsafe_allow_html=True)
top = df.loc[df["Average_SHAP"].idxmax()]
second = df["Average_SHAP"].nlargest(2).iloc[1]
st.markdown(f"""<div class="ac-danger-box">
<strong>{top['Feature']}</strong> has the highest average SHAP value ({top['Average_SHAP']:.4f}) —
{top['Average_SHAP']/second:.1f}× greater than the next feature ({second:.4f}).
A recruitment channel variable dominates the model, outweighing all job-relevant predictors.
This embeds <strong>indirect discrimination</strong> if sourcing channels are demographically skewed.
</div>""", unsafe_allow_html=True)

st.markdown("<div class='ac-section'>All Models Comparison</div>", unsafe_allow_html=True)
top8 = df.nlargest(8, "Average_SHAP").sort_values("Average_SHAP", ascending=True)
fig2 = go.Figure()
for col, name, colour in [("LR_SHAP","Logistic Regression",INDIGO),
                           ("RF_SHAP","Random Forest",GREEN),
                           ("XGB_SHAP","XGBoost",AMBER)]:
    fig2.add_trace(go.Bar(x=top8[col], y=top8["Feature"], orientation="h", name=name, marker_color=colour))
layout2 = dict(PLOTLY_LAYOUT)
layout2.update(barmode="group", height=380)
fig2.update_layout(**layout2)
st.plotly_chart(fig2, use_container_width=True)

with st.expander("Full SHAP Table"):
    d = df.sort_values("Average_SHAP", ascending=False).copy()
    for c in ["LR_SHAP","RF_SHAP","XGB_SHAP","Average_SHAP"]:
        d[c] = d[c].apply(lambda x: f"{float(x):.4f}")
    d["Proxy Risk"] = d["Feature"].apply(lambda x: "⚠️ Yes" if x in PROXY else "✅ No")
    st.dataframe(d, use_container_width=True, hide_index=True)

with st.expander("Technical Note: SHAP 3D Array Fix (Random Forest)"):
    st.markdown("Random Forest SHAP returned a 3D array `(n_samples, n_features, n_classes)`. "
                "Resolved by extracting `shap_values[:, :, 1]` for the positive class slice. "
                "This is standard SHAP `TreeExplainer` practice.")
