"""
file_handler.py - Strictly isolated file I/O layer.
All reading and writing of JSON data files is handled exclusively here.
"""

import json
import os

from ecommerce.product import Product
from ecommerce.order import Order


class FileHandler:
    """
    Handles all JSON file operations for the e-commerce system.

    Responsibilities:
        - Load / save products.json
        - Load / save orders.json
        - Auto-create missing files
        - Handle corrupt or empty files gracefully
    """

    def __init__(self, products_path, orders_path):
        self.products_path = products_path
        self.orders_path = orders_path

        # Ensure data directory and files exist on first run
        self._ensure_file(self.products_path, default=[])
        self._ensure_file(self.orders_path, default=[])


    @staticmethod
    def _ensure_file(path, default):
        """Create a JSON file with a default value if it does not exist."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(default, f, indent=2)

    @staticmethod
    def _read_json(path):
        """
        Read and parse a JSON file.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError, OSError):
            return []

    @staticmethod
    def _write_json(path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ------------------------------------------------------------------
    # Products
    # ------------------------------------------------------------------

    def load_products(self):
        """
        Read products.json
        """
        raw_list = self._read_json(self.products_path)
        products = []
        for item in raw_list:
            try:
                products.append(Product.from_dict(item))
            except (KeyError, TypeError, ValueError):
                # Skip malformed entries — don't crash the whole system
                continue
        return products

    def save_products(self, products):
        """
        Serialize and write a list of Product objects to products.json.
        """
        self._write_json(self.products_path, [p.to_dict() for p in products])

    # ------------------------------------------------------------------
    # Orders
    # ------------------------------------------------------------------

    def load_orders(self):
        """
        Read orders.json
        """
        raw_list = self._read_json(self.orders_path)
        orders = []
        for item in raw_list:
            try:
                orders.append(Order.from_dict(item))
            except (KeyError, TypeError, ValueError):
                continue
        return orders

    def save_orders(self, orders):
        """
        Serialize and write a list of Order objects to orders.json.
        """
        self._write_json(self.orders_path, [o.to_dict() for o in orders])
