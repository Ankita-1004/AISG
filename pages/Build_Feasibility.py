import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

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
        else:
            st.error("Could not find the specified address. Please check the address and try again.")
        
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
else:
    st.info("Please enter the site address and parameters in the sidebar to begin analysis.")
