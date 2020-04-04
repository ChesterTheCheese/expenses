from abc import ABC, abstractmethod
from typing import List

import topics
from operation import Operation, Location
from topics import GENERAL
from utils import Frogs


def match_all(operations: List[Operation]) -> None:
	for op in operations:
		match(op)


def match(operation: Operation) -> None:
	for matcher in REGISTERED_MATCHERS:
		matches = matcher.matches(matcher, operation)
		if matches:
			topic = matcher.get_topic()
			operation.topic = topic


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
	def self_matches(self, operation: Operation) -> bool:
		pass

	@classmethod
	def matches(cls, self, operation):
		"""
		In order for a Matcher to match the operation all the parent Matcher classes has to match as well. This
		function searches recursively through the matcher class hierarchy
		"""
		# check self matching
		self_matches = cls.self_matches(self, operation)
		if not self_matches:
			return False
		# check parent matching
		parent = cls.__bases__[0]
		if cls != GeneralMatcher:
			if not parent.matches(self, operation):
				return False
		return True


class GeneralMatcher(TopicMatcher):
	def get_topic(self):
		return GENERAL

	def self_matches(self, operation: Operation) -> bool:
		return True


class ExpensesMatcher(GeneralMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES

	def self_matches(self, operation: Operation) -> bool:
		amount = operation.amount and operation.amount < 0
		return amount


class WorkMatcher(ExpensesMatcher):
	pass


class WorkLunchMatcher(WorkMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.WORK.LUNCHES

	def self_matches(self, operation: Operation) -> bool:
		ludo = matches_address(operation, 'Ludovisko')
		thai_wok = matches_address(operation, 'THAI WOK')
		return ludo or thai_wok


class WorkFrogMatcher(WorkMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.WORK.FROG

	def self_matches(self, operation: Operation) -> bool:
		froggy1 = matches_address(operation, Frogs.WORK.value[0])
		froggy2 = matches_address(operation, Frogs.WORK.value[1])
		return froggy1 or froggy2


class WorkSubwayMatcher(WorkMatcher):

	def get_topic(self):
		return GENERAL.EXPENSES.WORK.SUBWAY

	def self_matches(self, operation: Operation) -> bool:
		matches = matches_address(operation, 'SUBWAY')
		return matches


class BadmintonMatcher(ExpensesMatcher):

	def get_topic(self) -> topics.Topic:
		return GENERAL.EXPENSES.SPORT.BADMINTON

	def self_matches(self, operation: Operation) -> bool:
		badminton = matches_address(operation, 'KLUB BADMINTONA')
		return badminton


REGISTERED_MATCHERS: List[TopicMatcher] = []


def register(matcher: TopicMatcher):
	REGISTERED_MATCHERS.append(matcher)


register(GeneralMatcher())
register(ExpensesMatcher())
register(WorkLunchMatcher())
register(WorkFrogMatcher())
register(WorkSubwayMatcher())
register(BadmintonMatcher())

if __name__ == '__main__':
	#  quick test
	o = Operation()
	o.amount = -100.0
	o.location = Location()
	o.location.address = 'THAI WOK'
	match(o)
	print(o.topic)
