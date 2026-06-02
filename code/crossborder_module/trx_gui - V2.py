# trx_gui.py
# Transparent Transaction GUI Demo (PoW vs PoS Simulation)
# Author: Peter (Quantum Financial System Project)

import streamlit as st
import json
from trx_core import Blockchain

st.title("🔍 Transparent Transaction Demo (PoW vs PoS)")

# Initialize blockchain
if "qfs_chain" not in st.session_state:
    st.session_state.qfs_chain = Blockchain()

# Transaction input
st.subheader("➕ Add Transaction")
sender = st.text_input("Sender")
receiver = st.text_input("Receiver")
amount = st.number_input("Amount", min_value=0.0, step=100.0)
asset_type = st.selectbox("Asset Type", ["Gold", "Commodity", "Currency"])

if st.button("Add Transaction"):
    result = st.session_state.qfs_chain.add_transaction(sender, receiver, amount, asset_type)
    if result:
        st.success("Transaction added!")
    else:
        st.error("Transaction failed ❌")

# Consensus choice
st.subheader("⚡ Choose Consensus Mode")
consensus = st.radio("Consensus Algorithm", ["PoW (10s simulation)", "PoS (2s simulation)"])

if st.button("Mine Block"):
    mode = "PoW" if "PoW" in consensus else "PoS"
    st.info(f"Simulating {mode}... (Educational simulation, not real network delay)")
    new_block = st.session_state.qfs_chain.mine_block(mode)
    st.success(f"Block {new_block.index} mined with {mode}, hash: {new_block.hash}")

# Display blockchain
st.subheader("📜 Blockchain Audit Trail")
for block in st.session_state.qfs_chain.chain:
    st.json(block.__dict__)

# Verify chain
st.subheader("✅ Chain Verification")
if st.session_state.qfs_chain.verify_chain():
    st.info("Blockchain integrity verified ✔")
else:
    st.error("Blockchain integrity check failed ❌")
