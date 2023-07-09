from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from alpaca.trading.enums import OrderStatus


@dataclass
class MockOrder(object):
    id: UUID
    created_at: datetime
    open_price: float
    close_price: float
    stop_price: float
    status: OrderStatus


def create_order(open_price, close_price, stop_price, tzinfo) -> MockOrder:
    return MockOrder(
        uuid4(),
        datetime.now(tzinfo),
        open_price,
        close_price,
        stop_price,
        OrderStatus.PENDING_NEW
    )
