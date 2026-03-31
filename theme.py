ARCTIC_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }

    .stApp { background: #F1F5F9; }

    [data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    [data-testid="stSidebar"] * { color: #0F172A !important; }

    h1, h2, h3 { color: #0F172A !important; font-weight: 600 !important; }

    hr { border-color: #E2E8F0 !important; }

    [data-testid="metric-container"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 16px !important;
    }

    .stButton > button {
        background: #4F46E5 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        padding: 0.5rem 1.25rem !important;
    }
    .stButton > button:hover {
        background: #4338CA !important;
    }

    thead tr th {
        background: #F8FAFC !important;
        color: #4F46E5 !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #E2E8F0 !important;
    }

    .stSelectbox > div, .stMultiSelect > div {
        border-radius: 8px !important;
    }

    .stAlert {
        border-radius: 10px !important;
    }

    /* Arctic metric card */
    .ac-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 0.75rem;
    }
    .ac-card:hover {
        border-color: #C7D2FE;
        box-shadow: 0 4px 16px rgba(79,70,229,0.08);
    }
    .ac-val {
        font-size: 2rem;
        font-weight: 700;
        color: #4F46E5;
    }
    .ac-lbl {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.6px;
        text-transform: uppercase;
        color: #94A3B8;
        margin-top: 0.25rem;
    }
    .ac-badge-ok {
        display: inline-block;
        background: #DCFCE7;
        color: #166534;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    .ac-badge-warn {
        display: inline-block;
        background: #FEF9C3;
        color: #854D0E;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    .ac-badge-danger {
        display: inline-block;
        background: #FEE2E2;
        color: #991B1B;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    .ac-info-box {
        background: #EEF2FF;
        border-left: 4px solid #4F46E5;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        color: #1E1B4B;
    }
    .ac-warn-box {
        background: #FFFBEB;
        border-left: 4px solid #F59E0B;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        color: #78350F;
    }
    .ac-danger-box {
        background: #FFF1F2;
        border-left: 4px solid #EF4444;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        color: #881337;
    }
    .ac-hero {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        border-radius: 16px;
        padding: 2rem;
        color: white;
        margin-bottom: 1.5rem;
    }
    .ac-section {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0F172A;
        margin: 1.5rem 0 0.75rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #EEF2FF;
    }
</style>
"""

# Plotly Arctic Clean layout defaults
PLOTLY_LAYOUT = dict(
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#F8FAFC",
    font_color="#0F172A",
    font_family="Inter, sans-serif",
    title_font_color="#0F172A",
    title_font_size=15,
    legend=dict(bgcolor="#FFFFFF", bordercolor="#E2E8F0", borderwidth=1),
    xaxis=dict(gridcolor="#E2E8F0", linecolor="#E2E8F0", zerolinecolor="#E2E8F0"),
    yaxis=dict(gridcolor="#E2E8F0", linecolor="#E2E8F0", zerolinecolor="#E2E8F0"),
)

# Colour palette
INDIGO  = "#4F46E5"
INDIGO2 = "#7C3AED"
GREEN   = "#10B981"
RED     = "#EF4444"
AMBER   = "#F59E0B"
BLUE    = "#3B82F6"
SLATE   = "#64748B"
LIGHT   = "#F8FAFC"
