"""
DtreeNodes.py - Class that encapsulates the leaf and question nodes and
proves functions to operate on them

Dennis La - Dennis.La@student.csulb.edu
Melissa Hazlewood - Melissa.Hazlewood@student.csulb.edu
Rowan Herbert - Rowan.Herbert@student.csulb.edu
Sophanna Ek - Sophanna.Ek@student.csulb.edu
"""
class leafNode:
	"""leafNode class"""

	def __init__(self, label):
		"""
		Constructor for a leaf node that takes in the label
		:param label: the classification label
		"""
		self.__label = label

	def get_label(self):
		"""
		Getter for the label
		:return: the label of the leaf node
		"""
		return self.__label

class questionNode:
	"""questionNode class"""

	def __init__(self, attribute_data, most_common_label):
		"""
		Constructor for the question node
		:param attribute_data: list that contains selected attribute, attribute value entropies,
		attribute entropies, and attribute info gains
		:param most_common_label: most common label seen in the dataset that reaches this question node
		Used for missing edge handling
		"""
		self.__best_attribute_data = attribute_data
		self.__attribute = attribute_data[0]
		self.__children = {}
		self.most_common_label_from_dataset = most_common_label

	def add_child(self, value, child_node):
		"""
		Adds child to a question node
		:param value: the question node's attribute's value associated with the child
		:param child_node: the child node to be added to the question node
		:return:
		"""
		self.__children[value] = child_node

	def get_child(self, value):
		"""
		Returns the child associated with a given attribute value
		:param value: the value associated with the child
		:return: the child node
		"""
		return self.__children[value]

	def get_children(self):
		"""
		Returns a question node's dictionary of children
		:return: the dictionary of children nodes
		"""
		return self.__children

	def get_attribute(self):
		"""
		Returns the attribute of the question node
		:return: the attribute of the question node
		"""
		return self.__attribute

	def print_attribute_data(self, columns_enum):
		"""
		Prints the attribute entropy data of the question node
		:param columns_enum: enum that identifies the columns of the data
		:return:
		"""
		print("Best attribute to split on:", columns_enum(self.__best_attribute_data[0]).name, "\n")
		print("Attribute value entropies:")
		for attribute_value_tuple in self.__best_attribute_data[1]:
			print("H(" + columns_enum(attribute_value_tuple[0]).name, "=", attribute_value_tuple[1] + ") =",
				  self.__best_attribute_data[1][attribute_value_tuple])
		print()
		print("Attribute entropies:")
		for attribute in self.__best_attribute_data[2]:
			print("H(T,", columns_enum(attribute).name + ") =", self.__best_attribute_data[2][attribute])
		print()
		print("Attribute information gains:")
		for attribute in self.__best_attribute_data[3]:
			print("I(T,", columns_enum(attribute).name + ") =", self.__best_attribute_data[3][attribute])
		print()
