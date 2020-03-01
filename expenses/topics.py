class Topic:

	def __init__(self, name: str, parent: 'Topic' = None) -> None:
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

	def has_parent(self):
		return bool(self.parent)


def print_assignment_code(topic):
	parent_constr_str = ''
	if topic.has_parent():
		parent_constr_str = ', ' + topic.parent.name  # , PARENT
	code = f'{topic.name} = Topic("{topic.name}"{parent_constr_str})'  # TOPIC = Topic("TOPIC", PARENT)

	hierarchical_name = topic.name
	while topic.parent:
		hierarchical_name = f'{topic.parent.name}.{hierarchical_name}'  # PARENT.TOPIC
		code = f'{hierarchical_name} = ' + code  # PARENT.TOPIC = TOPIC = Topic("TOPIC", PARENT)
		topic = topic.parent
	print(code)


def print_assignment_code_for_structure(topic):
	print_assignment_code(topic)
	for child in topic.children:
		print_assignment_code_for_structure(child)


def print_structure(topic: Topic, level: int = 0):
	indent = '\t' * level
	print(f'{indent}- {topic.name}')
	for child in topic.children:
		print_structure(child, level + 1)
