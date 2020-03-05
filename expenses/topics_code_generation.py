import topics

GENERAL = topics.Topic("GENERAL")
EXPENSES = topics.Topic("EXPENSES", GENERAL)
HOME = topics.Topic("HOME", EXPENSES)
RENT = topics.Topic("RENT", HOME)
SHOPPING = topics.Topic("SHOPPING", HOME)
DELIVERY_FOOD = topics.Topic("DELIVERY_FOOD", HOME)
CAT = topics.Topic("CAT", HOME)
WORK = topics.Topic("WORK", EXPENSES)
LUNCHES = topics.Topic("LUNCHES", WORK)
FROG = topics.Topic("FROG", WORK)
SUBWAY = topics.Topic("SUBWAY", WORK)
FOOD = topics.Topic("FOOD", EXPENSES)
FAST_FOODS = topics.Topic("FAST_FOODS", FOOD)
RESTAURANTS = topics.Topic("RESTAURANTS", FOOD)
SPORT = topics.Topic("SPORT", EXPENSES)
MULTISPORT = topics.Topic("MULTISPORT", SPORT)
SNOWBOARDING = topics.Topic("SNOWBOARDING", SPORT)
CLIMBING = topics.Topic("CLIMBING", SPORT)
CLIMBING_EQUIPMENT = topics.Topic("CLIMBING_EQUIPMENT", CLIMBING)
ENTRANCE = topics.Topic("ENTRANCE", CLIMBING)
POOL = topics.Topic("POOL", SPORT)
BADMINTON = topics.Topic("BADMINTON", SPORT)
BOXING = topics.Topic("BOXING", SPORT)
ENTERTAINMENT = topics.Topic("ENTERTAINMENT", EXPENSES)
NIGHTS_OUT = topics.Topic("NIGHTS_OUT", ENTERTAINMENT)
SPECTACLES = topics.Topic("SPECTACLES", ENTERTAINMENT)
NETFLIX_ISH = topics.Topic("NETFLIX_ISH", ENTERTAINMENT)
CAR = topics.Topic("CAR", EXPENSES)
FUEL = topics.Topic("FUEL", CAR)
REPAIRS = topics.Topic("REPAIRS", CAR)
HIGHWAYS = topics.Topic("HIGHWAYS", CAR)
CAR_FOOD = topics.Topic("CAR_FOOD", CAR)
CAR_EQUIPMENT = topics.Topic("CAR_EQUIPMENT", CAR)
HOLIDAY = topics.Topic("HOLIDAY", EXPENSES)
TRIP = topics.Topic("TRIP", HOLIDAY)
TRANSPORT = topics.Topic("TRANSPORT", HOLIDAY)
AT_THE_PLACE = topics.Topic("AT_THE_PLACE", HOLIDAY)
INCOMES = topics.Topic("INCOMES", GENERAL)
LUFTHANSA = topics.Topic("LUFTHANSA", INCOMES)
LUFTHANSA_INCOME = topics.Topic("LUFTHANSA_INCOME", LUFTHANSA)
LUFTHANSA_DELEGATION = topics.Topic("LUFTHANSA_DELEGATION", LUFTHANSA)
PARENTS = topics.Topic("PARENTS", INCOMES)
PARENT_PRESENTS = topics.Topic("PARENT_PRESENTS", PARENTS)
PARENT_RETURNS = topics.Topic("PARENT_RETURNS", PARENTS)


def print_assignment_code_for_structure(topic, extended):
	print_assignment_code(topic, extended)
	for child in topic.children:
		print_assignment_code_for_structure(child, extended)


def print_assignment_code(topic, extended):
	parent_constr_str = ''
	if topic.has_parent():
		parent_constr_str = ', ' + topic.parent.name  # , PARENT
	code = f'{topic.name} = topics.Topic("{topic.name}"{parent_constr_str})'  # TOPIC = topics.Topic("TOPIC", PARENT)

	if extended:
		hierarchical_name = topic.name
		while topic.parent:
			hierarchical_name = f'{topic.parent.name}.{hierarchical_name}'  # PARENT.TOPIC
			code = f'{hierarchical_name} = ' + code  # PARENT.TOPIC = TOPIC = topics.Topic("TOPIC", PARENT)
			topic = topic.parent
	print(code)


def print_classes_code_for_structure(topic):
	print_classes_code(topic)
	for child in topic.children:
		print_classes_code_for_structure(child)


def print_classes_code(topic: topics.Topic):
	def capitalize(upper_snake_case_string: str):  # UPPER_SNAKE_CASE
		capitalized_name = ''
		for s in upper_snake_case_string.split("_"):
			capitalized_name += s.capitalize()
		return capitalized_name

	code = ''
	code += f'class {capitalize(topic.name)}Topic(Topic):\n'
	# code += f'    name = "{topic.name}"\n'
	if topic.has_children():
		code += f'    def register_fields(self):\n'
		for child in topic.children:
			code += f'        self.{child.name} = {capitalize(child.name)}Topic("{child.name}", self)\n'
	else:
		code += f'    pass\n'

	print(code)


if __name__ == '__main__':
	print_assignment_code_for_structure(GENERAL, True)
	print()
	print_assignment_code_for_structure(GENERAL, False)
	print()
	print_classes_code_for_structure(GENERAL)
