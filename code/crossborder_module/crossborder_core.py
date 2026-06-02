# crossborder_core.py
# Cross-Border Instant Settlement with Consensus + FX Audit Trail
# Author: Peter (Quantum Financial System Project)

import logging
import time

class FXRates:
    def __init__(self):
        self.rates = {
            ("USD", "HKD"): 7.8,
            ("HKD", "USD"): 0.128,
            ("USD", "EUR"): 0.9,
            ("EUR", "USD"): 1.11,
            ("HKD", "EUR"): 0.115,
            ("EUR", "HKD"): 8.7
        }

    def convert(self, amount, from_currency, to_currency):
        if (from_currency, to_currency) not in self.rates:
            return None, None, f"No FX rate for {from_currency}->{to_currency}"
        rate = self.rates[(from_currency, to_currency)]
        converted = amount * rate
        return converted, rate, None

class CrossBorderSettlement:
    def __init__(self):
        self.audit_trail = []

    def settle(self, sender, receiver, amount, from_currency, to_currency,
               ny_status="Confirm", hk_status="Confirm"):
        fx = FXRates()
        converted, rate, error = fx.convert(amount, from_currency, to_currency)

        if error:
            outcome = "Failed"
            funds_status = error
            converted_amount = None
        else:
            # --- Case logic ---
            if ny_status == "Confirm" and hk_status == "Confirm":
                outcome = "Completed"
                funds_status = "Released to receiver"
            elif ny_status == "Confirm" and hk_status == "Reject":
                outcome = "Failed"
                funds_status = "Rolled back to sender"
            elif ny_status == "Confirm" and hk_status == "NoResponse":
                outcome = "Pending"
                funds_status = "Locked in escrow"
            elif ny_status == "Reject" and hk_status == "Confirm":
                outcome = "Failed"
                funds_status = "Rejected at sender side (no funds transmitted)"
            elif ny_status == "Reject" and hk_status == "Reject":
                outcome = "Failed"
                funds_status = "Dual rejection, no funds moved"
            else:
                outcome = "Unknown"
                funds_status = "Invalid status combination"
            converted_amount = f"{converted:.2f} {to_currency}"

        # --- Audit trail entry ---
        entry = {
            "sender": sender,
            "receiver": receiver,
            "original_amount": f"{amount} {from_currency}",
            "converted_amount": converted_amount,
            "exchange_rate": f"1 {from_currency} = {rate} {to_currency}" if rate else None,
            "ny_consensus": "PoW",
            "ny_status": ny_status,
            "hk_consensus": "PoS",
            "hk_status": hk_status,
            "funds_status": funds_status,
            "outcome": outcome,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.audit_trail.append(entry)
        logging.info(f"Cross-border settlement: {entry}")
        return entry
