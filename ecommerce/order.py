"""
order.py - Order entity class for the e-commerce system.
Each Order is immutable once created and represents a completed purchase.
"""

import uuid
from datetime import datetime


class Order:
    """
    Represents a completed purchase order.

    Attributes:
        order_id (str): UUID-based unique identifier.
        customer_name (str): Name provided at checkout.
        items (list[dict]): Snapshot of purchased items at time of order.
            Each item dict: {product_id, name, price, quantity, subtotal}
        total_price (float): Grand total at the time of purchase.
        timestamp (str): ISO-format datetime string when the order was placed.
    """

    def __init__(self, customer_name, items, total_price, order_id=None, timestamp=None):
        """
        Create an Order.
        Args:
            customer_name (str): Buyer's name.
            items (list[dict]): Enriched snapshot of cart items.
            total_price (float): Computed grand total.
            order_id (str): Provide existing ID when loading from file.
            timestamp (str): Provide existing timestamp when loading.
        """
        self.order_id = order_id or str(uuid.uuid4())[:8].upper()
        self.customer_name = customer_name
        self.items = items  # snapshot — prices are frozen at purchase time
        self.total_price = float(total_price)
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    def to_dict(self):
        """Convert the order to a JSON-serializable dictionary."""
        return {
            "order_id": self.order_id,
            "customer_name": self.customer_name,
            "items": self.items,
            "total_price": self.total_price,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Reconstruct an Order from a stored dictionary.
        """
        return cls(
            order_id=data["order_id"],
            customer_name=data["customer_name"],
            items=data["items"],
            total_price=data["total_price"],
            timestamp=data["timestamp"],
        )

    def __repr__(self):
        return (
            f"<Order id={self.order_id} customer='{self.customer_name}' "
            f"total={self.total_price} at={self.timestamp}>"
        )
