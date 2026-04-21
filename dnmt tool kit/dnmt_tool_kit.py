# dmmt_toolkit.py - Data Management Mini Toolkit
import collections

# --- TASK 1: BINARY SEARCH TREE (BST) ---
class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return BSTNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        return node

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None or node.key == key:
            return node is not None
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, root, key):
        if root is None: return root
        if key < root.key:
            root.left = self._delete(root.left, key)
        elif key > root.key:
            root.right = self._delete(root.right, key)
        else:
            # Case 1 & 2: No child or one child
            if root.left is None: return root.right
            elif root.right is None: return root.left
            # Case 3: Two children
            temp = self._min_value_node(root.right)
            root.key = temp.key
            root.right = self._delete(root.right, temp.key)
        return root

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder_traversal(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

# --- TASK 2: GRAPH (BFS & DFS) ---
class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_edge(self, u, v, weight):
        if u not in self.adj_list: self.adj_list[u] = []
        if v not in self.adj_list: self.adj_list[v] = []
        self.adj_list[u].append((v, weight))

    def bfs(self, start_node):
        visited = set()
        queue = collections.deque([start_node])
        visited.add(start_node)
        order = []
        while queue:
            u = queue.popleft()
            order.append(u)
            for v, w in self.adj_list.get(u, []):
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
        return order

    def dfs(self, start_node):
        visited = set()
        order = []
        def _dfs_util(u):
            visited.add(u)
            order.append(u)
            for v, w in self.adj_list.get(u, []):
                if v not in visited:
                    _dfs_util(v)
        _dfs_util(start_node)
        return order

# --- TASK 3: HASH TABLE (SEPARATE CHAINING) ---
class HashTable:
    def __init__(self, size=5):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return key % self.size

    def insert(self, key, value):
        idx = self._hash(key)
        for i, (k, v) in enumerate(self.table[idx]):
            if k == key:
                self.table[idx][i] = (key, value)
                return
        self.table[idx].append((key, value))

    def get(self, key):
        idx = self._hash(key)
        for k, v in self.table[idx]:
            if k == key: return v
        return None

    def delete(self, key):
        idx = self._hash(key)
        for i, (k, v) in enumerate(self.table[idx]):
            if k == key:
                self.table[idx].pop(i)
                return True
        return False

# --- MAIN RUNNER (TEST PLAN) ---
if __name__ == "__main__":
    print("--- BST TASK ---")
    bst = BST()
    for val in [50, 30, 70, 20, 40, 60, 80]: bst.insert(val)
    print("Inorder:", bst.inorder_traversal())
    print("Search 20:", bst.search(20), "| Search 90:", bst.search(90))
    bst.delete(20) # Leaf
    print("After delete 20 (leaf):", bst.inorder_traversal())
    bst.insert(65); bst.delete(60) # One child
    print("After delete 60 (one child):", bst.inorder_traversal())
    bst.delete(50) # Two children
    print("After delete 50 (root/two children):", bst.inorder_traversal())

    print("\n--- GRAPH TASK ---")
    g = Graph()
    edges = [('A','B',2), ('A','C',4), ('B','D',7), ('B','E',3), ('C','E',1), ('D','F',5), ('E','D',2), ('E','F',6), ('C','F',8)]
    for u, v, w in edges: g.add_edge(u, v, w)
    print("Adjacency List:", g.adj_list)
    print("BFS from A:", g.bfs('A'))
    print("DFS from A:", g.dfs('A'))

    print("\n--- HASH TABLE TASK ---")
    ht = HashTable(5)
    for k in [10, 15, 20, 7, 12]: ht.insert(k, f"Val_{k}")
    print("Table State (Chains):", ht.table)
    print("Get 15:", ht.get(15))
    ht.delete(10)
    print("Bucket 0 after deleting 10:", ht.table[0])