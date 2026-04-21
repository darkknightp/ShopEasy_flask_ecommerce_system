"""
product.py - Product entity class for the e-commerce system.
"""

class Product:
    """
    Represents a product in the e-commerce catalogue.

    Attributes:
        id (str): Unique product identifier.
        name (str): Product display name.
        price (float): Unit price in USD.
        stock (int): Available stock quantity.
        category (str): Product category label.
        description (str): Short product description.
        image_url (str): URL to the product image.
    """

    def __init__(self, id, name, price, stock, category, description, image_url=""):
        self.id = str(id)
        self.name = name
        self.price = float(price)
        self.stock = int(stock)
        self.category = category
        self.description = description
        self.image_url = image_url

    # ------------------------------------------------------------------
    # Stock management
    # ------------------------------------------------------------------

    def update_stock(self, quantity):
        """
        Reduce stock by the given quantity.
        """
        if quantity > self.stock:
            raise ValueError(
                f"Insufficient stock for '{self.name}'. "
                f"Available: {self.stock}, Requested: {quantity}"
            )
        self.stock -= quantity

    def is_in_stock(self):
        """Return True if at least one unit is available."""
        return self.stock > 0

    def to_dict(self):
        """Convert the product to a JSON-serializable dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "description": self.description,
            "image_url": self.image_url,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Construct a Product instance from a dictionary.
        """
        return cls(
            id=data["id"],
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
            category=data["category"],
            description=data["description"],
            image_url=data.get("image_url", ""),
        )

    def __repr__(self):
        return f"<Product id={self.id} name='{self.name}' price={self.price} stock={self.stock}>"
