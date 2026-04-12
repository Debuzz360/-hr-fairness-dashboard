import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from theme import ARCTIC_CSS, PLOTLY_LAYOUT, INDIGO, RED, GREEN, AMBER, SLATE

st.set_page_config(page_title="Live Bias Audit", page_icon="🔍", layout="wide")
st.markdown(ARCTIC_CSS, unsafe_allow_html=True)

st.title("🔍 Live Bias Audit")
st.markdown("Upload one or two recruitment datasets to receive a full five-metric fairness audit. Upload both datasets to run a cross-dataset validation comparison.")
st.divider()

# ── Helper functions ───────────────────────────────────────────────────────────
def compute_spd(df, out, grp, priv):
    p = df[df[grp]==priv][out].mean()
    u = df[df[grp]!=priv][out].mean()
    return round(u - p, 4) if p is not None else None

def compute_dir(df, out, grp, priv):
    p = df[df[grp]==priv][out].mean()
    u = df[df[grp]!=priv][out].mean()
    return round(u / p, 4) if p and p > 0 else None

def compute_eod(df, out, pred, grp, priv):
    p_df = df[df[grp]==priv]; u_df = df[df[grp]!=priv]
    tp = p_df[p_df[out]==1][pred].mean() if len(p_df[p_df[out]==1]) > 0 else None
    tu = u_df[u_df[out]==1][pred].mean() if len(u_df[u_df[out]==1]) > 0 else None
    return round(tu - tp, 4) if tp is not None and tu is not None else None

def compute_ppv(df, out, pred, grp, priv):
    p_df = df[(df[grp]==priv) & (df[pred]==1)]
    u_df = df[(df[grp]!=priv) & (df[pred]==1)]
    pp = p_df[out].mean() if len(p_df) > 0 else None
    pu = u_df[out].mean() if len(u_df) > 0 else None
    return round(pu - pp, 4) if pp is not None and pu is not None else None

def compute_fpr(df, out, pred, grp, priv):
    p_df = df[df[grp]==priv]; u_df = df[df[grp]!=priv]
    fp = p_df[p_df[out]==0][pred].mean() if len(p_df[p_df[out]==0]) > 0 else None
    fu = u_df[u_df[out]==0][pred].mean() if len(u_df[u_df[out]==0]) > 0 else None
    return round(fu - fp, 4) if fp is not None and fu is not None else None

def full_audit(df, out, pred, grp, priv):
    res = {}
    res["SPD"] = compute_spd(df, out, grp, priv)
    res["DIR"] = compute_dir(df, out, grp, priv)
    if pred and pred != "None":
        res["EOD"]       = compute_eod(df, out, pred, grp, priv)
        res["PPV Parity"] = compute_ppv(df, out, pred, grp, priv)
        res["FPR Parity"] = compute_fpr(df, out, pred, grp, priv)
    return res

def flag_spd(v):
    if v is None: return "N/A"
    return "✅ Fair" if abs(v) <= 0.05 else ("⚠️ Moderate" if abs(v) <= 0.1 else "🚨 Biased")

def flag_dir(v):
    if v is None: return "N/A"
    return "✅ Compliant" if v >= 0.8 else ("⚠️ Near threshold" if v >= 0.7 else "🚨 Legal risk")

def flag_other(v):
    if v is None: return "N/A"
    return "✅ Fair" if abs(v) <= 0.05 else ("⚠️ Moderate" if abs(v) <= 0.1 else "🚨 Biased")

def display_metrics(res):
    cols = st.columns(len(res))
    for i, (m, v) in enumerate(res.items()):
        with cols[i]:
            val = f"{v:.4f}" if v is not None else "N/A"
            flag = flag_dir(v) if m == "DIR" else flag_spd(v) if m == "SPD" else flag_other(v)
            st.metric(m, val, delta=flag, delta_color="off",
                      help="DIR ≥ 0.8 required for UK legal compliance" if m == "DIR" else
                           "Ideal value: 0" )

def results_table(res):
    rows = []
    for m, v in res.items():
        flag = flag_dir(v) if m == "DIR" else flag_spd(v) if m == "SPD" else flag_other(v)
        rows.append({"Metric": m, "Value": f"{v:.4f}" if v is not None else "N/A", "Status": flag})
    return pd.DataFrame(rows)

# ── Mode selector ──────────────────────────────────────────────────────────────
mode = st.radio("Upload mode", ["Single dataset", "Two datasets (cross-dataset validation)"],
                horizontal=True)
st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# SINGLE DATASET MODE
# ══════════════════════════════════════════════════════════════════════════════
if mode == "Single dataset":
    uploaded = st.file_uploader("Upload your recruitment CSV", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)
        st.success(f"✅ Dataset loaded: {len(df):,} records, {df.shape[1]} columns")
        with st.expander("Preview data"):
            st.dataframe(df.head(), use_container_width=True)

        st.markdown("<div class='ac-section'>Configure Audit</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            outcome_col = st.selectbox("Outcome column (hire decision 0/1)", df.columns.tolist())
            pred_col    = st.selectbox("Prediction column (optional — enables EOD, PPV, FPR)",
                                       ["None"] + df.columns.tolist())
        with c2:
            group_col = st.selectbox("Protected attribute column", df.columns.tolist())
            priv_val  = st.selectbox("Privileged group value",
                                     df[group_col].dropna().unique().tolist())

        if st.button("▶ Run Fairness Audit", type="primary"):
            res = full_audit(df, outcome_col,
                             pred_col if pred_col != "None" else None,
                             group_col, priv_val)

            st.markdown("<div class='ac-section'>Audit Results</div>", unsafe_allow_html=True)
            display_metrics(res)
            st.divider()
            st.dataframe(results_table(res), use_container_width=True, hide_index=True)

            # Alerts
            if res.get("DIR") and res["DIR"] < 0.8:
                st.markdown("""<div class="ac-danger-box">🚨 <strong>Adverse Impact Detected:</strong>
                DIR below 0.8 — potential legal exposure under the UK Equality Act 2010.</div>""",
                unsafe_allow_html=True)
            if res.get("SPD") and abs(res["SPD"]) > 0.1:
                st.markdown("""<div class="ac-danger-box">🚨 <strong>Significant bias detected:</strong>
                SPD exceeds 0.1 threshold.</div>""", unsafe_allow_html=True)

            st.download_button("⬇️ Download Audit Report",
                results_table(res).to_csv(index=False).encode(),
                "bias_audit_report.csv", "text/csv")

        if pred_col == "None":
            st.info("ℹ️ Add a prediction column to unlock EOD, PPV Parity and FPR Parity metrics.")

    else:
        st.markdown("""<div class="ac-info-box">👆 Upload a CSV to begin.
        Must contain a hire outcome column (0/1) and at least one protected attribute column.</div>""",
        unsafe_allow_html=True)
        ex = pd.DataFrame({"Gender":[1,0,1,0],"SkillScore":[75,82,68,79],
                           "HireDecision":[1,1,0,1],"ModelPred":[1,1,0,1]})
        st.dataframe(ex, use_container_width=True, hide_index=True)
        st.caption("Gender: 1=privileged. HireDecision & ModelPred: 1=hired.")

# ══════════════════════════════════════════════════════════════════════════════
# TWO DATASET MODE
# ══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown("""<div class="ac-info-box">
    📊 <strong>Cross-Dataset Validation Mode:</strong> Upload two datasets to compare all five
    fairness metrics side by side. This replicates the cross-dataset validation methodology
    used in the dissertation (primary n=1,500 vs secondary n=225).
    </div>""", unsafe_allow_html=True)
    st.markdown("")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Primary Dataset")
        file1 = st.file_uploader("Upload primary dataset CSV", type=["csv"], key="ba_file1")
    with col2:
        st.markdown("#### Secondary Dataset")
        file2 = st.file_uploader("Upload secondary dataset CSV", type=["csv"], key="ba_file2")

    if file1 and file2:
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        st.success(f"✅ Primary: {len(df1):,} records | Secondary: {len(df2):,} records")

        with st.expander("Preview both datasets"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Primary**")
                st.dataframe(df1.head(5), use_container_width=True)
            with c2:
                st.markdown("**Secondary**")
                st.dataframe(df2.head(5), use_container_width=True)

        st.markdown("<div class='ac-section'>Configure Audit</div>", unsafe_allow_html=True)
        shared_cols = list(set(df1.columns) & set(df2.columns))

        c1, c2, c3 = st.columns(3)
        with c1: outcome_col = st.selectbox("Hire outcome column", shared_cols, key="ba_out")
        with c2:
            pred_col = st.selectbox("Prediction column (optional)",
                                    ["None"] + shared_cols, key="ba_pred")
        with c3: group_col = st.selectbox("Protected attribute", shared_cols, key="ba_grp")

        all_vals = list(set(list(df1[group_col].dropna().unique()) +
                            list(df2[group_col].dropna().unique())))
        priv_val = st.selectbox("Privileged group value", all_vals, key="ba_priv")

        if st.button("▶ Run Cross-Dataset Audit", type="primary"):
            pred = pred_col if pred_col != "None" else None
            r1 = full_audit(df1, outcome_col, pred, group_col, priv_val)
            r2 = full_audit(df2, outcome_col, pred, group_col, priv_val)

            st.markdown("<div class='ac-section'>Side-by-Side Results</div>", unsafe_allow_html=True)

            metrics = list(r1.keys())
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("##### Primary Dataset")
                for m in metrics:
                    v = r1[m]
                    flag = flag_dir(v) if m=="DIR" else flag_spd(v) if m=="SPD" else flag_other(v)
                    st.metric(m, f"{v:.4f}" if v is not None else "N/A",
                              delta=flag, delta_color="off")
            with c2:
                st.markdown("##### Secondary Dataset")
                for m in metrics:
                    v = r2[m]
                    flag = flag_dir(v) if m=="DIR" else flag_spd(v) if m=="SPD" else flag_other(v)
                    st.metric(m, f"{v:.4f}" if v is not None else "N/A",
                              delta=flag, delta_color="off")

            st.divider()

            # Comparison bar chart for all metrics
            st.markdown("<div class='ac-section'>Metric Comparison Chart</div>", unsafe_allow_html=True)

            layout = dict(PLOTLY_LAYOUT); layout.update(height=380, barmode="group")
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Primary", x=metrics,
                y=[r1[m] if r1[m] is not None else 0 for m in metrics],
                marker_color=INDIGO,
                text=[f"{r1[m]:.4f}" if r1[m] is not None else "N/A" for m in metrics],
                textposition="outside"))
            fig.add_trace(go.Bar(name="Secondary", x=metrics,
                y=[r2[m] if r2[m] is not None else 0 for m in metrics],
                marker_color=AMBER,
                text=[f"{r2[m]:.4f}" if r2[m] is not None else "N/A" for m in metrics],
                textposition="outside"))
            fig.add_hline(y=0, line_dash="dash", line_color=SLATE, line_width=1)
            fig.update_layout(**layout, yaxis_title="Metric Value")
            st.plotly_chart(fig, use_container_width=True)

            # Direction consistency
            st.markdown("<div class='ac-section'>Direction Consistency Check</div>",
                        unsafe_allow_html=True)
            rows = []
            for m in metrics:
                v1, v2 = r1[m], r2[m]
                if v1 is not None and v2 is not None:
                    if m == "DIR":
                        consistent = (v1 >= 0.8) == (v2 >= 0.8)
                        check = "DIR compliance (both above or both below 0.8)"
                    else:
                        consistent = (v1 < 0) == (v2 < 0)
                        check = f"{m} direction (both negative or both positive)"
                    rows.append({
                        "Check": check,
                        "Primary": f"{v1:.4f}",
                        "Secondary": f"{v2:.4f}",
                        "Consistent?": "✅ Yes — findings generalise" if consistent
                                       else "❌ No — direction differs"
                    })
            if rows:
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

            # Overall consistency verdict
            all_consistent = all("✅" in r["Consistent?"] for r in rows)
            if all_consistent:
                st.markdown("""<div class="ac-info-box">✅ <strong>All metrics consistent across both datasets.</strong>
                The fairness findings generalise beyond the primary dataset, supporting external validity.</div>""",
                unsafe_allow_html=True)
            else:
                st.markdown("""<div class="ac-warn-box">⚠️ <strong>Some metrics differ in direction between datasets.</strong>
                Review individual metric results for details.</div>""", unsafe_allow_html=True)

            # Download combined report
            combined = pd.DataFrame({
                "Metric": metrics,
                "Primary": [f"{r1[m]:.4f}" if r1[m] is not None else "N/A" for m in metrics],
                "Secondary": [f"{r2[m]:.4f}" if r2[m] is not None else "N/A" for m in metrics],
                "Primary Status": [flag_dir(r1[m]) if m=="DIR" else flag_spd(r1[m]) if m=="SPD"
                                   else flag_other(r1[m]) for m in metrics],
                "Secondary Status": [flag_dir(r2[m]) if m=="DIR" else flag_spd(r2[m]) if m=="SPD"
                                     else flag_other(r2[m]) for m in metrics],
            })
            st.download_button("⬇️ Download Cross-Dataset Audit Report",
                combined.to_csv(index=False).encode(),
                "cross_dataset_audit.csv", "text/csv")

    elif file1 or file2:
        st.warning("⚠️ Please upload both datasets to run the cross-dataset audit.")
    else:
        st.markdown("""<div class="ac-info-box">👆 Upload both CSV files above to begin
        the full five-metric cross-dataset fairness audit.</div>""", unsafe_allow_html=True)
