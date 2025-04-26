import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
import os

# Try to import OpenAI, but make it optional
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    st.warning("OpenAI package not available. AI risk assessment will be disabled.")

# Utility functions
def analyze_feasibility(lat, lon, facility_type, size_sqm):
    # Mock data for demonstration
    zoning_score = 85
    infrastructure_score = 75
    overall_score = (zoning_score + infrastructure_score) / 2
    
    return {
        'zoning_score': zoning_score,
        'infrastructure_score': infrastructure_score,
        'overall_score': overall_score
    }

def generate_report(results):
    return f"""
    <p><strong>Feasibility Analysis Report</strong></p>
    <p>• Zoning Score: {results['zoning_score']}/100</p>
    <p>• Infrastructure Score: {results['infrastructure_score']}/100</p>
    <p>• Overall Feasibility: {results['overall_score']}/100</p>
    """

def generate_risk_assessment(lat, lon, facility_type, size_sqm, results):
    # Mock risk assessment data
    risks = {
        'zoning_challenges': [
            "Current zoning may require a conditional use permit",
            "Height restrictions may limit building capacity",
            "Parking requirements may need variance"
        ],
        'construction_risks': [
            "Moderate slope in northern section of site",
            "Seasonal flooding risk in southwest corner",
            "Soil stability concerns in eastern portion"
        ],
        'political_sensitivities': [
            "Elementary school within 500m",
            "Active neighborhood association in area",
            "Historic district considerations"
        ],
        'environmental_flags': [
            "Protected tree species on site",
            "Potential archaeological significance",
            "Stormwater management requirements"
        ]
    }
    
    return risks

# Set page config
st.set_page_config(
    page_title="EIH Build Feasibility",
    page_icon="🏗️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .header {
        color: #003b73;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .subheader {
        color: #60a3d9;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #bfd7ed;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .metric-title {
        color: #0074b7;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .example-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border-left: 4px solid #60a3d9;
    }
    .risk-card {
        background-color: #fff;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #ff6b6b;
    }
    .risk-title {
        color: #ff6b6b;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header">EIH Build Feasibility Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Analyze the feasibility of establishing Emergency Interim Housing sites</div>', unsafe_allow_html=True)

# Example section
st.markdown("""
    <div class="example-card">
        <h4>📋 Example Addresses</h4>
        <p>Try these San Jose addresses for testing:</p>
        <ul>
            <li>"200 E Santa Clara St, San Jose, CA 95113" (Downtown)</li>
            <li>"635 Phelan Ave, San Jose, CA 95112" (East Side)</li>
            <li>"1500 S 10th St, San Jose, CA 95112" (Central)</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Input parameters in sidebar
st.sidebar.markdown('<div class="metric-title">Analysis Parameters</div>', unsafe_allow_html=True)

# Location inputs
st.sidebar.markdown("### Location")
address = st.sidebar.text_input("Site Address", "200 E Santa Clara St, San Jose, CA 95113")

# Facility parameters
st.sidebar.markdown("### EIH Site Details")
facility_type = st.sidebar.selectbox(
    "Site Type",
    ["Temporary Shelter", "Transitional Housing", "Supportive Housing", "Emergency Shelter"]
)

size_sqm = st.sidebar.number_input("Proposed Size (sqm)", min_value=100, value=1000)

# Analysis button
if st.sidebar.button("Analyze Feasibility", type="primary"):
    try:
        # Geocode address with retry mechanism
        geolocator = Nominatim(user_agent="eih_analyzer", timeout=10)
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                location = geolocator.geocode(address)
                if location:
                    break
            except GeocoderTimedOut:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    raise Exception("Geocoding service timed out after multiple attempts. Please try again later.")
        
        if location:
            latitude = location.latitude
            longitude = location.longitude
            
            # Perform analysis
            results = analyze_feasibility(latitude, longitude, facility_type, size_sqm)
            
            # Display results
            st.markdown('<div class="metric-title">Feasibility Analysis Results</div>', unsafe_allow_html=True)
            
            # Create columns for metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-title">Zoning Score</div>
                        <div style="font-size: 2rem; color: #003b73;">{:.1f}/100</div>
                    </div>
                """.format(results['zoning_score']), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-title">Infrastructure Score</div>
                        <div style="font-size: 2rem; color: #003b73;">{:.1f}/100</div>
                    </div>
                """.format(results['infrastructure_score']), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-title">Overall Feasibility</div>
                        <div style="font-size: 2rem; color: #003b73;">{:.1f}/100</div>
                    </div>
                """.format(results['overall_score']), unsafe_allow_html=True)
            
            # Generate and display detailed report
            st.markdown('<div class="metric-title">Detailed Analysis</div>', unsafe_allow_html=True)
            report = generate_report(results)
            st.markdown(f"""
                <div class="metric-card">
                    {report}
                </div>
            """, unsafe_allow_html=True)

            # Generate and display risk assessment
            st.markdown('<div class="metric-title">Site Risk Assessment</div>', unsafe_allow_html=True)
            risks = generate_risk_assessment(latitude, longitude, facility_type, size_sqm, results)
            
            # Display each risk category
            for category, risk_list in risks.items():
                category_title = category.replace('_', ' ').title()
                st.markdown(f"""
                    <div class="risk-card">
                        <div class="risk-title">{category_title}</div>
                        <ul>
                            {''.join(f'<li>{risk}</li>' for risk in risk_list)}
                        </ul>
                    </div>
                """, unsafe_allow_html=True)

            # AI Risk Analysis
            if OPENAI_AVAILABLE and 'client' in locals():
                st.markdown('<div class="metric-title">AI Risk Analysis</div>', unsafe_allow_html=True)
                with st.spinner("Analyzing potential risks..."):
                    try:
                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "You are an expert in Emergency Interim Housing (EIH) site assessment and risk analysis. "
                                        "Analyze the following site data and provide a comprehensive risk assessment focusing on:"
                                        "\n• Zoning and regulatory challenges"
                                        "\n• Construction and environmental risks"
                                        "\n• Community and political considerations"
                                        "\n• Mitigation strategies"
                                        "\nBe specific and practical in your recommendations."
                                    )
                                },
                                {
                                    "role": "user",
                                    "content": f"""
                                    Site Details:
                                    - Type: {facility_type}
                                    - Size: {size_sqm} sqm
                                    - Location: {address}
                                    - Zoning Score: {results['zoning_score']}
                                    - Infrastructure Score: {results['infrastructure_score']}
                                    - Overall Feasibility: {results['overall_score']}
                                    
                                    Please provide a detailed risk assessment and recommendations.
                                    """
                                }
                            ]
                        )
                        st.markdown("""
                            <div class="metric-card">
                                <div class="metric-title">AI Risk Analysis</div>
                                <div style="padding: 1rem;">
                                    {}
                                </div>
                            </div>
                        """.format(response.choices[0].message.content), unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error generating AI risk analysis: {str(e)}")
            
        else:
            st.error("Could not find the specified address. Please check the address and try again.")
        
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
else:
    st.info("Please enter the site address and parameters in the sidebar to begin analysis.")
