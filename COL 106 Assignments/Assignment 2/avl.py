from node import Node
#comp1 - blue,green comp2 - yellow, red
def comp(node_1, node_2):
    if node_1.key < node_2.key:
        return -1
    elif node_1.key > node_2.key:
        return 1
    else:
        return 0
def comp_1(node_1, node_2):
    if node_1.key < node_2.key:
        return -1
    elif node_1.key > node_2.key:
        return 1
    else:
        if node_1.value < node_2.value:
            return -1
        elif node_1.value > node_2.value:
            return 1
        else:
            return 0

def comp_2(node_1, node_2):
    if node_1.key < node_2.key:
        return -1
    elif node_1.key > node_2.key:
        return 1
    else:
        if node_1.value > node_2.value:
            return -1
        elif node_1.value < node_2.value:
            return 1
        else:
            return 0






class AVLTree:
    def __init__(self, compare_function=comp):
        self.root = None
        self.size = 0
        self.comparator = compare_function

    def is_root(self, p):
        return self.root == p

    def is_leaf(self, p):
        return p.left is None and p.right is None

    def is_empty(self):
        return self.size == 0

    def sibling(self, p):
        if self.is_root(p):
            return None
        if p == p.parent.left:
            return p.parent.right
        else:
            return p.parent.left

    def children(self, p):
        if p.left is not None:
            yield p.left
        if p.right is not None:
            yield p.right

    def height(self, p):
        if p is None:
            return 0
        return p.height

    def update_height(self, p):
        p.height = 1 + max(self.height(p.left), self.height(p.right))

    def recompute_height(self, p):
        while p is not None:
            self.update_height(p)
            p = p.parent

    def is_balanced(self, p):
        return abs(self.height(p.left) - self.height(p.right)) <= 1

    def balance(self, p):
        if self.height(p.left) > self.height(p.right):
            if self.height(p.left.left) >= self.height(p.left.right):
                p = self.rotate_right(p)
            else:
                p = self.rotate_left_right(p)
        else:
            if self.height(p.right.right) >= self.height(p.right.left):
                p = self.rotate_left(p)
            else:
                p = self.rotate_right_left(p)
        return p

    def rotate_left(self, p):
        if p is None or p.right is None:
            raise ValueError("Cannot perform left rotation on a null node or a node with no right child")
        x = p.right
        x.parent = p.parent
        if p.parent is None:
            self.root = x
        else:
            if p == p.parent.left:
                p.parent.left = x
            else:
                p.parent.right = x
        p.right = x.left
        if x.left is not None:
            x.left.parent = p
        p.parent = x
        x.left = p
        self.update_height(p)
        self.update_height(x)
        return x

    def rotate_right(self, p):
        if p is None or p.left is None:
            raise ValueError("Cannot perform right rotation on a null node or a node with no left child")
        x = p.left
        x.parent = p.parent
        if p.parent is None:
            self.root = x
        else:
            if p == p.parent.left:
                p.parent.left = x
            else:
                p.parent.right = x
        p.left = x.right
        if x.right is not None:
            x.right.parent = p
        p.parent = x
        x.right = p
        self.update_height(p)
        self.update_height(x)
        return x

    def rotate_left_right(self, p):
        if p is None or p.left is None:
            raise ValueError("Cannot perform left-right rotation on a null node or a node with no left child")
        p.left = self.rotate_left(p.left)
        return self.rotate_right(p)

    def rotate_right_left(self, p):
        if p is None or p.right is None:
            raise ValueError("Cannot perform right-left rotation on a null node or a node with no right child")
        p.right = self.rotate_right(p.right)
        return self.rotate_left(p)

    def insert(self, key, value):
        if key is None:
            raise ValueError("Key cannot be None")
        p = self._insert(key, value)
        self.recompute_height(p)
        while p is not None:
            if not self.is_balanced(p):
                p = self.balance(p)
            p = p.parent


    def _insert(self, key, value):
        if self.is_empty():
            self.root = Node(key, value)
            self.size = 1
            return self.root
        p = self.root
        new_node = Node(key, value)
        while True:
            if self.comparator(new_node, p) < 0:
                if p.left is None:
                    p.left = new_node
                    new_node.parent = p
                    self.size += 1
                    return p.left
                p = p.left
            else:
                if p.right is None:
                    p.right = new_node
                    new_node.parent = p
                    self.size += 1
                    return p.right
                p = p.right

    def find(self, key):
        if key is None:

            raise ValueError("Key cannot be None")
        p = self._find(key)
        if p is None:
            return None
        return p.value

    def _find(self, key):
        p = self.root
        temp = Node(key, None)
        while p is not None:
            if self.comparator(temp, p) == 0:
                return p
            elif self.comparator(temp, p) < 0:
                p = p.left
            else:
                p = p.right
        return None

    def remove(self, key):
        if key is None:
            raise ValueError("Key cannot be None")
        p = self._find(key)
        if p is None:
            raise KeyError(f"KeyError: {key} not found")
        self._remove(p)

    def _remove(self, p):
        if p.left is not None and p.right is not None:
            replacement = self._subtree_min(p.right)
            p.key, p.value = replacement.key, replacement.value
            p = replacement
        parent = p.parent
        if p.left is not None:
            child = p.left
        else:
            child = p.right
        if child is not None:
            child.parent = parent
        if parent is None:
            self.root = child
        else:
            if p == parent.left:
                parent.left = child
            else:
                parent.right = child
            self.recompute_height(parent)
            self.rebalance(parent)
        self.size -= 1

    def _subtree_min(self, p):
        while p.left is not None:
            p = p.left
        return p

    def rebalance(self, p):
        while p is not None:
            if not self.is_balanced(p):
                p = self.balance(p)
            self.update_height(p)
            p = p.parent

    def __len__(self):
        return self.size

    def num_children(self, p):
        count = 0
        if p.left is not None:
            count += 1
        if p.right is not None:
            count += 1
        return count

    def delete(self, p):
        self._remove(self._find(p))

    def __iter__(self):
        for p in self.inorder():
            yield p.key

    def inorder(self):
        if not self.is_empty():
            for p in self._inorder(self.root):
                yield p.key

    def _inorder(self, p):
        if p.left is not None:
            for other in self._inorder(p.left):
                yield other
        yield p
        if p.right is not None:
            for other in self._inorder(p.right):
                yield other

    def find_min(self):
        if self.is_empty():
            return None
        p = self.root
        while p.left is not None:
            p = p.left
        return p.key
    def find_max(self):
        if self.is_empty():
            return None
        p = self.root
        while p.right is not None:
            p = p.right

        return p.key
    def find_max_for_bins(self):
        if self.is_empty():
            return None
        p = self.root
        while p.right is not None:
            p = p.right

        return p.value, p.key
    def find_just_greater_or_equal(self, key, flag):
        #find the node with the smallest key greater than or equal to the given key, and if multiple keys exists return the one with the smallest value
        p = self.root
        candidate = None
        temp_node = Node(key, -1e9 if flag == 0 else 1e9)
        while p is not None:
            if self.comparator(temp_node, p) == 0:
                return p.value, p.key
            elif self.comparator(temp_node, p) < 0:
                candidate = p
                p = p.left
            else:
                p = p.right
        if candidate is not None:
            return candidate.value, candidate.key
        else:
            return None


    def _find_for_bins(self, capacity, bin_id):

        p = self.root
        temp_node = Node(capacity, bin_id)
        while p is not None:
            if self.comparator(temp_node, p) == 0:
                return p
            elif self.comparator(temp_node, p) < 0:
                p = p.left
            else:
                p = p.right


        return None
    def find_for_bins(self, p):
        return self._find_for_bins(p.key, p.value)
    def remove_for_bins(self, key, value):

        if key is None:
            raise ValueError("Key cannot be None")

        self._remove(self._find_for_bins(key, value))



    def __getitem__(self, key):
        return self.find(key)

    def __setitem__(self, key, value):
        self.insert(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def __contains__(self, key):
        return self.find(key) is not None

    def __bool__(self):
        return not self.is_empty()




