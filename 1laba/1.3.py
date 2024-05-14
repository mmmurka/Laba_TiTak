import heapq
from collections import defaultdict, Counter, deque

import networkx as nx
from matplotlib import pyplot as plt


class Node:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

def build_codes(node, prefix='', codebook={}):
    if node:
        if node.char is not None:
            codebook[node.char] = prefix
        build_codes(node.left, prefix + '0', codebook)
        build_codes(node.right, prefix + '1', codebook)
    return codebook

def huffman_encoding(text):
    frequencies = Counter(text)
    tree = build_huffman_tree(frequencies)
    codebook = build_codes(tree)

    encoded_text = ''.join([codebook[char] for char in text])
    return encoded_text, codebook, tree

def huffman_decoding(encoded_text, tree):
    decoded_text = []
    node = tree
    for bit in encoded_text:
        node = node.left if bit == '0' else node.right
        if node.char is not None:
            decoded_text.append(node.char)
            node = tree

    return ''.join(decoded_text)

def calculate_average_length(codebook, frequencies):
    total_freq = sum(frequencies.values())
    weighted_length = sum(len(code) * freq for char, code in codebook.items() for freq in [frequencies[char]])
    return weighted_length / total_freq

def calculate_entropy(frequencies, total):
    from math import log2
    return -sum((freq / total) * log2(freq / total) for freq in frequencies.values())

# Ваша текстова фраза
text = """
Кохайтеся, чорнобриві,
Та не з москалями,
Бо москалі — чужі люде,
Роблять лихо з вами.
Москаль любить жартуючи,
Жартуючи кине;
Піде в свою Московщину,
А дівчина гине...
"""

# Кодування
encoded_text, codebook, tree = huffman_encoding(text)

# Розрахунки
frequencies = Counter(text)
average_length = calculate_average_length(codebook, frequencies)
entropy = calculate_entropy(frequencies, sum(frequencies.values()))

efficiency = entropy / average_length
compression_ratio = (len(text) * 8) / len(encoded_text)

# Роздрукуємо результати
print("Кодова книга Гаффмана:", codebook)
print("Закодований текст:", encoded_text)
print("Середня довжина кодового слова:", average_length)
print("Ентропія тексту:", entropy)
print("Ефективність кодування:", efficiency)
print("Коефіцієнт стиснення:", compression_ratio)

# Декодування
decoded_text = huffman_decoding(encoded_text, tree)
assert text == decoded_text, "Декодування не збігається з оригіналом!"


def plot_simple_huffman_tree(root):
    # Initialize a directed graph
    G = nx.DiGraph()
    labels = {}
    pos = {}
    queue = deque([(root, "", (0, 0))])  # (node, label, position)

    # Using BFS to visit nodes and build the graph
    while queue:
        node, path, (x, y) = queue.popleft()
        if node.char:
            node_label = f"{node.char}({node.freq})"
        else:
            node_label = f"{node.freq}"

        # Assign labels and positions
        G.add_node(node_label)
        labels[node_label] = node_label
        pos[node_label] = (x, y)

        # Calculate horizontal offset for children
        offset = 6 / (2 ** -y)  # Increase offset as depth increases

        # Add children to queue and graph with edges
        if node.left:
            left_label = f"{node.left.char}({node.left.freq})" if node.left.char else f"{node.left.freq}"
            queue.append((node.left, '0', (x - offset, y - 1)))
            G.add_edge(node_label, left_label, label='0')
        if node.right:
            right_label = f"{node.right.char}({node.right.freq})" if node.right.char else f"{node.right.freq}"
            queue.append((node.right, '1', (x + offset, y - 1)))
            G.add_edge(node_label, right_label, label='1')

    # Drawing settings
    pos = nx.spring_layout(G, pos=pos, fixed=pos.keys())
    plt.figure(figsize=(18, 12))  # Задаємо більший розмір зображення
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=1000, node_color='lightblue', font_size=10)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.title('Simplified Huffman Tree')
    plt.show()


# Plot the simplified Huffman tree focusing on characters
tree = build_huffman_tree(frequencies)
plot_simple_huffman_tree(tree)


def check_optimality_kraft(codebook):
    lengths = [len(code) for code in codebook.values()]
    max_length = max(lengths)
    kraft_sum = sum([2 ** (-length) for length in lengths])
    return kraft_sum <= 1, max_length


def check_optimality_shannon(entropy, average_length):
    return entropy < average_length


# Перевірка за теоремою Крафта
passed_kraft, max_length = check_optimality_kraft(codebook)
print("Перевірка оптимальності за теоремою Крафта:", "Пройдено" if passed_kraft else "Не пройдено")

# Перевірка за теоремою Шеннона
passed_shannon = check_optimality_shannon(entropy, average_length)
print("Перевірка оптимальності за теоремою Шеннона:", "Пройдено" if passed_shannon else "Не пройдено")


def huffman_decoding(encoded_text, tree):
    decoded_text = []
    node = tree
    for bit in encoded_text:
        node = node.left if bit == '0' else node.right
        if node.char is not None:
            decoded_text.append(node.char)
            node = tree

    return ''.join(decoded_text)

# Здійснюємо декодування закодованого тексту
decoded_text = huffman_decoding(encoded_text, tree)
print("Розкодований текст:", decoded_text)
