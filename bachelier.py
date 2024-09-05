import numpy as np
from scipy.stats import norm
import streamlit as st
import plotly.graph_objects as go

# Bachelier model function
def bachelier_option_pricing(S: float, X: float, T: float, r: float, sigma: float, option_type: str = 'call') -> float:
    """
    Bachelier option pricing formula for European options.

    Parameters:
    - S: Stock price (float)
    - X: Strike price (float)
    - T: Time to maturity in years (float)
    - r: Risk-free interest rate (float)
    - sigma: Volatility (float)
    - option_type: 'call' or 'put' (str)

    Returns:
    - The option price (float).
    """
    sigma_abs = sigma * S  # Absolute volatility
    d1 = (S - X) / (sigma_abs * np.sqrt(T))

    if option_type == 'call':
        # Call option pricing
        return (S - X) * norm.cdf(d1) + sigma_abs * np.sqrt(T) * norm.pdf(d1)
    else:
        # Put option pricing
        return (X - S) * norm.cdf(-d1) + sigma_abs * np.sqrt(T) * norm.pdf(-d1)

# Bachelier model page
def show_bachelier_page():
    st.title("Bachelier Option Pricing Model")

    # Input layout
    col1, col2 = st.columns([1, 2])  # Adjusted to give more space to the graphs

    with col1:
        S0 = st.number_input("Stock Price (S0)", value=100.0, step=1.0, format="%.2f")
        X = st.number_input("Strike Price (X)", value=100.0, step=1.0, format="%.2f")
        T = st.slider("Time to Maturity (T)", min_value=0.01, max_value=5.0, value=1.0, step=0.01)
        sigma = st.slider("Volatility (σ)", min_value=0.01, max_value=1.0, value=0.2, step=0.01)
        r = st.slider("Risk-Free Rate (r)", min_value=0.0, max_value=0.2, value=0.05, step=0.001)

        # Add padding between inputs and price boxes
        st.markdown("<div style='padding-top:20px;'></div>", unsafe_allow_html=True)

        # Calculate the call and put option prices
        call_option_price = bachelier_option_pricing(S0, X, T, r, sigma, 'call')
        put_option_price = bachelier_option_pricing(S0, X, T, r, sigma, 'put')

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
        call_prices_over_time = [bachelier_option_pricing(S0, X, t, r, sigma, 'call') for t in times]
        put_prices_over_time = [bachelier_option_pricing(S0, X, t, r, sigma, 'put') for t in times]

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

        # Sensitivity Analysis: Option Price vs Volatility (second graph)
        volatilities = np.linspace(0.01, 1.0, 50)
        call_prices_vs_volatility = [bachelier_option_pricing(S0, X, T, r, vol, 'call') for vol in volatilities]
        put_prices_vs_volatility = [bachelier_option_pricing(S0, X, T, r, vol, 'put') for vol in volatilities]

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=volatilities, y=call_prices_vs_volatility, mode='lines', name='Call Option', line=dict(color='blue')))
        fig2.add_trace(go.Scatter(x=volatilities, y=put_prices_vs_volatility, mode='lines', name='Put Option', line=dict(color='red')))
        fig2.update_layout(
            title="Option Prices vs. Volatility",
            xaxis_title="Volatility (σ)",
            yaxis_title="Option Price",
            height=350  # Increased height for better clarity
        )
        st.plotly_chart(fig2)

    # Bachelier Formula with LaTeX rendering and explanations on the sides
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_left:
        st.markdown(
            """
            **Stock Price (\( S_0 \)):**<br>
            This is the current price of the underlying asset. For a call option, a higher stock price increases the value of the option since the holder can buy at a lower strike price. For a put option, a higher stock price decreases its value as the holder can sell at a price lower than the current stock price.<br><br>

            **Strike Price (\( X \)):**<br>
            The strike price is the agreed-upon price at which the holder can exercise their option. A higher strike price decreases the value of a call option (as the option to buy becomes less attractive) and increases the value of a put option (as the option to sell at a higher price becomes more attractive).
            """, unsafe_allow_html=True
        )

    with col_center:
        st.latex(r"C = (S - X) N(d_1) + \sigma S \sqrt{T} N'(d_1)")
        st.latex(r"d_1 = \frac{S - X}{\sigma S \sqrt{T}}")

    with col_right:
        st.markdown(
            """
            **Time to Maturity (\( T \)):**<br>
            The longer the time to maturity, the more valuable the option, both for calls and puts, because the holder has more time to exercise the option. As time passes, the option value decreases due to time decay (Theta).<br><br>

            **Volatility (\( \sigma \)):**<br>
            Higher volatility means the underlying asset is more likely to experience significant price swings. This makes both call and put options more valuable, as the chance of the option ending in-the-money increases.<br><br>

            **Risk-Free Rate (\( r \)):**<br>
            The risk-free rate represents the return on a riskless investment. While this parameter doesn't directly affect the option price in the Bachelier model (unlike the Black-Scholes model), it can still play a role in discounting future cash flows and thus is included for completeness.
            """, unsafe_allow_html=True
        )

    # Space before the link
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Link to full Bachelier model paper with more spacing
    st.markdown(
        "[Read more about the Bachelier model here](https://en.wikipedia.org/wiki/Louis_Bachelier)"
    )

# Run the Bachelier model page
# show_bachelier_page()
