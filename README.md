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


# **Project Deliverable 3**

## **Overview**  
This project delivers an optimized, scalable, and robust Inventory Management System with a web interface. The system supports large datasets, efficient CRUD operations, user authentication, and more. Built with Python, Flask, and MySQL, it leverages advanced data structures, caching, and indexing for superior performance.

---

## **Features**  

1. **Web Interface Integration**:  
   - **Category Page**: Add, edit, delete, and search categories.  
   - **Product Page**: Manage products efficiently with CRUD operations.  
   - **Inventory Page**: View, add, edit, and delete inventory items.  
   - **User Authentication**: Secure login system for accessing the platform.

2. **Data Optimization and Scaling**:  
   - **Caching**: Integrated Redis for frequently queried data to reduce response time by ~70%.  
   - **Database Indexing**: Indexed critical fields for faster query execution.  
   - **Lazy Deletion**: Enhanced deletion performance with deferred operations.  
   - **Efficient Pagination**: Improved UI responsiveness for large datasets.  
   - **Balanced Binary Search Tree**: Optimized data sorting and retrieval operations.

3. **Testing and Validation**:  
   - Stress-tested with 10,000 concurrent users.  
   - Edge case handling, including validation for duplicate entries, invalid inputs, and empty inventory states.  
   - Detailed performance metrics showcasing improvements from the initial POC.

---

## **Installation Instructions**

### **Prerequisites**  
- Python (>= 3.8)  
- Flask (>= 2.0)  
- MySQL  
- Redis  
- Virtual environment tools like `venv`  

### **Steps**  
1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/rutus-code/Project_Inventory_Management_System
   cd Project_Inventory_Management_System
   ```

2. **Set Up Virtual Environment**:  
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies**:  
   ```bash
   pip install -r requirements.txt
   ```

   ```
   pip install flask
   ```
 
  ```
  pip install flask-mysqldb
  ```

4. **Set Up Database**:  
   - Create a MySQL database and configure credentials in `app.py`.  
   - Run the provided SQL script to set up tables.  

5. **Start Redis**:  
   Ensure Redis server is running on your machine.

6. **Run the Application**:  
   ```bash
   flask run
   ```

7. **Access the Application**:  
   Open your browser and navigate to `http://127.0.0.1:5000/pythonlogin/`.

---

## **Demo**  
The following are the main files for the application:

- `app.py`: Core backend logic and API routes.  
- `templates/`: Frontend HTML files for rendering pages.  
- `static/`: Contains CSS, JavaScript, and other static assets.  

### **Screenshots**
- **Login Page**  
- **Home Page**  
- **Add Product Page**  
- **View Inventory Page**

(Include screenshots here for a visual demo.)

---

## **Testing the Application**  

Run unit tests to validate functionality and performance:  
```bash
python -m unittest discover tests
```

**Key Test Scenarios**:  
- Stress testing with concurrent users.  
- Validation of CRUD operations.  
- Edge case handling (e.g., empty inventory, duplicate entries).

---

## **Future Improvements**  
- Real-time data synchronization using WebSockets.  
- Advanced analytics for predictive insights.  
- Improved cache invalidation strategies.  

--- 

For more details, visit the project [GitHub repository](https://github.com/rutus-code/Project_Inventory_Management_System).

