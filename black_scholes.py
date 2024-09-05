import numpy as np
from scipy.stats import norm
import streamlit as st
import plotly.graph_objects as go

# Black-Scholes model function
def black_scholes(S, X, T, r, sigma, option_type='call'):
    d1 = (np.log(S / X) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        return S * norm.cdf(d1) - X * np.exp(-r * T) * norm.cdf(d2)
    else:
        return X * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# Black-Scholes model page
def show_black_scholes_page():
    st.title("Black-Scholes Option Pricing Model")

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

        # Display calculated call and put option prices right underneath the inputs
        call_option_price = black_scholes(S0, X, T, r, sigma, 'call')
        put_option_price = black_scholes(S0, X, T, r, sigma, 'put')

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
        call_prices_over_time = [black_scholes(S0, X, t, r, sigma, 'call') for t in times]
        put_prices_over_time = [black_scholes(S0, X, t, r, sigma, 'put') for t in times]

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
        call_prices_vs_volatility = [black_scholes(S0, X, T, r, vol, 'call') for vol in volatilities]
        put_prices_vs_volatility = [black_scholes(S0, X, T, r, vol, 'put') for vol in volatilities]

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

    # Black-Scholes Formula with LaTeX rendering and explanations on the sides
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_left:
        st.markdown(
            """
            **Stock Price (\( S_0 \)):**<br>
            This is the current price of the underlying asset. For a call option, a higher stock price means the buyer has a better opportunity to buy the stock at a lower strike price, hence increasing the value of the call option. For a put option, a higher stock price decreases its value because the option holder has the right to sell at a lower strike price.<br><br>

            **Strike Price (\( X \)):**<br>
            This is the price at which the option can be exercised. A higher strike price decreases the value of call options, as the right to buy the stock at a higher price is less attractive. Conversely, a higher strike price increases the value of put options since the right to sell at a higher price becomes more valuable.<br>

            **Important Basic Fact:**<br>
            **Options** provide the right, but not the obligation, to buy (call) or sell (put) an asset. This means the holder cannot lose more than the premium they paid for the option. If the market moves unfavorably (i.e., the option becomes out-of-the-money), the holder can simply let the option expire worthless, with their maximum loss limited to the premium they paid. This makes options a relatively low-risk way of participating in the markets, with limited downside but potentially unlimited upside (for call options).
            """, unsafe_allow_html=True
        )

    with col_center:
        st.latex(r"C = S_0 N(d_1) - X e^{-rT} N(d_2)")
        st.latex(r"P = X e^{-rT} N(-d_2) - S_0 N(-d_1)")
        st.latex(r"d_1 = \frac{\log(S_0 / X) + (r + 0.5 \sigma^2) T}{\sigma \sqrt{T}}")
        st.latex(r"d_2 = d_1 - \sigma \sqrt{T}")

    with col_right:
        st.markdown(
            """
            **Time to Maturity (\( T \)):**<br>
            Time to maturity is the period until the option expires. Longer time means greater uncertainty and more potential for the stock price to fluctuate, making both call and put options more valuable. The holder of the option has more time to benefit from favorable price movements. As time approaches expiration, options lose value (this is called time decay or Theta) because there’s less opportunity for the price to move favorably.<br><br>

            **Volatility (\( \sigma \)):**<br>
            Volatility represents the degree of variation in the price of the underlying asset. Higher volatility increases the chance of significant price swings, making both call and put options more valuable. The higher the volatility, the greater the chance that the option will end up in-the-money by expiration.<br><br>

            **Risk-Free Rate (\( r \)):**<br>
            The risk-free rate is the return on a theoretically riskless investment, such as a government bond. A higher risk-free rate increases the value of call options and decreases the value of put options because it affects the discount factor applied to the strike price. Higher rates make the future cash flow associated with the option less valuable when discounted back to present value.
            """, unsafe_allow_html=True
        )

    # Space before the link
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Link to full Black-Scholes paper with more spacing
    st.markdown(
        "[Read the full Black-Scholes paper here](https://www.math.ku.dk/~rolf/teaching/blackscholes.pdf)"
    )

# Run the Black-Scholes page
show_black_scholes_page()
