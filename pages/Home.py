import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
import os

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .header {
        color: #003b73;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }
    .subtitle {
        color: #60a3d9;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .feature-card {
        background-color: #003b73;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: white;
        text-align: center;
        transition: transform 0.2s;
    }
    .feature-card:hover {
        transform: scale(1.02);
    }
    .feature-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: white;
    }
    .feature-button {
        display: inline-block;
        padding: 0.5rem 1rem;
        background-color: #60a3d9;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        margin-top: 1rem;
        transition: background-color 0.2s;
    }
    .feature-button:hover {
        background-color: #0074b7;
        color: white;
    }
    .logo-container {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto 2rem auto;
    }
    .logo {
        max-width: 300px;
        height: auto;
        display: block;
        margin: 0 auto;
    }
    .footer {
        text-align: center;
        padding: 1rem;
        color: #0074b7;
        font-size: 0.9rem;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load and display logo
logo_path = "../AISG Logo.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image(logo, width=300, use_container_width=False)
    st.markdown('</div>', unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div class="header">PlaceWell: Smarter EIH Site Planning for San Jose</div>
    <div class="subtitle">A data-driven platform for equitable and feasible Emergency Interim Housing placement</div>
""", unsafe_allow_html=True)

# Feature Cards Section - Two columns for first two features
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📊 Scoring Model</div>
            <p>Evaluate potential EIH locations using our comprehensive scoring system that considers multiple factors including population needs, accessibility, and community impact.</p>
            <a href="/Scoring_Model" class="feature-button">Launch Scoring Model</a>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🏗️ Build Feasibility Analyzer</div>
            <p>Analyze the feasibility of establishing EIH sites by considering zoning regulations, land availability, and infrastructure requirements.</p>
            <a href="/Build_Feasibility" class="feature-button">Launch Feasibility Analyzer</a>
        </div>
    """, unsafe_allow_html=True)

# Third feature in its own centered column
st.markdown("""
    <div style="max-width: 600px; margin: 0 auto;">
        <div class="feature-card">
            <div class="feature-title">🗺️ Service Area Coverage</div>
            <p>Visualize and analyze service area coverage for existing and proposed EIH sites to ensure optimal community access and resource distribution.</p>
            <a href="/Service_Area" class="feature-button">Launch Coverage Analyzer</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Ethical Design Banner
st.markdown("""
    <div class="ethics-banner">
        <div class="ethics-title">Built with public trust, equity, and inclusion in mind</div>
        <div class="ethics-item">✅ Transparency in data sources and decision-making processes</div>
        <div class="ethics-item">📊 Equity-driven analysis for fair resource distribution</div>
        <div class="ethics-item">♿ Accessibility considerations for all community members</div>
        <div class="ethics-item">🔒 Privacy-first approach to sensitive information</div>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        Created by Team Violet | 
        <a href="https://github.com/Ankita-1004/AISG/tree/1c3f7c6981e4df48967d8d63cce44b2bfa406da8" style="color: #0074b7; text-decoration: none;">GitHub</a>
    </div>
""", unsafe_allow_html=True) 