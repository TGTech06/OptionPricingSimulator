import streamlit as st
import numpy as np
from black_scholes import black_scholes
from binomial import binomial_option_pricing
from monte_carlo import monte_carlo_option_pricing
from heston import heston_price
from bachelier import bachelier_option_pricing
import plotly.graph_objects as go
import pandas as pd

# Comparison page
def show_comparison_page():
    st.title("Option Pricing Model Comparison")

    st.markdown("""
    In this section, you can compare different option pricing models under various conditions:

    - **Volatility Impact**: See how each model handles changes in market volatility.
    - **Time to Maturity**: Observe the differences in pricing with varying times to maturity.
    - **Interest Rate Sensitivity**: Analyze the effect of different risk-free rates on option prices.

    """)

    # Inputs for comparison on the left
    col1, col2 = st.columns([1, 2])

    with col1:
        S0 = st.number_input("Stock Price (S0)", value=100.0, step=1.0, format="%.2f")
        X = st.number_input("Strike Price (X)", value=100.0, step=1.0, format="%.2f")
        T = st.slider("Time to Maturity (T)", min_value=0.01, max_value=5.0, value=1.0, step=0.01)
        r = st.slider("Risk-Free Rate (r)", min_value=0.0, max_value=0.2, value=0.05, step=0.001)
        sigma = st.slider("Volatility (σ)", min_value=0.01, max_value=1.0, value=0.2, step=0.01)

    # Calculate prices for both call and put options for each model
    call_prices = {
        'Black-Scholes': black_scholes(S0, X, T, r, sigma, 'call'),
        'Binomial': binomial_option_pricing(S0, X, T, r, sigma, 100, 'call'),
        'Monte Carlo': monte_carlo_option_pricing(S0, X, T, r, sigma, 10000, 'call'),
        'Heston': heston_price(S0, X, T, r, 2.0, 0.04, sigma, -0.7, sigma**2, 'call'),
        'Bachelier': bachelier_option_pricing(S0, X, T, r, sigma, 'call')
    }

    put_prices = {
        'Black-Scholes': black_scholes(S0, X, T, r, sigma, 'put'),
        'Binomial': binomial_option_pricing(S0, X, T, r, sigma, 100, 'put'),
        'Monte Carlo': monte_carlo_option_pricing(S0, X, T, r, sigma, 10000, 'put'),
        'Heston': heston_price(S0, X, T, r, 2.0, 0.04, sigma, -0.7, sigma**2, 'put'),
        'Bachelier': bachelier_option_pricing(S0, X, T, r, sigma, 'put')
    }

    # Display prices in a table
    st.markdown("### Option Prices (Call and Put)")
    prices_df = pd.DataFrame({
        'Model': call_prices.keys(),
        'Call Price': call_prices.values(),
        'Put Price': put_prices.values()
    })
    st.table(prices_df)

    # Graph comparison: Call prices vs. Volatility
    volatilities = np.linspace(0.01, 1.0, 50)
    call_bs_prices = [black_scholes(S0, X, T, r, vol, 'call') for vol in volatilities]
    call_binomial_prices = [binomial_option_pricing(S0, X, T, r, vol, 100, 'call') for vol in volatilities]
    call_mc_prices = [monte_carlo_option_pricing(S0, X, T, r, vol, 10000, 'call') for vol in volatilities]
    call_heston_prices = [heston_price(S0, X, T, r, 2.0, 0.04, vol, -0.7, vol**2, 'call') for vol in volatilities]
    call_bachelier_prices = [bachelier_option_pricing(S0, X, T, r, vol, 'call') for vol in volatilities]

    fig_call = go.Figure()
    fig_call.add_trace(go.Scatter(x=volatilities, y=call_bs_prices, mode='lines', name="Black-Scholes", line=dict(color='blue')))
    fig_call.add_trace(go.Scatter(x=volatilities, y=call_binomial_prices, mode='lines', name="Binomial", line=dict(color='green')))
    fig_call.add_trace(go.Scatter(x=volatilities, y=call_mc_prices, mode='lines', name="Monte Carlo", line=dict(color='red')))
    fig_call.add_trace(go.Scatter(x=volatilities, y=call_heston_prices, mode='lines', name="Heston", line=dict(color='purple')))
    fig_call.add_trace(go.Scatter(x=volatilities, y=call_bachelier_prices, mode='lines', name="Bachelier", line=dict(color='orange')))

    fig_call.update_layout(
        title="Call Option Prices vs. Volatility",
        xaxis_title="Volatility (σ)",
        yaxis_title="Call Option Price",
        height=500,
        legend_title="Models"
    )

    # Graph comparison: Put prices vs. Volatility
    put_bs_prices = [black_scholes(S0, X, T, r, vol, 'put') for vol in volatilities]
    put_binomial_prices = [binomial_option_pricing(S0, X, T, r, vol, 100, 'put') for vol in volatilities]
    put_mc_prices = [monte_carlo_option_pricing(S0, X, T, r, vol, 10000, 'put') for vol in volatilities]
    put_heston_prices = [heston_price(S0, X, T, r, 2.0, 0.04, vol, -0.7, vol**2, 'put') for vol in volatilities]
    put_bachelier_prices = [bachelier_option_pricing(S0, X, T, r, vol, 'put') for vol in volatilities]

    fig_put = go.Figure()
    fig_put.add_trace(go.Scatter(x=volatilities, y=put_bs_prices, mode='lines', name="Black-Scholes", line=dict(color='blue')))
    fig_put.add_trace(go.Scatter(x=volatilities, y=put_binomial_prices, mode='lines', name="Binomial", line=dict(color='green')))
    fig_put.add_trace(go.Scatter(x=volatilities, y=put_mc_prices, mode='lines', name="Monte Carlo", line=dict(color='red')))
    fig_put.add_trace(go.Scatter(x=volatilities, y=put_heston_prices, mode='lines', name="Heston", line=dict(color='purple')))
    fig_put.add_trace(go.Scatter(x=volatilities, y=put_bachelier_prices, mode='lines', name="Bachelier", line=dict(color='orange')))

    fig_put.update_layout(
        title="Put Option Prices vs. Volatility",
        xaxis_title="Volatility (σ)",
        yaxis_title="Put Option Price",
        height=500,
        legend_title="Models"
    )

    st.plotly_chart(fig_call)
    st.plotly_chart(fig_put)

    # Explanation of key differences and why prices differ between models
    st.markdown("""
    ### Explanation of Price Differences:

    - **Black-Scholes Model**: This model assumes constant volatility, which can result in relatively stable prices. It is computationally efficient but may not handle real-world volatility well.

    - **Binomial Model**: The binomial model uses a discrete time-step approach. It tends to provide similar prices to Black-Scholes but is more flexible for American options, where early exercise is allowed.

    - **Monte Carlo Simulation**: Monte Carlo generates prices using random sampling, making it more flexible in volatile conditions. However, it is computationally intensive and may produce different results depending on the number of simulations.

    - **Heston Model**: The Heston model accounts for stochastic volatility, making it more adaptive to real-world market conditions where volatility varies. This often results in different prices compared to models assuming constant volatility.

    - **Bachelier Model**: Bachelier assumes a normal distribution for prices, which is better suited to low-volatility or mean-reverting markets. Prices from this model can differ significantly from the others, especially in high-volatility scenarios.

    These differences in assumptions and flexibility result in varying prices across the models, especially when dealing with volatility and time to maturity.
    """)

# Run the comparison page
show_comparison_page()
