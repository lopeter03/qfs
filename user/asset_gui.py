# asset_gui.py
# Asset Backing GUI Demo with Audit Trail
# Author: Peter (Quantum Financial System Project)

import streamlit as st
from asset_core import AssetReserve

st.title("🏦 Asset Backing Module Demo")

# Initialize reserves
if "asset_reserve" not in st.session_state:
    st.session_state.asset_reserve = AssetReserve()

# Transaction input
st.subheader("➕ Asset Transaction")
asset_type = st.selectbox("Asset Type", ["Gold", "Commodity", "Currency", "Equity", "Bond"])
amount = st.number_input("Amount", min_value=0.0, step=100.0)

if st.button("Check Reserve"):
    valid, error_msg = st.session_state.asset_reserve.check_reserve(asset_type, amount)
    if valid:
        entry = st.session_state.asset_reserve.process_transaction(asset_type, amount)
        st.success(f"Transaction approved ✔ {amount} {asset_type} backed by reserve")
        st.info(f"BEFORE: {entry['before'][asset_type]} | AFTER: {entry['after'][asset_type]}")
    else:
        st.error("Transaction rejected ❌")
        st.write("Reason:")
        st.text(error_msg)

# Display reserves
st.subheader("📊 Current Asset Reserves")
st.json(st.session_state.asset_reserve.reserves)

# Display audit trail
st.subheader("📝 Audit Trail (Before & After)")
for idx, entry in enumerate(st.session_state.asset_reserve.audit_trail, start=1):
    st.write(f"Transaction {idx}: {entry['amount']} {entry['asset_type']}")
    st.write("Before:")
    st.json(entry["before"])
    st.write("After:")
    st.json(entry["after"])
