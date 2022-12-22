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


def matches_title_simple(operation, title) -> bool:
	actual = operation.title
	if not actual:
		return False
	return title in actual


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


class HomeMatcher(ExpensesMatcher):
	pass


class HomeRentMatcher(HomeMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.HOME.RENT

	def self_matches(self, operation: Operation) -> bool:
		rent = matches_title_simple(operation, 'MIESZKANIE ALBATROS CZYNSZ')
		return rent


class HomeShoppingMatcher(HomeMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.HOME.SHOPPING

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class HomeDeliveryFoodMatcher(HomeMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.HOME.DELIVERY_FOOD

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class HomeCatMatcher(HomeMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.HOME.CAT

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


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


class FoodMatcher(ExpensesMatcher):
	pass


class FastFoodsMatcher(FoodMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.FOOD.FAST_FOODS

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class RestaurantsMatcher(FoodMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.FOOD.RESTAURANTS

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class SportMatcher(ExpensesMatcher):
	pass


# class MultisportMatcher(SportMatcher): # ??
# 	pass

class SnowboardingMatcher(SportMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.SPORT.SNOWBOARDING

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class ClimbingMatcher(SportMatcher):
	pass


class ClimbingEquipmentMatcher(ClimbingMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.SPORT.CLIMBING.CLIMBING_EQUIPMENT

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class ClimbingEntranceFeeMatcher(ClimbingMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.SPORT.CLIMBING.ENTRANCE

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class PoolMatcher(SportMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.SPORT.POOL

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class BadmintonMatcher(SportMatcher):

	def get_topic(self) -> topics.Topic:
		return GENERAL.EXPENSES.SPORT.BADMINTON

	def self_matches(self, operation: Operation) -> bool:
		badminton = matches_address(operation, 'KLUB BADMINTONA')
		return badminton


class BoxingMatcher(SportMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.SPORT.BOXING

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class EntertainmentMatcher(ExpensesMatcher):
	pass


class NightsOutMatcher(EntertainmentMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.ENTERTAINMENT.NIGHTS_OUT

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class SpectaclesMatcher(EntertainmentMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.ENTERTAINMENT.SPECTACLES

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class NetflixishMatcher(EntertainmentMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.ENTERTAINMENT.NETFLIX_ISH

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class CarMatcher(ExpensesMatcher):
	pass


class CarFuelMatcher(CarMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.CAR.FUEL

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class CarRepairsMatcher(CarMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.CAR.REPAIRS

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class CarHighwaysMatcher(CarMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.CAR.HIGHWAYS

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class CarFoodMatcher(CarMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.CAR.CAR_FOOD

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class CarEquipmentMatcher(CarMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.CAR.CAR_EQUIPMENT

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class HolidayMatcher(ExpensesMatcher):
	pass


class HolidayTripMatcher(HolidayMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.HOLIDAY.TRIP

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class HolidayTransportMatcher(HolidayMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.HOLIDAY.TRANSPORT

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class HolidayAtThePlaceMatcher(HolidayMatcher):
	def get_topic(self):
		return GENERAL.EXPENSES.HOLIDAY.AT_THE_PLACE

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class IncomeMatcher(GeneralMatcher):
	pass


class LufthansaMatcher(IncomeMatcher):
	pass


class LufthansaIncomeMatcher(LufthansaMatcher):
	def get_topic(self):
		return GENERAL.INCOMES.LUFTHANSA.LUFTHANSA_INCOME

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class LufthansaDelegationMatcher(LufthansaMatcher):
	def get_topic(self):
		return GENERAL.INCOMES.LUFTHANSA.LUFTHANSA_DELEGATION

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class ParentsMatcher(IncomeMatcher):
	pass


class ParentPresentsMatcher(ParentsMatcher):
	def get_topic(self):
		return GENERAL.INCOMES.PARENTS.PARENT_PRESENTS

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


class ParentReturnsMatcher(ParentsMatcher):
	def get_topic(self):
		return GENERAL.INCOMES.PARENTS.PARENT_RETURNS

	def self_matches(self, operation: Operation) -> bool:
		return False  # TODO


REGISTERED_MATCHERS: List[TopicMatcher] = []


def register_all():
	matcher_classes = TopicMatcher.__subclasses__()
	for mc in matcher_classes:
		register_subclasses(mc)


def register_subclasses(matcher_class):
	register(matcher_class())
	for sub in matcher_class.__subclasses__():
		register_subclasses(sub)


def register(matcher: TopicMatcher):
	print("Registering " + matcher.__class__.__name__)
	REGISTERED_MATCHERS.append(matcher)

register_all()
# register(GeneralMatcher())
# register(ExpensesMatcher())
# register(WorkLunchMatcher())
# register(WorkFrogMatcher())
# register(WorkSubwayMatcher())
# register(BadmintonMatcher())

# if __name__ == '__main__':
# 	#  quick test
# 	o = Operation()
# 	o.amount = -100.0
# 	o.location = Location()
# 	o.location.address = 'THAI WOK'
# 	match(o)
# 	print(o.topic)
