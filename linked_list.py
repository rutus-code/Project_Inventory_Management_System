#Created Date : 2nd November 2024
#Created By : Rutu Shah
# Data Structure Implemented : Linked List

class ChangeNode:
    def __init__(self, timestamp, product_id, change):
        self.timestamp = timestamp
        self.product_id = product_id
        self.change = change
        self.next = None

class ChangeHistory:
    def __init__(self):
        self.head = None

    def add_change(self, timestamp, product_id, change):
        new_node = ChangeNode(timestamp, product_id, change)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def view_history(self):
        history = []
        current = self.head
        while current:
            history.append((current.timestamp, current.product_id, current.change))
            current = current.next
        return history

# Example usage:
history = ChangeHistory()
history.add_change("2024-01-01", "P001", "+10")
history.add_change("2024-01-02", "P002", "-5")
print(history.view_history())
