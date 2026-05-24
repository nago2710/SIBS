"""
Utility module for NAV-MIS System
Contains styling, helper functions, and UI components
"""

import streamlit as st
from config import ui_config


def get_custom_css() -> str:
    """Get complete custom CSS for the application"""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ==================== GLOBAL STYLES ==================== */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Inter', sans-serif;
        background-color: """ + ui_config.DARK_BG + """ !important;
        color: """ + ui_config.TEXT_PRIMARY + """ !important;
    }

    [data-testid="stSidebar"] {
        background-color: #0f1626 !important;
        border-right: 1px solid """ + ui_config.BORDER_COLOR + """ !important;
    }

    /* ==================== TYPOGRAPHY ==================== */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: """ + ui_config.TEXT_PRIMARY + """ !important;
    }

    p {
        color: """ + ui_config.TEXT_SECONDARY + """ !important;
        line-height: 1.6;
    }

    /* ==================== DASHBOARD HEADER ==================== */
    .dashboard-header {
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 1px solid """ + ui_config.BORDER_COLOR + """;
    }

    .dashboard-header h1 {
        color: """ + ui_config.TEXT_PRIMARY + """ !important;
        font-size: 28px !important;
        font-weight: 700 !important;
        margin: 0 0 8px 0 !important;
    }

    .dashboard-header p {
        color: """ + ui_config.TEXT_SECONDARY + """ !important;
        font-size: 14px;
        margin: 0 !important;
    }

    /* ==================== CARDS & CONTAINERS ==================== */
    .premium-card {
        background: """ + ui_config.CARD_BG + """;
        border: 1px solid """ + ui_config.BORDER_COLOR + """;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .card-title {
        font-size: 16px;
        font-weight: 600;
        color: """ + ui_config.TEXT_PRIMARY + """;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid """ + ui_config.BORDER_COLOR + """;
    }

    /* ==================== METRICS GRID ==================== */
    .navistock-grid {
        display: flex;
        gap: 20px;
        margin-bottom: 25px;
        flex-wrap: wrap;
    }

    .navistock-metric {
        flex: 1;
        min-width: 250px;
        background: """ + ui_config.CARD_BG + """;
        border: 1px solid """ + ui_config.BORDER_COLOR + """;
        border-radius: 10px;
        padding: 20px;
        position: relative;
        transition: all 0.3s ease;
    }

    .navistock-metric:hover {
        border-color: """ + ui_config.PRIMARY_COLOR + """;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.1);
    }

    .navistock-label {
        color: """ + ui_config.TEXT_SECONDARY + """;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .navistock-value {
        color: """ + ui_config.TEXT_PRIMARY + """;
        font-size: 26px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .navistock-subtext {
        font-size: 12px;
        margin-top: 6px;
        font-weight: 500;
        color: """ + ui_config.TEXT_SECONDARY + """;
    }

    /* ==================== BUTTONS ==================== */
    div.stButton > button {
        background-color: """ + ui_config.PRIMARY_COLOR + """ !important;
        color: """ + ui_config.TEXT_PRIMARY + """ !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 10px 24px !important;
        transition: all 0.2s ease !important;
        width: 100%;
    }

    div.stButton > button:hover {
        background-color: #1d4ed8 !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
        transform: translateY(-1px);
    }

    div.stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2) !important;
    }

    /* ==================== TABS ==================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #0f1626;
        padding: 6px;
        border-radius: 8px;
        border: 1px solid """ + ui_config.BORDER_COLOR + """;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 10px 16px;
        border-radius: 6px;
        color: """ + ui_config.TEXT_SECONDARY + """;
        font-weight: 500;
        background-color: transparent;
        transition: all 0.2s;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1e293b !important;
        color: """ + ui_config.PRIMARY_COLOR + """ !important;
        font-weight: 600 !important;
    }

    /* ==================== FORMS & INPUTS ==================== */
    .stTextInput, .stNumberInput, .stSelectbox, .stTextArea {
        color: """ + ui_config.TEXT_PRIMARY + """ !important;
    }

    input, select, textarea {
        background-color: """ + ui_config.CARD_BG + """ !important;
        color: """ + ui_config.TEXT_PRIMARY + """ !important;
        border: 1px solid """ + ui_config.BORDER_COLOR + """ !important;
        border-radius: 6px !important;
    }

    input:focus, select:focus, textarea:focus {
        border-color: """ + ui_config.PRIMARY_COLOR + """ !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1) !important;
    }

    /* ==================== TABLES ==================== */
    .stDataFrame, div[data-testid="stTable"] {
        background-color: """ + ui_config.CARD_BG + """ !important;
        border: 1px solid """ + ui_config.BORDER_COLOR + """ !important;
        border-radius: 8px !important;
    }

    th {
        background-color: #1e293b !important;
        color: """ + ui_config.TEXT_PRIMARY + """ !important;
        font-weight: 600 !important;
    }

    td {
        color: """ + ui_config.TEXT_PRIMARY + """ !important;
        border-color: """ + ui_config.BORDER_COLOR + """ !important;
    }

    /* ==================== ALERTS & MESSAGES ==================== */
    .stAlert {
        border-radius: 8px !important;
    }

    .stSuccess {
        background-color: rgba(74, 222, 128, 0.1) !important;
        border: 1px solid #4ade80 !important;
        color: #4ade80 !important;
    }

    .stError {
        background-color: rgba(248, 113, 113, 0.1) !important;
        border: 1px solid """ + ui_config.ERROR_COLOR + """ !important;
        color: """ + ui_config.ERROR_COLOR + """ !important;
    }

    .stWarning {
        background-color: rgba(251, 191, 36, 0.1) !important;
        border: 1px solid """ + ui_config.WARNING_COLOR + """ !important;
        color: """ + ui_config.WARNING_COLOR + """ !important;
    }

    .stInfo {
        background-color: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid """ + ui_config.PRIMARY_COLOR + """ !important;
        color: #60a5fa !important;
    }

    /* ==================== PROGRESS BAR ==================== */
    .stProgress > div > div > div {
        background-color: """ + ui_config.PRIMARY_COLOR + """ !important;
    }

    /* ==================== SLIDERS ==================== */
    .stSlider > div > div > div {
        color: """ + ui_config.PRIMARY_COLOR + """ !important;
    }

    /* ==================== RADIO & CHECKBOX ==================== */
    .stRadio label, .stCheckbox label {
        color: """ + ui_config.TEXT_PRIMARY + """ !important;
    }

    /* ==================== SIDEBAR ELEMENTS ==================== */
    .sidebar-header {
        padding: 10px 0px;
        margin-bottom: 20px;
        border-bottom: 1px solid """ + ui_config.BORDER_COLOR + """;
    }

    .user-info-box {
        background: """ + ui_config.CARD_BG + """;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid """ + ui_config.BORDER_COLOR + """;
        margin-bottom: 25px;
    }

    /* ==================== RESPONSIVE ==================== */
    @media (max-width: 768px) {
        .navistock-grid {
            flex-direction: column;
        }

        .navistock-metric {
            flex: 1 1 100%;
        }
    }
    </style>
    """


def apply_custom_styling():
    """Apply custom CSS to the entire application"""
    st.markdown(get_custom_css(), unsafe_allow_html=True)


def render_sidebar_header(app_name: str, version: str):
    """Render sidebar header with app info"""
    st.markdown(f"""
        <div class="sidebar-header">
            <h4 style='color: white; margin: 0;'>⚓ {app_name}</h4>
            <p style='color: #64748b; font-size: 12px; margin: 0;'>{version}</p>
        </div>
    """, unsafe_allow_html=True)


def render_user_info(username: str, role: str, department: str):
    """Render user information box in sidebar"""
    st.markdown(f"""
        <div class="user-info-box">
            <div style='font-size: 11px; color: #94a3b8; text-transform: uppercase; margin-bottom: 4px;'>
                Active User
            </div>
            <div style='font-weight: 600; color: white; font-size: 14px;'>{username}</div>
            <div style='font-size: 12px; color: """ + ui_config.PRIMARY_COLOR + """'>
                {role.upper()} ({department})
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_login_header():
    """Render login page header"""
    st.markdown("""
        <div style='text-align: center; margin-bottom: 30px;'>
            <div style='background: """ + ui_config.PRIMARY_COLOR + """; width: 60px; height: 60px; border-radius: 12px; 
                        display: inline-flex; align-items: center; justify-content: center; font-size: 32px; font-weight: bold; 
                        color: white; margin-bottom: 15px;'>⚓</div>
            <h2 style='color: white; margin: 0 0 8px 0; font-size: 28px;'>Sistem Integrasi NAV-MIS</h2>
            <p style='color: #64748b; font-size: 14px; margin: 0;'>
                Portal Manajemen Galangan Kapal Terpadu
            </p>
        </div>
    """, unsafe_allow_html=True)


def format_currency(value: float) -> str:
    """Format number as Indonesian currency"""
    return f"Rp {int(value):,}".replace(",", ".")


def format_percentage(value: float) -> str:
    """Format number as percentage"""
    return f"{value:.1f}%"


def create_metric_card(label: str, value: str, subtext: str = "", color: str = None):
    """Create a metric card component"""
    if color is None:
        color = ui_config.TEXT_PRIMARY

    return f"""
    <div class="navistock-metric">
        <div class="navistock-label">{label}</div>
        <div class="navistock-value" style="color: {color};">{value}</div>
        <div class="navistock-subtext">{subtext}</div>
    </div>
    """


def render_dashboard_header(title: str, subtitle: str = ""):
    """Render dashboard header section"""
    st.markdown(f"""
        <div class="dashboard-header">
            <h1>{title}</h1>
            {f'<p>{subtitle}</p>' if subtitle else ''}
        </div>
    """, unsafe_allow_html=True)


def render_premium_card(title: str, content: str = ""):
    """Render premium styled card"""
    return f"""
    <div class="premium-card">
        {f'<div class="card-title">{title}</div>' if title else ''}
        {content}
    </div>
    """


def show_success_toast(message: str):
    """Show success notification"""
    st.success(f"✅ {message}")


def show_error_toast(message: str):
    """Show error notification"""
    st.error(f"❌ {message}")


def show_warning_toast(message: str):
    """Show warning notification"""
    st.warning(f"⚠️ {message}")


def show_info_toast(message: str):
    """Show info notification"""
    st.info(f"ℹ️ {message}")
