# blockchain_core.py
# Blockchain Ledger with Cross-Border Settlement Integration
# Author: Peter (Quantum Financial System Project)

import hashlib
import json
import time

class Block:
    def __init__(self, index, previous_hash, transaction, settlement):
        self.index = index
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.transaction = transaction          # Original transaction data
        self.settlement = settlement            # Settlement audit trail entry
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transaction": self.transaction,
            "settlement": self.settlement,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", {"info": "Genesis Block"}, {"info": "No settlement"})

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, transaction, settlement):
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), latest_block.hash, transaction, settlement)
        self.chain.append(new_block)
        return new_block

if __name__ == "__main__":
    # Demo run
    from pprint import pprint

    # Initialize blockchain
    ledger = Blockchain()

    # Example transaction + settlement
    transaction = {"sender": "Alice", "receiver": "Bob", "amount": "1000 USD"}
    settlement = {
        "original_amount": "1000 USD",
        "converted_amount": "7800 HKD",
        "exchange_rate": "1 USD = 7.8 HKD",
        "ny_consensus": "PoW",
        "ny_status": "Confirm",
        "hk_consensus": "PoS",
        "hk_status": "Confirm",
        "funds_status": "Released to receiver",
        "outcome": "Completed",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    # Add block
    block = ledger.add_block(transaction, settlement)

    print("✅ New block added:")
    pprint(vars(block))

    print("\n📜 Full blockchain ledger:")
    for b in ledger.chain:
        pprint(vars(b))
