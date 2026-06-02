# asset_core.py
# Asset Backing Module with Audit Trail
# Author: Peter (Quantum Financial System Project)

import logging
import copy

class AssetReserve:
    def __init__(self):
        # Simulated reserves for valid assets only
        self.reserves = {
            "Gold": 1000000,        # grams
            "Commodity": 500000,    # units
            "Currency": 2000000     # USD
        }
        # Audit trail list
        self.audit_trail = []

    def check_reserve(self, asset_type, amount):
        # Only allow Gold, Commodity, Currency
        if asset_type not in self.reserves:
            return False, f"Asset type {asset_type} not supported (only Gold, Commodity, Currency allowed)"
        if amount > self.reserves[asset_type]:
            return False, f"Insufficient {asset_type} reserve"
        return True, None

    def process_transaction(self, asset_type, amount):
        """
        Process a transaction:
        - Capture BEFORE snapshot
        - Deduct reserves
        - Capture AFTER snapshot
        - Append both to audit trail
        """
        before_snapshot = copy.deepcopy(self.reserves)

        # Deduct reserve dynamically
        self.reserves[asset_type] -= amount

        after_snapshot = copy.deepcopy(self.reserves)

        # Record audit trail entry
        entry = {
            "asset_type": asset_type,
            "amount": amount,
            "before": before_snapshot,
            "after": after_snapshot
        }
        self.audit_trail.append(entry)

        logging.info(f"Transaction {amount} {asset_type}: BEFORE={before_snapshot[asset_type]}, AFTER={after_snapshot[asset_type]}")
        return entry
