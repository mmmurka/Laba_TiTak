from collections import defaultdict
import math

class Node:
    def __init__(self, symbol, probability):
        self.symbol = symbol
        self.probability = probability
        self.bit = ""

def calculate_probabilities(text):
    probabilities = defaultdict(int)
    total_characters = len(text)

    for c in text:
        probabilities[c] += 1

    for key in probabilities.keys():
        probabilities[key] /= total_characters

    return probabilities

def build_tree(probabilities):
    nodes = [Node(symbol, probability) for symbol, probability in probabilities.items()]
    nodes.sort(key=lambda x: x.probability, reverse=True)
    return build_tree_recursive(nodes)

def build_tree_recursive(nodes):
    if len(nodes) == 1:
        return nodes

    total_probability = sum(node.probability for node in nodes)
    cumulative_probability = 0
    split_index = -1

    for i, node in enumerate(nodes):
        cumulative_probability += node.probability
        if cumulative_probability >= total_probability / 2:
            split_index = i
            break

    left_subtree = nodes[:split_index + 1]
    right_subtree = nodes[split_index + 1:]

    for node in left_subtree:
        node.bit += "0"

    for node in right_subtree:
        node.bit += "1"

    result = []
    result.extend(build_tree_recursive(left_subtree))
    result.extend(build_tree_recursive(right_subtree))

    return result

def encode_text(text, tree):
    encoding_table = {node.symbol: node.bit for node in tree}
    encoded_text = ""
    for c in text:
        encoded_text += encoding_table[c]
    return encoded_text

def add_parity_bits(encoded_text, parity_bits_count):
    length = len(encoded_text)
    total_bits = length + parity_bits_count
    current_index = 0
    result = ""

    for i in range(total_bits):
        if (i + 1) & i == 0:
            result += '0'
        else:
            result += encoded_text[current_index] if current_index < length else '0'
            current_index += 1

    for i in range(parity_bits_count):
        index = 2 ** i - 1
        parity_bit = calculate_parity_bit(index, result)
        result = result[:index] + parity_bit + result[index + 1:]

    return result

def calculate_parity_bit(parity_index, text):
    count = 0
    length = len(text)
    for i in range(parity_index, length, (parity_index + 1) * 2):
        for j in range(i, min(i + parity_index + 1, length)):
            if text[j] == '1':
                count += 1
    return '0' if count % 2 == 0 else '1'

def check_for_errors(encoded_text):
    parity_bits_count = math.ceil(math.log2(len(encoded_text)))
    for i in range(parity_bits_count):
        index = 2 ** i - 1
        parity_bit = calculate_parity_bit(index, encoded_text)
        if encoded_text[index] != parity_bit:
            return True
    return False

def shannon_fano(nodes, start, end):
    if start == end:
        return
    total_probability = sum(node.probability for node in nodes[start:end+1])
    cumulative_probability = 0
    split_index = -1
    min_difference = math.inf

    for i in range(start, end+1):
        cumulative_probability += nodes[i].probability
        difference = abs(2 * cumulative_probability - total_probability)
        if difference < min_difference:
            min_difference = difference
            split_index = i

    for i in range(start, end+1):
        if i <= split_index:
            nodes[i].bit += '0'
        else:
            nodes[i].bit += '1'

    shannon_fano(nodes, start, split_index)
    shannon_fano(nodes, split_index+1, end)


def main():
    text = """Кохайтеся, чорнобриві,
Та не з москалями,
Бо москалі — чужі люде,
Роблять лихо з вами.
Москаль любить жартуючи,
Жартуючи кине;
Піде в свою Московщину,
А дівчина гине..."""

    print("Исходный текст:")
    print(text)

    probabilities = calculate_probabilities(text)
    tree = build_tree(probabilities)
    encoded_text = encode_text(text, tree)

    print("\nЗакодированный текст (Шеннон-Фано):")
    shannon_fano(tree, 0, len(tree)-1)
    for node in tree:
        print(f"{node.symbol}: {node.bit}")

    print("\nЗакодированный текст:\n")

    parity_bits_count = 4
    encoded_text_with_parity = add_parity_bits(encoded_text, parity_bits_count)

    def print_binary_with_line_break(binary_string):
        for i in range(0, len(binary_string), 70):
            print(binary_string[i:i + 70])

    print_binary_with_line_break(encoded_text)
    print("\nТекст с добавленными битами четности:\n")
    print_binary_with_line_break(encoded_text_with_parity)

    if check_for_errors(encoded_text_with_parity):
        print("\nОбнаружена ошибка в передаче данных.")
    else:
        print("\nОшибка в передаче данных не обнаружена.")


if __name__ == "__main__":
    main()
