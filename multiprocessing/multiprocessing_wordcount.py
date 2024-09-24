import multiprocessing
import string

from multiprocessing_mapreduce import SimpleMapReduce


def file_to_words(filename):
    """Прочитать файл и вернуть последовательность значений
    (число вхождений слов)."""

    STOP_WORDS = set(['a', 'an', 'and', 'are', 'as', 'be', 'by', 'for', 'if',
                      'in', 'is', 'it', 'of', 'or', 'py', 'rst', 'that', 'the',
                      'to', 'with'])
    TR = str.maketrans({
        p: ' '
        for p in string.punctuation
    })
    print(f'{multiprocessing.current_process().name} reading {filename}')
    output = []
    with open(filename, 'rt') as file:
        for line in file:
            if line.lstrip().startswith('..'):
                continue
            line = line.translate(TR)
            for word in line.split():
                word = word.lower()
                if word.isalpha() and word not in STOP_WORDS:
                    output.append((word, 1))
    return output


def count_words(item):
    """Преобразовать сгруппированные данные для слова в кортеж,
    содержащий слово и число вхождений."""

    word, occurences = item
    return (word, sum(occurences))


if __name__ == '__main__':
    import operator
    import glob

    input_files = glob.glob('*.rst')
    mapper = SimpleMapReduce(file_to_words, count_words)
    word_counts = mapper(input_files)
    word_counts.sort(key=operator.itemgetter(1))
    word_counts.reverse()

    print('\nTOP 20 WORDS BY FREQUENCY\n')
    top_20 = word_counts[:20]
    longest = max(len(word) for word, count in top_20)
    for word, count in top_20:
        print('{word:<{len}} {count:5}'.format(
            len=longest + 1,
            word=word,
            count=count
        ))
