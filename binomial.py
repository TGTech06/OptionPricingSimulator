import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Binomial model function
def binomial_option_pricing(S: float, X: float, T: float, r: float, sigma: float, N: int, option_type: str = 'call') -> float:
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))  # Upward movement factor
    d = 1 / u  # Downward movement factor
    p = (np.exp(r * dt) - d) / (u - d)  # Probability of upward movement

    # Initialize stock price tree
    prices = np.zeros(N + 1)
    for i in range(N + 1):
        prices[i] = S * (u ** (N - i)) * (d ** i)

    # Initialize option values at maturity
    option_values = np.zeros(N + 1)
    for i in range(N + 1):
        if option_type == 'call':
            option_values[i] = max(0, prices[i] - X)  # Call option payoff
        else:
            option_values[i] = max(0, X - prices[i])  # Put option payoff

    # Step backward through the tree to calculate option price
    for j in range(N - 1, -1, -1):
        for i in range(j + 1):
            option_values[i] = np.exp(-r * dt) * (p * option_values[i] + (1 - p) * option_values[i + 1])

    return option_values[0]

# Binomial model page
def show_binomial_page():
    st.title("Binomial Option Pricing Model")

    st.markdown("""
    The **Binomial model** calculates option prices by simulating discrete price movements over the life of the option.

    ### Binomial Option Pricing Formula:
    In each time step, the stock price can either move up or down, and the option price is calculated by working backward through the price tree. The model is widely used for American options but can also be applied to European options.

    The option price at any node is computed as the discounted expected value of the option price in the subsequent time step.

    """)

    # Input layout
    col1, col2 = st.columns([1, 2])  # Adjusted to give more space to the graphs

    with col1:
        S0 = st.number_input("Stock Price (S0)", value=100.0, step=1.0, format="%.2f")
        X = st.number_input("Strike Price (X)", value=100.0, step=1.0, format="%.2f")
        T = st.slider("Time to Maturity (T)", min_value=0.01, max_value=5.0, value=1.0, step=0.01)
        sigma = st.slider("Volatility (σ)", min_value=0.01, max_value=1.0, value=0.2, step=0.01)
        r = st.slider("Risk-Free Rate (r)", min_value=0.0, max_value=0.2, value=0.05, step=0.001)
        N = st.number_input("Number of Steps (N)", value=100, step=1)

        # Add padding between inputs and price boxes
        st.markdown("<div style='padding-top:20px;'></div>", unsafe_allow_html=True)

        # Calculate the call and put option prices
        call_option_price = binomial_option_pricing(S0, X, T, r, sigma, N, 'call')
        put_option_price = binomial_option_pricing(S0, X, T, r, sigma, N, 'put')

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
        call_prices_over_time = [binomial_option_pricing(S0, X, t, r, sigma, N, 'call') for t in times]
        put_prices_over_time = [binomial_option_pricing(S0, X, t, r, sigma, N, 'put') for t in times]

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
        call_prices_vs_volatility = [binomial_option_pricing(S0, X, T, r, vol, N, 'call') for vol in volatilities]
        put_prices_vs_volatility = [binomial_option_pricing(S0, X, T, r, vol, N, 'put') for vol in volatilities]

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

    # Binomial Formula with LaTeX rendering and explanations on the sides
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
        st.latex(r"Option\ Value = e^{-r\Delta t}\ [pV_{up} + (1-p)V_{down}]")
        st.markdown("""
        In the binomial tree model, we calculate the option price at each step by working backward from maturity. At each node, we compute the expected value of the option in the next time step, weighted by the probability of moving up or down, and discount it to the present value.
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

    # Link to Binomial method explanation with more spacing
    st.markdown(
        "[Learn more about the Binomial option pricing model](https://en.wikipedia.org/wiki/Binomial_options_pricing_model)"
        "[Read the original paper here](https://tv-prod.s3.amazonaws.com/documents%2Fnull-Binomial+Option+Pricing+_f-0943_.pdf)"
    )

# Run the Binomial model page
# show_binomial_page()
