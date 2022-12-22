#
import utils


class Topic:

	def __init__(self, name: str, parent: 'Topic' = None) -> None:
		self.children = []
		self.name = name
		self.parent = parent
		if parent:
			parent.children.append(self)
		self.register_fields()

	def register_fields(self):
		pass

	def __str__(self) -> str:
		parent_str = (self.parent.__str__() + ".") if self.parent else ""
		# return f'{parent_str}{self.name}'
		return f'{self.name}'

	def __repr__(self) -> str:
		return self.__str__()

	def has_parent(self) -> bool:
		return bool(self.parent)

	def has_children(self) -> bool:
		return bool(self.children)


def print_structure(topic: Topic, level: int = 0):
	indent = '\t' * level
	print(f'{indent}- {topic.name}')
	for child in topic.children:
		print_structure(child, level + 1)


# Topics structure #

class GeneralTopic(Topic):
	name = "GENERAL_TOPIC_NAME"

	def register_fields(self):
		self.EXPENSES = ExpensesTopic("EXPENSES", self)
		self.INCOMES = IncomesTopic("INCOMES", self)


class ExpensesTopic(Topic):
	def register_fields(self):
		self.HOME = HomeTopic("HOME", self)
		self.WORK = WorkTopic("WORK", self)
		self.FOOD = FoodTopic("FOOD", self)
		self.SPORT = SportTopic("SPORT", self)
		self.ENTERTAINMENT = EntertainmentTopic("ENTERTAINMENT", self)
		self.CAR = CarTopic("CAR", self)
		self.HOLIDAY = HolidayTopic("HOLIDAY", self)


class HomeTopic(Topic):
	def register_fields(self):
		self.RENT = RentTopic("RENT", self)
		self.SHOPPING = ShoppingTopic("SHOPPING", self)
		self.DELIVERY_FOOD = DeliveryFoodTopic("DELIVERY_FOOD", self)
		self.CAT = CatTopic("CAT", self)


class RentTopic(Topic):
	pass


class ShoppingTopic(Topic):
	pass


class DeliveryFoodTopic(Topic):
	pass


class CatTopic(Topic):
	pass


class WorkTopic(Topic):
	def register_fields(self):
		self.LUNCHES = LunchesTopic("LUNCHES", self)
		self.FROG = FrogTopic("FROG", self)
		self.SUBWAY = SubwayTopic("SUBWAY", self)


class LunchesTopic(Topic):
	pass


class FrogTopic(Topic):
	pass


class SubwayTopic(Topic):
	pass


class FoodTopic(Topic):
	def register_fields(self):
		self.FAST_FOODS = FastFoodsTopic("FAST_FOODS", self)
		self.RESTAURANTS = RestaurantsTopic("RESTAURANTS", self)


class FastFoodsTopic(Topic):
	pass


class RestaurantsTopic(Topic):
	pass


class SportTopic(Topic):
	def register_fields(self):
		self.MULTISPORT = MultisportTopic("MULTISPORT", self)
		self.SNOWBOARDING = SnowboardingTopic("SNOWBOARDING", self)
		self.CLIMBING = ClimbingTopic("CLIMBING", self)
		self.POOL = PoolTopic("POOL", self)
		self.BADMINTON = BadmintonTopic("BADMINTON", self)
		self.BOXING = BoxingTopic("BOXING", self)


class MultisportTopic(Topic):
	pass


class SnowboardingTopic(Topic):
	pass


class ClimbingTopic(Topic):
	def register_fields(self):
		self.CLIMBING_EQUIPMENT = ClimbingEquipmentTopic("CLIMBING_EQUIPMENT", self)
		self.ENTRANCE = EntranceTopic("ENTRANCE", self)


class ClimbingEquipmentTopic(Topic):
	pass


class EntranceTopic(Topic):
	pass


class PoolTopic(Topic):
	pass


class BadmintonTopic(Topic):
	pass


class BoxingTopic(Topic):
	pass


class EntertainmentTopic(Topic):
	def register_fields(self):
		self.NIGHTS_OUT = NightsOutTopic("NIGHTS_OUT", self)
		self.SPECTACLES = SpectaclesTopic("SPECTACLES", self)
		self.NETFLIX_ISH = NetflixIshTopic("NETFLIX_ISH", self)


class NightsOutTopic(Topic):
	pass


class SpectaclesTopic(Topic):
	pass


class NetflixIshTopic(Topic):
	pass


class CarTopic(Topic):
	def register_fields(self):
		self.FUEL = FuelTopic("FUEL", self)
		self.REPAIRS = RepairsTopic("REPAIRS", self)
		self.HIGHWAYS = HighwaysTopic("HIGHWAYS", self)
		self.CAR_FOOD = CarFoodTopic("CAR_FOOD", self)
		self.CAR_EQUIPMENT = CarEquipmentTopic("CAR_EQUIPMENT", self)


class FuelTopic(Topic):
	pass


class RepairsTopic(Topic):
	pass


class HighwaysTopic(Topic):
	pass


class CarFoodTopic(Topic):
	pass


class CarEquipmentTopic(Topic):
	pass


class HolidayTopic(Topic):
	def register_fields(self):
		self.TRIP = TripTopic("TRIP", self)
		self.TRANSPORT = TransportTopic("TRANSPORT", self)
		self.AT_THE_PLACE = AtThePlaceTopic("AT_THE_PLACE", self)


class TripTopic(Topic):
	pass


class TransportTopic(Topic):
	pass


class AtThePlaceTopic(Topic):
	pass


class IncomesTopic(Topic):
	def register_fields(self):
		self.LUFTHANSA = LufthansaTopic("LUFTHANSA", self)
		self.PARENTS = ParentsTopic("PARENTS", self)


class LufthansaTopic(Topic):
	def register_fields(self):
		self.LUFTHANSA_INCOME = LufthansaIncomeTopic("LUFTHANSA_INCOME", self)
		self.LUFTHANSA_DELEGATION = LufthansaDelegationTopic("LUFTHANSA_DELEGATION", self)


class LufthansaIncomeTopic(Topic):
	pass


class LufthansaDelegationTopic(Topic):
	pass


class ParentsTopic(Topic):
	def register_fields(self):
		self.PARENT_PRESENTS = ParentPresentsTopic("PARENT_PRESENTS", self)
		self.PARENT_RETURNS = ParentReturnsTopic("PARENT_RETURNS", self)


class ParentPresentsTopic(Topic):
	pass


class ParentReturnsTopic(Topic):
	pass


GENERAL = GeneralTopic("GENERAL")
print_structure(GENERAL)
