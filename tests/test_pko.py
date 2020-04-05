import csv
from typing import List
from unittest import TestCase

import operation
from operation import Operation
from parsers import pko


class TestPkoBpParser(TestCase):

	def test_load_and_parse_operations(self):
		filename = './../data/js_20200101_20200131.csv'
		with open(filename) as csv_file:
			csv_count = len(list(csv.reader(csv_file))) - 1

		pko.debug_print = False
		pko.debug_check = False
		operations: List[Operation] = pko.load_and_parse_operations(filename)
		count_ok = operation.check_entries_count(operations, csv_count)
		untyped = operation.check_untyped(operations)
		unassigned_descriptions = operation.check_unassigned_descriptions(operations)
		untopiced = operation.check_untopiced(operations)

		self.assertTrue(count_ok)
		self.assertTrue(len(untyped) == 0)
		self.assertTrue(len(unassigned_descriptions) == 0)
		self.assertTrue(len(untopiced) == 0)
