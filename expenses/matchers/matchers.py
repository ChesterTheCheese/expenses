from abc import ABC, abstractmethod
from typing import List

import topics
from operation import Operation, Location
from topics import GENERAL


def match_all(operations: List[Operation]) -> None:
	for op in operations:
		match(op)


def match(op: Operation) -> None:
	for matcher in REGISTERED_MATCHERS:
		if matcher.matches(op):
			op.topic = matcher.get_topic()


def matches_address(operation, address) -> bool:
	loc = operation.location
	if not loc or not loc.address:
		return False
	return address in loc.address


class TopicMatcher(ABC):

	@abstractmethod
	def get_topic(self) -> topics.Topic:
		pass

	@abstractmethod
	def matches(self, operation: Operation) -> bool:
		pass


class GeneralMatcher(TopicMatcher):
	def get_topic(self):
		return GENERAL

	def matches(self, operation: Operation) -> bool:
		return True


class ExpensesMatcher(TopicMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES

	def matches(self, operation: Operation) -> bool:
		return o.amount < 0


class WorkLunchMatcher(TopicMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.WORK.LUNCHES

	def matches(self, operation: Operation) -> bool:
		return matches_address(operation, 'Ludovisko') \
		       or matches_address(operation, 'THAI WOK')


class WorkSubwayMatcher(TopicMatcher):

	def get_topic(self):
		return GENERAL.EXPENSES.WORK.SUBWAY

	def matches(self, operation: Operation) -> bool:
		return matches_address(operation, 'SUBWAY')


class BadmintonMatcher(TopicMatcher):

	def matches(self, operation: Operation) -> bool:
		return False  # TODO


REGISTERED_MATCHERS: List[TopicMatcher] = []


def register(matcher: TopicMatcher):
	REGISTERED_MATCHERS.append(matcher)


register(GeneralMatcher())
register(ExpensesMatcher())
register(WorkLunchMatcher())

#  quick test
o = Operation()
o.amount = -100.0
o.location = Location()
o.location.address = 'THAI WOK'
match(o)
print(o.topic)
