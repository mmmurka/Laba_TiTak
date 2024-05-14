from collections import Counter


def main():
    text = ("Кохайтеся, чорнобриві, "
            "Та не з москалями, "
            "Бо москалі — чужі люде, "
            "Роблять лихо з вами. "
            "Москаль любить жартуючи, "
            "Жартуючи кине; "
            "Піде в свою Московщину, "
            "А дівчина гине... ")

    # Перевірка дублювання символів
    freq = Counter(text)
    duplicates = {char: count for char, count in freq.items() if count > 1}
    if duplicates:
        print("Символи, що дублюються:")
        for char, count in duplicates.items():
            print(f"Символ '{char}' зустрічається {count} разів")
    else:
        print("У тексті немає дублюючихся символів")

if __name__ == '__main__':
    main()