# ShopEasy — Flask E-Commerce Web Application

A fully functional, object-oriented, JSON-persisted e-commerce system built with
**Flask**, **Bootstrap 5**, and **Jinja2** — no database required.

---

## Project Structure

```
ecommerce_project/
│
├── app.py                        ← Flask entry point (thin routes only)
│
├── ecommerce/                    ← OOP business logic package
│   ├── __init__.py
│   ├── product.py                ← Product entity (stock management)
│   ├── cart.py                   ← Cart (session-backed, calculations)
│   ├── order.py                  ← Order entity (immutable snapshot)
│   ├── user.py                   ← User (owns cart, drives checkout)
│   ├── file_handler.py           ← Strictly isolated JSON I/O
│   └── ecommerce_system.py       ← Core controller / facade
│
├── data/
│   ├── products.json             ← 10 seed products (auto-created if missing)
│   └── orders.json               ← Order history (starts empty)
│
├── templates/
│   ├── base.html                 ← Navbar, flash messages, footer
│   ├── products.html             ← Product grid + search/filter
│   ├── cart.html                 ← Cart view, update qty, remove
│   ├── checkout.html             ← Customer name form + order review
│   ├── order_confirmation.html   ← Post-purchase summary
│   └── orders.html               ← Full order history
│
├── static/
│   └── style.css                 ← Custom styles (Sora font, CSS vars)
│
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Clone / unzip the project

```bash
cd ecommerce_project
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open in browser

```
http://127.0.0.1:5000
```

---

## Features

| Feature | Details |
|---|---|
| Browse products | Product card grid with images, price, stock badge, category |
| Search | Case-insensitive name + description keyword search |
| Category filter | Dropdown populated dynamically from catalogue |
| Add to cart | Quantity selector per product; validates against stock |
| Cart management | Update quantities, remove items, running total |
| Checkout | Customer name form, full order review, stock validation |
| Stock deduction | Automatic on successful checkout, persisted to JSON |
| Order history | All past orders newest-first with item breakdown |
| Flash messages | Success / warning / error feedback on every action |
| Cart counter | Live badge in navbar showing total units in cart |
| Data persistence | products.json + orders.json survive server restarts |
| Edge cases | Empty cart blocked, over-stock blocked, invalid IDs handled |

---

## OOP Architecture

```
ECommerceSystem  ←  core controller; holds products + orders in memory
    │
    ├── FileHandler       ← ONLY does file I/O (load/save JSON)
    ├── Product           ← entity; update_stock(), to_dict(), from_dict()
    ├── Order             ← immutable snapshot; to_dict(), from_dict()
    └── User              ← owns Cart; drives checkout() workflow
            │
            └── Cart      ← {product_id: quantity}; add/remove/update/total
```

### Checkout flow (User.checkout)

1. Guard: raise ValueError if cart is empty
2. Guard: validate stock for every item before making changes
3. Deduct stock from each Product
4. Build frozen Order snapshot (prices locked at purchase time)
5. `FileHandler.save_products()` → persist updated stock
6. Append Order → `FileHandler.save_orders()` → persist order history
7. Clear cart

---

## Routes

| Method | URL | Purpose |
|---|---|---|
| GET | `/` or `/products` | Product catalogue (search/filter) |
| POST | `/add/<product_id>` | Add item to cart |
| GET | `/cart` | View cart |
| POST | `/update_cart/<product_id>` | Update cart item quantity |
| POST | `/remove/<product_id>` | Remove item from cart |
| GET | `/checkout` | Show checkout form |
| POST | `/checkout` | Process order |
| GET | `/order_confirmation/<order_id>` | Post-purchase confirmation |
| GET | `/orders` | Full order history |

---

## Validated Edge Cases

- **Empty cart checkout** → flash warning, redirect to products
- **Add quantity > stock** → flash error, cart unchanged
- **Update quantity to 0** → item removed from cart
- **Invalid product ID in URL** → flash error, redirect safely
- **Stock never goes negative** → double-validated before any mutation
- **Corrupt / missing JSON** → FileHandler returns empty list, app continues

---

## Technologies Used

- Python 3.10+
- Flask 3.x
- Jinja2 (bundled with Flask)
- Bootstrap 5.3
- Bootstrap Icons 1.11
- Google Fonts — Sora
- JSON file persistence (no database)
