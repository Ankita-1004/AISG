
# PlaceWell – EIH Decision Support Features

PlaceWell is a multi-feature web application built with Streamlit that empowers city planners to make informed decisions about placing 90-day Emergency Interim Housing (EIH) sites in San Jose. Below is an overview of its three key modules:

---

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
