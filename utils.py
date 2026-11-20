"""
SIBS: Shipyard Integrated Business System
Utilities — CSS Theme (Light & Dark), Format Helpers, Dynamic UI Components

Maritime Corporate Edition (Refined per Marine Industry Website Reference)
"""

import os
import base64
from pathlib import Path
import streamlit as st
from datetime import datetime


# ==================== ASSET LOADER (BASE64) ====================

def get_asset_base64(filename: str = "shipyard_hero.jpg") -> str:
    """Read local asset image as base64 string for embedding in CSS."""
    asset_dir = Path(__file__).parent / "asset"
    target = asset_dir / filename
    if target.exists():
        with open(target, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""


# ==================== THEME STYLING (LIGHT & DARK MODE) ====================

def apply_sibs_theme(theme: str = "light"):
    """
    Apply ultra-modern interactive Glassmorphism enterprise theme,
    based on Timothy Ricks' Webflow Glassmorphism design system (tricks-glassmorphism).
    Features:
    - Multi-layer specular edge highlights (top-left light refraction)
    - Background ambient light mesh (cyan, emerald, marine sapphire blur blobs)
    - Authentic frosted glass backdrop-filter (blur 24px + saturation 180%)
    - Dynamic micro-interactions (spring easing cubic-bezier, hover elevation & glow)
    - Tailored corporate marine palette (Abyssal Glass for Dark, Glacial Quartz for Light)
    """
    hero_b64 = get_asset_base64("shipyard_hero.jpg")

    if theme == "dark":
        st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

        :root {{ color-scheme: dark !important; }}
        html, body, [class*="css"] {{
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
        }}

        /* Ambient Light Mesh Background (Timothy Ricks Canvas Engine) */
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            background-color: #050811 !important;
            background-image: 
                radial-gradient(circle at 10% 12%, rgba(14, 165, 233, 0.16) 0%, transparent 45%),
                radial-gradient(circle at 90% 18%, rgba(16, 185, 129, 0.14) 0%, transparent 40%),
                radial-gradient(circle at 50% 55%, rgba(30, 58, 138, 0.16) 0%, transparent 55%),
                radial-gradient(circle at 85% 88%, rgba(56, 189, 248, 0.12) 0%, transparent 45%),
                radial-gradient(circle at 15% 90%, rgba(15, 23, 42, 0.95) 0%, transparent 50%) !important;
            background-attachment: fixed !important;
            color: #F1F5F9 !important;
        }}
        .block-container {{
            padding: 1.25rem 3.5rem 3rem 3.5rem !important;
            max-width: 1440px !important; background-color: transparent !important;
        }}

        /* Floating Frosted Glass Navbar */
        .sibs-navbar-container {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 16px 32px;
            background: linear-gradient(135deg, rgba(10, 18, 38, 0.78) 0%, rgba(7, 12, 24, 0.82) 100%) !important;
            backdrop-filter: blur(28px) saturate(190%) !important;
            -webkit-backdrop-filter: blur(28px) saturate(190%) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.4) !important;
            border-left: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 12px; margin-bottom: 22px;
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.45), inset 0 1px 1px rgba(255, 255, 255, 0.25) !important;
        }}
        .sibs-brand-title {{
            font-size: 19px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.5px;
            display: flex; align-items: center; gap: 12px;
        }}
        .sibs-brand-sub {{
            font-size: 10.5px; font-weight: 600; color: #94A3B8; letter-spacing: 0.3px;
            border-left: 2px solid rgba(148, 163, 184, 0.3); padding-left: 10px;
        }}
        .sibs-nav-links {{
            display: flex; align-items: center; gap: 26px; list-style: none; margin: 0; padding: 0;
        }}
        .sibs-nav-link {{
            color: #94A3B8; text-decoration: none; font-size: 13px; font-weight: 600;
            padding-bottom: 4px; transition: all 0.25s ease;
        }}
        .sibs-nav-link:hover {{
            color: #38BDF8; text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
        }}
        .sibs-nav-link.active {{
            color: #38BDF8 !important; border-bottom: 2px solid #38BDF8 !important;
            text-shadow: 0 0 12px rgba(56, 189, 248, 0.7);
        }}

        /* Hero Container with Layered Glass Cockpit */
        .st-key-sibs_hero_section, .sibs-hero-wrapper {{
            background: linear-gradient(135deg, rgba(5, 9, 18, 0.88) 0%, rgba(9, 16, 32, 0.82) 48%, rgba(15, 23, 42, 0.62) 100%),
                        url('data:image/jpeg;base64,{hero_b64}') !important;
            background-size: cover !important;
            background-position: center 36% !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-radius: 16px !important;
            padding: 38px 46px 40px 46px !important;
            margin-bottom: 26px !important;
            border: 1px solid rgba(255, 255, 255, 0.16) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.42) !important;
            border-left: 1px solid rgba(255, 255, 255, 0.25) !important;
            box-shadow: 0 28px 60px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.3) !important;
        }}
        .sibs-hero-tag {{
            display: inline-block; font-size: 11px; font-weight: 700;
            color: #38BDF8; letter-spacing: 1.5px; text-transform: uppercase;
            background: rgba(56, 189, 248, 0.14);
            padding: 6px 14px; border-radius: 999px;
            border: 1px solid rgba(56, 189, 248, 0.35);
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 14px rgba(56, 189, 248, 0.18), inset 0 1px 0 rgba(255, 255, 255, 0.3);
        }}
        .sibs-hero-badge {{
            display: inline-block; font-size: 11px; font-weight: 700;
            color: #34D399; letter-spacing: 1px; text-transform: uppercase;
            background: rgba(16, 185, 129, 0.14);
            padding: 6px 14px; border-radius: 999px;
            border: 1px solid rgba(52, 211, 153, 0.35);
            backdrop-filter: blur(10px);
            animation: glassPulse 3.2s infinite ease-in-out;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.3);
        }}
        @keyframes glassPulse {{
            0%, 100% {{ box-shadow: 0 0 10px rgba(52, 211, 153, 0.35); }}
            50% {{ box-shadow: 0 0 22px rgba(52, 211, 153, 0.75); }}
        }}
        .sibs-hero-sub-title {{
            font-size: 12px; font-weight: 700; color: #38BDF8; letter-spacing: 1.2px;
            text-transform: uppercase; margin-bottom: 8px;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.7);
        }}
        .sibs-hero-main-title {{
            font-size: 42px; font-weight: 800; line-height: 1.15; color: #FFFFFF !important;
            margin: 0 0 16px 0; letter-spacing: -0.5px; max-width: 840px;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.9);
        }}
        .sibs-hero-paragraph {{
            font-size: 14.5px; line-height: 1.7; color: #E2E8F0 !important;
            max-width: 760px; margin-bottom: 22px; font-weight: 400;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
        }}

        /* Hero Cockpit Footer Bar (Glass Inset) */
        .sibs-hero-footer-bar {{
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;
            margin-top: 26px; padding: 18px 22px;
            background: rgba(10, 16, 32, 0.6) !important;
            backdrop-filter: blur(16px) !important;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-top: 1px solid rgba(255, 255, 255, 0.25);
            box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.15);
        }}
        .sibs-footer-stat-item {{
            display: flex; flex-direction: column; gap: 3px;
        }}
        .stat-label {{
            font-size: 10px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.8px;
        }}
        .stat-value {{
            font-size: 13.5px; font-weight: 700; color: #FFFFFF;
        }}

        /* Sidebar - Glassmorphic */
        [data-testid="stSidebar"], [data-testid="stSidebarContent"] {{
            background: linear-gradient(180deg, rgba(6, 10, 20, 0.95) 0%, rgba(4, 7, 15, 0.98) 100%) !important;
            backdrop-filter: blur(24px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }}
        [data-testid="stSidebar"] * {{ color: #F8FAFC !important; }}

        /* T.RICKS True Glassmorphic Cards (Interactive 3D Hover & Specular Highlights) */
        .sibs-card {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.07) 0%, rgba(255, 255, 255, 0.02) 100%) !important;
            backdrop-filter: blur(22px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(22px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.38) !important;
            border-left: 1px solid rgba(255, 255, 255, 0.22) !important;
            border-radius: 12px !important;
            padding: 22px 26px !important;
            box-shadow: 0 16px 36px 0 rgba(0, 0, 0, 0.45), inset 0 1px 1px 0 rgba(255, 255, 255, 0.25), inset 0 -1px 1px 0 rgba(0, 0, 0, 0.2) !important;
            margin-bottom: 20px !important;
            color: #F8FAFC !important;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }}
        .sibs-card:hover {{
            transform: translateY(-6px) scale(1.012) !important;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.11) 0%, rgba(255, 255, 255, 0.04) 100%) !important;
            border-color: rgba(56, 189, 248, 0.55) !important;
            border-top-color: rgba(125, 211, 252, 0.8) !important;
            box-shadow: 0 24px 50px -10px rgba(0, 0, 0, 0.65), 0 0 30px rgba(56, 189, 248, 0.25), inset 0 1px 1px 0 rgba(255, 255, 255, 0.45) !important;
        }}

        /* KPI Metric Cards (Glass + Glowing Bevel) */
        .sibs-kpi {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.02) 100%) !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.36) !important;
            border-left: 4px solid #38BDF8 !important;
            border-radius: 12px !important;
            padding: 18px 22px !important;
            height: 100%;
            box-shadow: 0 14px 34px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.25) !important;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }}
        .sibs-kpi:hover {{
            transform: translateY(-5px) scale(1.01) !important;
            border-top-color: rgba(125, 211, 252, 0.8) !important;
            box-shadow: 0 22px 46px rgba(0, 0, 0, 0.55), 0 0 26px rgba(56, 189, 248, 0.22), inset 0 1px 1px rgba(255, 255, 255, 0.45) !important;
        }}
        .sibs-kpi-label {{
            color: #94A3B8 !important; font-size: 11px !important; font-weight: 700 !important;
            text-transform: uppercase !important; letter-spacing: 0.8px !important; margin-bottom: 6px !important;
        }}
        .sibs-kpi-value {{
            color: #FFFFFF !important; font-size: 26px !important; font-weight: 800 !important; margin-bottom: 4px !important;
            letter-spacing: -0.5px !important; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
        }}
        .sibs-kpi-sub {{
            color: #64748B !important; font-size: 12px !important; font-weight: 500 !important;
        }}

        /* Frosted Glass Status Pills */
        .status-pill-green {{
            display:inline-block; background:rgba(5, 150, 105, 0.22); color:#34D399 !important;
            font-size:10.5px; font-weight:700; padding:4px 11px; border-radius:999px;
            border:1px solid rgba(52, 211, 153, 0.45); backdrop-filter:blur(10px);
            box-shadow:0 2px 8px rgba(5, 150, 105, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.3);
            letter-spacing:0.5px;
        }}
        .status-pill-navy {{
            display:inline-block; background:rgba(37, 99, 235, 0.22); color:#93C5FD !important;
            font-size:10.5px; font-weight:700; padding:4px 11px; border-radius:999px;
            border:1px solid rgba(96, 165, 250, 0.45); backdrop-filter:blur(10px);
            box-shadow:0 2px 8px rgba(37, 99, 235, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.3);
            letter-spacing:0.5px;
        }}
        .status-pill-red {{
            display:inline-block; background:rgba(220, 38, 38, 0.22); color:#FCA5A5 !important;
            font-size:10.5px; font-weight:700; padding:4px 11px; border-radius:999px;
            border:1px solid rgba(248, 113, 113, 0.45); backdrop-filter:blur(10px);
            box-shadow:0 2px 8px rgba(220, 38, 38, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.3);
            letter-spacing:0.5px;
        }}
        .status-pill-yellow {{
            display:inline-block; background:rgba(217, 119, 6, 0.22); color:#FCD34D !important;
            font-size:10.5px; font-weight:700; padding:4px 11px; border-radius:999px;
            border:1px solid rgba(251, 191, 36, 0.45); backdrop-filter:blur(10px);
            box-shadow:0 2px 8px rgba(217, 119, 6, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.3);
            letter-spacing:0.5px;
        }}

        /* Interactive Modern Glass Buttons */
        .stButton > button, [data-testid="stFormSubmitButton"] > button, [data-testid="stDownloadButton"] > button {{
            background: linear-gradient(135deg, rgba(14, 165, 233, 0.88) 0%, rgba(2, 132, 199, 0.92) 100%) !important;
            color: #FFFFFF !important;
            backdrop-filter: blur(14px) !important;
            -webkit-backdrop-filter: blur(14px) !important;
            border: 1px solid rgba(56, 189, 248, 0.45) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.55) !important;
            border-radius: 9px !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            padding: 0.65rem 1.4rem !important;
            transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
            box-shadow: 0 8px 20px rgba(2, 132, 199, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.35) !important;
        }}
        .stButton > button:hover {{
            transform: translateY(-3px) scale(1.02) !important;
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.95) 0%, rgba(14, 165, 233, 0.98) 100%) !important;
            border-color: #7DD3FC !important;
            box-shadow: 0 14px 30px rgba(14, 165, 233, 0.55), inset 0 1px 1px #FFFFFF !important;
        }}
        .stButton > button:active {{ transform: translateY(0px) scale(0.99) !important; }}

        /* Primary Emerald Glass Button (Glowing Highlight) */
        button[kind="primary"], [data-testid="stBaseButton-primary"] {{
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.95) 0%, rgba(5, 150, 105, 0.95) 100%) !important;
            backdrop-filter: blur(14px) !important;
            border: 1px solid rgba(52, 211, 153, 0.6) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.65) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            letter-spacing: 0.3px !important;
            border-radius: 9px !important;
            box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.5) !important;
            transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }}
        button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover {{
            background: linear-gradient(135deg, rgba(52, 211, 153, 0.98) 0%, rgba(16, 185, 129, 1) 100%) !important;
            box-shadow: 0 16px 36px rgba(16, 185, 129, 0.65), inset 0 1px 1px #FFFFFF !important;
            transform: translateY(-3px) scale(1.02) !important;
        }}

        /* Frosted Glass Theme Capsule Toggle (Top Right of Hero) */
        .st-key-hero_switch_theme button, .st-key-switch_theme_hero button {{
            background: rgba(255, 255, 255, 0.14) !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.28) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.6) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 12px !important;
            border-radius: 999px !important;
            padding: 0.45rem 1.1rem !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.4) !important;
            transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }}
        .st-key-hero_switch_theme button:hover, .st-key-switch_theme_hero button:hover {{
            background: rgba(255, 255, 255, 0.25) !important;
            border-color: rgba(255, 255, 255, 0.7) !important;
            transform: translateY(-2px) scale(1.03) !important;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5), inset 0 1px 1px #FFFFFF !important;
        }}

        /* Floating Support Glass Capsule */
        .sibs-floating-support {{
            position: fixed; bottom: 24px; right: 28px; z-index: 999;
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.9) 0%, rgba(5, 150, 105, 0.95) 100%);
            backdrop-filter: blur(20px) saturate(180%);
            color: #FFFFFF; padding: 11px 20px; border-radius: 999px;
            display: flex; align-items: center; gap: 8px; font-size: 12.5px; font-weight: 700;
            box-shadow: 0 14px 38px rgba(16, 185, 129, 0.45), inset 0 1px 1px rgba(255, 255, 255, 0.5);
            border: 1px solid rgba(52, 211, 153, 0.6);
            border-top: 1px solid rgba(255, 255, 255, 0.7);
            text-decoration: none; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .sibs-floating-support:hover {{
            transform: translateY(-4px) scale(1.03);
            box-shadow: 0 20px 48px rgba(16, 185, 129, 0.65), inset 0 1px 1px #FFFFFF;
            color: #FFFFFF;
        }}

        /* Inputs & Controls (Frosted Glass Fields) */
        input, textarea, select,
        [data-baseweb="input"], [data-baseweb="input"] > div, [data-baseweb="select"] > div,
        [data-baseweb="base-input"], [data-testid="stNumberInputContainer"], [data-testid="stForm"] {{
            background: rgba(15, 23, 42, 0.75) !important;
            backdrop-filter: blur(16px) !important;
            color: #F8FAFC !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 8px !important;
            box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.4) !important;
        }}

        /* Clean Minimalist Modern Tabs (Dark Mode - No Clunky Box Overlays) */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 24px !important;
            background: transparent !important;
            padding: 0 0 4px 0 !important;
            border: none !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.12) !important;
            margin-bottom: 18px !important;
        }}
        .stTabs [data-baseweb="tab-highlight"],
        .stTabs [data-baseweb="tab-border"] {{
            display: none !important;
        }}
        .stTabs [data-baseweb="tab"] {{
            background: transparent !important;
            border: none !important;
            border-bottom: 2px solid transparent !important;
            color: #94A3B8 !important;
            font-weight: 600 !important;
            font-size: 13.5px !important;
            padding: 8px 4px 12px 4px !important;
            margin: 0 !important;
            border-radius: 0 !important;
            box-shadow: none !important;
            transition: all 0.2s ease !important;
        }}
        .stTabs [data-baseweb="tab"]:hover {{
            color: #FFFFFF !important;
            background: transparent !important;
            border-bottom: 2px solid rgba(56, 189, 248, 0.45) !important;
        }}
        .stTabs [data-baseweb="tab"] p,
        .stTabs [data-baseweb="tab"] div,
        .stTabs [data-baseweb="tab"] span {{
            color: inherit !important;
            font-size: inherit !important;
            font-weight: inherit !important;
        }}
        .stTabs [aria-selected="true"] {{
            background: transparent !important;
            border-bottom: 2px solid #38BDF8 !important;
            color: #38BDF8 !important;
            box-shadow: none !important;
        }}
        .stTabs [aria-selected="true"] p,
        .stTabs [aria-selected="true"] div,
        .stTabs [aria-selected="true"] span {{
            color: #38BDF8 !important;
            font-weight: 700 !important;
        }}

        h1, h2, h3, h4, h5, h6 {{ color:#F8FAFC !important; }}
        p, span, label, div {{ color:#CBD5E1; }}

        /* Header Status Box Base */
        .sibs-header-status-box {{
            text-align: right;
            padding-top: 8px;
        }}
        .sibs-header-date {{
            font-size: 11px;
            opacity: 0.7;
            margin-top: 4px;
        }}

        /* =========================================================================
           RESPONSIVE DESIGN SYSTEM (PC, TABLET, HANDPHONE) — DARK MODE
           ========================================================================= */

        /* 1. PC / DESKTOP (> 1024px) */
        @media screen and (min-width: 1025px) {{
            .block-container {{
                padding: 1.25rem 3.5rem 3rem 3.5rem !important;
                max-width: 1440px !important;
            }}
            .sibs-navbar-container {{
                padding: 16px 32px !important;
            }}
            .sibs-hero-wrapper, .st-key-sibs_hero_section {{
                padding: 38px 46px 40px 46px !important;
            }}
            .sibs-hero-main-title {{
                font-size: 42px !important;
            }}
            .sibs-hero-footer-bar {{
                grid-template-columns: repeat(4, 1fr) !important;
            }}
        }}

        /* 2. TABLET (641px - 1024px) */
        @media screen and (min-width: 641px) and (max-width: 1024px) {{
            .block-container {{
                padding: 1rem 1.75rem 2.5rem 1.75rem !important;
                max-width: 100% !important;
            }}
            .sibs-navbar-container {{
                padding: 14px 20px !important;
                margin-bottom: 18px !important;
            }}
            .sibs-brand-title {{
                font-size: 16.5px !important;
            }}
            .sibs-brand-sub {{
                font-size: 9.5px !important;
                padding-left: 8px !important;
            }}
            .sibs-nav-links {{
                gap: 14px !important;
            }}
            .sibs-nav-link {{
                font-size: 12px !important;
            }}
            .sibs-hero-wrapper, .st-key-sibs_hero_section {{
                padding: 28px 24px 30px 24px !important;
                border-radius: 14px !important;
                margin-bottom: 20px !important;
            }}
            .sibs-hero-main-title {{
                font-size: 30px !important;
                line-height: 1.2 !important;
            }}
            .sibs-hero-paragraph {{
                font-size: 13.5px !important;
                line-height: 1.6 !important;
            }}
            .sibs-hero-footer-bar {{
                grid-template-columns: repeat(2, 1fr) !important;
                gap: 12px !important;
                padding: 14px 18px !important;
            }}
            .sibs-card {{
                padding: 18px 20px !important;
            }}
            .sibs-kpi {{
                padding: 16px 18px !important;
            }}
            .sibs-kpi-value {{
                font-size: 23px !important;
            }}

            /* Responsive wrapping for 3+ column layouts on tablet */
            div[data-testid="stHorizontalBlock"]:has(> div[data-testid="column"]:nth-child(3)) {{
                flex-wrap: wrap !important;
                gap: 14px !important;
            }}
            div[data-testid="stHorizontalBlock"]:has(> div[data-testid="column"]:nth-child(3)) > div[data-testid="column"] {{
                flex: 1 1 calc(50% - 14px) !important;
                min-width: calc(50% - 14px) !important;
                max-width: 100% !important;
            }}

            .stTabs [data-baseweb="tab-list"] {{
                gap: 16px !important;
                overflow-x: auto !important;
                flex-wrap: nowrap !important;
                -webkit-overflow-scrolling: touch !important;
            }}
            .stTabs [data-baseweb="tab"] {{
                font-size: 13px !important;
                white-space: nowrap !important;
                flex-shrink: 0 !important;
            }}
            .sibs-floating-support {{
                bottom: 18px !important;
                right: 18px !important;
                padding: 9px 16px !important;
                font-size: 12px !important;
            }}
        }}

        /* 3. HANDPHONE / MOBILE (<= 640px) */
        @media screen and (max-width: 640px) {{
            .block-container {{
                padding: 0.75rem 0.75rem 2.5rem 0.75rem !important;
                max-width: 100% !important;
            }}

            /* Mobile Navbar (Stacked Header + Smooth Horizontal Swipable Links) */
            .sibs-navbar-container {{
                flex-direction: column !important;
                align-items: stretch !important;
                padding: 12px 14px !important;
                margin-bottom: 14px !important;
                gap: 10px !important;
                border-radius: 10px !important;
            }}
            .sibs-brand-title {{
                font-size: 15px !important;
                justify-content: flex-start !important;
                gap: 8px !important;
            }}
            .sibs-brand-sub {{
                display: none !important;
            }}
            .sibs-nav-links {{
                display: flex !important;
                flex-wrap: nowrap !important;
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch !important;
                gap: 12px !important;
                padding: 6px 2px 4px 2px !important;
                scrollbar-width: none !important;
                border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
            }}
            .sibs-nav-links::-webkit-scrollbar {{
                display: none !important;
            }}
            .sibs-nav-link {{
                font-size: 11.5px !important;
                white-space: nowrap !important;
                flex-shrink: 0 !important;
            }}

            /* Mobile Hero */
            .sibs-hero-wrapper, .st-key-sibs_hero_section {{
                padding: 18px 14px 20px 14px !important;
                border-radius: 12px !important;
                margin-bottom: 16px !important;
                background-position: center center !important;
            }}
            .sibs-hero-tag, .sibs-hero-badge {{
                font-size: 9px !important;
                padding: 4px 8px !important;
                letter-spacing: 0.4px !important;
            }}
            .sibs-hero-sub-title {{
                font-size: 10px !important;
                letter-spacing: 0.8px !important;
                margin-bottom: 4px !important;
            }}
            .sibs-hero-main-title {{
                font-size: 22px !important;
                line-height: 1.25 !important;
                margin: 6px 0 10px 0 !important;
            }}
            .sibs-hero-paragraph {{
                font-size: 12px !important;
                line-height: 1.55 !important;
                margin-bottom: 14px !important;
            }}

            /* Switch Mode Button on Mobile */
            .st-key-hero_switch_theme, .st-key-switch_theme_hero {{
                display: flex !important;
                justify-content: flex-start !important;
                margin-top: 6px !important;
            }}
            .st-key-hero_switch_theme button, .st-key-switch_theme_hero button {{
                width: auto !important;
                padding: 5px 14px !important;
                font-size: 11px !important;
            }}

            /* Mobile Cockpit Footer Strip */
            .sibs-hero-footer-bar {{
                grid-template-columns: 1fr !important;
                gap: 8px !important;
                padding: 12px 14px !important;
                margin-top: 14px !important;
                border-radius: 8px !important;
            }}
            .sibs-footer-stat-item {{
                padding-bottom: 6px !important;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
            }}
            .sibs-footer-stat-item:last-child {{
                border-bottom: none !important;
                padding-bottom: 0 !important;
            }}
            .stat-label {{
                font-size: 9px !important;
            }}
            .stat-value {{
                font-size: 12px !important;
            }}

            /* Streamlit Columns Stacking on Handphone */
            div[data-testid="stHorizontalBlock"] {{
                flex-direction: column !important;
                flex-wrap: nowrap !important;
                gap: 12px !important;
            }}
            div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {{
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
                margin-bottom: 0px !important;
            }}
            div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:empty {{
                display: none !important;
            }}

            /* Mobile Buttons */
            .stButton > button, [data-testid="stFormSubmitButton"] > button, [data-testid="stDownloadButton"] > button {{
                width: 100% !important;
                font-size: 12.5px !important;
                padding: 0.65rem 1rem !important;
                min-height: 42px !important;
            }}

            /* Mobile Cards & KPIs */
            .sibs-card {{
                padding: 14px 14px !important;
                border-radius: 10px !important;
                margin-bottom: 12px !important;
            }}
            .sibs-kpi {{
                padding: 12px 14px !important;
                border-radius: 10px !important;
                margin-bottom: 8px !important;
            }}
            .sibs-kpi-label {{
                font-size: 9.5px !important;
                margin-bottom: 4px !important;
            }}
            .sibs-kpi-value {{
                font-size: 20px !important;
                margin-bottom: 2px !important;
            }}
            .sibs-kpi-sub {{
                font-size: 10.5px !important;
            }}

            /* Mobile Tabs (Horizontal Swipe) */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 12px !important;
                overflow-x: auto !important;
                flex-wrap: nowrap !important;
                -webkit-overflow-scrolling: touch !important;
                scrollbar-width: none !important;
                padding-bottom: 4px !important;
                margin-bottom: 12px !important;
            }}
            .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {{
                display: none !important;
            }}
            .stTabs [data-baseweb="tab"] {{
                font-size: 12px !important;
                padding: 6px 2px 8px 2px !important;
                white-space: nowrap !important;
                flex-shrink: 0 !important;
            }}

            /* Header Status Box on Mobile */
            .sibs-header-status-box {{
                text-align: left !important;
                padding-top: 0 !important;
                margin-top: -8px !important;
                margin-bottom: 8px !important;
                display: flex !important;
                align-items: center !important;
                gap: 10px !important;
            }}
            .sibs-header-date {{
                font-size: 11px !important;
                opacity: 0.7 !important;
                margin-top: 0 !important;
            }}

            /* Mobile Tables & Dataframes */
            [data-testid="stDataFrame"], [data-testid="stTable"] {{
                width: 100% !important;
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch !important;
            }}
            .sibs-card table td {{
                font-size: 11px !important;
                padding: 5px 0 !important;
            }}

            /* Mobile Floating Support */
            .sibs-floating-support {{
                bottom: 12px !important;
                right: 12px !important;
                padding: 7px 12px !important;
                font-size: 11px !important;
                gap: 5px !important;
            }}

            /* Mobile Inputs */
            input, textarea, select, [data-baseweb="select"] {{
                font-size: 14px !important;
                min-height: 40px !important;
            }}

            /* Mobile Sidebar */
            [data-testid="stSidebar"] {{
                width: 84vw !important;
                max-width: 320px !important;
            }}
        }}

        /* Print Media */
        @media print {{
            [data-testid="stSidebar"], header, footer, .stButton, .stTabs, hr, .sibs-floating-support {{ display:none !important; }}
            .block-container {{ padding:0 !important; margin:0 !important; max-width:100% !important; background-color:#FFFFFF !important; }}
            .bap-print-container {{
                background-color:#FFFFFF !important; color:#000000 !important; padding:25px !important;
                font-family:'Times New Roman',Times,serif !important; border:none !important;
            }}
            .bap-print-container * {{ color:#000000 !important; }}
        }}
        </style>
        """, unsafe_allow_html=True)

    else:
        # LIGHT MODE (Glacial Frosted Quartz / Modern Glass White)
        st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

        :root {{ color-scheme: light !important; }}
        html, body, [class*="css"] {{
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
        }}

        /* Ambient Glacial Light Mesh Background */
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            background-color: #F8FAFC !important;
            background-image: 
                radial-gradient(circle at 10% 12%, rgba(186, 230, 253, 0.5) 0%, transparent 45%),
                radial-gradient(circle at 90% 18%, rgba(167, 243, 208, 0.42) 0%, transparent 40%),
                radial-gradient(circle at 50% 55%, rgba(224, 242, 254, 0.45) 0%, transparent 55%),
                radial-gradient(circle at 85% 88%, rgba(199, 210, 254, 0.38) 0%, transparent 45%),
                radial-gradient(circle at 15% 90%, rgba(241, 245, 249, 0.95) 0%, transparent 50%) !important;
            background-attachment: fixed !important;
            color: #0F172A !important;
        }}
        .block-container {{
            padding: 1.25rem 3.5rem 3rem 3.5rem !important;
            max-width: 1440px !important; background-color: transparent !important;
        }}

        /* Floating Frosted Glass Navbar */
        .sibs-navbar-container {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 16px 32px;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.82) 0%, rgba(248, 250, 252, 0.88) 100%) !important;
            backdrop-filter: blur(28px) saturate(190%) !important;
            -webkit-backdrop-filter: blur(28px) saturate(190%) !important;
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
            border-top: 1px solid #FFFFFF !important;
            border-radius: 12px; margin-bottom: 22px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05), inset 0 1px 1px #FFFFFF !important;
        }}
        .sibs-brand-title {{
            font-size: 19px; font-weight: 800; color: #0F172A; letter-spacing: 0.5px;
            display: flex; align-items: center; gap: 12px;
        }}
        .sibs-brand-sub {{
            font-size: 10.5px; font-weight: 600; color: #64748B; letter-spacing: 0.3px;
            border-left: 2px solid #CBD5E1; padding-left: 10px;
        }}
        .sibs-nav-links {{
            display: flex; align-items: center; gap: 26px; list-style: none; margin: 0; padding: 0;
        }}
        .sibs-nav-link {{
            color: #64748B; text-decoration: none; font-size: 13px; font-weight: 600;
            padding-bottom: 4px; transition: all 0.25s ease;
        }}
        .sibs-nav-link:hover {{
            color: #0284C7; text-shadow: 0 0 10px rgba(2, 132, 199, 0.3);
        }}
        .sibs-nav-link.active {{
            color: #0284C7 !important; border-bottom: 2px solid #0284C7 !important;
        }}

        /* Hero Container with Layered Glass */
        .st-key-sibs_hero_section, .sibs-hero-wrapper {{
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.88) 0%, rgba(30, 58, 138, 0.78) 50%, rgba(15, 23, 42, 0.65) 100%),
                        url('data:image/jpeg;base64,{hero_b64}') !important;
            background-size: cover !important;
            background-position: center 36% !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-radius: 16px !important;
            padding: 38px 46px 40px 46px !important;
            margin-bottom: 26px !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.5) !important;
            box-shadow: 0 24px 50px rgba(15, 23, 42, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.4) !important;
        }}
        .sibs-hero-tag {{
            display: inline-block; font-size: 11px; font-weight: 700;
            color: #38BDF8; letter-spacing: 1.5px; text-transform: uppercase;
            background: rgba(56, 189, 248, 0.18);
            padding: 6px 14px; border-radius: 999px;
            border: 1px solid rgba(56, 189, 248, 0.4);
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 14px rgba(56, 189, 248, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.35);
        }}
        .sibs-hero-badge {{
            display: inline-block; font-size: 11px; font-weight: 700;
            color: #34D399; letter-spacing: 1px; text-transform: uppercase;
            background: rgba(16, 185, 129, 0.18);
            padding: 6px 14px; border-radius: 999px;
            border: 1px solid rgba(52, 211, 153, 0.4);
            backdrop-filter: blur(10px);
            animation: glassPulse 3.2s infinite ease-in-out;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.22), inset 0 1px 0 rgba(255, 255, 255, 0.35);
        }}
        .sibs-hero-sub-title {{
            font-size: 12px; font-weight: 700; color: #38BDF8; letter-spacing: 1.2px;
            text-transform: uppercase; margin-bottom: 8px;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.7);
        }}
        .sibs-hero-main-title {{
            font-size: 42px; font-weight: 800; line-height: 1.15; color: #FFFFFF !important;
            margin: 0 0 16px 0; letter-spacing: -0.5px; max-width: 840px;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.9);
        }}
        .sibs-hero-paragraph {{
            font-size: 14.5px; line-height: 1.7; color: #F1F5F9 !important;
            max-width: 760px; margin-bottom: 22px; font-weight: 400;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
        }}

        /* Hero Cockpit Footer Bar */
        .sibs-hero-footer-bar {{
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;
            margin-top: 26px; padding: 18px 22px;
            background: rgba(15, 23, 42, 0.65) !important;
            backdrop-filter: blur(16px) !important;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-top: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.2);
        }}
        .sibs-footer-stat-item {{
            display: flex; flex-direction: column; gap: 3px;
        }}
        .stat-label {{
            font-size: 10px; font-weight: 700; color: #CBD5E1; text-transform: uppercase; letter-spacing: 0.8px;
        }}
        .stat-value {{
            font-size: 13.5px; font-weight: 700; color: #FFFFFF;
        }}

        /* Sidebar - Light Glass */
        [data-testid="stSidebar"], [data-testid="stSidebarContent"] {{
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.95) 100%) !important;
            backdrop-filter: blur(24px) !important;
            border-right: 1px solid #E2E8F0 !important;
        }}
        [data-testid="stSidebar"] * {{ color: #0F172A !important; }}

        /* T.RICKS True Glassmorphic Cards (Glacial Quartz Light) */
        .sibs-card {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.82) 0%, rgba(255, 255, 255, 0.6) 100%) !important;
            backdrop-filter: blur(22px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(22px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
            border-top: 1px solid #FFFFFF !important;
            border-left: 1px solid rgba(255, 255, 255, 0.9) !important;
            border-radius: 12px !important;
            padding: 22px 26px !important;
            box-shadow: 0 12px 32px rgba(15, 23, 42, 0.06), inset 0 1px 1px #FFFFFF, inset 0 -1px 1px rgba(0, 0, 0, 0.03) !important;
            margin-bottom: 20px !important;
            color: #0F172A !important;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }}
        .sibs-card:hover {{
            transform: translateY(-6px) scale(1.012) !important;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.75) 100%) !important;
            border-color: rgba(2, 132, 199, 0.4) !important;
            box-shadow: 0 20px 42px rgba(15, 23, 42, 0.1), 0 0 24px rgba(2, 132, 199, 0.15), inset 0 1px 1px #FFFFFF !important;
        }}

        /* KPI Metric Cards */
        .sibs-kpi {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.82) 0%, rgba(255, 255, 255, 0.6) 100%) !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
            border-top: 1px solid #FFFFFF !important;
            border-left: 4px solid #0284C7 !important;
            border-radius: 12px !important;
            padding: 18px 22px !important;
            height: 100%;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05), inset 0 1px 1px #FFFFFF !important;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }}
        .sibs-kpi:hover {{
            transform: translateY(-5px) scale(1.01) !important;
            box-shadow: 0 18px 38px rgba(15, 23, 42, 0.09), inset 0 1px 1px #FFFFFF !important;
        }}
        .sibs-kpi-label {{
            color: #64748B !important; font-size: 11px !important; font-weight: 700 !important;
            text-transform: uppercase !important; letter-spacing: 0.8px !important; margin-bottom: 6px !important;
        }}
        .sibs-kpi-value {{
            color: #0F172A !important; font-size: 26px !important; font-weight: 800 !important; margin-bottom: 4px !important;
            letter-spacing: -0.5px !important;
        }}
        .sibs-kpi-sub {{
            color: #475569 !important; font-size: 12px !important; font-weight: 500 !important;
        }}

        /* Status Pills */
        .status-pill-green {{
            display:inline-block; background:rgba(220, 252, 231, 0.85); color:#15803D !important;
            font-size:10.5px; font-weight:700; padding:4px 11px; border-radius:999px;
            border:1px solid #86EFAC; backdrop-filter:blur(8px);
            box-shadow:0 2px 8px rgba(22, 163, 74, 0.15), inset 0 1px 0 #FFFFFF;
            letter-spacing:0.5px;
        }}
        .status-pill-navy {{
            display:inline-block; background:rgba(224, 242, 254, 0.85); color:#0369A1 !important;
            font-size:10.5px; font-weight:700; padding:4px 11px; border-radius:999px;
            border:1px solid #7DD3FC; backdrop-filter:blur(8px);
            box-shadow:0 2px 8px rgba(2, 132, 199, 0.15), inset 0 1px 0 #FFFFFF;
            letter-spacing:0.5px;
        }}
        .status-pill-red {{
            display:inline-block; background:rgba(254, 226, 226, 0.85); color:#B91C1C !important;
            font-size:10.5px; font-weight:700; padding:4px 11px; border-radius:999px;
            border:1px solid #FCA5A5; backdrop-filter:blur(8px);
            box-shadow:0 2px 8px rgba(220, 38, 38, 0.15), inset 0 1px 0 #FFFFFF;
            letter-spacing:0.5px;
        }}
        .status-pill-yellow {{
            display:inline-block; background:rgba(254, 249, 195, 0.85); color:#A16207 !important;
            font-size:10.5px; font-weight:700; padding:4px 11px; border-radius:999px;
            border:1px solid #FDE047; backdrop-filter:blur(8px);
            box-shadow:0 2px 8px rgba(202, 138, 4, 0.15), inset 0 1px 0 #FFFFFF;
            letter-spacing:0.5px;
        }}

        /* Modern Responsive Dynamic Buttons */
        .stButton > button, [data-testid="stFormSubmitButton"] > button, [data-testid="stDownloadButton"] > button {{
            background: linear-gradient(135deg, rgba(2, 132, 199, 0.9) 0%, rgba(3, 105, 161, 0.95) 100%) !important;
            color: #FFFFFF !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid #0284C7 !important;
            border-top: 1px solid rgba(255, 255, 255, 0.5) !important;
            border-radius: 9px !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            padding: 0.65rem 1.4rem !important;
            transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
            box-shadow: 0 6px 18px rgba(2, 132, 199, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.4) !important;
        }}
        .stButton > button:hover {{
            transform: translateY(-3px) scale(1.02) !important;
            background: linear-gradient(135deg, rgba(14, 165, 233, 0.95) 0%, rgba(2, 132, 199, 1) 100%) !important;
            box-shadow: 0 12px 26px rgba(2, 132, 199, 0.4), inset 0 1px 1px #FFFFFF !important;
        }}
        .stButton > button:active {{ transform: translateY(0px) scale(0.99) !important; }}

        /* Primary Green CTA Button */
        button[kind="primary"], [data-testid="stBaseButton-primary"] {{
            background: linear-gradient(135deg, rgba(22, 163, 74, 0.95) 0%, rgba(21, 128, 61, 0.98) 100%) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid #16A34A !important;
            border-top: 1px solid rgba(255, 255, 255, 0.6) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            letter-spacing: 0.3px !important;
            border-radius: 9px !important;
            box-shadow: 0 6px 20px rgba(22, 163, 74, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.5) !important;
            transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }}
        button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover {{
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.98) 0%, rgba(22, 163, 74, 1) 100%) !important;
            box-shadow: 0 14px 32px rgba(22, 163, 74, 0.55), inset 0 1px 1px #FFFFFF !important;
            transform: translateY(-3px) scale(1.02) !important;
        }}

        /* Frosted Glass Theme Toggle */
        .st-key-hero_switch_theme button, .st-key-switch_theme_hero button {{
            background: rgba(255, 255, 255, 0.2) !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.7) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 12px !important;
            border-radius: 999px !important;
            padding: 0.45rem 1.1rem !important;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.45) !important;
            transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }}
        .st-key-hero_switch_theme button:hover, .st-key-switch_theme_hero button:hover {{
            background: rgba(255, 255, 255, 0.35) !important;
            border-color: #FFFFFF !important;
            transform: translateY(-2px) scale(1.03) !important;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.3), inset 0 1px 1px #FFFFFF !important;
        }}

        /* Floating Support Pill */
        .sibs-floating-support {{
            position: fixed; bottom: 24px; right: 28px; z-index: 999;
            background: linear-gradient(135deg, rgba(22, 163, 74, 0.92) 0%, rgba(21, 128, 61, 0.98) 100%);
            backdrop-filter: blur(20px) saturate(180%);
            color: #FFFFFF; padding: 11px 20px; border-radius: 999px;
            display: flex; align-items: center; gap: 8px; font-size: 12.5px; font-weight: 700;
            box-shadow: 0 12px 34px rgba(22, 163, 74, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.5);
            border: 1px solid #16A34A;
            border-top: 1px solid rgba(255, 255, 255, 0.75);
            text-decoration: none; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .sibs-floating-support:hover {{
            transform: translateY(-4px) scale(1.03);
            box-shadow: 0 18px 42px rgba(22, 163, 74, 0.55), inset 0 1px 1px #FFFFFF;
            color: #FFFFFF;
        }}

        /* Inputs & Controls */
        input, textarea, select,
        [data-baseweb="input"], [data-baseweb="input"] > div, [data-baseweb="select"] > div,
        [data-baseweb="base-input"], [data-testid="stNumberInputContainer"], [data-testid="stForm"] {{
            background: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(16px) !important;
            color: #0F172A !important;
            border: 1px solid #CBD5E1 !important;
            border-top: 1px solid #FFFFFF !important;
            border-radius: 8px !important;
            box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.04) !important;
        }}

        /* Clean Minimalist Modern Tabs (Light Mode - No Clunky Box Overlays) */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 24px !important;
            background: transparent !important;
            padding: 0 0 4px 0 !important;
            border: none !important;
            border-bottom: 1px solid #E2E8F0 !important;
            margin-bottom: 18px !important;
        }}
        .stTabs [data-baseweb="tab-highlight"],
        .stTabs [data-baseweb="tab-border"] {{
            display: none !important;
        }}
        .stTabs [data-baseweb="tab"] {{
            background: transparent !important;
            border: none !important;
            border-bottom: 2px solid transparent !important;
            color: #64748B !important;
            font-weight: 600 !important;
            font-size: 13.5px !important;
            padding: 8px 4px 12px 4px !important;
            margin: 0 !important;
            border-radius: 0 !important;
            box-shadow: none !important;
            transition: all 0.2s ease !important;
        }}
        .stTabs [data-baseweb="tab"]:hover {{
            color: #0F172A !important;
            background: transparent !important;
            border-bottom: 2px solid #94A3B8 !important;
        }}
        .stTabs [data-baseweb="tab"] p,
        .stTabs [data-baseweb="tab"] div,
        .stTabs [data-baseweb="tab"] span {{
            color: inherit !important;
            font-size: inherit !important;
            font-weight: inherit !important;
        }}
        .stTabs [aria-selected="true"] {{
            background: transparent !important;
            border-bottom: 2px solid #0284C7 !important;
            color: #0284C7 !important;
            box-shadow: none !important;
        }}
        .stTabs [aria-selected="true"] p,
        .stTabs [aria-selected="true"] div,
        .stTabs [aria-selected="true"] span {{
            color: #0284C7 !important;
            font-weight: 700 !important;
        }}

        h1, h2, h3, h4, h5, h6 {{ color:#0F172A !important; }}
        p, span, label, div {{ color:#334155; }}

        /* Header Status Box Base */
        .sibs-header-status-box {{
            text-align: right;
            padding-top: 8px;
        }}
        .sibs-header-date {{
            font-size: 11px;
            opacity: 0.7;
            margin-top: 4px;
        }}

        /* =========================================================================
           RESPONSIVE DESIGN SYSTEM (PC, TABLET, HANDPHONE) — DARK MODE
           ========================================================================= */

        /* 1. PC / DESKTOP (> 1024px) */
        @media screen and (min-width: 1025px) {{
            .block-container {{
                padding: 1.25rem 3.5rem 3rem 3.5rem !important;
                max-width: 1440px !important;
            }}
            .sibs-navbar-container {{
                padding: 16px 32px !important;
            }}
            .sibs-hero-wrapper, .st-key-sibs_hero_section {{
                padding: 38px 46px 40px 46px !important;
            }}
            .sibs-hero-main-title {{
                font-size: 42px !important;
            }}
            .sibs-hero-footer-bar {{
                grid-template-columns: repeat(4, 1fr) !important;
            }}
        }}

        /* 2. TABLET (641px - 1024px) */
        @media screen and (min-width: 641px) and (max-width: 1024px) {{
            .block-container {{
                padding: 1rem 1.75rem 2.5rem 1.75rem !important;
                max-width: 100% !important;
            }}
            .sibs-navbar-container {{
                padding: 14px 20px !important;
                margin-bottom: 18px !important;
            }}
            .sibs-brand-title {{
                font-size: 16.5px !important;
            }}
            .sibs-brand-sub {{
                font-size: 9.5px !important;
                padding-left: 8px !important;
            }}
            .sibs-nav-links {{
                gap: 14px !important;
            }}
            .sibs-nav-link {{
                font-size: 12px !important;
            }}
            .sibs-hero-wrapper, .st-key-sibs_hero_section {{
                padding: 28px 24px 30px 24px !important;
                border-radius: 14px !important;
                margin-bottom: 20px !important;
            }}
            .sibs-hero-main-title {{
                font-size: 30px !important;
                line-height: 1.2 !important;
            }}
            .sibs-hero-paragraph {{
                font-size: 13.5px !important;
                line-height: 1.6 !important;
            }}
            .sibs-hero-footer-bar {{
                grid-template-columns: repeat(2, 1fr) !important;
                gap: 12px !important;
                padding: 14px 18px !important;
            }}
            .sibs-card {{
                padding: 18px 20px !important;
            }}
            .sibs-kpi {{
                padding: 16px 18px !important;
            }}
            .sibs-kpi-value {{
                font-size: 23px !important;
            }}

            /* Responsive wrapping for 3+ column layouts on tablet */
            div[data-testid="stHorizontalBlock"]:has(> div[data-testid="column"]:nth-child(3)) {{
                flex-wrap: wrap !important;
                gap: 14px !important;
            }}
            div[data-testid="stHorizontalBlock"]:has(> div[data-testid="column"]:nth-child(3)) > div[data-testid="column"] {{
                flex: 1 1 calc(50% - 14px) !important;
                min-width: calc(50% - 14px) !important;
                max-width: 100% !important;
            }}

            .stTabs [data-baseweb="tab-list"] {{
                gap: 16px !important;
                overflow-x: auto !important;
                flex-wrap: nowrap !important;
                -webkit-overflow-scrolling: touch !important;
            }}
            .stTabs [data-baseweb="tab"] {{
                font-size: 13px !important;
                white-space: nowrap !important;
                flex-shrink: 0 !important;
            }}
            .sibs-floating-support {{
                bottom: 18px !important;
                right: 18px !important;
                padding: 9px 16px !important;
                font-size: 12px !important;
            }}
        }}

        /* 3. HANDPHONE / MOBILE (<= 640px) */
        @media screen and (max-width: 640px) {{
            .block-container {{
                padding: 0.75rem 0.75rem 2.5rem 0.75rem !important;
                max-width: 100% !important;
            }}

            /* Mobile Navbar (Stacked Header + Smooth Horizontal Swipable Links) */
            .sibs-navbar-container {{
                flex-direction: column !important;
                align-items: stretch !important;
                padding: 12px 14px !important;
                margin-bottom: 14px !important;
                gap: 10px !important;
                border-radius: 10px !important;
            }}
            .sibs-brand-title {{
                font-size: 15px !important;
                justify-content: flex-start !important;
                gap: 8px !important;
            }}
            .sibs-brand-sub {{
                display: none !important;
            }}
            .sibs-nav-links {{
                display: flex !important;
                flex-wrap: nowrap !important;
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch !important;
                gap: 12px !important;
                padding: 6px 2px 4px 2px !important;
                scrollbar-width: none !important;
                border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
            }}
            .sibs-nav-links::-webkit-scrollbar {{
                display: none !important;
            }}
            .sibs-nav-link {{
                font-size: 11.5px !important;
                white-space: nowrap !important;
                flex-shrink: 0 !important;
            }}

            /* Mobile Hero */
            .sibs-hero-wrapper, .st-key-sibs_hero_section {{
                padding: 18px 14px 20px 14px !important;
                border-radius: 12px !important;
                margin-bottom: 16px !important;
                background-position: center center !important;
            }}
            .sibs-hero-tag, .sibs-hero-badge {{
                font-size: 9px !important;
                padding: 4px 8px !important;
                letter-spacing: 0.4px !important;
            }}
            .sibs-hero-sub-title {{
                font-size: 10px !important;
                letter-spacing: 0.8px !important;
                margin-bottom: 4px !important;
            }}
            .sibs-hero-main-title {{
                font-size: 22px !important;
                line-height: 1.25 !important;
                margin: 6px 0 10px 0 !important;
            }}
            .sibs-hero-paragraph {{
                font-size: 12px !important;
                line-height: 1.55 !important;
                margin-bottom: 14px !important;
            }}

            /* Switch Mode Button on Mobile */
            .st-key-hero_switch_theme, .st-key-switch_theme_hero {{
                display: flex !important;
                justify-content: flex-start !important;
                margin-top: 6px !important;
            }}
            .st-key-hero_switch_theme button, .st-key-switch_theme_hero button {{
                width: auto !important;
                padding: 5px 14px !important;
                font-size: 11px !important;
            }}

            /* Mobile Cockpit Footer Strip */
            .sibs-hero-footer-bar {{
                grid-template-columns: 1fr !important;
                gap: 8px !important;
                padding: 12px 14px !important;
                margin-top: 14px !important;
                border-radius: 8px !important;
            }}
            .sibs-footer-stat-item {{
                padding-bottom: 6px !important;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
            }}
            .sibs-footer-stat-item:last-child {{
                border-bottom: none !important;
                padding-bottom: 0 !important;
            }}
            .stat-label {{
                font-size: 9px !important;
            }}
            .stat-value {{
                font-size: 12px !important;
            }}

            /* Streamlit Columns Stacking on Handphone */
            div[data-testid="stHorizontalBlock"] {{
                flex-direction: column !important;
                flex-wrap: nowrap !important;
                gap: 12px !important;
            }}
            div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {{
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
                margin-bottom: 0px !important;
            }}
            div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:empty {{
                display: none !important;
            }}

            /* Mobile Buttons */
            .stButton > button, [data-testid="stFormSubmitButton"] > button, [data-testid="stDownloadButton"] > button {{
                width: 100% !important;
                font-size: 12.5px !important;
                padding: 0.65rem 1rem !important;
                min-height: 42px !important;
            }}

            /* Mobile Cards & KPIs */
            .sibs-card {{
                padding: 14px 14px !important;
                border-radius: 10px !important;
                margin-bottom: 12px !important;
            }}
            .sibs-kpi {{
                padding: 12px 14px !important;
                border-radius: 10px !important;
                margin-bottom: 8px !important;
            }}
            .sibs-kpi-label {{
                font-size: 9.5px !important;
                margin-bottom: 4px !important;
            }}
            .sibs-kpi-value {{
                font-size: 20px !important;
                margin-bottom: 2px !important;
            }}
            .sibs-kpi-sub {{
                font-size: 10.5px !important;
            }}

            /* Mobile Tabs (Horizontal Swipe) */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 12px !important;
                overflow-x: auto !important;
                flex-wrap: nowrap !important;
                -webkit-overflow-scrolling: touch !important;
                scrollbar-width: none !important;
                padding-bottom: 4px !important;
                margin-bottom: 12px !important;
            }}
            .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {{
                display: none !important;
            }}
            .stTabs [data-baseweb="tab"] {{
                font-size: 12px !important;
                padding: 6px 2px 8px 2px !important;
                white-space: nowrap !important;
                flex-shrink: 0 !important;
            }}

            /* Header Status Box on Mobile */
            .sibs-header-status-box {{
                text-align: left !important;
                padding-top: 0 !important;
                margin-top: -8px !important;
                margin-bottom: 8px !important;
                display: flex !important;
                align-items: center !important;
                gap: 10px !important;
            }}
            .sibs-header-date {{
                font-size: 11px !important;
                opacity: 0.7 !important;
                margin-top: 0 !important;
            }}

            /* Mobile Tables & Dataframes */
            [data-testid="stDataFrame"], [data-testid="stTable"] {{
                width: 100% !important;
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch !important;
            }}
            .sibs-card table td {{
                font-size: 11px !important;
                padding: 5px 0 !important;
            }}

            /* Mobile Floating Support */
            .sibs-floating-support {{
                bottom: 12px !important;
                right: 12px !important;
                padding: 7px 12px !important;
                font-size: 11px !important;
                gap: 5px !important;
            }}

            /* Mobile Inputs */
            input, textarea, select, [data-baseweb="select"] {{
                font-size: 14px !important;
                min-height: 40px !important;
            }}

            /* Mobile Sidebar */
            [data-testid="stSidebar"] {{
                width: 84vw !important;
                max-width: 320px !important;
            }}
        }}

        /* Print Media */
        @media print {{
            [data-testid="stSidebar"], header, footer, .stButton, .stTabs, hr, .sibs-floating-support {{ display:none !important; }}
            .block-container {{ padding:0 !important; margin:0 !important; max-width:100% !important; background-color:#FFFFFF !important; }}
            .bap-print-container {{
                background-color:#FFFFFF !important; color:#000000 !important; padding:25px !important;
                font-family:'Times New Roman',Times,serif !important; border:none !important;
            }}
            .bap-print-container * {{ color:#000000 !important; }}
        }}
        </style>
        """, unsafe_allow_html=True)


# ==================== FORMAT HELPERS ====================

def format_currency(value) -> str:
    """Format as Indonesian Rupiah."""
    try:
        return f"Rp {int(float(value)):,}".replace(",", ".")
    except (ValueError, TypeError):
        return "Rp 0"


def format_percentage(value) -> str:
    try:
        return f"{float(value):.1f}%"
    except (ValueError, TypeError):
        return "0.0%"


def format_date(value, fmt: str = "%d %B %Y") -> str:
    """Format date string to a clean Indonesian readable string."""
    if isinstance(value, str):
        for pattern in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S%z"):
            try:
                value = datetime.strptime(value.split("+")[0].split("Z")[0], pattern.replace("%z", ""))
                break
            except ValueError:
                continue
        else:
            return str(value)
    if isinstance(value, datetime):
        return value.strftime(fmt)
    return str(value)


# ==================== NOTIFICATIONS ====================

def show_success(msg: str):
    st.success(f"[BERHASIL] {msg}")

def show_error(msg: str):
    st.error(f"[ERROR] {msg}")

def show_warning(msg: str):
    st.warning(f"[PERINGATAN] {msg}")

def show_info(msg: str):
    st.info(f"[INFORMASI] {msg}")


# ==================== UI COMPONENT HELPERS ====================

def render_kpi(label: str, value: str, sub: str = "", border_color: str = "#0284C7", value_color: str = ""):
    """Render a KPI metric card with clean styling."""
    val_style = f"color: {value_color} !important;" if value_color else ""
    st.markdown(f"""
        <div class="sibs-kpi" style="border-left-color: {border_color} !important;">
            <div class="sibs-kpi-label">{label}</div>
            <div class="sibs-kpi-value" style="{val_style}">{value}</div>
            <div class="sibs-kpi-sub">{sub}</div>
        </div>
    """, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str, badge: str = "SIBS", show_back: bool = False, back_callback=None):
    """Render a clean industrial page header."""
    col_title, col_status = st.columns([6, 2])
    with col_title:
        st.markdown(f"""
            <div style="margin-bottom:16px;">
                <span class="status-pill-navy">{badge}</span>
                <h2 style="margin:6px 0 0 0; font-size:24px; font-weight:800;">{title}</h2>
                <p style="margin:3px 0 0 0; font-size:12.5px; opacity:0.8;">{subtitle}</p>
            </div>
        """, unsafe_allow_html=True)
    with col_status:
        st.markdown(f"""
            <div class="sibs-header-status-box">
                <span class="status-pill-green">SISTEM AKTIF</span>
                <div class="sibs-header-date">
                    {datetime.now().strftime('%d %B %Y')}
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:0 0 20px 0; border-color: rgba(148, 163, 184, 0.2);'>", unsafe_allow_html=True)


def status_pill(status: str) -> str:
    """Return HTML for an enterprise status pill."""
    s = str(status).lower()
    if s in ("approved", "selesai", "delivered", "active", "operasional", "ready"):
        return f'<span class="status-pill-green">{status.upper()}</span>'
    elif s in ("rejected", "ditolak", "overdue", "rusak"):
        return f'<span class="status-pill-red">{status.upper()}</span>'
    elif s in ("pending", "draft", "review", "diajukan"):
        return f'<span class="status-pill-yellow">{status.upper()}</span>'
    else:
        return f'<span class="status-pill-navy">{status.upper()}</span>'
