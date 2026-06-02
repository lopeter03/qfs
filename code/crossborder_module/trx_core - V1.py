# trx_core.py
# Transparent Transaction Core Logic with Quality Stack
# Author: Peter (Quantum Financial System Project)

import logging
import json
import time
from hashlib import sha256

# --- Quality Stack Setup ---
logging.basicConfig(
    filename="transaction_audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def safe_execute(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper

# --- Block structure ---
class Block:
    def __init__(self, index, previous_hash, transactions, consensus, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.transactions = transactions
        self.consensus = consensus
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'consensus': self.consensus
        }, sort_keys=True).encode()
        return sha256(block_string).hexdigest()

# --- Blockchain structure ---
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    @safe_execute
    def create_genesis_block(self):
        logging.info("Genesis block created")
        return Block(0, "0", ["Genesis Block"], "N/A")

    @safe_execute
    def add_transaction(self, sender, receiver, amount, asset_type="Gold"):
        tx = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "asset_type": asset_type,
            "audit_timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.pending_transactions.append(tx)
        logging.info(f"Transaction added: {tx}")

    @safe_execute
    def mine_block(self, consensus="PoW"):
        previous_hash = self.chain[-1].hash
        delay = 10 if consensus == "PoW" else 2  # 模擬耗時
        time.sleep(delay)
        new_block = Block(len(self.chain), previous_hash, self.pending_transactions, consensus)
        self.chain.append(new_block)
        self.pending_transactions = []
        logging.info(f"Block {new_block.index} mined with {consensus}, hash: {new_block.hash}")
        return new_block

    @safe_execute
    def verify_chain(self):
        for i in range(1, len(self.chain)):
            prev = self.chain[i - 1]
            curr = self.chain[i]
            if curr.previous_hash != prev.hash:
                logging.error("Blockchain integrity check failed")
                return False
        logging.info("Blockchain integrity verified")
        return True
