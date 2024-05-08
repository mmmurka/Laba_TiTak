import heapq
from collections import Counter, defaultdict

def compress(text):
    compressed = []
    dictionary = {}
    currentIndex = 1
    currentSequence = ''

    for char in text:
        currentSequence += char

        if currentSequence not in dictionary:
            if currentSequence[:-1] in dictionary:
                compressed.append((dictionary[currentSequence[:-1]], char))
            else:
                compressed.append((0, char))
            dictionary[currentSequence] = currentIndex
            currentIndex += 1
            currentSequence = ''

    return compressed


def decompress(compressed):
    decompressed = ''
    dictionary = {}
    currentIndex = 1

    for entry in compressed:
        if entry[0] == 0:
            decompressed += entry[1]
            dictionary[currentIndex] = entry[1]
        else:
            decompressed += dictionary[entry[0]] + entry[1]
            dictionary[currentIndex] = dictionary[entry[0]] + entry[1]

        currentIndex += 1

    return decompressed


def compression_ratio(original_text, compressed):
    original_size = len(original_text) * 16
    compressed_size = len(compressed) * 24

    return compressed_size / original_size


def build_huffman_tree(data):
    freq = Counter(data)
    heap = [[weight, [symbol, '']] for symbol, weight in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return heap[0][1:]


def huffman_compress(text):
    tree = build_huffman_tree(text)
    codes = dict(tree)
    compressed = ''.join(codes[symbol] for symbol in text)
    return compressed, codes


def huffman_decompress(compressed, codes):
    codes_reverse = {code: symbol for symbol, code in codes.items()}
    decompressed = ''
    code = ''
    for bit in compressed:
        code += bit
        if code in codes_reverse:
            decompressed += codes_reverse[code]
            code = ''
    return decompressed


def shannon_fano_compress(text):
    freq = Counter(text)
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    codes = defaultdict(str)
    def shannon_fano_encoding(symbol_list):
        if len(symbol_list) == 1:
            return
        mid = len(symbol_list) // 2
        for symbol, _ in symbol_list[:mid]:
            codes[symbol] += '0'
        for symbol, _ in symbol_list[mid:]:
            codes[symbol] += '1'
        shannon_fano_encoding(symbol_list[:mid])
        shannon_fano_encoding(symbol_list[mid:])
    shannon_fano_encoding(sorted_freq)
    compressed = ''.join(codes[symbol] for symbol in text)
    return compressed, codes


def shannon_fano_decompress(compressed, codes):
    codes_reverse = {code: symbol for symbol, code in codes.items()}
    decompressed = ''
    code = ''
    for bit in compressed:
        code += bit
        if code in codes_reverse:
            decompressed += codes_reverse[code]
            code = ''
    return decompressed


def main():
    text = """Кохайтеся, чорнобриві,
Та не з москалями,
Бо москалі — чужі люде,
Роблять лихо з вами.
Москаль любить жартуючи,
Жартуючи кине;
Піде в свою Московщину,
А дівчина гине..."""

    print("Початковий текст:")
    print(text)

    compressed_text_lz78 = compress(text)
    decompressed_text_lz78 = decompress(compressed_text_lz78)

    print("\nСтиснений текст (LZ-78):")
    count = 0
    for entry in compressed_text_lz78:
        print(entry, end=' ')
        count += 1
        if count % 10 == 0:
            print()

    print("\nРозкодований текст (LZ-78):")
    print(decompressed_text_lz78)

    compression_ratio_value_lz78 = compression_ratio(text, compressed_text_lz78)
    print("\nКоефіцієнт стиснення (LZ-78):", compression_ratio_value_lz78)

    compressed_text_huffman, huffman_codes = huffman_compress(text)
    decompressed_text_huffman = huffman_decompress(compressed_text_huffman, huffman_codes)

    print("\nСтиснений текст (Huffman):")
    print(compressed_text_huffman)

    print("\nРозкодований текст (Huffman):")
    print(decompressed_text_huffman)

    compression_ratio_value_huffman = compression_ratio(text, compressed_text_huffman)
    print("\nКоефіцієнт стиснення (Huffman):", compression_ratio_value_huffman)

    compressed_text_sf, sf_codes = shannon_fano_compress(text)
    decompressed_text_sf = shannon_fano_decompress(compressed_text_sf, sf_codes)

    print("\nСтиснений текст (Shannon-Fano):")
    print(compressed_text_sf)

    print("\nРозкодований текст (Shannon-Fano):")
    print(decompressed_text_sf)

    compression_ratio_value_sf = compression_ratio(text, compressed_text_sf)
    print("\nКоефіцієнт стиснення (Shannon-Fano):", compression_ratio_value_sf)

if __name__ == "__main__":
    main()
