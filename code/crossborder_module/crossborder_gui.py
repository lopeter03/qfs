# crossborder_gui.py
# Cross-Border Settlement GUI Demo with Consensus + FX Audit Trail
# Author: Peter (Quantum Financial System Project)

import streamlit as st
from crossborder_core import CrossBorderSettlement

st.title("🌍 Cross-Border Instant Settlement Demo (Dual Consensus + FX)")

if "crossborder" not in st.session_state:
    st.session_state.crossborder = CrossBorderSettlement()

sender = st.text_input("Sender")
receiver = st.text_input("Receiver")
amount = st.number_input("Amount", min_value=0.0, step=100.0)
from_currency = st.selectbox("From Currency", ["USD", "HKD", "EUR"])
to_currency = st.selectbox("To Currency", ["USD", "HKD", "EUR"])

ny_status = st.selectbox("NY Consensus Result", ["Confirm", "Reject"])
hk_status = st.selectbox("HK Consensus Result", ["Confirm", "Reject", "NoResponse"])

if st.button("Settle Transaction"):
    entry = st.session_state.crossborder.settle(
        sender, receiver, amount, from_currency, to_currency,
        ny_status=ny_status, hk_status=hk_status
    )
    st.success(f"Settlement outcome: {entry['outcome']}")
    st.write("📊 Transaction Details")
    st.write(f"Original Amount: {entry['original_amount']}")
    st.write(f"Converted Amount: {entry['converted_amount']}")
    st.write(f"Exchange Rate: {entry['exchange_rate']}")
    st.write(f"NY Consensus: {entry['ny_consensus']} ({entry['ny_status']})")
    st.write(f"HK Consensus: {entry['hk_consensus']} ({entry['hk_status']})")
    st.write(f"Funds Status: {entry['funds_status']}")

st.subheader("📝 Settlement Audit Trail")
for idx, entry in enumerate(st.session_state.crossborder.audit_trail, start=1):
    st.write(f"Case {idx}: {entry['outcome']}")
    st.json(entry)
