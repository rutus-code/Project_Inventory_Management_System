class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.products = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, product_name, product_details):
        node = self.root
        for char in product_name:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.products.append(product_details)

    def search_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._collect_all_products(node)

    def _collect_all_products(self, node):
        results = []
        if node.is_end_of_word:
            results.extend(node.products)
        for child in node.children.values():
            results.extend(self._collect_all_products(child))
        return results

# Example usage:
trie = Trie()
trie.insert("Rutu", {"name": "Rutu", "price": 25})
trie.insert("Detu Shah", {"name": "Detu Shah", "price": 40})
print(trie.search_prefix("D"))
