import streamlit as st
import math

st.title("Micro Futures Position Size Calculator")

# Micro futures data (symbol: [name, multiplier])
futures_data = {
    "/MES": ["Micro E-mini S&P 500", 5],
    "/M2K": ["Micro E-mini Russell 2000", 5],
    "/MYM": ["Micro E-mini DOW", 0.5],
    "/MNQ": ["Micro E-mini Nasdaq-100", 2],
    "/MGC": ["Micro Gold", 10],
    "/SIL": ["Micro Silver", 1000],
    "/MHG": ["Micro Copper", 2500],
    "/MCL": ["Micro WTI Crude Oil", 100],
    "/MNG": ["Micro Natural Gas", 1000],
    "/M6E": ["Micro EUR/USD", 12500],
    "/M6A": ["Micro AUD/USD", 10000],
    "/MCD": ["Micro CAD/USD", 10000],
    "/M6B": ["Micro GBP/USD", 6250],
    "/MSF": ["Micro CHF/USD", 12500],
    "/10Y": ["Micro 10-Year Yield", 1000],
    "/MBT": ["Micro Bitcoin", 0.1],
    "/MET": ["Micro Ether", 0.1],
}

# --- UI Inputs ---
symbol = st.selectbox("Select Micro Futures Symbol", list(futures_data.keys()), format_func=lambda x: f"{x} - {futures_data[x][0]}")
account_balance = st.number_input("Account Balance ($)", min_value=0.0, value=10000.0, step=100.0)
entry_price = st.number_input("Current Futures Price", min_value=0.0, value=60000.0, step=100.0)
stop_loss_price = st.number_input("Stop Loss Price", min_value=0.0, value=59000.0, step=100.0)
risk_percent = st.number_input("Risk per Trade (% of Account)", min_value=0.1, max_value=100.0, value=1.0, step=0.1)
r_multiple = st.number_input("Take Profit Multiple (R)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

# --- Button ---
if st.button("Calculate Position Size"):
    multiplier = futures_data[symbol][1]
    price_diff = abs(entry_price - stop_loss_price)
    risk_amount = account_balance * (risk_percent / 100)
    loss_per_contract = price_diff * multiplier

    if loss_per_contract == 0:
        st.warning("Stop loss must be different from entry price.")
    else:
        num_contracts = math.floor(risk_amount / loss_per_contract)

        # Determine direction for TP
        if entry_price > stop_loss_price:
            # Long
            target_price = entry_price + (price_diff * r_multiple)
        else:
            # Short
            target_price = entry_price - (price_diff * r_multiple)

        # --- Dollar offsets ---
        dollar_distance_to_stop = abs(entry_price - stop_loss_price)
        dollar_distance_to_target = abs(target_price - entry_price)

        # --- Display Results ---
        st.subheader("Results")
        st.write(f"**Contract:** {symbol} - {futures_data[symbol][0]}")
        st.write(f"**Contract Multiplier:** {multiplier}")
        st.write(f"**Risk Amount:** ${risk_amount:,.2f}")
        st.write(f"**Loss per Contract:** ${loss_per_contract:,.2f}")
        st.write(f"**Max Contracts to Trade:** {num_contracts} contracts")
        st.write(f"**Target Profit Price (for {r_multiple}R):** {target_price:,.2f}")
        st.write(f"**$ Distance from Entry to Stop Loss:** {dollar_distance_to_stop:,.2f}")
        st.write(f"**$ Distance from Entry to {r_multiple}R Target:** {dollar_distance_to_target:,.2f}")

        if num_contracts == 0:
            st.warning("Risk too low for even 1 contract. Increase risk % or widen stop.")
