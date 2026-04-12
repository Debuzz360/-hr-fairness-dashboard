import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from theme import ARCTIC_CSS, PLOTLY_LAYOUT, INDIGO, GREEN, RED, AMBER

st.set_page_config(
    page_title="FairHire Audit Tool",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(ARCTIC_CSS, unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ac-hero">
    <div style="font-size:2rem; font-weight:700;">⚖️ FairHire Audit Tool</div>
    <div style="font-size:1rem; margin-top:0.5rem; opacity:0.9;">
        Reducing Bias in ML Algorithms for HR Recruitment<br>
        <span style="font-weight:600;">MSc Business Analytics & Technology — University of Greater Manchester</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
cards = [
    ("1,500", "Primary Dataset", "ok", "Records"),
    ("225",   "Secondary Dataset", "ok", "Records"),
    ("3",     "ML Classifiers", "ok", "LR · RF · XGB"),
    ("5",     "Fairness Metrics", "ok", "SPD·DIR·EOD·PPV·FPR"),
    ("86.0%", "Best F1 Score", "ok", "XGBoost"),
]
for col, (val, lbl, status, sub) in zip([c1,c2,c3,c4,c5], cards):
    with col:
        st.markdown(f"""
        <div class="ac-card">
            <div class="ac-val">{val}</div>
            <div class="ac-lbl">{lbl}</div>
            <div style="font-size:0.75rem; color:#64748B; margin-top:4px;">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='ac-section'>Risk Assessment Dashboard</div>", unsafe_allow_html=True)

# ── Gauge + Alerts ────────────────────────────────────────────────────────────
col_g, col_a = st.columns([2, 1])

with col_g:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=72,
        title={"text": "Overall Fairness Risk Score", "font": {"size": 14, "color": "#0F172A"}},
        number={"font": {"color": "#4F46E5", "size": 42}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#94A3B8",
                     "tickfont": {"color": "#64748B"}},
            "bar": {"color": INDIGO},
            "bgcolor": "#F8FAFC",
            "borderwidth": 1,
            "bordercolor": "#E2E8F0",
            "steps": [
                {"range": [0,  40], "color": "#DCFCE7"},
                {"range": [40, 70], "color": "#FEF9C3"},
                {"range": [70,100], "color": "#FEE2E2"},
            ],
            "threshold": {
                "line": {"color": RED, "width": 3},
                "thickness": 0.75,
                "value": 80
            }
        }
    ))
    layout = dict(PLOTLY_LAYOUT)
    layout.update(title='', height=280, margin=dict(l=30, r=30, t=50, b=10))
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Score above 70 = high risk. Red threshold at 80 = critical intervention required.")

with col_a:
    st.markdown("<div class='ac-section'>Live Alerts</div>", unsafe_allow_html=True)
    alerts = [
        ("danger",  "Education bias: DIR = 0.536 — below 0.8 legal threshold"),
        ("warn",    "RecruitmentStrategy_1 identified as dominant proxy feature"),
        ("ok",      "XGBoost performance stable: F1 = 86.0%"),
    ]
    icons = {"danger": "🔴", "warn": "🟡", "ok": "🟢"}
    box_cls = {"danger": "ac-danger-box", "warn": "ac-warn-box", "ok": "ac-info-box"}
    for level, msg in alerts:
        st.markdown(f"""
        <div class="{box_cls[level]}">
            {icons[level]} <span style="font-size:0.85rem;">{msg}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='ac-section'>About This Tool</div>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    This application accompanies a dissertation investigating **algorithmic bias in HR recruitment
    ML systems** within UK financial services. It provides:

    - 📊 Interactive visualisation of dissertation fairness audit results
    - 🔍 Live bias audit — upload any recruitment CSV and receive a full fairness report
    - 🤖 SHAP proxy analysis — understand which features drive biased predictions
    - ⚖️ Mitigation simulator — compare Reweighting, ExponentiatedGradient, ThresholdOptimizer
    - 🔄 Cross-dataset validation — primary (n=1,500) vs secondary (n=225) findings
    - 📊 Compare strategies, 🔮 Predict & assess, 📈 Trend analysis
    - 📤 Upload & analyse, 📄 Generate downloadable reports
    """)
with col2:
    st.markdown("""
    **Research Questions**

    **RQ1** — What fairness disparities exist across protected groups?

    **RQ2** — Which features act as proxies?

    **RQ3** — How do mitigations affect fairness-accuracy trade-offs?

    **RQ4** — Do findings generalise across datasets?

    **RQ5** — What socio-technical framework can reduce bias?
    """)

st.markdown("---")
st.markdown("<p style='text-align:center; color:#94A3B8; font-size:0.8rem;'>MSc Dissertation · University of Greater Manchester · 2025–2026</p>", unsafe_allow_html=True)
