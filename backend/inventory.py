import json
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Item:
    id: int
    name: str
    quantity: int
    price: float
    category: str

class Inventory:
    def __init__(self):
        self.items_by_id = {}
        self.inventory_value_history = []
        self.transaction_history = []
        self._total_value = 0.0

    def add_item(self, item):
        """Add a new item to the inventory with validation."""
        if item.quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        if item.price <= 0:
            raise ValueError("Price must be positive.")
        if item.id in self.items_by_id:
            raise ValueError(f"Item with ID {item.id} already exists.")
        self.items_by_id[item.id] = item
        self._total_value += item.quantity * item.price
        self._update_inventory_value_history()
        self.transaction_history.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"Added item {item.id}: {item.name}"))

    def remove_item(self, item_id):
        """Remove an item from the inventory."""
        if item_id not in self.items_by_id:
            raise ValueError(f"Item with ID {item_id} does not exist.")
        item = self.items_by_id[item_id]
        self._total_value -= item.quantity * item.price
        del self.items_by_id[item_id]
        self._update_inventory_value_history()
        self.transaction_history.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"Removed item {item_id}: {item.name}"))

    def update_item(self, item_id, new_quantity=None, new_price=None):
        """Update an item's quantity and/or price with validation."""
        if item_id not in self.items_by_id:
            raise ValueError(f"Item with ID {item_id} does not exist.")
        item = self.items_by_id[item_id]
        old_quantity = item.quantity
        old_price = item.price
        old_value = old_quantity * old_price
        if new_quantity is not None:
            if new_quantity < 0:
                raise ValueError("New quantity cannot be negative.")
            item.quantity = new_quantity
        if new_price is not None:
            if new_price <= 0:
                raise ValueError("New price must be positive.")
            item.price = new_price
        new_value = item.quantity * item.price
        self._total_value += new_value - old_value
        self._update_inventory_value_history()
        self.transaction_history.append((
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            f"Updated item {item_id}: Quantity {old_quantity} -> {item.quantity}, Price {old_price} -> {item.price}"
        ))

    def _update_inventory_value_history(self):
        """Update the inventory value history with total and category-wise values."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        category_values = {}
        for item in self.items_by_id.values():
            category_values[item.category] = category_values.get(item.category, 0) + item.quantity * item.price
        total_value = sum(category_values.values())
        self.inventory_value_history.append((timestamp, total_value, category_values))

    def total_inventory_value(self):
        """Return the current total inventory value."""
        return self._total_value

    def get_low_stock_items(self, threshold=10):
        """Get a list of items with quantity below the threshold."""
        return [item for item in self.items_by_id.values() if item.quantity < threshold]

    def save_to_file(self, filename="inventory_data.json"):
        """Save inventory data to a JSON file."""
        data = {
            "items": [
                {
                    "id": item.id,
                    "name": item.name,
                    "quantity": item.quantity,
                    "price": item.price,
                    "category": item.category,
                }
                for item in self.items_by_id.values()
            ],
            "history": self.inventory_value_history,
            "transactions": self.transaction_history,
        }
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def load_from_file(self, filename="inventory_data.json"):
        """Load inventory data from a JSON file."""
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                self.items_by_id = {}
                for item_data in data["items"]:
                    item = Item(
                        item_data["id"],
                        item_data["name"],
                        item_data["quantity"],
                        item_data["price"],
                        item_data["category"],
                    )
                    self.items_by_id[item.id] = item
                self._total_value = sum(item.quantity * item.price for item in self.items_by_id.values())
                self.inventory_value_history = data["history"]
                self.transaction_history = data.get("transactions", [])
        except FileNotFoundError:
            print("No existing data found. Starting with an empty inventory.")
        except json.JSONDecodeError:
            print("Invalid JSON data. Starting with an empty inventory.")
            self.items_by_id = {}
            self._total_value = 0.0
            self.inventory_value_history = []
            self.transaction_history = []