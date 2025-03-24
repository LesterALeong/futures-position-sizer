import streamlit as st
import math

st.title("Micro Bitcoin Futures Position Size Calculator")

# Inputs
account_balance = st.number_input("Account Balance ($)", min_value=0.0, value=10000.0, step=100.0)
current_price = st.number_input("Current Futures Price (USD)", min_value=0.0, value=60000.0, step=100.0)
stop_loss_price = st.number_input("Stop Loss Price (USD)", min_value=0.0, value=59000.0, step=100.0)
risk_percent = st.number_input("Risk per Trade (% of Account)", min_value=0.1, max_value=100.0, value=1.0, step=0.1)

# Calculation
risk_amount = account_balance * (risk_percent / 100)
price_diff = abs(current_price - stop_loss_price)
loss_per_contract = price_diff * 0.1  # 0.1 BTC per micro contract

if loss_per_contract == 0:
    st.warning("Stop loss must be different from current price.")
else:
    num_contracts = math.floor(risk_amount / loss_per_contract)

    # Display results
    st.subheader("Results")
    st.write(f"**Risk Amount:** ${risk_amount:,.2f}")
    st.write(f"**Loss per Contract:** ${loss_per_contract:,.2f}")
    st.write(f"**Max Contracts to Trade:** {num_contracts} contracts")

    if num_contracts == 0:
        st.warning("Risk too low for even 1 contract. Increase risk % or widen stop.")
