from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st




APP_NAME = "Data Analysis Toolkit"
MAIN_PAGE = "app.py"

LOGO_CANDIDATES = [
    Path("assets/logo.png"),
    Path(r"C:\Users\JOEL\Downloads\logo.png"),
]

NAVIGATION = [
    ("Main", MAIN_PAGE, ":material/home:", "Project overview and navigation guide."),
    ("Data Upload", "pages/1_Data_Upload.py", ":material/upload_file:", "Load CSV, Excel, or sample data."),
    ("Data Cleaning", "pages/2_Data_Cleaning.py", ":material/cleaning_services:", "Handle missing values, duplicates, and numeric conversion."),
    ("Descriptive Statistics", "pages/3_Descriptive_Statistics.py", ":material/query_stats:", "Summaries, correlations, outliers, and recommendations."),
    ("Visualizations", "pages/4_Visualizations.py", ":material/insert_chart:", "Histograms, boxplots, scatter plots, heatmaps, and Q-Q plots."),
    ("Distributions", "pages/5_Distributions.py", ":material/functions:", "Normal, binomial, poisson, PDF, CDF, PMF, and fitting."),
    ("Normality", "pages/6_Normality.py", ":material/monitoring:", "Shapiro-Wilk, Q-Q plot, and fitted normal curve."),
    ("Parametric Tests", "pages/7_Parametric_Tests.py", ":material/science:", "t-tests, z-tests, chi-square, correlation, and regression significance."),
    ("Nonparametric Tests", "pages/8_Nonparametric_Tests.py", ":material/bar_chart:", "Mann-Whitney, Wilcoxon, Kruskal-Wallis, and Friedman."),
    ("ANOVA", "pages/9_ANOVA.py", ":material/dataset:", "One-way and two-way ANOVA."),
    ("Correlation Regression", "pages/10_Correlation_Regression.py", ":material/timeline:", "Association and linear modeling."),
    ("CLT Simulator", "pages/11_CLT_Simulator.py", ":material/model_training:", "Central Limit Theorem sampling simulation."),
    ("Report", "pages/12_Report.py", ":material/picture_as_pdf:", "PDF reports with analyses and plots."),
]

NAVIGATION_GROUPS = {
    "Main": ["Main"],
    "Data": ["Data Upload", "Data Cleaning"],
    "Statistics": ["Descriptive Statistics", "Correlation Regression"],
    "Visualizations": ["Visualizations", "Normality"],
    "Distributions": ["Distributions", "CLT Simulator"],
    "Tests": ["Parametric Tests", "Nonparametric Tests", "ANOVA"],
    "Reports": ["Report"],
}


def get_logo_data_uri() -> str | None:
    for path in LOGO_CANDIDATES:
        if path.exists():
            encoded = base64.b64encode(path.read_bytes()).decode("ascii")
            return f"data:image/png;base64,{encoded}"
    return None


def apply_global_theme() -> None:
    st.markdown(
        """
        <style>
        /* ============================================================
           IMPORTS
        ============================================================ */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

        /* ============================================================
           DESIGN TOKENS
        ============================================================ */
        :root {
            --bg-base:        #05080f;
            --bg-deep:        #080d18;
            --surface-0:      #0c1120;
            --surface-1:      #111827;
            --surface-2:      #161f32;
            --surface-3:      #1e2a40;
            --surface-glass:  rgba(13, 18, 32, 0.72);

            --text:           #edf2fb;
            --text-dim:       #8a97b0;
            --text-faint:     #4a5568;

            --border:         rgba(99, 130, 201, 0.15);
            --border-bright:  rgba(99, 179, 237, 0.35);

            /* Accent palette */
            --gold:           #f6c90e;
            --gold-dim:       rgba(246, 201, 14, 0.15);
            --gold-glow:      rgba(246, 201, 14, 0.35);
            --amber:          #f59e0b;
            --blue-light:     #60a5fa;
            --blue-mid:       #3b82f6;
            --blue-deep:      #1d4ed8;
            --indigo:         #6366f1;
            --violet:         #7c3aed;
            --teal:           #14b8a6;
            --emerald:        #10b981;
            --rose:           #f43f5e;

            /* Semantic */
            --accent-primary:   var(--gold);
            --accent-secondary: var(--blue-light);
            --accent-tertiary:  var(--teal);

            /* Sidebar */
            --sidebar-bg:     #060a14;
            --sidebar-border: rgba(246, 201, 14, 0.12);

            /* Radii */
            --r-sm:  6px;
            --r-md:  10px;
            --r-lg:  16px;
            --r-xl:  22px;

            /* Shadows */
            --shadow-sm:  0 2px 8px rgba(0,0,0,0.35);
            --shadow-md:  0 8px 32px rgba(0,0,0,0.45);
            --shadow-lg:  0 20px 64px rgba(0,0,0,0.55);
            --shadow-gold: 0 0 40px rgba(246,201,14,0.18);

            /* Transitions */
            --t-fast:   0.15s ease;
            --t-base:   0.25s ease;
            --t-slow:   0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }

        /* ============================================================
           GLOBAL RESET & BASE
        ============================================================ */
        *, *::before, *::after { box-sizing: border-box; }

        html, body,
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"],
        .stApp {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            color: var(--text);
            background: var(--bg-base);
        }

        /* Animated background */
        [data-testid="stAppViewContainer"]::before {
            content: '';
            position: fixed;
            inset: 0;
            z-index: -1;
            background:
                radial-gradient(ellipse 80% 50% at 90% -10%, rgba(246,201,14,0.07) 0%, transparent 55%),
                radial-gradient(ellipse 60% 40% at 10% 100%, rgba(99,102,241,0.08) 0%, transparent 50%),
                radial-gradient(ellipse 50% 60% at 50% 50%, rgba(20,184,166,0.04) 0%, transparent 60%),
                linear-gradient(160deg, #05080f 0%, #080d18 40%, #0a1020 70%, #05080f 100%);
            animation: bg-drift 18s ease-in-out infinite alternate;
        }

        @keyframes bg-drift {
            0%   { opacity: 1; filter: hue-rotate(0deg); }
            50%  { opacity: 0.92; filter: hue-rotate(8deg); }
            100% { opacity: 1; filter: hue-rotate(0deg); }
        }

        [data-testid="stHeader"] { background: transparent !important; }

        /* ============================================================
           MAIN CONTENT AREA
        ============================================================ */
        .main .block-container {
            max-width: 1200px;
            padding-top: 2.5rem;
            padding-bottom: 5rem;
            animation: page-enter 0.45s var(--t-slow) both;
        }

        @keyframes page-enter {
            from { opacity: 0; transform: translateY(18px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        /* ============================================================
           TYPOGRAPHY
        ============================================================ */
        h1 {
            font-size: clamp(1.6rem, 3vw, 2.4rem);
            font-weight: 800;
            letter-spacing: -0.02em;
            color: var(--text);
            line-height: 1.15;
            margin-bottom: 0.25rem;

            /* Gold left-border accent */
            padding-left: 1rem;
            border-left: 3px solid var(--gold);
        }

        h2 {
            font-size: clamp(1.15rem, 2vw, 1.5rem);
            font-weight: 700;
            letter-spacing: -0.01em;
            color: var(--text);
            margin-top: 2rem;
        }

        h3 {
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text-dim);
        }

        p, li { line-height: 1.7; }

        /* Caption / small text */
        .stCaption, small, [data-testid="stCaptionContainer"] p {
            color: var(--text-dim) !important;
            font-size: 0.82rem;
        }

        code, pre, .stCode {
            font-family: 'JetBrains Mono', monospace;
        }

        /* ============================================================
           SIDEBAR
        ============================================================ */
        [data-testid="stSidebarNav"] { display: none; }

        [data-testid="stSidebar"] {
            background: var(--sidebar-bg) !important;
            border-right: 1px solid var(--sidebar-border) !important;
            box-shadow: 4px 0 32px rgba(0,0,0,0.6);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 0.55rem;
        }

        [data-testid="stSidebar"] * { color: var(--text) !important; }

        /* Sidebar scroll — clean thin scrollbar */
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            overflow-y: auto;
            scrollbar-width: thin;
            scrollbar-color: rgba(246, 201, 14, 0.18) transparent;
        }

        [data-testid="stSidebar"] [data-testid="stSidebarContent"]::-webkit-scrollbar {
            width: 3px;
        }

        [data-testid="stSidebar"] [data-testid="stSidebarContent"]::-webkit-scrollbar-track {
            background: transparent;
        }

        [data-testid="stSidebar"] [data-testid="stSidebarContent"]::-webkit-scrollbar-thumb {
            background: rgba(246, 201, 14, 0.22);
            border-radius: 999px;
        }

        [data-testid="stSidebar"] [data-testid="stSidebarContent"]::-webkit-scrollbar-thumb:hover {
            background: rgba(246, 201, 14, 0.45);
        }

        /* Page links inside sidebar */
        [data-testid="stSidebar"] .stPageLink a {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            background: transparent;
            border: 1px solid transparent;
            border-radius: var(--r-sm);
            margin: 0.12rem 0.4rem;
            padding: 0.38rem 0.65rem;
            font-size: 0.84rem;
            font-weight: 500;
            color: var(--text-dim) !important;
            text-decoration: none;
            transition: background var(--t-fast), border-color var(--t-fast), color var(--t-fast), transform var(--t-fast);
        }

        [data-testid="stSidebar"] .stPageLink a:hover {
            background: rgba(246, 201, 14, 0.08);
            border-color: rgba(246, 201, 14, 0.28);
            color: var(--gold) !important;
            transform: translateX(3px);
        }

        /* ============================================================
           SIDEBAR CUSTOM COMPONENTS
        ============================================================ */

        /* Icon-only header block — vertically aligned with the << collapse button */
        .sidebar-icon-header {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            padding: 0rem 0.7rem 0.9rem;
            border-bottom: 1px solid var(--border);
            margin-bottom: 0.2rem;
            margin-top: -0.6rem;
        }

        .sidebar-icon-link {
            display: inline-flex;
            align-items: center;
            text-decoration: none;
            transition: transform var(--t-base), filter var(--t-base);
        }

        .sidebar-icon-link:hover {
            transform: scale(1.06);
            filter: drop-shadow(0 0 8px rgba(246,201,14,0.45));
        }

        /* Section group label */
        .section-label {
            display: flex;
            align-items: center;
            gap: 0.4rem;
            color: var(--gold) !important;
            font-size: 0.63rem;
            font-weight: 800;
            letter-spacing: 0.12rem;
            text-transform: uppercase;
            margin: 1.35rem 0.6rem 0.35rem;
            padding-bottom: 0.28rem;
            border-bottom: 1px solid var(--gold-dim);
        }

        .section-label::before {
            content: '';
            display: inline-block;
            width: 4px;
            height: 4px;
            border-radius: 50%;
            background: var(--gold);
            flex-shrink: 0;
        }

        /* Page links — consistent vertical rhythm */
        [data-testid="stSidebar"] .stPageLink {
            margin-bottom: 0.04rem;
        }

        [data-testid="stSidebar"] .stPageLink a {
            padding: 0.36rem 0.65rem !important;
        }

        /* ============================================================
           BUTTONS
        ============================================================ */
        .stButton > button,
        .stDownloadButton > button {
            position: relative;
            overflow: hidden;
            background: linear-gradient(135deg, #c9a800 0%, #f6c90e 45%, #f59e0b 100%);
            color: #08070a;
            border: 0;
            border-radius: var(--r-md);
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            font-size: 0.85rem;
            letter-spacing: 0.01em;
            padding: 0.55rem 1.3rem;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(246, 201, 14, 0.3), var(--shadow-sm);
            transition: transform var(--t-fast), box-shadow var(--t-fast), filter var(--t-fast);
        }

        /* Shimmer sweep on hover */
        .stButton > button::after,
        .stDownloadButton > button::after {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 60%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.28), transparent);
            transform: skewX(-20deg);
            transition: left 0.45s ease;
        }

        .stButton > button:hover::after,
        .stDownloadButton > button:hover::after {
            left: 160%;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 32px rgba(246, 201, 14, 0.45), var(--shadow-md);
            filter: brightness(1.06);
            color: #08070a;
        }

        .stButton > button:active,
        .stDownloadButton > button:active {
            transform: translateY(0px);
            box-shadow: 0 2px 12px rgba(246, 201, 14, 0.3);
        }

        /* Kill the browser cyan focus-visible ring, replace with gold */
        .stButton > button:focus-visible,
        .stDownloadButton > button:focus-visible {
            outline: 2px solid rgba(246, 201, 14, 0.6) !important;
            outline-offset: 2px !important;
        }

        .stButton > button:focus:not(:focus-visible),
        .stDownloadButton > button:focus:not(:focus-visible) {
            outline: none !important;
            box-shadow: 0 4px 20px rgba(246, 201, 14, 0.3), var(--shadow-sm) !important;
        }

        /* Primary type buttons get a stronger glow */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #d4a000, #f6c90e, #fbbf24);
            box-shadow: 0 4px 24px rgba(246, 201, 14, 0.4), 0 0 0 1px rgba(246,201,14,0.2);
        }

        /* ============================================================
           METRIC CARDS
        ============================================================ */
        div[data-testid="stMetric"] {
            background: var(--surface-glass);
            border: 1px solid var(--border);
            border-radius: var(--r-lg);
            padding: 1rem 1.25rem;
            backdrop-filter: blur(12px);
            box-shadow: var(--shadow-sm);
            transition: border-color var(--t-base), box-shadow var(--t-base), transform var(--t-base);
            animation: metric-pop 0.4s var(--t-slow) both;
        }

        div[data-testid="stMetric"]:hover {
            border-color: rgba(246, 201, 14, 0.3);
            box-shadow: 0 0 20px rgba(246, 201, 14, 0.1), var(--shadow-md);
            transform: translateY(-2px);
        }

        @keyframes metric-pop {
            from { opacity: 0; transform: scale(0.96) translateY(8px); }
            to   { opacity: 1; transform: scale(1) translateY(0); }
        }

        div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
            font-size: 0.72rem !important;
            font-weight: 700;
            letter-spacing: 0.08rem;
            text-transform: uppercase;
            color: var(--text-dim) !important;
        }

        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-size: 1.6rem !important;
            font-weight: 800;
            color: var(--gold) !important;
            line-height: 1.1;
        }

        div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
            font-size: 0.78rem !important;
            font-weight: 600;
        }

        /* ============================================================
           TABS
        ============================================================ */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.25rem;
            border-bottom: 1px solid var(--border);
            background: transparent;
            padding-bottom: 0;
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border: 1px solid transparent;
            border-bottom: none;
            border-radius: var(--r-sm) var(--r-sm) 0 0;
            color: var(--text-dim);
            font-weight: 500;
            font-size: 0.84rem;
            padding: 0.5rem 1rem;
            transition: color var(--t-fast), background var(--t-fast), border-color var(--t-fast);
        }

        .stTabs [data-baseweb="tab"]:hover {
            color: var(--text);
            background: rgba(246, 201, 14, 0.05);
            border-color: var(--border);
        }

        .stTabs [aria-selected="true"] {
            color: var(--gold) !important;
            background: rgba(246, 201, 14, 0.06) !important;
            border-color: var(--border) var(--border) transparent !important;
            border-top: 2px solid var(--gold) !important;
            font-weight: 700;
        }

        /* ============================================================
           DATA FRAMES / TABLES
        ============================================================ */
        [data-testid="stDataFrame"],
        [data-testid="stTable"] {
            background: var(--surface-glass);
            border: 1px solid var(--border);
            border-radius: var(--r-md);
            overflow: hidden;
            backdrop-filter: blur(8px);
        }

        /* ============================================================
           EXPANDERS
        ============================================================ */
        div[data-testid="stExpander"] {
            background: var(--surface-glass);
            border: 1px solid var(--border);
            border-radius: var(--r-md);
            backdrop-filter: blur(8px);
            transition: border-color var(--t-base);
        }

        div[data-testid="stExpander"]:hover {
            border-color: var(--border-bright);
        }

        div[data-testid="stExpander"] summary {
            font-weight: 600;
            font-size: 0.88rem;
        }

        /* ============================================================
           ALERTS / INFO BOXES
        ============================================================ */
        [data-testid="stAlert"] {
            border-radius: var(--r-md) !important;
            border-width: 1px !important;
            border-left-width: 3px !important;
            backdrop-filter: blur(8px);
            font-size: 0.88rem;
        }

        /* Info → teal */
        [data-testid="stAlert"][data-baseweb="notification"]:has(.st-emotion-cache-16idsys),
        div[data-testid="stAlert"] {
            background: rgba(13, 18, 32, 0.75) !important;
        }

        /* ============================================================
           INPUTS (SELECT, NUMBER, TEXT)
        ============================================================ */
        .stSelectbox [data-baseweb="select"] > div,
        .stNumberInput input,
        .stTextInput input,
        .stTextArea textarea {
            background: var(--surface-1) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--r-sm) !important;
            color: var(--text) !important;
            font-size: 0.88rem;
            transition: border-color var(--t-fast), box-shadow var(--t-fast);
        }

        .stSelectbox [data-baseweb="select"] > div:focus-within,
        .stNumberInput input:focus,
        .stTextInput input:focus,
        .stTextArea textarea:focus {
            border-color: var(--gold) !important;
            box-shadow: 0 0 0 3px rgba(246, 201, 14, 0.12) !important;
            outline: none;
        }

        /* Dropdown menu */
        [data-baseweb="menu"],
        [data-baseweb="popover"] [data-baseweb="list"] {
            background: var(--surface-2) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--r-md) !important;
        }

        [data-baseweb="option"]:hover {
            background: rgba(246, 201, 14, 0.08) !important;
        }

        /* ============================================================
           SLIDERS
        ============================================================ */
        [data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
            background: var(--gold) !important;
            border: 2px solid #08070a !important;
            box-shadow: 0 0 10px var(--gold-glow);
        }

        [data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stTickBar"] + div > div > div {
            background: var(--gold) !important;
        }

        /* ============================================================
           JSON VIEWER
        ============================================================ */
        [data-testid="stJson"] {
            background: var(--surface-0) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--r-md) !important;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
        }

        /* ============================================================
           CHECKBOXES & RADIO
        ============================================================ */
        .stCheckbox label,
        .stRadio label {
            font-size: 0.86rem;
            font-weight: 500;
            color: var(--text-dim) !important;
            transition: color var(--t-fast);
        }

        .stCheckbox label:hover,
        .stRadio label:hover {
            color: var(--text) !important;
        }

        /* ============================================================
           FILE UPLOADER
        ============================================================ */
        [data-testid="stFileUploader"] {
            background: var(--surface-glass);
            border: 2px dashed var(--border);
            border-radius: var(--r-lg);
            transition: border-color var(--t-base), background var(--t-base);
        }

        [data-testid="stFileUploader"]:hover {
            border-color: var(--gold);
            background: var(--gold-dim);
        }

        /* ============================================================
           HERO SECTION (app.py main page)
        ============================================================ */
        .hero-shell {
            position: relative;
            min-height: 60vh;
            display: flex;
            align-items: center;
            border: 1px solid rgba(246, 201, 14, 0.2);
            background: linear-gradient(135deg,
                rgba(13, 18, 32, 0.9) 0%,
                rgba(10, 14, 26, 0.85) 60%,
                rgba(13, 18, 32, 0.9) 100%
            );
            border-radius: var(--r-xl);
            padding: clamp(2rem, 5vw, 4rem);
            box-shadow:
                0 32px 80px rgba(0, 0, 0, 0.5),
                inset 0 1px 0 rgba(246, 201, 14, 0.1);
            overflow: hidden;
            animation: hero-enter 0.6s var(--t-slow) both;
        }

        @keyframes hero-enter {
            from { opacity: 0; transform: translateY(28px) scale(0.98); }
            to   { opacity: 1; transform: translateY(0) scale(1); }
        }

        /* Animated shimmer bar at the top edge */
        .hero-shell::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg,
                transparent 0%,
                var(--gold) 30%,
                var(--amber) 50%,
                var(--gold) 70%,
                transparent 100%
            );
            background-size: 200% 100%;
            animation: shimmer-bar 3s linear infinite;
        }

        @keyframes shimmer-bar {
            0%   { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }

        /* Radial glow inside hero */
        .hero-shell::after {
            content: '';
            position: absolute;
            top: -30%;
            right: -10%;
            width: 55%;
            height: 140%;
            background: radial-gradient(ellipse, rgba(246,201,14,0.06) 0%, transparent 65%);
            pointer-events: none;
            animation: glow-pulse 4s ease-in-out infinite alternate;
        }

        @keyframes glow-pulse {
            0%   { opacity: 0.6; transform: scale(1); }
            100% { opacity: 1;   transform: scale(1.08); }
        }

        .hero-kicker {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--gold);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.14rem;
            text-transform: uppercase;
            margin-bottom: 1rem;
            padding: 0.3rem 0.8rem;
            border: 1px solid rgba(246, 201, 14, 0.3);
            border-radius: 999px;
            background: rgba(246, 201, 14, 0.06);
        }

        .hero-kicker::before {
            content: '';
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--gold);
            animation: dot-pulse 1.8s ease-in-out infinite;
        }

        @keyframes dot-pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50%       { opacity: 0.4; transform: scale(0.6); }
        }

        .hero-title {
            font-size: clamp(2.4rem, 6.5vw, 5.5rem);
            font-weight: 900;
            line-height: 0.95;
            letter-spacing: -0.03em;
            margin: 0 0 1.25rem 0;
            background: linear-gradient(135deg, #ffffff 0%, #f6c90e 50%, #f59e0b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero-meta {
            color: var(--text-dim);
            font-size: 1.05rem;
            max-width: 780px;
            line-height: 1.75;
        }

        .hero-meta > div:first-child {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.1rem;
            color: var(--text-faint);
            font-weight: 600;
            margin-bottom: 0.2rem;
        }

        .creator-name {
            color: var(--text);
            font-size: 1.45rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin: 0 0 1rem 0;
        }

        .creator-name::after {
            content: '';
            display: block;
            width: 2.5rem;
            height: 2px;
            background: var(--gold);
            margin-top: 0.4rem;
            border-radius: 1px;
        }

        .note-panel {
            background: rgba(99, 102, 241, 0.06);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-left: 3px solid var(--indigo);
            border-radius: var(--r-md);
            padding: 1rem 1.2rem;
            margin-top: 1.5rem;
            font-size: 0.88rem;
        }

        .note-panel b {
            color: var(--text);
            font-weight: 700;
        }

        /* Hero stat strip */
        .hero-stats {
            display: flex;
            gap: 1.5rem;
            margin-top: 1.75rem;
            flex-wrap: wrap;
        }

        .hero-stat {
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
            padding: 0.65rem 1.1rem;
            background: rgba(246, 201, 14, 0.05);
            border: 1px solid rgba(246, 201, 14, 0.18);
            border-radius: var(--r-md);
            min-width: 72px;
        }

        .hero-stat-num {
            color: var(--gold);
            font-size: 1.55rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1;
        }

        .hero-stat-label {
            color: var(--text-dim);
            font-size: 0.7rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        /* ============================================================
           NAVIGATION TUTORIAL (render_navigation_tutorial)
        ============================================================ */
        .navigation-spacer {
            height: 6vh;
            min-height: 48px;
        }

        .nav-card {
            position: relative;
            height: 130px;
            background: var(--surface-glass);
            border: 1px solid var(--border);
            border-radius: var(--r-lg);
            padding: 1.1rem 1.2rem 1rem;
            backdrop-filter: blur(10px);
            overflow: hidden;
            transition: border-color var(--t-base), box-shadow var(--t-base), transform var(--t-base);
            margin-bottom: 0.5rem;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }

        .nav-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--gold), var(--amber), transparent);
            opacity: 0;
            transition: opacity var(--t-base);
        }

        .nav-card:hover {
            border-color: rgba(246, 201, 14, 0.3);
            box-shadow: 0 8px 32px rgba(246, 201, 14, 0.08), var(--shadow-md);
            transform: translateY(-3px);
        }

        .nav-card:hover::before { opacity: 1; }

        .nav-card h4 {
            color: var(--text);
            font-size: 0.92rem;
            font-weight: 700;
            letter-spacing: -0.01em;
            margin: 0 0 0.4rem 0;
        }

        .nav-card p {
            color: var(--text-dim);
            font-size: 0.8rem;
            line-height: 1.5;
            margin-bottom: 0.75rem;
        }

        /* ============================================================
           SCROLLBAR
        ============================================================ */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb {
            background: var(--surface-3);
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover { background: var(--text-faint); }

        /* ============================================================
           MISC UTILITY CLASSES
        ============================================================ */
        .accent-gold    { color: var(--gold); }
        .accent-cyan    { color: var(--blue-light); }
        .accent-purple  { color: var(--indigo); }
        .accent-teal    { color: var(--teal); }

        /* Divider */
        hr {
            border: none;
            border-top: 1px solid var(--border);
            margin: 1.5rem 0;
        }

        /* Spinner */
        [data-testid="stSpinner"] > div {
            border-top-color: var(--gold) !important;
        }

        /* Success / error / warning colours stay readable */
        [data-testid="stAlert"][kind="success"]  { border-left-color: var(--emerald) !important; }
        [data-testid="stAlert"][kind="error"]    { border-left-color: var(--rose)    !important; }
        [data-testid="stAlert"][kind="warning"]  { border-left-color: var(--amber)   !important; }
        [data-testid="stAlert"][kind="info"]     { border-left-color: var(--teal)    !important; }

        /* Stagger nav-card entrance animation */
        .nav-card:nth-child(1) { animation-delay: 0.05s; }
        .nav-card:nth-child(2) { animation-delay: 0.10s; }
        .nav-card:nth-child(3) { animation-delay: 0.15s; }

        @keyframes card-enter {
            from { opacity: 0; transform: translateY(14px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .nav-card {
            animation: card-enter 0.45s var(--t-slow) both;
        }

        /* Nav tutorial — page links under each card sit flush, no stray gap */
        [data-testid="stVerticalBlock"] > [data-testid="stPageLink"] a,
        [data-testid="stColumn"] > [data-testid="stVerticalBlock"] > [data-testid="stPageLink"] a {
            font-size: 0.83rem !important;
            padding: 0.3rem 0.5rem !important;
        }

        /* ============================================================
           DATA UPLOAD — file uploader + buttons uniform row
        ============================================================ */

        /* Row stretches to match column heights */
        [data-testid="stHorizontalBlock"]:has([data-testid="stFileUploader"]) {
            align-items: flex-end !important;
            gap: 1rem !important;
        }

        /* Upload column (col 1) — flex column, uploader on top, button below */
        [data-testid="stHorizontalBlock"]:has([data-testid="stFileUploader"])
        > [data-testid="stColumn"]:first-child {
            flex: 3 1 0 !important;
            display: flex !important;
            flex-direction: column !important;
            gap: 0.5rem !important;
        }

        /* Sample column (col 2) — flex column, bottom-aligned */
        [data-testid="stHorizontalBlock"]:has([data-testid="stFileUploader"])
        > [data-testid="stColumn"]:last-child {
            flex: 1 1 0 !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: flex-end !important;
        }

        /* All buttons in the upload row full-width, same height */
        [data-testid="stHorizontalBlock"]:has([data-testid="stFileUploader"])
        .stButton > button {
            width: 100% !important;
            height: 2.75rem !important;
            font-size: 0.85rem !important;
        }

        /* ============================================================
           EMPTY STATE
        ============================================================ */
        .empty-state {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            gap: 1rem;
            margin: 3rem auto;
            max-width: 500px;
            padding: 2.5rem 2.5rem 2rem;
            background: rgba(13, 18, 32, 0.6);
            border: 1px solid rgba(246, 201, 14, 0.15);
            border-radius: var(--r-lg);
        }

        /* Animated bar chart icon */
        .empty-state-bars {
            display: flex;
            align-items: flex-end;
            gap: 4px;
            height: 32px;
            margin-bottom: 0.25rem;
        }

        .empty-state-bar {
            width: 6px;
            border-radius: 3px 3px 0 0;
            background: rgba(246, 201, 14, 0.55);
            animation: bar-breathe 2.4s ease-in-out infinite;
        }

        .empty-state-bar:nth-child(1) { height: 40%; animation-delay: 0s; }
        .empty-state-bar:nth-child(2) { height: 70%; animation-delay: 0.2s; }
        .empty-state-bar:nth-child(3) { height: 55%; animation-delay: 0.4s; }
        .empty-state-bar:nth-child(4) { height: 90%; animation-delay: 0.1s; background: rgba(246,201,14,0.8); }
        .empty-state-bar:nth-child(5) { height: 45%; animation-delay: 0.3s; }

        @keyframes bar-breathe {
            0%, 100% { opacity: 0.4; transform: scaleY(0.85); }
            50%       { opacity: 1;   transform: scaleY(1); }
        }

        .empty-state-text {
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }

        .empty-state-title {
            color: var(--text) !important;
            font-size: 1.05rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: -0.01em;
        }

        .empty-state-desc {
            color: var(--text-dim) !important;
            font-size: 0.85rem;
            line-height: 1.6;
            margin: 0;
        }

        /* CTA button inside the empty state box */
        .empty-state-cta {
            display: inline-block;
            margin-top: 1.25rem;
            padding: 0.8rem 2.5rem;
            font-size: 0.92rem;
            font-weight: 700;
            letter-spacing: -0.01em;
            background: linear-gradient(135deg, #c9a800 0%, #f6c90e 45%, #f59e0b 100%);
            color: #08070a !important;
            border-radius: var(--r-md);
            border: none;
            text-decoration: none !important;
            box-shadow: 0 4px 20px rgba(246, 201, 14, 0.25);
            transition: box-shadow var(--t-base), transform var(--t-base);
        }

        .empty-state-cta:hover {
            box-shadow: 0 6px 28px rgba(246, 201, 14, 0.45);
            transform: translateY(-2px);
            color: #08070a !important;
        }

        /* ============================================================
           FOOTER — fixed to viewport bottom
        ============================================================ */

        /* Push page content up so footer doesn't cover it */
        .main .block-container {
            padding-bottom: 6rem !important;
        }

        .app-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            z-index: 99999;
            padding: 0.7rem 2rem;
            background: rgba(6, 10, 20, 0.96);
            backdrop-filter: blur(12px);
            border-top: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 0.5rem;
        }

        .footer-left {
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
        }

        .footer-name {
            color: var(--text);
            font-size: 0.82rem;
            font-weight: 600;
            letter-spacing: -0.01em;
        }

        .footer-license {
            color: var(--text-faint);
            font-size: 0.72rem;
        }

        .footer-right {
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }

        .footer-link {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            color: var(--text-dim) !important;
            text-decoration: none !important;
            font-size: 0.76rem;
            font-weight: 500;
            padding: 0.3rem 0.65rem;
            border: 1px solid var(--border);
            border-radius: 999px;
            background: transparent;
            transition: color var(--t-base), border-color var(--t-base), background var(--t-base);
        }

        .footer-link:hover {
            color: var(--gold) !important;
            border-color: rgba(246, 201, 14, 0.4);
            background: rgba(246, 201, 14, 0.05);
        }

        .footer-link svg {
            width: 13px;
            height: 13px;
            fill: currentColor;
            flex-shrink: 0;
        }

        .footer-sep {
            color: var(--border);
            font-size: 0.7rem;
            user-select: none;
        }

        /* Inline text links inside footer license line */
        .footer-inline-link {
            color: var(--text-dim) !important;
            text-decoration: underline !important;
            text-underline-offset: 2px;
            transition: color var(--t-fast);
        }

        .footer-inline-link:hover {
            color: var(--gold) !important;
        }

        /* Hero creator credit */
        .hero-creator {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            color: var(--text-dim);
            font-size: 0.8rem;
            font-weight: 500;
            margin-top: 1.5rem;
            padding-top: 1.25rem;
            border-top: 1px solid var(--border);
        }

        .hero-creator span {
            color: var(--text);
            font-weight: 600;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )



def render_navigation_sidebar(active_page: str) -> None:
    with st.sidebar:
        st.markdown(
            '''<div class="sidebar-icon-header">
                <a href="/" target="_self" class="sidebar-icon-link">
                    <svg width="38" height="38" viewBox="0 0 38 38" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect width="38" height="38" rx="10" fill="#111827"/>
                        <rect width="38" height="38" rx="10" fill="url(#grad)" opacity="0.18"/>
                        <rect x="0.5" y="0.5" width="37" height="37" rx="9.5" stroke="#f6c90e" stroke-opacity="0.35"/>
                        <path d="M10 27 L10 19 L15 14 L20 19 L25 12 L28 15" stroke="#f6c90e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                        <circle cx="10" cy="27" r="1.5" fill="#f6c90e"/>
                        <circle cx="15" cy="14" r="1.5" fill="#f59e0b"/>
                        <circle cx="20" cy="19" r="1.5" fill="#f6c90e"/>
                        <circle cx="25" cy="12" r="1.5" fill="#f59e0b"/>
                        <circle cx="28" cy="15" r="1.5" fill="#f6c90e"/>
                        <defs>
                            <linearGradient id="grad" x1="0" y1="0" x2="38" y2="38" gradientUnits="userSpaceOnUse">
                                <stop offset="0%" stop-color="#f6c90e"/>
                                <stop offset="100%" stop-color="#7c3aed"/>
                            </linearGradient>
                        </defs>
                    </svg>
                </a>
            </div>''',
            unsafe_allow_html=True,
        )

        by_name = {name: (path, icon, description) for name, path, icon, description in NAVIGATION}
        for group, page_names in NAVIGATION_GROUPS.items():
            st.markdown(f'<div class="section-label">{group}</div>', unsafe_allow_html=True)
            for name in page_names:
                path, icon, _ = by_name[name]
                label = "Main" if name == "Main" else name
                st.page_link(path, label=label, icon=icon)




def render_navigation_tutorial() -> None:
    st.markdown('<div class="navigation-spacer"></div>', unsafe_allow_html=True)
    st.subheader("Navigation Tutorial")
    st.caption("Use the sidebar icons for quick movement, or start from the guide below.")

    groups = [
        ("Data", "Upload and clean your dataset before running statistics.", ["Data Upload", "Data Cleaning"]),
        ("Statistics", "Summarize variables, inspect correlations, and detect outliers.", ["Descriptive Statistics", "Correlation Regression"]),
        ("Visualizations", "Build plots, check normality, and export PNG images.", ["Visualizations", "Normality"]),
        ("Distributions", "Explore probability models and simulate the Central Limit Theorem.", ["Distributions", "CLT Simulator"]),
        ("Tests", "Run parametric, nonparametric, and ANOVA procedures.", ["Parametric Tests", "Nonparametric Tests", "ANOVA"]),
        ("Reports", "Generate a PDF report from saved analyses and plots.", ["Report"]),
    ]
    by_name = {name: (path, icon, description) for name, path, icon, description in NAVIGATION}

    for row_start in range(0, len(groups), 3):
        columns = st.columns(3)
        for column, (group, description, pages) in zip(columns, groups[row_start : row_start + 3]):
            with column:
                st.markdown(
                    f'<div class="nav-card"><h4>{group}</h4><p>{description}</p></div>',
                    unsafe_allow_html=True,
                )
                for page_name in pages:
                    path, icon, _ = by_name[page_name]
                    st.page_link(path, label=page_name, icon=icon)


def render_empty_state(
    title: str = "No dataset loaded",
    message: str = "Upload a CSV or Excel file, or load the sample dataset to get started.",
) -> None:
    """Render a styled empty-state panel when no dataset is available."""
    st.markdown(
        f'''<div class="empty-state">
            <div class="empty-state-bars">
                <div class="empty-state-bar"></div>
                <div class="empty-state-bar"></div>
                <div class="empty-state-bar"></div>
                <div class="empty-state-bar"></div>
                <div class="empty-state-bar"></div>
            </div>
            <div class="empty-state-text">
                <p class="empty-state-title">{title}</p>
                <p class="empty-state-desc">{message}</p>
            </div>
            <a href="/Data_Upload" target="_self" class="empty-state-cta">
                Go to Data Upload
            </a>
        </div>''',
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Render the global footer with author credit and external links."""
    # GitHub SVG icon
    github_svg = (
        '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
        '<path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385'
        '.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41'
        '-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23'
        ' 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925'
        ' 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23'
        '.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23'
        '.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925'
        '.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57'
        'A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>'
    )
    # LinkedIn SVG icon
    linkedin_svg = (
        '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
        '<path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037'
        '-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046'
        'c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433'
        'a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452z'
        'M22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451'
        'C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>'
    )
    # Email SVG icon
    email_svg = (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">'
        '<rect x="2" y="4" width="20" height="16" rx="2"/>'
        '<path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>'
    )

    st.markdown(
        f'''<div class="app-footer">
            <div class="footer-left">
                <span class="footer-name">Joel Payyappilly Elias</span>
                <span class="footer-license">
                    MIT License &nbsp;·&nbsp; Data Analysis Toolkit
                    &nbsp;&nbsp;|&nbsp;&nbsp;
                    Contact:&nbsp;
                    <a href="https://github.com/joel-p-elias" target="_blank" rel="noopener" class="footer-inline-link">GitHub</a>
                    &nbsp;or&nbsp;
                    <a href="https://www.linkedin.com/in/joel-p-elias/" target="_blank" rel="noopener" class="footer-inline-link">LinkedIn</a>
                </span>
            </div>
            <div class="footer-right">
                <a class="footer-link"
                   href="https://github.com/joel-p-elias"
                   target="_blank" rel="noopener">
                    {github_svg} GitHub
                </a>
                <a class="footer-link"
                   href="https://www.linkedin.com/in/joel-p-elias/"
                   target="_blank" rel="noopener">
                    {linkedin_svg} LinkedIn
                </a>
            </div>
        </div>''',
        unsafe_allow_html=True,
    )