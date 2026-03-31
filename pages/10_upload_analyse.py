import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from theme import ARCTIC_CSS, PLOTLY_LAYOUT, INDIGO, RED, GREEN, AMBER

st.set_page_config(page_title="Upload & Analyse", page_icon="📤", layout="wide")
st.markdown(ARCTIC_CSS, unsafe_allow_html=True)
st.title("📤 Upload & Analyse")
st.markdown("Upload your own recruitment dataset and receive an instant fairness analysis.")

uploaded = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded:
    try:
        df = pd.read_csv(uploaded)
        st.success(f"✅ Loaded {len(df):,} records — {df.shape[1]} columns")
        with st.expander("Data Preview", expanded=True):
            st.dataframe(df.head(10), use_container_width=True)

        c1,c2,c3,c4 = st.columns(4)
        with c1: st.metric("Records", f"{len(df):,}")
        with c2: st.metric("Hire Rate", f"{df['HiringDecision'].mean():.1%}" if "HiringDecision" in df.columns else "N/A")
        with c3: st.metric("Male %", f"{(df['Gender']==1).sum()/len(df):.1%}" if "Gender" in df.columns else "N/A")
        with c4: st.metric("Avg Age", f"{df['Age'].mean():.0f}" if "Age" in df.columns else "N/A")

        if "Gender" in df.columns and "HiringDecision" in df.columns:
            st.markdown("<div class='ac-section'>Quick Fairness Analysis</div>", unsafe_allow_html=True)
            f = df[df["Gender"]==0]["HiringDecision"].mean() if 0 in df["Gender"].values else None
            m = df[df["Gender"]==1]["HiringDecision"].mean() if 1 in df["Gender"].values else None
            if f and m and m > 0:
                spd = f-m; dir_r = f/m
                ca, cb = st.columns(2)
                with ca:
                    st.metric("Gender SPD", f"{spd:+.4f}")
                    if spd < -0.05:
                        st.markdown("""<div class="ac-warn-box">⚠️ Gender disparity exceeds threshold</div>""", unsafe_allow_html=True)
                    else:
                        st.markdown("""<div class="ac-info-box">✅ Gender parity within range</div>""", unsafe_allow_html=True)
                with cb:
                    st.metric("Disparate Impact Ratio", f"{dir_r:.4f}")
                    if dir_r < 0.8:
                        st.markdown("""<div class="ac-danger-box">🚨 Adverse impact — DIR below 0.8 legal threshold</div>""", unsafe_allow_html=True)
                    else:
                        st.markdown("""<div class="ac-info-box">✅ DIR within legal range</div>""", unsafe_allow_html=True)

        st.markdown("<div class='ac-section'>Feature Distribution</div>", unsafe_allow_html=True)
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            feat = st.selectbox("Select feature", num_cols)
            color_col = "HiringDecision" if "HiringDecision" in df.columns else None
            layout = dict(PLOTLY_LAYOUT); layout.update(height=340)
            fig = px.histogram(df, x=feat, color=color_col, barmode="overlay",
                               color_discrete_map={0:RED,1:GREEN} if color_col else None,
                               template="plotly_white")
            fig.update_layout(**layout)
            st.plotly_chart(fig, use_container_width=True)

        st.download_button("⬇️ Download Analysed Data",
            df.to_csv(index=False).encode(), "analysed_data.csv", "text/csv")

    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.markdown("""<div class="ac-info-box">👆 Upload a CSV to begin. Must contain a HiringDecision column (0/1).</div>""", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({"Age":[26,39,48],"Gender":[1,1,0],"EducationLevel":[2,4,2],
                                "HiringDecision":[1,1,0]}), use_container_width=True, hide_index=True)
    st.caption("Gender: 1=Male (privileged), 0=Female. HiringDecision: 1=hired, 0=not hired.")
