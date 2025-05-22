from functools import lru_cache
import time
import matplotlib.pyplot as plt
import statistics

# LRU function
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Splay Tree Class
class Node:
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left_node = None
        self.right_node = None

class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        """Вставка нового елемента в дерево."""
        if self.root is None:
            self.root = Node(key, value)
        else:
            self._insert_node(key, value, self.root)

    def _insert_node(self, key, value, current_node):
        """Пошук елемента в дереві із застосуванням сплаювання."""
        if key < current_node.key:
            if current_node.left_node:
                self._insert_node(key, value, current_node.left_node)
            else:
                current_node.left_node = Node(key, value, current_node)
        elif key > current_node.key:
            if current_node.right_node:
                self._insert_node(key, value, current_node.right_node)
            else:
                current_node.right_node = Node(key, value, current_node)
        else:
            current_node.value = value  # Якщо такий ключ вже існує — оновити значення

    def get(self, key):
        """Пошук елемента в дереві із застосуванням сплаювання."""
        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left_node
            elif key > node.key:
                node = node.right_node
            else:
                self._splay(node)
                return node.value
        return None

    def _splay(self, node):
        """Реалізація сплаювання для переміщення вузла до кореня."""
        while node.parent is not None:
            if node.parent.parent is None:  # Zig-ситуація
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif node == node.parent.left_node and node.parent == node.parent.parent.left_node:  # Zig-Zig
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node == node.parent.right_node and node.parent == node.parent.parent.right_node:  # Zig-Zig
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:  # Zig-Zag
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        """Права ротація вузла."""
        left_child = node.left_node
        if left_child is None:
            return

        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node

        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child

        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        """Ліва ротація вузла."""
        right_child = node.right_node
        if right_child is None:
            return

        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node

        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child

        right_child.left_node = node
        node.parent = right_child


# Splay Tree function
def fibonacci_splay(n, tree):
    cached = tree.get(n)
    if cached is not None:
        return cached
    if n < 2:
        tree.insert(n, n)
        return n
    value = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, value)
    return value

# Measure
def measure_time(func, *args, repeats=5):
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        func(*args)
        end = time.perf_counter()
        times.append(end - start)
    return statistics.mean(times)

def main():
    n_values = list(range(0, 1000, 50))
    lru_times = []
    splay_times = []

    fibonacci_lru.cache_clear()

    for n in n_values:
        fibonacci_lru.cache_clear()
        lru_time = measure_time(fibonacci_lru, n)
        lru_times.append(lru_time)

        tree = SplayTree()
        splay_time = measure_time(fibonacci_splay, n, tree)
        splay_times.append(splay_time)

    # Зберегти графік
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, lru_times, marker='o', linestyle='--', label="LRU Cache")
    plt.plot(n_values, splay_times, marker='x', linestyle='-', label="Splay Tree")
    plt.xlabel("Число Фібоначчі (n)")
    plt.ylabel("Середній час виконання (секунди)")
    plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("fibonacci_comparison.png")

    # Створити README.md
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# Порівняння продуктивності: LRU Cache vs Splay Tree\n\n")
        f.write("## Таблиця результатів\n\n")
        f.write("| n | LRU Cache Time (s) | Splay Tree Time (s) |\n")
        f.write("|---|---------------------|----------------------|\n")
        for n, lru, splay in zip(n_values, lru_times, splay_times):
            f.write(f"| {n} | {lru:.8f} | {splay:.8f} |\n")

        f.write("\n## Графік виконання\n\n")
        f.write("![Графік виконання](fibonacci_comparison.png)\n\n")

        f.write("## Висновки\n\n")

if __name__ == "__main__":
    main()
