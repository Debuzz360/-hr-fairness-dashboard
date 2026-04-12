import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from theme import ARCTIC_CSS, PLOTLY_LAYOUT, INDIGO, RED, GREEN, AMBER, SLATE

st.set_page_config(page_title="Upload & Analyse", page_icon="📤", layout="wide")
st.markdown(ARCTIC_CSS, unsafe_allow_html=True)

st.title("📤 Upload & Analyse")
st.markdown("Upload one or two recruitment datasets and receive an instant fairness analysis. Upload both to replicate the cross-dataset validation methodology used in this dissertation.")
st.divider()

# ── Helper functions ───────────────────────────────────────────────────────────
def compute_metrics(df, outcome_col, group_col, priv_val):
    results = {}
    results["total"] = len(df)
    results["hire_rate"] = df[outcome_col].mean()
    priv = df[df[group_col] == priv_val][outcome_col].mean()
    unpriv = df[df[group_col] != priv_val][outcome_col].mean()
    results["priv_rate"] = priv
    results["unpriv_rate"] = unpriv
    results["spd"] = round(unpriv - priv, 4) if priv is not None else None
    results["dir"] = round(unpriv / priv, 4) if priv and priv > 0 else None
    return results

def flag_spd(v):
    if v is None: return "N/A"
    return "✅ Fair" if abs(v) <= 0.05 else ("⚠️ Moderate" if abs(v) <= 0.1 else "🚨 Significant bias")

def flag_dir(v):
    if v is None: return "N/A"
    return "✅ Compliant" if v >= 0.8 else ("⚠️ Near threshold" if v >= 0.7 else "🚨 Legal risk")

# ── Upload mode selector ───────────────────────────────────────────────────────
mode = st.radio("Upload mode", ["Single dataset", "Two datasets (cross-dataset validation)"],
                horizontal=True)
st.divider()

if mode == "Single dataset":
    uploaded = st.file_uploader("Upload your recruitment CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        st.success(f"✅ Loaded {len(df):,} records — {df.shape[1]} columns")

        with st.expander("Data Preview"):
            st.dataframe(df.head(10), use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            outcome_col = st.selectbox("Hire outcome column (0/1)", df.columns.tolist())
        with c2:
            group_col = st.selectbox("Protected attribute column", df.columns.tolist())

        if group_col:
            priv_val = st.selectbox("Privileged group value", df[group_col].dropna().unique().tolist())

        if st.button("▶ Run Analysis", type="primary"):
            res = compute_metrics(df, outcome_col, group_col, priv_val)

            c1, c2, c3, c4 = st.columns(4)
            with c1: st.metric("Records", f"{res['total']:,}")
            with c2: st.metric("Hire Rate", f"{res['hire_rate']:.1%}")
            with c3: st.metric("SPD", f"{res['spd']:.4f}", delta=flag_spd(res['spd']), delta_color="off")
            with c4: st.metric("DIR", f"{res['dir']:.4f}", delta=flag_dir(res['dir']), delta_color="off")

            if res['dir'] < 0.8:
                st.markdown("""<div class="ac-danger-box">🚨 <strong>Adverse Impact Detected:</strong> DIR below 0.8 legal threshold (UK Equality Act 2010).</div>""", unsafe_allow_html=True)
            elif res['spd'] is not None and abs(res['spd']) > 0.05:
                st.markdown("""<div class="ac-warn-box">⚠️ <strong>Gender disparity detected:</strong> SPD exceeds the 0.05 fairness threshold.</div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class="ac-info-box">✅ <strong>Within acceptable range.</strong> No adverse impact detected on this metric.</div>""", unsafe_allow_html=True)

            # Feature distribution
            st.markdown("<div class='ac-section'>Feature Distribution</div>", unsafe_allow_html=True)
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if num_cols:
                feat = st.selectbox("Select feature to visualise", num_cols)
                layout = dict(PLOTLY_LAYOUT); layout.update(height=320)
                fig = px.histogram(df, x=feat,
                    color=outcome_col if outcome_col in df.columns else None,
                    barmode="overlay",
                    color_discrete_map={0: RED, 1: GREEN},
                    template="plotly_white")
                fig.update_layout(**layout)
                st.plotly_chart(fig, use_container_width=True)

            # Download
            report = pd.DataFrame({
                "Metric": ["Records", "Hire Rate", "Privileged Rate", "Unprivileged Rate", "SPD", "DIR"],
                "Value": [res['total'], f"{res['hire_rate']:.4f}", f"{res['priv_rate']:.4f}",
                          f"{res['unpriv_rate']:.4f}", res['spd'], res['dir']],
                "Status": ["", "", "", "", flag_spd(res['spd']), flag_dir(res['dir'])]
            })
            st.download_button("⬇️ Download Analysis Report",
                report.to_csv(index=False).encode(), "fairness_report.csv", "text/csv")
    else:
        st.markdown("""<div class="ac-info-box">👆 Upload a CSV with a hiring outcome column (0/1) and at least one protected attribute column.</div>""", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({"Age":[26,39,48],"Gender":[1,1,0],
            "EducationLevel":[2,4,2],"HiringDecision":[1,1,0]}),
            use_container_width=True, hide_index=True)
        st.caption("Gender: 1=Male (privileged), 0=Female. HiringDecision: 1=hired, 0=not hired.")

# ── TWO DATASET MODE ───────────────────────────────────────────────────────────
else:
    st.markdown("""<div class="ac-info-box">
    📊 <strong>Cross-Dataset Validation Mode:</strong> Upload two datasets to compare fairness metrics side by side.
    This replicates the cross-dataset validation methodology used in the dissertation
    (primary n=1,500 vs secondary n=225).
    </div>""", unsafe_allow_html=True)
    st.markdown("")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Primary Dataset")
        file1 = st.file_uploader("Upload primary dataset CSV", type=["csv"], key="file1")
    with col2:
        st.markdown("#### Secondary Dataset")
        file2 = st.file_uploader("Upload secondary dataset CSV", type=["csv"], key="file2")

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

        st.markdown("<div class='ac-section'>Configure Analysis</div>", unsafe_allow_html=True)
        shared_cols = list(set(df1.columns) & set(df2.columns))

        c1, c2, c3 = st.columns(3)
        with c1: outcome_col = st.selectbox("Hire outcome column", shared_cols)
        with c2: group_col   = st.selectbox("Protected attribute", shared_cols)
        with c3:
            all_vals = list(set(df1[group_col].dropna().unique()) |
                            set(df2[group_col].dropna().unique()))
            priv_val = st.selectbox("Privileged group value", all_vals)

        if st.button("▶ Run Cross-Dataset Analysis", type="primary"):
            r1 = compute_metrics(df1, outcome_col, group_col, priv_val)
            r2 = compute_metrics(df2, outcome_col, group_col, priv_val)

            st.markdown("<div class='ac-section'>Side-by-Side Comparison</div>", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("##### Primary Dataset")
                st.metric("Records", f"{r1['total']:,}")
                st.metric("Hire Rate", f"{r1['hire_rate']:.1%}")
                st.metric("SPD", f"{r1['spd']:.4f}", delta=flag_spd(r1['spd']), delta_color="off")
                st.metric("DIR", f"{r1['dir']:.4f}", delta=flag_dir(r1['dir']), delta_color="off")
            with c2:
                st.markdown("##### Secondary Dataset")
                st.metric("Records", f"{r2['total']:,}")
                st.metric("Hire Rate", f"{r2['hire_rate']:.1%}")
                st.metric("SPD", f"{r2['spd']:.4f}", delta=flag_spd(r2['spd']), delta_color="off")
                st.metric("DIR", f"{r2['dir']:.4f}", delta=flag_dir(r2['dir']), delta_color="off")

            st.divider()

            # SPD comparison chart
            st.markdown("<div class='ac-section'>SPD Comparison Chart</div>", unsafe_allow_html=True)
            fig_spd = go.Figure()
            fig_spd.add_trace(go.Bar(name="Primary", x=["SPD"], y=[r1['spd']],
                marker_color=INDIGO, text=[f"{r1['spd']:.4f}"], textposition="outside"))
            fig_spd.add_trace(go.Bar(name="Secondary", x=["SPD"], y=[r2['spd']],
                marker_color=AMBER, text=[f"{r2['spd']:.4f}"], textposition="outside"))
            fig_spd.add_hline(y=0, line_dash="dash", line_color=SLATE, line_width=1)
            fig_spd.add_hline(y=-0.05, line_dash="dot", line_color=RED,
                              annotation_text="Fairness threshold", annotation_font_color=RED)
            layout = dict(PLOTLY_LAYOUT); layout.update(height=320, barmode="group",
                yaxis_title="SPD", xaxis_title="")
            fig_spd.update_layout(**layout)
            st.plotly_chart(fig_spd, use_container_width=True)

            # DIR comparison chart
            st.markdown("<div class='ac-section'>DIR Comparison Chart</div>", unsafe_allow_html=True)
            fig_dir = go.Figure()
            fig_dir.add_trace(go.Bar(name="Primary", x=["DIR"], y=[r1['dir']],
                marker_color=INDIGO, text=[f"{r1['dir']:.4f}"], textposition="outside"))
            fig_dir.add_trace(go.Bar(name="Secondary", x=["DIR"], y=[r2['dir']],
                marker_color=AMBER, text=[f"{r2['dir']:.4f}"], textposition="outside"))
            fig_dir.add_hline(y=0.8, line_dash="dot", line_color=RED,
                              annotation_text="Legal threshold (0.8)", annotation_font_color=RED)
            layout2 = dict(PLOTLY_LAYOUT); layout2.update(height=320, barmode="group",
                yaxis_title="DIR", yaxis_range=[0, 1.1], xaxis_title="")
            fig_dir.update_layout(**layout2)
            st.plotly_chart(fig_dir, use_container_width=True)

            # Direction consistency check
            st.markdown("<div class='ac-section'>Direction Consistency Check</div>", unsafe_allow_html=True)
            spd_consistent = (r1['spd'] < 0 and r2['spd'] < 0) or (r1['spd'] > 0 and r2['spd'] > 0)
            dir_consistent = (r1['dir'] < 0.8 and r2['dir'] < 0.8) or (r1['dir'] >= 0.8 and r2['dir'] >= 0.8)

            consistency_df = pd.DataFrame({
                "Check": ["SPD direction (both negative or both positive)",
                          "DIR compliance (both above or both below 0.8)"],
                "Primary": [f"{r1['spd']:.4f}", f"{r1['dir']:.4f}"],
                "Secondary": [f"{r2['spd']:.4f}", f"{r2['dir']:.4f}"],
                "Consistent?": [
                    "✅ Yes — findings generalise" if spd_consistent else "❌ No — direction differs",
                    "✅ Yes — findings generalise" if dir_consistent else "❌ No — compliance differs"
                ]
            })
            st.dataframe(consistency_df, use_container_width=True, hide_index=True)

            if spd_consistent:
                st.markdown("""<div class="ac-info-box">✅ <strong>SPD direction is consistent across both datasets.</strong>
                This supports the external validity of the fairness findings.</div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class="ac-warn-box">⚠️ <strong>SPD direction differs between datasets.</strong>
                This suggests the bias pattern may be dataset-specific.</div>""", unsafe_allow_html=True)

            # Download combined report
            report = pd.DataFrame({
                "Metric": ["Records", "Hire Rate", "SPD", "DIR", "SPD Status", "DIR Status"],
                "Primary": [r1['total'], f"{r1['hire_rate']:.4f}", r1['spd'], r1['dir'],
                            flag_spd(r1['spd']), flag_dir(r1['dir'])],
                "Secondary": [r2['total'], f"{r2['hire_rate']:.4f}", r2['spd'], r2['dir'],
                              flag_spd(r2['spd']), flag_dir(r2['dir'])]
            })
            st.download_button("⬇️ Download Cross-Dataset Report",
                report.to_csv(index=False).encode(),
                "cross_dataset_report.csv", "text/csv")

    elif file1 or file2:
        st.warning("⚠️ Please upload both datasets to run the cross-dataset comparison.")
    else:
        st.markdown("""<div class="ac-info-box">👆 Upload both CSV files above to begin the cross-dataset validation analysis.</div>""", unsafe_allow_html=True)
