import re
from collections import Counter


def process_file(filename, stopwords=None):
    word_counts = Counter()
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            words = re.findall(r'\b\w+\b', line.lower())  # Разбиваем строку на слова и приводим к нижнему регистру
            if stopwords:
                words = [word for word in words if word not in stopwords]
            word_counts.update(words)
    return word_counts


def most_common_words(word_counts, n):
    return word_counts.most_common(n)


def test():
    filename = 'text_test.txt'  # Путь к вашему текстовому файлу
    stopwords = {'the', 'and', 'in', 'of', 'a', 'to', 'on', 'is'}  # Пример стоп-слов
    word_counts = process_file(filename, stopwords)
    most_common = most_common_words(word_counts, 10)  # Наиболее часто встречающиеся 10 слов
    print("Most common words:")
    for word, count in most_common:
        print(f"{word}: {count}")


if __name__ == "__main__":
    test()
