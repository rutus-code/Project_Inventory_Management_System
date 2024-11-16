# Created By : Rutu Shah 
# Created Date : 15th November 2024
# This is the unitTestForInventoryManagement.py file which i have implemented to test the working of 
# Inventory Lookup developed using Hash Map Data Structure by importing unittest package, providing in built testing framework in python


import unittest
from HaspMapForInventory import  InventoryItem,  Inventory

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()
        self.inventory.add_item(1, "Laptop", "Electronics", 10, 1500.0)
        self.inventory.add_item(2, "Phone", "Electronics", 25, 800.0)

    def test_add_item(self):
        self.assertTrue(self.inventory.add_item(3, "Chair", "Furniture", 50, 45.0))
        self.assertFalse(self.inventory.add_item(1, "Duplicate Laptop", "Electronics", 5, 1400.0))

    def test_search_item(self):
        item = self.inventory.search_item(1)
        self.assertIsNotNone(item)
        self.assertEqual(item.name, "Laptop")

    def test_delete_item(self):
        self.assertTrue(self.inventory.delete_item(1))
        self.assertFalse(self.inventory.delete_item(4))

    def test_list_items(self):
        self.inventory.list_items()  # Manually verify output if necessary

if __name__ == "__main__":
    unittest.main()
