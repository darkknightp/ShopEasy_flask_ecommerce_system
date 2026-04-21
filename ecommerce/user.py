"""
user.py - User entity class for the e-commerce system.
"""

from ecommerce.cart import Cart
from ecommerce.order import Order

class User:
    """
    Represents the active session user.

    Attributes:
        name (str): Customer name (collected at checkout).
        cart (Cart): The user's current shopping cart.
    """

    def __init__(self, name="Guest", cart_items=None):
        """
        Initialize a User.
        """
        self.name = name
        self.cart = Cart(items=cart_items if cart_items is not None else {})


    def add_to_cart(self, product, quantity=1):
        """
        Add a product to this user's cart:
            product (Product): Product to add.
            quantity (int): Units to add.
        """
        self.cart.add_item(product, quantity)

    def remove_from_cart(self, product_id):
        """Remove a product line from this user's cart."""
        self.cart.remove_item(product_id)

    def update_cart_quantity(self, product_id, quantity, product=None):
        """Update the quantity for a cart item."""
        self.cart.update_quantity(product_id, quantity, product)

    # ------------------------------------------------------------------
    # Checkout
    # ------------------------------------------------------------------

    def checkout(self, customer_name, products_map, file_handler, orders_list):
        """
        Complete the purchase.

        Steps:
            1. Validate the cart is not empty.
            2. Validate stock availability for every item.
            3. Deduct stock from each product.
            4. Build an Order snapshot.
            5. Persist the updated products and the new order.
            6. Clear the cart.

        Raises:
            ValueError: If the cart is empty or stock is insufficient.
        """
        # 1. Guard: empty cart
        if self.cart.is_empty():
            raise ValueError("Your cart is empty. Please add items before checking out.")

        # 2. Guard: validate stock for every item before making any changes
        for product_id, quantity in self.cart.items.items():
            product = products_map.get(str(product_id))
            if not product:
                raise ValueError(f"Product ID '{product_id}' no longer exists.")
            if quantity > product.stock:
                raise ValueError(
                    f"Insufficient stock for '{product.name}'. "
                    f"Available: {product.stock}, In cart: {quantity}."
                )

        # 3. Deduct stock and build order item snapshot
        order_items = []
        for product_id, quantity in self.cart.items.items():
            product = products_map[str(product_id)]
            product.update_stock(quantity)  # mutates in-place
            order_items.append(
                {
                    "product_id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "quantity": quantity,
                    "subtotal": round(product.price * quantity, 2),
                }
            )

        total = self.cart.calculate_total(products_map)

        # 4. Create the order object
        order = Order(
            customer_name=customer_name,
            items=order_items,
            total_price=total,
        )

        # 5. Persist data
        file_handler.save_products(list(products_map.values()))
        orders_list.append(order)
        file_handler.save_orders(orders_list)

        # 6. Clear cart
        self.cart.clear()

        return order

    def __repr__(self):
        return f"<User name='{self.name}' cart_items={self.cart.get_cart_count()}>"
