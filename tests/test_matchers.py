import unittest

from matchers import matchers
from operation import Operation
from topics import GENERAL, Topic


def operation_of(amount=None, address=None):
	""" Operation object factory """
	o = Operation()
	o.amount = amount
	o.get_init_location().address = address
	return o


class MatcherTestCase(unittest.TestCase):
	assertions = []

	def test_something(self):
		MatcherTestCase.assertions = []
		self.doAssert(operation_of(), GENERAL)
		self.doAssert(operation_of(amount=-1), GENERAL.EXPENSES)
		self.doAssert(operation_of(amount=-1, address='Ludovisko'), GENERAL.EXPENSES.WORK.LUNCHES)
		self.doAssert(operation_of(amount=-1, address='THAI WOK'), GENERAL.EXPENSES.WORK.LUNCHES)
		self.doAssert(operation_of(amount=-1, address='SUBWAY'), GENERAL.EXPENSES.WORK.SUBWAY)
		self.doAssert(operation_of(amount=-1, address='ZABKA Z5615 K.1'), GENERAL.EXPENSES.WORK.FROG)
		self.doAssert(operation_of(amount=-1, address='ZABKA Z5615 K.2'), GENERAL.EXPENSES.WORK.FROG)
		self.doAssert(operation_of(amount=-1, address='KLUB BADMINTONA'), GENERAL.EXPENSES.SPORT.BADMINTON)

		for assertion in MatcherTestCase.assertions:
			operation, topic, success = assertion
			print('Assertion', 'OK  ' if success else 'FAIL', topic)
		for assertion in MatcherTestCase.assertions:
			operation, topic, success = assertion
			if not success:
				self.assertEqual(operation.topic, topic)  # redo to get pretty printed error

	def doAssert(self, operation: Operation, topic: Topic):
		try:
			matchers.match(operation)
			self.assertEqual(operation.topic, topic)
			MatcherTestCase.assertions.append((operation, topic, True))
		except:
			MatcherTestCase.assertions.append((operation, topic, False))


if __name__ == '__main__':
	unittest.main()
