import sys

sys.setrecursionlimit(200000)

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self, mode='standard'):
        if mode not in ['standard', 'optimized']:
            raise ValueError("Mode must be 'standard' or 'optimized'")
        self.mode = mode
        self.root = None
        self.stats = {'rotations': 0, 'comparisons': 0}

    def reset_stats(self):
        self.stats = {'rotations': 0, 'comparisons': 0}

    def get_height(self, node):
        if not node: return 0
        return node.height

    def get_balance(self, node):
        if not node: return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def _get_min_node(self, node):
        current = node
        while current.left: current = current.left
        return current

    def _get_max_node(self, node):
        current = node
        while current.right: current = current.right
        return current

    def _rotate_right(self, z):
        self.stats['rotations'] += 1
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def _rotate_left(self, z):
        self.stats['rotations'] += 1
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, key):
        self.root = self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if not node: return Node(key)
        
        self.stats['comparisons'] += 1
        if key < node.key: node.left = self._insert_recursive(node.left, key)
        else: node.right = self._insert_recursive(node.right, key)

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        if balance > 1 and key < node.left.key: return self._rotate_right(node)
        if balance < -1 and key > node.right.key: return self._rotate_left(node)
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def delete(self, key):
        self.root = self._delete_recursive(self.root, key)

    def _choose_replacement(self, node):
        use_predecessor = False
        if self.mode == 'standard':
            use_predecessor = False 
        elif self.mode == 'optimized':
            if self.get_height(node.left) > self.get_height(node.right):
                use_predecessor = True
        
        if use_predecessor:
            temp = self._get_max_node(node.left)
            new_key = temp.key
            new_sub = self._delete_recursive(node.left, new_key)
            return new_key, new_sub, 'left'
        else:
            temp = self._get_min_node(node.right)
            new_key = temp.key
            new_sub = self._delete_recursive(node.right, new_key)
            return new_key, new_sub, 'right'

    def _delete_recursive(self, node, key):
        if not node: return node
        self.stats['comparisons'] += 1
        
        if key < node.key: node.left = self._delete_recursive(node.left, key)
        elif key > node.key: node.right = self._delete_recursive(node.right, key)
        else:
            if node.left is None: return node.right
            elif node.right is None: return node.left
            
            new_key, new_sub, side = self._choose_replacement(node)
            node.key = new_key
            if side == 'left': node.left = new_sub
            else: node.right = new_sub

        if node is None: return node
        
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        if balance > 1 and self.get_balance(node.left) >= 0: return self._rotate_right(node)
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and self.get_balance(node.right) <= 0: return self._rotate_left(node)
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node
    
    def search(self, key):
        current = self.root
        while current:
            if key == current.key:
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return False
    
    def _count_nodes(self, node):
        if not node: return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)

    def _get_internal_path_length(self, node, current_depth):
        """Calculates the sum of depths of all nodes."""
        if not node: return 0
        return current_depth + \
               self._get_internal_path_length(node.left, current_depth + 1) + \
               self._get_internal_path_length(node.right, current_depth + 1)

    def get_average_depth(self):
        """Returns the average depth of nodes in the tree."""
        if not self.root: return 0
        n = self._count_nodes(self.root)
        if n == 0: return 0
        
        total_path_length = self._get_internal_path_length(self.root, 0)
        return total_path_length / n