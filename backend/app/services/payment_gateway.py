"""A pretend payment company (sandbox). No real money moves.

A real version would call the bKash or Nagad API here. Everything else in the
project stays the same, because only these two functions would change.
"""

import uuid
from dataclasses import dataclass


@dataclass
class GatewayResult:
    ok: bool
    reference: str
    message: str


def charge(method: str, account: str, amount: int) -> GatewayResult:
    # Sandbox rule: a number ending in 0000 is "out of balance", so you can test a failure.
    if account.endswith("0000"):
        return GatewayResult(False, "", "Payment declined by the sandbox: not enough balance")
    return GatewayResult(True, f"SBX-{uuid.uuid4().hex[:10].upper()}", "Approved")


def refund(reference: str) -> str:
    return f"RF-{uuid.uuid4().hex[:10].upper()}"