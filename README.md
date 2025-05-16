## PlaceWell: What is it?

PlaceWell is a web-based application that integrates spatial analysis, AI-powered scoring, and infrastructure readiness into one cohesive platform for urban planners. It features three core modules:

- **Scoring Model**: Ranks parcels based on proximity to key services like transit, healthcare, and existing shelters.
- **Build Feasibility Analyzer**: Assesses each site's build-readiness by analyzing slope, accessibility, flood risk, and soil stability.
- **Service Area Coverage Simulator**: Visualizes service gaps and overlap when a new site is proposed, helping cities avoid redundancy and expand reach.

**AI capabilities also include:**
- An AI-generated **Site Risk Assessment Report** that flags zoning, environmental, and construction challenges.
- A **Scoring Assistant Chatbot** that helps planners interpret scores and explore alternatives.
---
## Why PlaceWell?

The City of San Jose faces major challenges in placing EIH sites due to:

- Limited insight into physical infrastructure and zoning constraints
- Inconsistent evaluation of construction feasibility
- High demand for shelter solutions and limited resources
- Scattered data sources and lack of integration tools

**PlaceWell directly addresses these issues by:**
- Automating parcel scoring based on key planning metrics
- Flagging risk early to avoid delays or missteps
- Empowering planners with a simplified, all-in-one decision support dashboard
- Promoting equity in shelter access by highlighting underserved zones
---
## Our Solution

We developed PlaceWell as a prototype using Streamlit and generative AI tools to support real-world urban planning. The project is informed by consultation with public sector housing teams and focused on building a system that reflects actual civic workflows. The tool’s three features allow users to:

- Input a site address and receive a breakdown of zoning, infrastructure, and readiness scores
- Visualize how a proposed site would affect coverage across the city
- Generate reports and AI summaries for presentations or council meetings
- Navigate siting decisions with the help of an AI chatbot for quick data interpretation
"""
## Feature 1: Scoring Model

**Purpose:**  
Scores a proposed EIH site (via coordinates) using a composite model that factors in community need, infrastructure readiness, and access to services.

**Key Metrics:**
- Access to Services (40%): Proximity to shelters, healthcare, groceries, and public transit
- Infrastructure (30%): Site utility and logistics readiness
- Community Impact (30%): Poverty rate, unhoused count, environmental equity

**User Interaction:**
- Users enter latitude and longitude
- A score (0–1) and radar chart are generated
- Outputs include tract ID, component scores, and a site map

**Tech Stack:**
- Python, Streamlit, Plotly, Pandas
- `mock_shelters_sanjose.csv`, `mock_census_tracts_sanjose.csv`

**Dependencies:**
```
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=0.24.2
streamlit>=1.22.0
plotly>=5.13.0
geopy>=2.4.1
```

---

## Feature 2: Build Feasibility Analyzer

**Purpose:**  
Evaluates the construction feasibility of EIH sites based on terrain conditions and geographic factors.

**Evaluated Parameters:**
- Flood risk (simulated via longitude)
- Soil stability (based on latitude threshold)
- Terrain slope (used to estimate cost per square foot)
- Feasibility Score (0–1 scale)

**User Interaction:**
- Users input a San Jose address
- Map markers and 1-mile radius visualizations are generated
- Outputs include a styled DataFrame with color-coded feasibility scores

**Tech Stack:**
- Python, Streamlit, Folium, Geopy
- Interactive map using `streamlit-folium`

**Dependencies:**
```
streamlit==1.32.0
pandas==2.2.0
geopy==2.4.1
folium==0.15.1
streamlit-folium==0.15.1
```

---

## Feature 3: Service Area Coverage

**Purpose:**  
Visualizes how adding a new EIH site affects shelter access across San Jose and identifies service gaps.

**Features:**
- Coverage circles (1-mile buffer zones) around all shelters
- Census tract overlays: Unhoused count, poverty rate, and population density
- Map layers to toggle analysis focus
- PIT summary and shelter statistics

**User Interaction:**
- Users input addresses to propose sites
- Interactive map updates with coverage radii and data overlays
- Charts show shelter types and occupancy breakdown

**Tech Stack:**
- Python, Streamlit, GeoPandas, Shapely, Folium, Plotly
- Dataset support: mock shelter locations, census tracts, PIT data

**Dependencies:**
```
streamlit>=1.28.0
pandas>=2.0.0
geopandas>=0.14.0
folium>=0.14.0
streamlit-folium>=0.15.0
geopy>=2.4.0
shapely>=2.0.0
plotly>=5.18.0
numpy>=1.24.0
```
---
## See Our Demo Video

Watch our walkthrough of PlaceWell in action to see how city planners can:

- Score potential EIH sites using AI-generated metrics
- Evaluate build feasibility instantly with environmental risk detection
- Visualize shelter coverage and identify service gaps across San Jose
- Use the built-in AI chatbot to interpret results and support decision-making

![PlaceWell Demo](./PlaceWellDemo.gif)

