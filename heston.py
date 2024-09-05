import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from black_scholes import black_scholes
import plotly.graph_objects as go

# Heston model (simplified) using Black-Scholes
def heston_price(S0: float, X: float, T: float, r: float, kappa: float, theta: float, sigma: float, rho: float, v0: float, option_type: str = 'call') -> float:
    """
    Simplified Heston model using Black-Scholes with stochastic volatility.

    Parameters:
    - S0: Stock price (float)
    - X: Strike price (float)
    - T: Time to maturity in years (float)
    - r: Risk-free interest rate (float)
    - kappa: Speed of mean reversion of variance (float)
    - theta: Long-run average variance (float)
    - sigma: Volatility of volatility (float)
    - rho: Correlation between asset returns and volatility (float)
    - v0: Initial variance (float)
    - option_type: 'call' or 'put' (str)

    Returns:
    - The option price (float).
    """
    sigma_avg = np.sqrt(theta)  # Using long-run variance as the average volatility
    return black_scholes(S0, X, T, r, sigma_avg, option_type)

# Heston model page
def show_heston_page():
    st.title("Heston Stochastic Volatility Model")

    # Equation explanation
    st.markdown("""
    The **Heston model** introduces stochastic volatility, meaning that volatility changes over time, rather than being constant as in the Black-Scholes model.

    ### Heston Stochastic Volatility Equations:
    - The stock price follows the SDE:
    $$ dS_t = \mu S_t dt + \sqrt{v_t} S_t dW^S_t $$
    - The variance follows the SDE:
    $$ dv_t = \kappa (\theta - v_t) dt + \sigma \sqrt{v_t} dW^v_t $$
    - Where \( dW^S_t \) and \( dW^v_t \) are correlated Wiener processes with correlation \( \rho \).
    """)

    # Input layout
    col1, col2 = st.columns([1, 2])  # Adjusted to give more space to the graphs

    with col1:
        S0 = st.number_input("Stock Price (S0)", value=100.0, step=1.0, format="%.2f")
        X = st.number_input("Strike Price (X)", value=100.0, step=1.0, format="%.2f")
        T = st.slider("Time to Maturity (T)", min_value=0.01, max_value=5.0, value=1.0, step=0.01)
        r = st.slider("Risk-Free Rate (r)", min_value=0.0, max_value=0.2, value=0.05, step=0.001)
        kappa = st.slider("Heston kappa", min_value=0.1, max_value=5.0, value=2.0, step=0.1)
        theta = st.slider("Heston theta", min_value=0.01, max_value=0.2, value=0.04, step=0.01)
        rho = st.slider("Heston rho", min_value=-1.0, max_value=1.0, value=-0.7, step=0.05)
        v0 = st.slider("Heston v0 (Initial Variance)", min_value=0.01, max_value=0.2, value=0.02, step=0.01)
        sigma = st.slider("Volatility of Volatility (σ)", min_value=0.01, max_value=1.0, value=0.2, step=0.01)

        # Add padding between inputs and price boxes
        st.markdown("<div style='padding-top:20px;'></div>", unsafe_allow_html=True)

        # Calculate the call and put option prices
        call_option_price = heston_price(S0, X, T, r, kappa, theta, sigma, rho, v0, 'call')
        put_option_price = heston_price(S0, X, T, r, kappa, theta, sigma, rho, v0, 'put')

        # Display prices in colorful rounded boxes
        col3, col4 = st.columns(2)

        with col3:
            st.markdown(
                f"""
                <div style="background-color:#E3F2FD; border-radius:10px; padding:15px; text-align:center;">
                    <span style="font-size:20px; color:blue;"><b>Call Option Price</b></span><br>
                    <span style="font-size:45px; color:blue;"><b>${call_option_price:.2f}</b></span>
                </div>
                """, unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f"""
                <div style="background-color:#FFEBEE; border-radius:10px; padding:15px; text-align:center;">
                    <span style="font-size:20px; color:red;"><b>Put Option Price</b></span><br>
                    <span style="font-size:45px; color:red;"><b>${put_option_price:.2f}</b></span>
                </div>
                """, unsafe_allow_html=True
            )

    # Graphs placed next to the inputs
    with col2:
        # Option price vs. time to maturity (first graph)
        times = np.linspace(0.01, T, 100)
        call_prices_over_time = [heston_price(S0, X, t, r, kappa, theta, sigma, rho, v0, 'call') for t in times]
        put_prices_over_time = [heston_price(S0, X, t, r, kappa, theta, sigma, rho, v0, 'put') for t in times]

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=times, y=call_prices_over_time, mode='lines', name='Call Option', line=dict(color='blue')))
        fig1.add_trace(go.Scatter(x=times, y=put_prices_over_time, mode='lines', name='Put Option', line=dict(color='red')))
        fig1.update_layout(
            title="Option Prices vs. Time to Maturity",
            xaxis_title="Time to Maturity (Years)",
            yaxis_title="Option Price",
            height=350  # Increased height for better clarity
        )
        st.plotly_chart(fig1)

        # Sensitivity Analysis: Option Price vs Volatility of Volatility (σ)
        volatilities_of_vol = np.linspace(0.01, 1.0, 50)
        call_prices_vs_vol_of_vol = [heston_price(S0, X, T, r, kappa, theta, vol, rho, v0, 'call') for vol in volatilities_of_vol]
        put_prices_vs_vol_of_vol = [heston_price(S0, X, T, r, kappa, theta, vol, rho, v0, 'put') for vol in volatilities_of_vol]

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=volatilities_of_vol, y=call_prices_vs_vol_of_vol, mode='lines', name='Call Option', line=dict(color='blue')))
        fig2.add_trace(go.Scatter(x=volatilities_of_vol, y=put_prices_vs_vol_of_vol, mode='lines', name='Put Option', line=dict(color='red')))
        fig2.update_layout(
            title="Option Prices vs. Volatility of Volatility (σ)",
            xaxis_title="Volatility of Volatility (σ)",
            yaxis_title="Option Price",
            height=350  # Increased height for better clarity
        )
        st.plotly_chart(fig2)

    # Heston Formula with LaTeX rendering and explanations on the sides
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_left:
        st.markdown(
            """
            **Stock Price (\( S_0 \)):**<br>
            The current price of the underlying asset. For a call option, a higher stock price increases its value because the holder can buy at a lower strike price. For a put option, a higher stock price decreases its value since the holder can sell at a lower price.<br><br>

            **Strike Price (\( X \)):**<br>
            The strike price is the price at which the holder can exercise their option. A higher strike price decreases the value of a call option and increases the value of a put option.
            """, unsafe_allow_html=True
        )

    with col_center:
        st.latex(r" dS_t = \mu S_t dt + \sqrt{v_t} S_t dW^S_t ")
        st.latex(r" dv_t = \kappa (\theta - v_t) dt + \sigma \sqrt{v_t} dW^v_t ")
        st.markdown("""
        In the Heston model, volatility is stochastic. The asset price and the variance evolve according to these stochastic differential equations, where the asset price is correlated with the variance through the parameter \( \rho \).
        """)

    with col_right:
        st.markdown(
            """
            **Time to Maturity (\( T \)):**<br>
            The longer the time to maturity, the more valuable the option, both for calls and puts, because the holder has more time to exercise the option. Over time, options lose value due to time decay (Theta).<br><br>

            **Volatility (\( \sigma \)):**<br>
            The volatility of volatility measures how much the variance changes over time. Higher values of \( \sigma \) mean the volatility is more volatile itself, which can make the option more valuable due to the increased uncertainty.
            """, unsafe_allow_html=True
        )

    # Space before the link
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Link to more information about the Heston model
    st.markdown(
        "[Learn more about the Heston model](https://en.wikipedia.org/wiki/Heston_model)"
    )

# Run the Heston model page
show_heston_page()
