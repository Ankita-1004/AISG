import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import folium_static
from Feature_3_Service_Area_Coverage import calculate_coverage, plot_coverage_map
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

# Set page config
st.set_page_config(
    page_title="EIH Service Area Coverage",
    page_icon="🗺️",
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
st.markdown('<div class="header">EIH Service Area Coverage</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Visualize and analyze service area coverage for Emergency Interim Housing sites</div>', unsafe_allow_html=True)

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
        <p>Recommended service radius by site type:</p>
        <ul>
            <li>Temporary Shelter: 2-5 km</li>
            <li>Transitional Housing: 3-7 km</li>
            <li>Supportive Housing: 5-10 km</li>
            <li>Emergency Shelter: 1-3 km</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Input parameters in sidebar
st.sidebar.markdown('<div class="metric-title">Coverage Parameters</div>', unsafe_allow_html=True)

# Location inputs
st.sidebar.markdown("### Location")
address = st.sidebar.text_input("Site Address", "200 E Santa Clara St, San Jose, CA 95113")

# Coverage parameters
st.sidebar.markdown("### Coverage Details")
radius_km = st.sidebar.slider("Service Radius (km)", min_value=1, max_value=50, value=10)
facility_type = st.sidebar.selectbox(
    "Site Type",
    ["Temporary Shelter", "Transitional Housing", "Supportive Housing", "Emergency Shelter"]
)

# Analysis button
if st.sidebar.button("Analyze Coverage", type="primary"):
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
            
            # Calculate coverage
            coverage_data = calculate_coverage(latitude, longitude, radius_km, facility_type)
            
            # Display coverage metrics
            st.markdown('<div class="metric-title">Coverage Metrics</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-title">Population Covered</div>
                        <div style="font-size: 2rem; color: #003b73;">{:,}</div>
                    </div>
                """.format(int(coverage_data['population_covered'])), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-title">Area Covered</div>
                        <div style="font-size: 2rem; color: #003b73;">{:.2f} km²</div>
                    </div>
                """.format(coverage_data['area_covered']), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-title">Coverage Efficiency</div>
                        <div style="font-size: 2rem; color: #003b73;">{:.1f}%</div>
                    </div>
                """.format(coverage_data['coverage_efficiency']), unsafe_allow_html=True)
            
            # Display coverage map
            st.markdown('<div class="metric-title">Coverage Map</div>', unsafe_allow_html=True)
            coverage_map = plot_coverage_map(coverage_data)
            folium_static(coverage_map, width=1200, height=600)
            
            # Display detailed analysis
            st.markdown('<div class="metric-title">Detailed Analysis</div>', unsafe_allow_html=True)
            st.markdown(f"""
                <div class="metric-card">
                    {coverage_data['analysis_report']}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Could not find the specified address. Please check the address and try again.")
        
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
else:
    st.info("Please enter the site address and coverage parameters in the sidebar to begin analysis.") 