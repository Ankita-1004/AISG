import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math
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
    st.warning("OpenAI package not available. AI chatbox will be disabled.")

# Set page config
st.set_page_config(
    page_title="EIH Scoring Model",
    page_icon="📊",
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
    .example-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border-left: 4px solid #60a3d9;
    }
    .chat-response {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
        border-left: 4px solid #60a3d9;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
try:
    census_df = pd.read_csv("data sets/mock_census_tracts_sanjose.csv")
    shelters_df = pd.read_csv("data sets/mock_shelters_sanjose.csv")
    pit_df = pd.read_csv("data sets/mock_pit_summary_sanjose.csv")
except FileNotFoundError:
    st.error("Data files not found. Please make sure the data files are in the correct location.")
    st.stop()

# Initialize OpenAI client only if available
client = None
if OPENAI_AVAILABLE:
    try:
        api_key = st.secrets["openai"]["api_key"] if "openai" in st.secrets else os.getenv("OPENAI_API_KEY")
        if api_key:
            # Updated client initialization
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.openai.com/v1"  # Explicitly set the base URL
            )
        else:
            st.warning("OpenAI API key not found. AI chatbox will be disabled.")
    except Exception as e:
        st.warning(f"Error initializing OpenAI client: {str(e)}. AI chatbox will be disabled.")

# ------------------------
# Utility & Scoring Class
# ------------------------
class SiteScorer:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        return R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def score_location(self):
        def distance(row):
            return math.sqrt((row['Latitude'] - self.lat)**2 + (row['Longitude'] - self.lon)**2)
        census_df['dist'] = census_df.apply(distance, axis=1)
        best_row = census_df.loc[census_df['dist'].idxmin()]

        # Community data
        poverty_score = min(best_row['Poverty Rate (%)'] / 50, 1.0)
        unhoused_score = min(best_row['Unhoused Count'] / 400, 1.0)
        env_justice_score = 0.65

        # Infrastructure score
        infrastructure_score = (0.9 + 0.7 + 0.85) / 3

        # Shelter access score
        shelters_df['distance_km'] = shelters_df.apply(
            lambda row: self.haversine(self.lat, self.lon, row['Latitude'], row['Longitude']), axis=1
        )
        nearby_shelters = shelters_df[shelters_df['distance_km'] <= 3]
        if not nearby_shelters.empty:
            avg_capacity_score = 1 - (nearby_shelters['Current Occupancy'] / nearby_shelters['Capacity']).mean()
            shelter_access_score = min(avg_capacity_score, 1.0)
        else:
            shelter_access_score = 0.2

        services_score = (shelter_access_score + 0.7 + 0.6 + 0.8) / 4
        community_impact = (poverty_score + unhoused_score + env_justice_score) / 3
        total_score = round(0.4 * services_score + 0.3 * infrastructure_score + 0.3 * community_impact, 2)

        return {
            "total_score": total_score,
            "component_scores": {
                "Access to Services": services_score,
                "Infrastructure": infrastructure_score,
                "Community Impact": community_impact,
                "Poverty Rate": poverty_score,
                "Unhoused Count": unhoused_score,
                "Shelter Access": shelter_access_score
            },
            "tract_id": best_row['Tract ID']
        }

# Header
st.markdown('<div class="header">EIH Location Scoring Model</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Evaluate potential Emergency Interim Housing locations using our comprehensive scoring system</div>', unsafe_allow_html=True)

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
st.sidebar.markdown('<div class="metric-title">Location Parameters</div>', unsafe_allow_html=True)

# Location input
address = st.sidebar.text_input("Site Address", "200 E Santa Clara St, San Jose, CA 95113")

# Analysis button
if st.sidebar.button("Score Location", type="primary"):
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
            
            # Score location
            scorer = SiteScorer(latitude, longitude)
            result = scorer.score_location()
            
            # Display results
            st.markdown('<div class="metric-title">Scoring Results</div>', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-title">Access to Services</div>
                        <div style="font-size: 2rem; color: #003b73;">{:.1f}/100</div>
                    </div>
                """.format(result['component_scores']['Access to Services'] * 100), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-title">Infrastructure</div>
                        <div style="font-size: 2rem; color: #003b73;">{:.1f}/100</div>
                    </div>
                """.format(result['component_scores']['Infrastructure'] * 100), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-title">Community Impact</div>
                        <div style="font-size: 2rem; color: #003b73;">{:.1f}/100</div>
                    </div>
                """.format(result['component_scores']['Community Impact'] * 100), unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-title">Overall Score</div>
                        <div style="font-size: 2rem; color: #003b73;">{:.1f}/100</div>
                    </div>
                """.format(result['total_score'] * 100), unsafe_allow_html=True)
            
            # Display map
            st.markdown('<div class="metric-title">Location Map</div>', unsafe_allow_html=True)
            st.map(pd.DataFrame([{"lat": latitude, "lon": longitude}]))
            
            # Display detailed scores
            st.markdown('<div class="metric-title">Detailed Scores</div>', unsafe_allow_html=True)
            st.markdown(f"""
                <div class="metric-card">
                    <p><strong>Tract ID:</strong> {result['tract_id']}</p>
                    <p><strong>Poverty Rate Score:</strong> {result['component_scores']['Poverty Rate'] * 100:.1f}/100</p>
                    <p><strong>Unhoused Count Score:</strong> {result['component_scores']['Unhoused Count'] * 100:.1f}/100</p>
                    <p><strong>Shelter Access Score:</strong> {result['component_scores']['Shelter Access'] * 100:.1f}/100</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Radar chart
            st.markdown('<div class="metric-title">Score Breakdown</div>', unsafe_allow_html=True)
            radar_labels = list(result["component_scores"].keys())[:3]
            radar_values = [v * 100 for k, v in result["component_scores"].items() if k in radar_labels]
            radar_fig = go.Figure(data=go.Scatterpolar(
                r=radar_values,
                theta=radar_labels,
                fill='toself'
            ))
            radar_fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                title="Scoring Breakdown (Radar Chart)"
            )
            st.plotly_chart(radar_fig, use_container_width=True)
            
        else:
            st.error("Could not find the specified address. Please check the address and try again.")
        
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
else:
    st.info("Please enter a site address in the sidebar to begin analysis.")

# AI Chatbox - Only show if OpenAI is available and client is initialized
if client:
    st.markdown("---")
    st.markdown('<div class="header">💬 Chat with Pia: EIH Specialist</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="example-card">
            <p>Pia is an experienced Emergency Interim Housing specialist who can help you understand the scoring model and provide insights about potential EIH sites.</p>
        </div>
    """, unsafe_allow_html=True)
    
    user_question = st.text_input("Ask Pia about the EIH scoring model or a specific score:")
    
    if st.button("Ask Pia"):
        if user_question.strip():
            with st.spinner("Pia is thinking..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are Pia, an experienced Emergency Interim Housing (EIH) specialist with over 15 years of experience in housing policy and urban planning. "
                                    "You have a deep understanding of the challenges faced by unhoused communities and the importance of thoughtful site selection. "
                                    "Your responses should be:"
                                    "\n• Professional yet approachable"
                                    "\n• Focused on practical insights and real-world implications"
                                    "\n• Informed by your experience working with unhoused communities"
                                    "\n• Clear about how different factors affect site suitability"
                                    "\n• Empathetic to the needs of both unhoused individuals and surrounding communities"
                                    "\nWhen explaining scores or factors, relate them to real-world impacts and community needs."
                                )
                            },
                            {"role": "user", "content": user_question}
                        ]
                    )
                    st.markdown("""
                        <div class="metric-card">
                            <div class="metric-title">Pia's Response</div>
                            <div style="padding: 1rem;">
                                {}
                            </div>
                        </div>
                    """.format(response.choices[0].message.content), unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error communicating with Pia: {str(e)}")
        else:
            st.warning("Please enter a question for Pia.")
