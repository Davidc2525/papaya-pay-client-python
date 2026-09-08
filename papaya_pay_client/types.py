from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Transaction:
    id: str
    fee_cents: int
    net_amount_cents: int
    paid_currency: str

@dataclass
class WebhookEvent:
    app_id: str
    checkout_id: str
    status: str
    transaction: Transaction

@dataclass
class CheckoutItem:
    name: str
    quantity: int
    unit_price_ves_cents: int
    unit_price_usdc_cents: int

@dataclass
class Checkout:
    id: str
    app_id: str
    external_reference: str
    amount_ves_cents: int
    amount_usdc_cents: int
    paid_currency: Optional[str]
    status: str
    items: List[CheckoutItem]
    expires_at: int
    created_at: int
