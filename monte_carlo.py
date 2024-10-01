import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import streamlit as st
import plotly.graph_objects as go

# Monte Carlo option pricing function
def monte_carlo_option_pricing(S: float, X: float, T: float, r: float, sigma: float, iterations: int, option_type: str = 'call') -> float:
    """
    Monte Carlo option pricing model.

    Parameters:
    - S: Stock price (float)
    - X: Strike price (float)
    - T: Time to maturity in years (float)
    - r: Risk-free interest rate (float)
    - sigma: Volatility (float)
    - iterations: Number of Monte Carlo iterations (int)
    - option_type: 'call' or 'put' (str)

    Returns:
    - The option price (float).
    """
    np.random.seed(42)  # For reproducibility
    payoffs = []
    for _ in range(iterations):
        ST = S * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * np.random.normal())
        if option_type == 'call':
            payoffs.append(max(0, ST - X))
        else:
            payoffs.append(max(0, X - ST))
    return np.exp(-r * T) * np.mean(payoffs)

# Monte Carlo model page
def show_monte_carlo_page():
    st.title("Monte Carlo Option Pricing Model")

    # Input layout
    col1, col2 = st.columns([1, 2])  # Adjusted to give more space to the graphs

    with col1:
        S0 = st.number_input("Stock Price (S0)", value=100.0, step=1.0, format="%.2f")
        X = st.number_input("Strike Price (X)", value=100.0, step=1.0, format="%.2f")
        T = st.slider("Time to Maturity (T)", min_value=0.01, max_value=5.0, value=1.0, step=0.01)
        sigma = st.slider("Volatility (σ)", min_value=0.01, max_value=1.0, value=0.2, step=0.01)
        r = st.slider("Risk-Free Rate (r)", min_value=0.0, max_value=0.2, value=0.05, step=0.001)
        iterations = st.number_input("Monte Carlo Iterations", value=10000)

        # Add padding between inputs and price boxes
        st.markdown("<div style='padding-top:20px;'></div>", unsafe_allow_html=True)

        # Calculate the call and put option prices
        call_option_price = monte_carlo_option_pricing(S0, X, T, r, sigma, iterations, 'call')
        put_option_price = monte_carlo_option_pricing(S0, X, T, r, sigma, iterations, 'put')

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
        call_prices_over_time = [monte_carlo_option_pricing(S0, X, t, r, sigma, iterations, 'call') for t in times]
        put_prices_over_time = [monte_carlo_option_pricing(S0, X, t, r, sigma, iterations, 'put') for t in times]

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
        call_prices_vs_volatility = [monte_carlo_option_pricing(S0, X, T, r, vol, iterations, 'call') for vol in volatilities]
        put_prices_vs_volatility = [monte_carlo_option_pricing(S0, X, T, r, vol, iterations, 'put') for vol in volatilities]

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

    # Monte Carlo Formula with LaTeX rendering and explanations on the sides
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
        st.latex(r"S_T = S_0 e^{(r - 0.5\sigma^2)T + \sigma \sqrt{T} Z}")
        st.markdown("""
        The Monte Carlo simulation calculates the possible future stock price \( S_T \) by randomly drawing from a normal distribution \( Z \), representing the uncertainty in future prices.
        """)

    with col_right:
        st.markdown(
            """
            **Time to Maturity (\( T \)):**<br>
            The longer the time to maturity, the more valuable the option, both for calls and puts, because the holder has more time to exercise the option. As time passes, the option value decreases due to time decay (Theta).<br><br>

            **Volatility (\( \sigma \)):**<br>
            Higher volatility means the underlying asset is more likely to experience significant price swings. This makes both call and put options more valuable, as the chance of the option ending in-the-money increases.<br><br>

            **Risk-Free Rate (\( r \)):**<br>
            The risk-free rate represents the return on a riskless investment. A higher rate increases the call option price (since future profits are worth more when discounted back) and decreases the put option price.
            """, unsafe_allow_html=True
        )

    # Space before the link
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Link to Monte Carlo method paper with more spacing
    st.markdown(
        "[Learn more about the Monte Carlo method](https://en.wikipedia.org/wiki/Monte_Carlo_method)"
        "[Read the original paper here](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/3741c4b04ff70a29c125809300569439/$FILE/1976_Options_A_Monte_Carlo_Approach.pdf)"
    )

# Run the Monte Carlo model page
# show_monte_carlo_page()
