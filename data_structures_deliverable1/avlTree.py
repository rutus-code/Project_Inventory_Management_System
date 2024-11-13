#Created Date : 2nd November 2024
#Created By : Rutu Shah
# Data Structure Implemented : AVL Tree

class TreeNode:
    def __init__(self, key, product_details):
        self.key = key
        self.product_details = product_details
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def insert(self, root, key, product_details):
        if not root:
            return TreeNode(key, product_details)

        if key < root.key:
            root.left = self.insert(root.left, key, product_details)
        else:
            root.right = self.insert(root.right, key, product_details)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

# Instantiate the AVL Tree
avl_tree = AVLTree()
root = None  

# Inserting some products with different prices
products = [
    (30, {"name": "Product A", "price": 30, "stock": 15}),
    (20, {"name": "Product B", "price": 20, "stock": 10}),
    (40, {"name": "Product C", "price": 40, "stock": 5}),
    (10, {"name": "Product D", "price": 10, "stock": 20}),
    (25, {"name": "Product E", "price": 25, "stock": 8}),
    (50, {"name": "Product F", "price": 50, "stock": 7}),
]

# Insert each product into the AVL tree
for price, details in products:
    root = avl_tree.insert(root, price, details)

# Function to print the AVL tree in order
def in_order_traversal(node):
    if node:
        in_order_traversal(node.left)
        print(f"Product: {node.product_details['name']}, Price: {node.key}, Stock: {node.product_details['stock']}")
        in_order_traversal(node.right)

# Perform an in-order traversal to display the products
print("Products in AVL Tree (sorted by price):")
in_order_traversal(root)
