import streamlit as st

# Set page config
st.set_page_config(
    page_title="PlaceWell: Smarter EIH Site Planning",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add navigation menu
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Scoring Model", "Build Feasibility", "Service Area Coverage"])

# Handle page navigation
if page == "Home":
    st.switch_page("pages/Home.py")
elif page == "Scoring Model":
    st.switch_page("pages/Scoring_Model.py")
elif page == "Build Feasibility":
    st.switch_page("pages/Build_Feasibility.py")
elif page == "Service Area Coverage":
    st.switch_page("pages/Service_Area.py") 
