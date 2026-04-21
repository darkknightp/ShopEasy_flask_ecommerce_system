"""
cart.py - Shopping cart class for the e-commerce system.
"""
class Cart:
    """
    Items are stored as: {product_id (str): quantity (int)}
    """

    def __init__(self, items=None):
        """
        Initialise the cart.
        """
        # items is the dict stored directly in the Flask session
        self.items = items if items is not None else {}

    def add_item(self, product, quantity=1):
        """
        Add a product to the cart or increase its quantity.

        Raises:
            ValueError: If the quantity requested would exceed stock.
        """
        quantity = int(quantity)
        current_qty = self.items.get(str(product.id), 0)
        new_qty = current_qty + quantity

        if new_qty > product.stock:
            raise ValueError(
                f"Cannot add {quantity} unit(s) of '{product.name}'. "
                f"Only {product.stock - current_qty} unit(s) left to add."
            )

        self.items[str(product.id)] = new_qty

    def remove_item(self, product_id):
        """Remove a product line from the cart entirely."""
        self.items.pop(str(product_id), None)

    def update_quantity(self, product_id, quantity, product=None):
        """
        Set the cart quantity for a product to an exact value.

        Raises:
            ValueError: If the new quantity exceeds available stock.
        """
        quantity = int(quantity)
        if quantity <= 0:
            self.remove_item(product_id)
            return

        if product and quantity > product.stock:
            raise ValueError(
                f"Requested quantity ({quantity}) exceeds stock ({product.stock}) "
                f"for '{product.name}'."
            )

        self.items[str(product_id)] = quantity

    def clear(self):
        """Empty the cart."""
        self.items.clear()


    def is_empty(self):
        """Return True when the cart contains no items."""
        return len(self.items) == 0

    def calculate_total(self, products_map):
        """
        Compute the grand total for all items in the cart.
        """
        total = 0.0
        for product_id, quantity in self.items.items():
            product = products_map.get(str(product_id))
            if product:
                total += product.price * quantity
        return round(total, 2)

    def get_cart_count(self):
        """Return the total number of individual units in the cart."""
        return sum(self.items.values())

    def get_enriched_items(self, products_map):
        """
        Return cart lines enriched with full product details.
        """
        enriched = []
        for product_id, quantity in self.items.items():
            product = products_map.get(str(product_id))
            if product:
                enriched.append(
                    {
                        "product": product,
                        "quantity": quantity,
                        "subtotal": round(product.price * quantity, 2),
                    }
                )
        return enriched

    def __repr__(self):
        return f"<Cart items={self.items}>"
