# Created By : Rutu Shah
# Created Date : 15th November 2024
# Implementation of Hash Map data structure for inventory lookup 


class InventoryItem:
    def __init__(self, item_id, name, category, quantity, price):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price

    def __str__(self):
        return f"ID: {self.item_id}, Name: {self.name}, Category: {self.category}, Quantity: {self.quantity}, Price: {self.price}"

class Inventory:
    def __init__(self):
        self.items = {}  # Hash map for storing inventory items

    def add_item(self, item_id, name, category, quantity, price):
        if item_id in self.items:
            print(f"Item with ID {item_id} already exists.")
            return False
        self.items[item_id] = InventoryItem(item_id, name, category, quantity, price)
        print(f"Item {name} added successfully.")
        return True

    def delete_item(self, item_id):
        if item_id not in self.items:
            print(f"Item with ID {item_id} does not exist.")
            return False
        del self.items[item_id]
        print(f"Item with ID {item_id} deleted successfully.")
        return True

    def search_item(self, item_id):
        return self.items.get(item_id, None)

    def list_items(self):
        for item in sorted(self.items.values(), key=lambda x: x.name):
            print(item)


# Adding Test Cases : 
def demonstrate_inventory():
    inventory = Inventory()

    # Add items
    inventory.add_item(1, "Laptop", "Electronics", 10, 1500.0)
    inventory.add_item(2, "Phone", "Electronics", 25, 800.0)
    inventory.add_item(3, "Chair", "Furniture", 50, 45.0)

    # Search for an item
    item = inventory.search_item(2)
    if item:
        print("\nSearch Result:")
        print(item)

    # List all items
    print("\nAll Inventory Items (Sorted by Name):")
    inventory.list_items()

    # Delete an item
    inventory.delete_item(1)

    # List items after deletion
    print("\nInventory After Deletion:")
    inventory.list_items()

# Run demonstration
if __name__ == "__main__":
    demonstrate_inventory()


