"""
ecommerce_system.py
Loads, stores, and coordinates all components.
"""

from ecommerce.file_handler import FileHandler

class ECommerceSystem:
    """
    Core controller that ties together all components.

    Responsibilities:
        - Load and hold the product catalogue and order history in memory.
        - Expose search / filter helpers.
        - Provide the products_map ({id: Product}) for O(1) lookup.
        - Coordinate checkout via the User class.
        - Surface the FileHandler for persistence where needed.
    """

    def __init__(self, products_path, orders_path):
        self.file_handler = FileHandler(products_path, orders_path)

        self.products = self.file_handler.load_products()
        self.orders = self.file_handler.load_orders()

    # ------------------------------------------------------------------
    # Products
    # ------------------------------------------------------------------

    def get_products_map(self):
        """
        Return a fast-lookup dictionary of all products.
        """
        return {p.id: p for p in self.products}

    def get_all_categories(self):
        """
        Return a sorted, deduplicated list of product categories.
        """
        return sorted({p.category for p in self.products})

    def search_and_filter(self, query="", category=""):
        """
        Filter the product catalogue by name/description and/or category.

        Returns:
            list[Product]: Matching products.
        """
        results = self.products

        if query:
            q = query.strip().lower()
            results = [
                p for p in results
                if q in p.name.lower() or q in p.description.lower()
            ]

        if category:
            cat = category.strip().lower()
            results = [p for p in results if p.category.strip().lower() == cat]

        return results

    def get_product_by_id(self, product_id):
        """
        Retrieve a single product by its ID.
        """
        return self.get_products_map().get(str(product_id))

    def reload_products(self):
        self.products = self.file_handler.load_products()

    # ------------------------------------------------------------------
    # Orders
    # ------------------------------------------------------------------

    def get_all_orders(self):
        """
        Return all orders, newest first.
        """
        return sorted(self.orders, key=lambda o: o.timestamp, reverse=True)

    def get_order_by_id(self, order_id):
        """
        Find a single order by its ID.
        """
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None

    # ------------------------------------------------------------------
    # Checkout coordination
    # ------------------------------------------------------------------

    def perform_checkout(self, user, customer_name):
        """
        Order: The newly created order.
        """
        products_map = self.get_products_map()

        order = user.checkout(
            customer_name=customer_name,
            products_map=products_map,
            file_handler=self.file_handler,
            orders_list=self.orders,
        )

        # Sync the flat list from the (now mutated) map
        self.products = list(products_map.values())

        return order
