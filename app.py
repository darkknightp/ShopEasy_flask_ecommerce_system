"""
app.py - Flask entry point for the ShopEasy e-commerce application.
"""

import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)

from ecommerce.ecommerce_system import ECommerceSystem
from ecommerce.user import User

# ---------------------------------------------------------------------------
# App configuration
# ---------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = "shopeasy-secret-key-2026"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_PATH = os.path.join(BASE_DIR, "data", "products.json")
ORDERS_PATH = os.path.join(BASE_DIR, "data", "orders.json")

system = ECommerceSystem(PRODUCTS_PATH, ORDERS_PATH)

# ---------------------------------------------------------------------------
# Session helpers
# ---------------------------------------------------------------------------
def get_user():
    cart_items = session.get("cart", {})
    return User(name=session.get("customer_name", "Guest"), cart_items=cart_items)

def save_cart(user):
    session["cart"] = user.cart.items
    session.modified = True

# ---------------------------------------------------------------------------
# Context processor — injects cart count into every template
# ---------------------------------------------------------------------------

@app.context_processor
def inject_cart_count():
    user = get_user()
    return {"cart_count": user.cart.get_cart_count()}

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
@app.route("/products")
def products():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()

    filtered = system.search_and_filter(query=query, category=category)
    categories = system.get_all_categories()

    return render_template(
        "products.html",
        products=filtered,
        categories=categories,
        selected_category=category,
        search_query=query,
    )

@app.route("/add/<product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = system.get_product_by_id(product_id)
    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for("products"))

    quantity = int(request.form.get("quantity", 1))
    user = get_user()

    try:
        user.add_to_cart(product, quantity)
        save_cart(user)
        flash(f"'{product.name}' added to cart.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("products"))

@app.route("/cart")
def cart():
    """Display the current cart contents."""
    user = get_user()
    products_map = system.get_products_map()
    enriched = user.cart.get_enriched_items(products_map)
    total = user.cart.calculate_total(products_map)

    return render_template("cart.html", cart_items=enriched, total=total)

@app.route("/update_cart/<product_id>", methods=["POST"])
def update_cart(product_id):
    quantity = request.form.get("quantity", 1)
    product = system.get_product_by_id(product_id)
    user = get_user()

    try:
        user.update_cart_quantity(product_id, quantity, product)
        save_cart(user)
        flash("Cart updated.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("cart"))

@app.route("/remove/<product_id>", methods=["POST"])
def remove_from_cart(product_id):
    user = get_user()
    user.remove_from_cart(product_id)
    save_cart(user)
    flash("Item removed from cart.", "info")
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    user = get_user()
    products_map = system.get_products_map()

    if request.method == "GET":
        if user.cart.is_empty():
            flash("Your cart is empty. Please add items first.", "warning")
            return redirect(url_for("products"))

        enriched = user.cart.get_enriched_items(products_map)
        total = user.cart.calculate_total(products_map)
        return render_template("checkout.html", cart_items=enriched, total=total)

    customer_name = request.form.get("customer_name", "").strip()
    if not customer_name:
        flash("Please enter your name to complete the order.", "danger")
        return redirect(url_for("checkout"))

    try:
        order = system.perform_checkout(user, customer_name)
        save_cart(user)  # Cart is now cleared — sync to session
        session["customer_name"] = customer_name
        flash(f"Order #{order.order_id} placed successfully!", "success")
        return redirect(url_for("order_confirmation", order_id=order.order_id))
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("cart"))


@app.route("/order_confirmation/<order_id>")
def order_confirmation(order_id):
    order = system.get_order_by_id(order_id)
    if not order:
        flash("Order not found.", "danger")
        return redirect(url_for("products"))
    return render_template("order_confirmation.html", order=order)


@app.route("/orders")
def orders():
    all_orders = system.get_all_orders()
    return render_template("orders.html", orders=all_orders)

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
