"""
Dtree.py - Class that encapsulates all functions needed to create a Dtree.
Provides a constructor for creating a Dtree and functions to operate on the Dtree.

Dennis La - Dennis.La@student.csulb.edu
Melissa Hazlewood - Melissa.Hazlewood@student.csulb.edu
Rowan Herbert - Rowan.Herbert@student.csulb.edu
Sophanna Ek - Sophanna.Ek@student.csulb.edu
"""
import math
from DtreeNodes import leafNode
from DtreeNodes import questionNode
import random


class Dtree:

    def __init__(self, dataset, columns_enum):
        """
        Dtree constructor, takes in a dataset and an enum that identifies the columns of the dataset
        :param dataset: training set
        :param columns_enum: enum that identifies the columns of the dataset
        """
        self.__root = self.__build_tree(dataset)
        self.__columns_enum = columns_enum
        # set default voting weight
        self.__voting_weight = 1

    def get_classification(self, example):
        """
        Returns the label of a given example
        :param example: the example to classify
        :return: the label of the example that the dtree assigns
        """
        return self.__get_classification(self.__root, example)

    def output_q_node_data(self):
        """
        Outputs the question node data
        :return:
        """
        return self.__output_q_node_data(self.__root, None, None)

    def output_leaf_node_data(self):
        """
        Outputs the leaf node data
        :return:
        """
        return self.__output_leaf_node_data(self.__root, None, None)

    def output_parents(self):
        """
        Outputs the parents of each node
        :return:
        """
        return self.__output_parents(self.__root, None, None)

    def output_everything(self):
        """
        Outputs all data for each node
        :return:
        """
        return self.__output_everything(self.__root, None, None)

    def get_accuracy(self, dataset):
        """
        Returns accuracy of the dtree on a given dataset
        :param dataset: testing set
        :return: the dtree's accuracy on the testing set
        """
        correct = 0
        for example in dataset:
            if example[len(dataset[0]) - 1] == self.get_classification(example):
                correct += 1
        return correct / len(dataset)

    def get_voting_weight(self):
        """
        Returns the voting weight of the dtree
        :return: voting weight of the dtree
        """
        return self.__voting_weight

    def set_voting_weight(self, weight):
        """
        Sets the voting weight of the dtree
        :param weight: the weight of the tree
        :return:
        """
        self.__voting_weight = weight

    def get_enum(self):
        """
        Returns the enum that identifies the columns of the dataset
        :return: enum that identifies the columns of the dataset
        """
        return self.__columns_enum

    # ****************THE REST OF THE STUFF BELOW ARE PRIVATE METHODS****************

    def __get_classification(self, node, example):
        """
        Recursive method for finding classification given an example
        :param node: the current root of the subtree
        :param example: example to classify
        :return: the label of the example that the dtree assigns
        """
        if isinstance(node, leafNode):
            return node.get_label()
        elif isinstance(node, questionNode):
            attribute = node.get_attribute()
            value = example[attribute]
            # need to check for missing edge
            if value in node.get_children():
                return self.__get_classification(node.get_child(value), example)
            else:
                # we have a missing edge, give the most common label that reached the node
                return node.most_common_label_from_dataset

    def __output_q_node_data(self, node, parent, value):
        """
        Recursive method for printing question node data
        :param node: the current root of the subtree
        :param parent: the parent of the current node
        :param value: the attribute value associated with the current node
        :return:
        """
        if isinstance(node, leafNode):
            return
        elif isinstance(node, questionNode):
            #print the q node data
            print("***************************QUESTION NODE ATTRIBUTE DATA***************************")
            if parent is not None:
                self.__print_q_message(node, parent, value)
            else:
                self.__print_root_message(node)
            print("Entropy data for question node:")
            node.print_attribute_data(self.__columns_enum)
            for value in node.get_children():
                self.__output_q_node_data(node.get_child(value), node, value)

    def __output_leaf_node_data(self, node, parent, value):
        """
        Recursive method for printing leaf node data
        :param node: the current root of the subtree
        :param parent: the parent of the current node
        :param value: the attribute value associated with the current node
        :return:
        """
        if isinstance(node, leafNode):
            print("*****************************LEAF NODE ATTRIBUTE DATA*****************************")
            self.__print_leaf_message(node, parent, value)
            return
        elif isinstance(node, questionNode):
            for value in node.get_children():
                self.__output_leaf_node_data(node.get_child(value), node, value)

    def __output_everything(self, node, parent, value):
        """
        Recursive method for printing all data for each node
        :param node: the current root of the subtree
        :param parent: the parent of the current node
        :param value: the attribute value associated with the current node
        :return:
        """
        if isinstance(node, leafNode):
            print("*****************************LEAF NODE ATTRIBUTE DATA*****************************")
            self.__print_leaf_message(node, parent, value)
            return
        elif isinstance(node, questionNode):
            print("***************************QUESTION NODE ATTRIBUTE DATA***************************")
            if parent is not None:
                self.__print_q_message(node, parent, value)
            else:
                self.__print_root_message(node)
            print("Entropy data for question node:")
            node.print_attribute_data(self.__columns_enum)
            for value in node.get_children():
                self.__output_everything(node.get_child(value), node, value)

    def __output_parents(self, node, parent, value):
        """
        Recursive method for printing parent data for each node
        :param node: the current root of the subtree
        :param parent: the parent of the current node
        :param value: the attribute value associated with the current node
        :return:
        """
        if isinstance(node, leafNode):
            print("*****************************LEAF NODE*****************************")
            self.__print_leaf_message(node, parent, value)
            return
        elif isinstance(node, questionNode):
            print("***************************QUESTION NODE***************************")
            if parent is not None:
                self.__print_q_message(node, parent, value)
            else:
                self.__print_root_message(node)
            for value in node.get_children():
                self.__output_parents(node.get_child(value), node, value)

    def __print_root_message(self, node):
        """
        Helper function to print the roots data
        :param node: the root node
        :return:
        """
        print("Question node's attribute:", self.__columns_enum(node.get_attribute()).name)
        print("This question node is the root.")

    def __print_q_message(self, node, parent, value):
        """
        Helper function to print the question node data
        :param node: the question node
        :param parent: the parent of the question node
        :param value: the attribute value associated with the question node
        :return:
        """
        print("Question node's attribute:", self.__columns_enum(node.get_attribute()).name)
        print("Question node's parent attribute:", self.__columns_enum(parent.get_attribute()).name)
        print("Question node's parent value:", value)

    def __print_leaf_message(self, node, parent, value):
        """
        Helper function to print the leaf node data
        :param node: the leaf node
        :param parent: the parent of the lead node
        :param value: the attribute value associated with the leaf node
        :return:
        """
        print("Leaf node's parent attribute:", self.__columns_enum(parent.get_attribute()).name)
        print("Leaf node's parent value:", value)
        print("Leaf node's label:", node.get_label())

    def __find_best_attribute(self, dataset):
        """
        Function to find the best attribute to split on.
        Also finds the attribute value entropies, attribute entropies, and attribute info gains.
        Returns all of the above
        :param dataset: the dataset to find the best attribute on
        :return: best attribute to split on, attribute value entropies, attribute entropies,
        and attribute info gains
        """
        num_columns = len(dataset[0])
        list_of_pi = []
        set_of_classes = set()
        # get all the possible classes
        for example in dataset:
            set_of_classes.add(example[num_columns - 1])
        for c in set_of_classes:
            list_of_pi.append(self.__get_pi(dataset, num_columns - 1, c, c))

        h_t = self.__calc_entropy(list_of_pi)

        # H(T, attribute) values
        h_t_attributes = {}
        collection_of_attribute_value_entropies = {}

        # calculate the H(T, attribute)
        for column in range(1, len(dataset[0]) - 1):
            # H(attribute = value) values
            h_attributes_values = {}

            # get possible values from column
            possible_values = set()
            for example in dataset:
                possible_values.add(example[column])
            # calculate the H(attribute = value) for each possible value
            for value in possible_values:
                list_of_pi = []
                for c in set_of_classes:
                    list_of_pi.append(self.__get_pi(dataset, column, value, c))
                entropy = self.__calc_entropy(list_of_pi)

                h_attributes_values[value] = entropy
                collection_of_attribute_value_entropies[(column, value)] = entropy

            # calculate average entropy
            average_entropy = 0
            for value in possible_values:
                average_entropy += self.__get_relative_freq(dataset, column, value) * h_attributes_values[value]
            h_t_attributes[column] = average_entropy

        # find attribute with most info gain
        highest_gain = 0
        best_attribute = ""
        attribute_info_gains = {}
        for attribute in h_t_attributes:
            current_gain = h_t - h_t_attributes[attribute]
            attribute_info_gains[attribute] = current_gain
            if current_gain > highest_gain:
                highest_gain = current_gain
                best_attribute = attribute

        # case of no best attribute to split on. this means we will have a leaf
        if best_attribute == "":
            best_attribute = -1
        # returns selected attribute, attribute value entropies, attribute entropies, and attribute info gains
        return best_attribute, collection_of_attribute_value_entropies, h_t_attributes, attribute_info_gains

    def __get_relative_freq(self, dataset, attribute, value):
        """
        Helper function to get the relative frequency of examples with a given attribute's value out of
        all examples from a given dataset
        :param dataset: list of examples
        :param attribute: the column to focus on
        :param value: the value of the given attribute
        :return: the relative frequency of examples with that value
        """
        num_total_examples = 0
        num_examples_with_value = 0
        for example in dataset:
            num_total_examples += 1
            if example[attribute] == value:
                num_examples_with_value += 1

        if num_total_examples == 0:
            return 0
        return num_examples_with_value / num_total_examples

    def __calc_entropy(self, list_of_pi):
        """
        Function to calculate the entropy given a list of probabilities for each label
        :param list_of_pi: list of probabilities for each label
        :return: the entropy from shannon entropy
        """
        entropy = 0
        for pi in list_of_pi:
            if pi == 0:
                entropy += 0
            else:
                entropy += -pi * math.log2(pi)
        return entropy

    def __get_pi(self, dataset, attribute, value, label):
        """
        Function that calculates relative frequency of examples with a given label from a given data set
        Used for calculating the entropy
        :param dataset: the list of examples
        :param attribute: the attribute to focus on
        :param value: the value of the attribute
        :param label: the classification label
        :return: relative frequency of examples with a given label from a given data set
        """
        num_examples_with_value = 0
        num_examples_with_value_with_label = 0
        num_total_examples = 0
        num_columns = len(dataset[0])

        # find number of examples with the value of a given attribute
        for example in dataset:
            num_total_examples += 1
            if example[attribute] == value:
                num_examples_with_value += 1

                if example[num_columns - 1] == label:
                    num_examples_with_value_with_label += 1

        if num_examples_with_value == 0:
            return 0

        # if the attribute in question is the class label itself
        if attribute == num_columns - 1:
            return num_examples_with_value / num_total_examples

        # if the attribute in question is NOT the class label itself
        return num_examples_with_value_with_label / num_examples_with_value

    def __build_tree(self, dataset):
        """
        Function to build the Decision Tree.
        :param dataset: the training set used to induce the tree
        :return: the root of the dtree
        """
        list_of_subsets = []
        # find the best attribute for current data subset
        best_attribute_data = self.__find_best_attribute(dataset)
        # get most common class from dataset
        most_common_label = self.__get_most_common_label(dataset)
        # create question node using the best attribute
        q_node = questionNode(best_attribute_data, most_common_label)
        # divide dataset into subsets i.e shape, fillling size
        list_of_subsets = self.__divide_set_by_attribute(best_attribute_data[0], dataset)

        for subset in list_of_subsets:
            if self.__is_same_class(subset[1]):
                # add new leafNode
                new_class = self.__get_class(subset[1][0])
                child_node = leafNode(new_class)
                # add the class with its subset
                q_node.add_child(subset[0], child_node)

            else:
                q_node.add_child(subset[0], self.__build_tree(subset[1]))
        return q_node

    def __divide_set_by_attribute(self, attribute, dataset):
        """
        Function that divides a given dataset in subsets that correspond to each of the
        attribute's values.
        Example:
        divide the data set by the given attribute
        i.e attribute is shape --- return 3 subsets !
        return list of tuple (square, list_of_square_subset)...
        :param attribute: the attribute to split on
        :param dataset: the dataset to split
        :return: list of subsets split by the attribute values
        """
        list_of_subset = []
        # list of unqiue values in the given attribute:
        unique_values = self.__get_unique_values_for_attribute(attribute, dataset)
        for value in unique_values:
            subset = []
            # for each vector in dataset
            for example in dataset:
                if example[attribute] == value:
                    subset.append(example)

            list_of_subset.append((value, subset))

        return list_of_subset

    def __is_same_class(self, subset):
        """
        Function that returns true if all vectors in the subset have the same class
        :param subset: list of examples
        :return: true if all vectors in the subset have the same class, otherwise returns false
        """
        num_columns = len(subset[0])
        this_class = subset[0][num_columns - 1]
        for i in range(1, len(subset)):
            if subset[i][num_columns - 1] != this_class:
                return False
        return True

    def __get_unique_values_for_attribute(self, attribute, dataset):
        """
        Function to return the unique values for a given attribute in a given dataset
        Example:
        return subsets of each attribute
        shape: return cirlce, square, triangle
        :param attribute: the attribute to focus on
        :param dataset: the list of examples
        :return: a set of all the unique values the attribute has from a given dataset
        """
        subset = []
        for example in dataset:
            # print(example)
            # print('attribute: ', example[attribute])
            if not subset:
                subset.append(example[attribute])
            if example[attribute] not in subset:
                subset.append(example[attribute])
        # print(subset)
        return subset

    def __get_class(self, data):
        """
        Function that returns the class of each vector
        :param data: a feature vector
        :return: the class of that given feature vector
        """
        num_columns = len(data)
        return data[num_columns - 1]

    def __get_most_common_label(self, dataset):
        """
        Function that returns the most common label seen in a given dataset
        Used for handling the case of a missing edge in the tree
        :param dataset: the list of examples
        :return:
        """
        label_dict = {}
        num_columns = len(dataset[0])
        for example in dataset:
            label = example[num_columns - 1]
            if label in label_dict:
                label_dict[label] += 1
            else:
                label_dict[label] = 1
        most_common_label = random.choice(list(label_dict))
        for label in label_dict:
            if label_dict[label] > label_dict[most_common_label]:
                # found a new max
                most_common_label = label

        return most_common_label
