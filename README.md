# Project_Inventory_Management_System
MSCS532_Project_Inventory_Management_System

Hello Professor, 

## Project Phase Deliverable 1: 
In this project I am implementing inventory Management System using following data structures. 
1. Hash Table
2. AVL Tree
3. Heap Priority Queue
4. Linked list
5. Trie for searching product by name or category.

This is the part 1 deliverable where i have implemented the codes for the above mentioned data structure and a brief summary of how IMS works to capture the data dynamically.


## Project Phase Deliverable 2: 
## Overview
This is a Proof of Concept (POC) implementation of an Inventory Management System using Python and the Flask framework. The core functionality leverages a hash map data structure for efficient inventory lookup. The project includes a web interface for user interaction and demonstrates the insertion, deletion, searching, and listing of inventory items to be implemented in phase 3. 

## Features
* Efficient Lookup: Uses hash maps for quick and efficient inventory operations.
Core Operations:
1. Add new inventory items.
2. Search for existing items by ID.
3. Delete items from the inventory.
4. Display all items, sorted alphabetically by name.
5. Web Interface: A Flask-based user interface to interact with the inventory system to be implemented in phase 3
6. Testing: Includes unit tests to verify the correctness of key operations.

## Technologies Used
* Backend: Python 3.x
* Data Structure: Hash Map (Python Dictionary)
* Testing: Python unittest framework

## Prerequisites
* Python 3.x installed

## Setup and execution

 1. Git clone the repository
```
git clone https://github.com/rutus-code/Project_Inventory_Management_System
cd Project_Inventory_Management_System
```
 2. Execute HaspMapForInventory.py file
```
python3 HaspMapForInventory.py 
```
 3. For unittest execute unitTestForInventoryManagement.py 
```
python3 unitTestForInventoryManagement.py 
```

## How It Works
* The system uses a hash map to store inventory items. Each item is represented by an InventoryItem object, stored with a unique item_id as the key. Key operations include:

1. Add Item: Adds a new inventory item to the hash map.
2. Search Item: Finds an item by its item_id.
3. Delete Item: Removes an item by its item_id.
4. List Items: Displays all items sorted by their names.

## Future Enhancements
1. Extend the hash map to handle complex queries.
2. Integrate a database for persistent storage.
3. Add user authentication and role-based access control.
4. Introducing the web interface for IMS to enhance user experience.
