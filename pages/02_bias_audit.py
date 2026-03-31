import streamlit as st
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from theme import ARCTIC_CSS, PLOTLY_LAYOUT, INDIGO, GREEN, RED, AMBER, SLATE

st.set_page_config(page_title="Live Bias Audit", page_icon="🔍", layout="wide")
st.markdown(ARCTIC_CSS, unsafe_allow_html=True)

st.title("🔍 Live Bias Audit")
st.markdown("Upload any recruitment dataset (CSV) to receive a full five-metric fairness audit.")

def compute_spd(df, out, grp, priv):
    p = df[df[grp]==priv][out].mean()
    u = df[df[grp]!=priv][out].mean()
    return round(u-p, 4)

def compute_dir(df, out, grp, priv):
    p = df[df[grp]==priv][out].mean()
    u = df[df[grp]!=priv][out].mean()
    return round(u/p, 4) if p else np.nan

def compute_eod(df, out, pred, grp, priv):
    p_df = df[df[grp]==priv]; u_df = df[df[grp]!=priv]
    tp = p_df[p_df[out]==1][pred].mean() if len(p_df[p_df[out]==1])>0 else np.nan
    tu = u_df[u_df[out]==1][pred].mean() if len(u_df[u_df[out]==1])>0 else np.nan
    return round(tu-tp, 4) if not (pd.isna(tp) or pd.isna(tu)) else np.nan

def flag_spd(v):
    if pd.isna(v): return "⚠️ N/A"
    return "✅ Fair" if abs(v)<=0.05 else ("⚠️ Moderate" if abs(v)<=0.1 else "🚨 Biased")

def flag_dir(v):
    if pd.isna(v): return "⚠️ N/A"
    return "✅ Compliant" if v>=0.8 else ("⚠️ Near threshold" if v>=0.7 else "🚨 Legal risk")

uploaded = st.file_uploader("Upload your recruitment CSV", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
    st.success(f"Dataset loaded: {len(df):,} records, {df.shape[1]} columns")
    with st.expander("Preview data"):
        st.dataframe(df.head(), use_container_width=True)
    c1, c2 = st.columns(2)
    with c1:
        outcome_col = st.selectbox("Outcome column (0/1)", df.columns.tolist())
        pred_col    = st.selectbox("Prediction column (optional)", ["None"]+df.columns.tolist())
    with c2:
        group_col   = st.selectbox("Protected attribute column", df.columns.tolist())
        priv_val    = st.selectbox("Privileged group value", df[group_col].dropna().unique().tolist())
    if st.button("▶ Run Fairness Audit", type="primary"):
        res = {"SPD": compute_spd(df, outcome_col, group_col, priv_val),
               "DIR": compute_dir(df, outcome_col, group_col, priv_val)}
        if pred_col != "None":
            res["EOD"] = compute_eod(df, outcome_col, pred_col, group_col, priv_val)
        cols = st.columns(len(res))
        for i, (m, v) in enumerate(res.items()):
            with cols[i]:
                st.metric(m, f"{v:.4f}" if not pd.isna(v) else "N/A",
                          delta=flag_dir(v) if m=="DIR" else flag_spd(v), delta_color="off")
        rows = [{"Metric": m, "Value": f"{v:.4f}" if not pd.isna(v) else "N/A",
                 "Status": flag_dir(v) if m=="DIR" else flag_spd(v)} for m,v in res.items()]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        st.download_button("⬇️ Download Report", pd.DataFrame(rows).to_csv(index=False).encode(),
                           "audit_report.csv", "text/csv")
else:
    st.markdown("""<div class="ac-info-box">👆 Upload a CSV with a hire outcome column (0/1) and at least one protected attribute column.</div>""", unsafe_allow_html=True)
    ex = pd.DataFrame({"Gender":[1,0,1,0],"SkillScore":[75,82,68,79],"HireDecision":[1,1,0,1],"ModelPred":[1,1,0,1]})
    st.dataframe(ex, use_container_width=True, hide_index=True)
    st.caption("Gender: 1=privileged. HireDecision & ModelPred: 1=hired.")
