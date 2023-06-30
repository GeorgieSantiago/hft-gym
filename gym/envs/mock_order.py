from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from alpaca.trading.enums import OrderStatus

@dataclass
class MockOrder(object):
    id: UUID
    created_at: datetime
    open_price: float
    close_price: float
    stop_price: float
    status: OrderStatus