# TOPICS
#   EXPENSES
#       FOOD
#           HOME_FOOD
#           WORK_FOOD
#               FROG
#               SUBWAY
#               LUNCHES = 'EXPENSES.FOOD.HOME_FOOD.WORK_FOOD'
#               OTHER (assumed)
#
#               FAST_FOODS


class Topic:

	def __init__(self, name: str, parent=None) -> None:
		self.children = []
		self.name = name
		self.parent = parent
		if parent:
			parent.children.append(self)

	# print(len(parent.children))

	def __str__(self) -> str:
		parent_str = (self.parent.__str__() + ".") if self.parent else ""
		# return f'{parent_str}{self.name}'
		return f'{self.name}'

	def __repr__(self) -> str:
		return self.__str__()


def print_children(topic: Topic, level: int = 0):
	indent = '\t' * level
	print(f'{indent}- {topic.name}')
	for child in topic.children:
		print_children(child, level + 1)


# TODO: finish topics

GENERAL = Topic("GENERAL")
GENERAL.EXPENSES = EXPENSES = Topic("EXPENSES", GENERAL)
GENERAL.EXPENSES.HOME = HOME = Topic("HOME", EXPENSES)
GENERAL.EXPENSES.HOME.CAT = CAT = Topic("CAT", HOME)
GENERAL.EXPENSES.HOME.HOME_FOOD = HOME_FOOD = Topic("HOME_FOOD", HOME)
GENERAL.EXPENSES.HOME.RENT = RENT = Topic("RENT", HOME)

print_children(GENERAL)
