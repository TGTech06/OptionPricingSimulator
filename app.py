import streamlit as st
from streamlit_option_menu import option_menu
from monte_carlo import show_monte_carlo_page  # Importing from monte_carlo.py
from heston import show_heston_page            # Importing from heston.py
from bachelier import show_bachelier_page      # Importing from bachelier.py
from black_scholes import show_black_scholes_page  # Importing from black_scholes.py
from binomial import show_binomial_page        # Importing from binomial.py
from comparison import show_comparison_page    # Importing from comparison.py

# Set up the sidebar for navigation
st.set_page_config(page_title="Option Pricing Models", layout="wide")

# Get the query parameters (if any)
query_params = st.experimental_get_query_params()

# Check if there is a "page" query param, otherwise default to "Home"
if "page" in query_params:
    selected_page = query_params["page"][0]
else:
    selected_page = "Home"

# Sidebar with options, updating query params when a new page is selected
with st.sidebar:
    selected_page = option_menu(
        "Navigation",
        ["Home", "Black-Scholes", "Binomial", "Monte Carlo", "Heston", "Bachelier"],
        icons=["house", "bar-chart", "graph-up", "calculator", "pie-chart", "graph-up"],
        menu_icon="cast",
        default_index=0,
        key="menu",
        on_change=lambda: st.experimental_set_query_params(page=selected_page)
    )

# Save the selected page in the URL query parameters
st.experimental_set_query_params(page=selected_page)

# Routing to different pages based on selection
if selected_page == "Home":
    st.title("Option Pricing Models Overview")
    st.write("Welcome! Use the sidebar to navigate to individual model pages for detailed information or go to the comparison page to see how the models perform under different conditions.")
    show_comparison_page()

elif selected_page == "Black-Scholes":
    show_black_scholes_page()

elif selected_page == "Binomial":
    show_binomial_page()

elif selected_page == "Monte Carlo":
    show_monte_carlo_page()

elif selected_page == "Heston":
    show_heston_page()

elif selected_page == "Bachelier":
    show_bachelier_page()
