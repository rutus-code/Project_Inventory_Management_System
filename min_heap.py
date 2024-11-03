import heapq

class LowStockHeap:
    def __init__(self):
        self.heap = []

    def add_product(self, stock_level, product_details):
        """Adds a product to the heap based on stock level."""
        heapq.heappush(self.heap, (stock_level, product_details))

    def get_lowest_stock(self):
        """Retrieves the product with the lowest stock."""
        return heapq.heappop(self.heap) if self.heap else "No products in inventory"

# Example usage:
low_stock_heap = LowStockHeap()
low_stock_heap.add_product(10, {"name": "Rutu A"})
low_stock_heap.add_product(5, {"name": "Rutu B"})
print(low_stock_heap.get_lowest_stock())
