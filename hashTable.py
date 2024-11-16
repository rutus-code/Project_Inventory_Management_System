#Created Date : 2nd November 2024
#Created By : Rutu Shah
# Data Structure Implemented : Hash Table

class InventoryHashTable:
    def __init__(self):
        # Dictionary to store product details by ID
        self.products = {}  

    def add_product(self, product_id, product_details):
        """To add or update a product in the hash table."""
        self.products[product_id] = product_details

    def get_product(self, product_id):
        """To retrieve product details by ID."""
        return self.products.get(product_id, "Product not found")

    def remove_product(self, product_id):
        """To Remove a product from the hash table by ID."""
        if product_id in self.products:
            del self.products[product_id]

# Example usage:
inventory = InventoryHashTable()
inventory.add_product("P001", {"name": "Rutu","price": 25, "stock": 100})
print(inventory.get_product("P001"))
inventory.remove_product("P001")
