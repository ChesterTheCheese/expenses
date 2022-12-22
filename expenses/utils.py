import collections
from enum import Enum
from typing import List


# unused
def groupby_unsorted(seq, key=lambda x: x):
	indexes = collections.defaultdict(list)
	for i, elem in enumerate(seq):
		indexes[key(elem)].append(i)
	for k, idxs in indexes.items():
		yield k, (seq[i] for i in idxs)


def print_bank_operations_list(l: List):
	try:
		print(f'bankOperations ({len(l)})')
		for e in l:
			print(e)
	except Exception as er:  # for finding None values with debugger
		print(f'Exception caught! {er}')


class Frogs(Enum):
	HOME = ['ZABKA Z5218 K.1']
	WORK = ['ZABKA Z5615 K.1', 'ZABKA Z5615 K.2']
	VET = ['ZABKA Z4916 K.1']

	@staticmethod
	def get(value):
		for frog in Frogs:
			for frog_id in frog.value:  # search list
				if value in frog_id:  # match by partial string
					return frog
		raise KeyError
