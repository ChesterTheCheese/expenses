import collections
from typing import List


def groupby_unsorted(seq, key=lambda x: x):
    indexes = collections.defaultdict(list)
    for i, elem in enumerate(seq):
        indexes[key(elem)].append(i)
    for k, idxs in indexes.items():
        yield k, (seq[i] for i in idxs)


def print_bank_operations_list(l: List):
    print(f'bankOperations ({len(l)})')
    for e in l:
        print(e)