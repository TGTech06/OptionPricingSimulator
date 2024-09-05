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

# Set default page in session state if not already present
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Home"

# Sidebar with options
with st.sidebar:
    selected_page = option_menu(
        "Navigation",
        ["Home", "Black-Scholes", "Binomial", "Monte Carlo", "Heston", "Bachelier"],
        icons=["house", "bar-chart", "graph-up", "calculator", "pie-chart", "graph-up"],
        menu_icon="cast",
        default_index=0,
        key="menu"
    )

    # Store the selected page in session state
    st.session_state["selected_page"] = selected_page

# Routing based on the selected page from session state
if st.session_state["selected_page"] == "Home":
    st.title("Option Pricing Models Overview")
    st.write("Welcome! Use the sidebar to navigate to individual model pages for detailed information or go to the comparison page to see how the models perform under different conditions.")
    show_comparison_page()

elif st.session_state["selected_page"] == "Black-Scholes":
    show_black_scholes_page()

elif st.session_state["selected_page"] == "Binomial":
    show_binomial_page()

elif st.session_state["selected_page"] == "Monte Carlo":
    show_monte_carlo_page()

elif st.session_state["selected_page"] == "Heston":
    show_heston_page()

elif st.session_state["selected_page"] == "Bachelier":
    show_bachelier_page()
