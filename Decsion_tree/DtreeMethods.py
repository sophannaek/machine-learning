<<<<<<< HEAD
from DtreeNodes import leafNode
from DtreeNodes import questionNode
import math
from enum import Enum



class DtreeMethods:

    @staticmethod
    def find_best_attribute(dataset):
        num_columns = len(dataset[0])
        list_of_pi = []
        set_of_classes = set()
        # get all the possible classes
        for example in dataset:
            set_of_classes.add(example[num_columns - 1])
        for c in set_of_classes:
            list_of_pi.append(DtreeMethods.__get_pi(dataset, num_columns - 1, c, c))

        h_t = DtreeMethods.__calc_entropy(list_of_pi)

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
                    list_of_pi.append(DtreeMethods.__get_pi(dataset, column, value, c))
                entropy = DtreeMethods.__calc_entropy(list_of_pi)

                h_attributes_values[value] = entropy
                collection_of_attribute_value_entropies[(column, value)] = entropy

            # calculate average entropy
            average_entropy = 0
            for value in possible_values:
                average_entropy += DtreeMethods.__get_relative_freq(dataset, column, value) * h_attributes_values[value]
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

    @staticmethod
    def __get_relative_freq(dataset, attribute, value):
        num_total_examples = 0
        num_examples_with_value = 0
        for example in dataset:
            num_total_examples += 1
            if example[attribute] == value:
                num_examples_with_value += 1

        if num_total_examples == 0:
            return 0
        return num_examples_with_value / num_total_examples

    @staticmethod
    def __calc_entropy(list_of_pi):
        entropy = 0
        for pi in list_of_pi:
            if pi == 0:
                entropy += 0
            else:
                entropy += -pi * math.log2(pi)
        return entropy

    @staticmethod
    def __get_pi(dataset, attribute, value, label):
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

        if attribute == num_columns - 1:
            return num_examples_with_value / num_total_examples

        return num_examples_with_value_with_label / num_examples_with_value

    @staticmethod
    def print_attribute_data(best_attribute_data, COLUMNS):
        print("best attribute to split on:", COLUMNS(best_attribute_data[0]).name, "column:",
              best_attribute_data[0], "\n")
        print("attribute value entropies:")
        for attribute_value_tuple in best_attribute_data[1]:
            print(COLUMNS(attribute_value_tuple[0]).name, attribute_value_tuple[1],
                  best_attribute_data[1][attribute_value_tuple])
        print()
        print("attribute entropies:")
        for attribute in best_attribute_data[2]:
            print(COLUMNS(attribute).name, best_attribute_data[2][attribute])
        print()
        print("attribute information gains:")
        for attribute in best_attribute_data[3]:
            print(COLUMNS(attribute).name, best_attribute_data[3][attribute])
        print()


    @staticmethod
    def getClassification(node, example):
        if node is type leafNode:
            return node.getClassification()
        else node is type questionNode:
            attribute = node.getAttribute()
            value = example[attribute]

        getClassification(node.getChild(value), example)


    """
    Build the Decision Tree. 
    """

    # return best_attribute, collection_of_attribute_value_entropies, h_t_attributes, attribute_info_gains
    def build_tree(dataset): 
        list_of_subsets = []
        # find the best attribute for current data subset
        best_attribute = DtreeMethods.find_best_attribute(dataset)
        
        #create question node using the best attribute 
        q_node = questionNode(best_attribute[0])
        # divide dataset into subsets i.e shape, fillling size 
        list_of_subsets = DtreeMethods.divide_set_by_attribute(best_attribute[0], dataset)
        print("attriubte ",best_attribute[0] )
        for subset in list_of_subsets: 
            if DtreeMethods.__is_same_class(subset[1]):
                # add new leafNode
                new_class = DtreeMethods.__get_class(subset[1][0])
                child_node = leafNode(new_class) 
                # add the class with its subset 
               
                q_node.addChild(subset[1], child_node.classification)       
                print("adding child  node: ", child_node.classification)
                print("its children are: ", q_node.getChild(child_node.classification))
            else: 
                DtreeMethods.build_tree(subset[1])
        return q_node


    # divide the data set by the given attribute
    # i.e attribute is shape --- return 3 subsets ! 
    # return list of tuple (square, list_of_square_subset)...
    def divide_set_by_attribute(attribute, dataset):
        list_of_subset = []
        # list of unqiue values in the given attribute:
        unique_values = DtreeMethods.__get_unique_values_for_attribute(attribute, dataset)
        for value in unique_values:         
            subset=[]
            # for each vector in dataset  
            for example in dataset:          
                # print("example: ", example) 
                if example[attribute] == value : 
                    subset.append(example)
                   
            list_of_subset.append((value, subset))
            
      
        return list_of_subset



    # return true if all vectors in the subset have the same class
    @staticmethod
    def __is_same_class(subset):
        num_columns = len(subset[0])
        this_class = subset[0][num_columns - 1]
        for i in range(1, len(subset)):
            if subset[i][num_columns - 1] != this_class:
               return False           
        return True
            
            
    # return subsets of each attribute 
    # shape: return cirlce, square, triangle   
    @staticmethod
    def __get_unique_values_for_attribute(attribute, dataset):
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

    # return the class of each vector 
    @staticmethod
    def __get_class(data):
        num_columns = len(data)
        return data[num_columns - 1]


def main():
    class PIE_COLUMNS(Enum):
        NO_ATTRIBUTE = -1
        ID = 0
        CRUST_SIZE = 1
        SHAPE = 2
        FILLING_SIZE = 3
        CLASS = 4

    # data must be in order from crust size, shape, filling size and class, according to the Enum
    pie_data = [
        ["1", "big", "circle", "small", "pos"],
        ["2", "small", "circle", "small", "pos"],
        ["3", "big", "square", "small", "neg"],
        ["4", "big", "triangle", "small", "neg"],
        ["5", "big", "square", "big", "pos"],
        ["6", "small", "square", "small", "neg"],
        ["7", "small", "square", "big", "pos"],
        ["8", "big", "circle", "big", "pos"],
    ]

    best_pie_attribute_data = DtreeMethods.find_best_attribute(pie_data)
    print("best attribute in pies domain to split on:", PIE_COLUMNS(best_pie_attribute_data[0]).name, "\n")
    print("pie domain attribute value entropies:")
    for attribute_value_tuple in best_pie_attribute_data[1]:
        print(PIE_COLUMNS(attribute_value_tuple[0]).name, attribute_value_tuple[1],
              best_pie_attribute_data[1][attribute_value_tuple])
    print()
    print("pie domain attribute entropies:")
    for attribute in best_pie_attribute_data[2]:
        print(PIE_COLUMNS(attribute).name, best_pie_attribute_data[2][attribute])
    print()
    print("pie domain attribute information gains:")
    for attribute in best_pie_attribute_data[3]:
        print(PIE_COLUMNS(attribute).name, best_pie_attribute_data[3][attribute])
    print()

    class CHESS_COLUMNS(Enum):
        NO_ATTRIBUTE = -1
        ID = 0
        WHITE_KING_FILE = 1
        WHITE_KING_RANK = 2
        WHITE_ROOK_FILE = 3
        WHITE_ROOK_RANK = 4
        BLACK_KING_FILE = 5
        BLACK_KING_RANK = 6
        CLASS = 7

    # attributes are in order by the Enum
    chess_data = [
        ["1", "d", "1", "f", "3", "e", "4", "draw"],
        ["2", "a", "1", "f", "3", "g", "3", "draw"],
        ["3", "c", "2", "d", "6", "a", "1", "one"],
        ["4", "d", "2", "e", "8", "a", "1", "four"],
        ["5", "c", "3", "e", "8", "c", "1", "two"],
        ["6", "c", "3", "d", "4", "e", "1", "eight"],
        ["7", "d", "3", "a", "8", "f", "3", "nine"],
        ["8", "d", "3", "e", "2", "b", "1", "four"],
        ["9", "d", "3", "b", "8", "b", "1", "three"],
    ]

    best_chess_attribute_data = DtreeMethods.find_best_attribute(chess_data)
    print("best attribute in chess domain to split on:", CHESS_COLUMNS(best_chess_attribute_data[0]).name, "\n")
    print("chess domain attribute value entropies:")
    for attribute_value_tuple in best_chess_attribute_data[1]:
        print(CHESS_COLUMNS(attribute_value_tuple[0]).name, attribute_value_tuple[1],
              best_chess_attribute_data[1][attribute_value_tuple])
    print()
    print("chess domain attribute entropies:")
    for attribute in best_chess_attribute_data[2]:
        print(CHESS_COLUMNS(attribute).name, best_chess_attribute_data[2][attribute])
    print()
    print("chess domain attribute information gains:")
    for attribute in best_chess_attribute_data[3]:
        print(CHESS_COLUMNS(attribute).name, best_chess_attribute_data[3][attribute])
    print()

    # test divide_set_by_attribute
    list_of_subset = DtreeMethods.divide_set_by_attribute(1, chess_data)
    for subset in list_of_subset: 
        print("subset by : " ,subset[0], subset[1])
        # to test need to change this method to public 
        # print("class for this subset: ", DtreeMethods.get_class(subset[1][0]))
    # test build tree
    question_node = DtreeMethods.build_tree(pie_data)
    

if __name__ == "__main__":
    main()
=======
# from DtreeNodes import leafNode
# from DtreeNodes import questionNode
# import math
# import random
# from enum import Enum
#
#
#
# class DtreeMethods:
#
#     @staticmethod
#     def find_best_attribute(dataset):
#         num_columns = len(dataset[0])
#         list_of_pi = []
#         set_of_classes = set()
#         # get all the possible classes
#         for example in dataset:
#             set_of_classes.add(example[num_columns - 1])
#         for c in set_of_classes:
#             list_of_pi.append(DtreeMethods.__get_pi(dataset, num_columns - 1, c, c))
#
#         h_t = DtreeMethods.__calc_entropy(list_of_pi)
#
#         # H(T, attribute) values
#         h_t_attributes = {}
#         collection_of_attribute_value_entropies = {}
#
#         # calculate the H(T, attribute)
#         for column in range(1, len(dataset[0]) - 1):
#             # H(attribute = value) values
#             h_attributes_values = {}
#
#             # get possible values from column
#             possible_values = set()
#             for example in dataset:
#                 possible_values.add(example[column])
#             # calculate the H(attribute = value) for each possible value
#             for value in possible_values:
#                 list_of_pi = []
#                 for c in set_of_classes:
#                     list_of_pi.append(DtreeMethods.__get_pi(dataset, column, value, c))
#                 entropy = DtreeMethods.__calc_entropy(list_of_pi)
#
#                 h_attributes_values[value] = entropy
#                 collection_of_attribute_value_entropies[(column, value)] = entropy
#
#             # calculate average entropy
#             average_entropy = 0
#             for value in possible_values:
#                 average_entropy += DtreeMethods.__get_relative_freq(dataset, column, value) * h_attributes_values[value]
#             h_t_attributes[column] = average_entropy
#
#         # find attribute with most info gain
#         highest_gain = 0
#         best_attribute = ""
#         attribute_info_gains = {}
#         for attribute in h_t_attributes:
#             current_gain = h_t - h_t_attributes[attribute]
#             attribute_info_gains[attribute] = current_gain
#             if current_gain > highest_gain:
#                 highest_gain = current_gain
#                 best_attribute = attribute
#
#         # case of no best attribute to split on. this means we will have a leaf
#         if best_attribute == "":
#             best_attribute = -1
#         # returns selected attribute, attribute value entropies, attribute entropies, and attribute info gains
#         return best_attribute, collection_of_attribute_value_entropies, h_t_attributes, attribute_info_gains
#
#     @staticmethod
#     def __get_relative_freq(dataset, attribute, value):
#         num_total_examples = 0
#         num_examples_with_value = 0
#         for example in dataset:
#             num_total_examples += 1
#             if example[attribute] == value:
#                 num_examples_with_value += 1
#
#         if num_total_examples == 0:
#             return 0
#         return num_examples_with_value / num_total_examples
#
#     @staticmethod
#     def __calc_entropy(list_of_pi):
#         entropy = 0
#         for pi in list_of_pi:
#             if pi == 0:
#                 entropy += 0
#             else:
#                 entropy += -pi * math.log2(pi)
#         return entropy
#
#     @staticmethod
#     def __get_pi(dataset, attribute, value, label):
#         num_examples_with_value = 0
#         num_examples_with_value_with_label = 0
#         num_total_examples = 0
#         num_columns = len(dataset[0])
#
#         # find number of examples with the value of a given attribute
#         for example in dataset:
#             num_total_examples += 1
#             if example[attribute] == value:
#                 num_examples_with_value += 1
#
#                 if example[num_columns - 1] == label:
#                     num_examples_with_value_with_label += 1
#
#         if num_examples_with_value == 0:
#             return 0
#
#         if attribute == num_columns - 1:
#             return num_examples_with_value / num_total_examples
#
#         return num_examples_with_value_with_label / num_examples_with_value
#
#     @staticmethod
#     def print_attribute_data(best_attribute_data, COLUMNS):
#         print("best attribute to split on:", COLUMNS(best_attribute_data[0]).name, "column:",
#               best_attribute_data[0], "\n")
#         print("attribute value entropies:")
#         for attribute_value_tuple in best_attribute_data[1]:
#             print(COLUMNS(attribute_value_tuple[0]).name, attribute_value_tuple[1],
#                   best_attribute_data[1][attribute_value_tuple])
#         print()
#         print("attribute entropies:")
#         for attribute in best_attribute_data[2]:
#             print(COLUMNS(attribute).name, best_attribute_data[2][attribute])
#         print()
#         print("attribute information gains:")
#         for attribute in best_attribute_data[3]:
#             print(COLUMNS(attribute).name, best_attribute_data[3][attribute])
#         print()
#
#
#     @staticmethod
#     def getClassification(node, example, possible_labels):
#         if isinstance(node, leafNode):
#             return node.getLabel()
#         elif isinstance(node, questionNode):
#             attribute = node.getAttribute()
#             value = example[attribute]
#             # need to check for missing edge
#             if value in node.children:
#                 return DtreeMethods.getClassification(node.getChild(value), example, possible_labels)
#             else:
#                 # we have a missing edge, need to give a random class
#                 random_index = random.randint(0, len(possible_labels) - 1)
#                 return possible_labels[random_index]
#
#     @staticmethod
#     def get_possible_labels_from_data(dataset):
#         set_of_possible_classes = set()
#         num_columns = len(dataset[0])
#         for example in dataset:
#             set_of_possible_classes.add(example[num_columns - 1])
#         return list(set_of_possible_classes)
#
#
#     """
#     Build the Decision Tree.
#     """
#     # return best_attribute, collection_of_attribute_value_entropies, h_t_attributes, attribute_info_gains
#     @staticmethod
#     def build_tree(dataset):
#         list_of_subsets = []
#         # find the best attribute for current data subset
#         best_attribute = DtreeMethods.find_best_attribute(dataset)
#
#         #create question node using the best attribute
#         q_node = questionNode(best_attribute[0])
#         # divide dataset into subsets i.e shape, fillling size
#         list_of_subsets = DtreeMethods.divide_set_by_attribute(best_attribute[0], dataset)
#
#         for subset in list_of_subsets:
#             if DtreeMethods.__is_same_class(subset[1]):
#                 # add new leafNode
#                 new_class = DtreeMethods.__get_class(subset[1][0])
#                 child_node = leafNode(new_class)
#                 # add the class with its subset
#                 # print("subset[1] ", subset[1])
#                 q_node.addChild(subset[0], child_node)
#                 #print("adding child  node: ", child_node.label)
#                 #print("its children are: ", q_node.getChild(child_node.label))
#             else:
#                 q_node.addChild(subset[0], DtreeMethods.build_tree(subset[1]))
#         return q_node
#
#
#     # divide the data set by the given attribute
#     # i.e attribute is shape --- return 3 subsets !
#     # return list of tuple (square, list_of_square_subset)...
#     @staticmethod
#     def divide_set_by_attribute(attribute, dataset):
#         list_of_subset = []
#         # list of unqiue values in the given attribute:
#         unique_values = DtreeMethods.__get_unique_values_for_attribute(attribute, dataset)
#         for value in unique_values:
#             subset=[]
#             # for each vector in dataset
#             for example in dataset:
#                 # print("example: ", example)
#                 if example[attribute] == value :
#                     subset.append(example)
#
#             list_of_subset.append((value, subset))
#
#
#         return list_of_subset
#
#
#
#     # return true if all vectors in the subset have the same class
#     @staticmethod
#     def __is_same_class(subset):
#         num_columns = len(subset[0])
#         this_class = subset[0][num_columns - 1]
#         for i in range(1, len(subset)):
#             if subset[i][num_columns - 1] != this_class:
#                return False
#         return True
#
#
#     # return subsets of each attribute
#     # shape: return cirlce, square, triangle
#     @staticmethod
#     def __get_unique_values_for_attribute(attribute, dataset):
#         subset = []
#         for example in dataset:
#             # print(example)
#             # print('attribute: ', example[attribute])
#             if not subset:
#                 subset.append(example[attribute])
#             if example[attribute] not in subset:
#                 subset.append(example[attribute])
#         # print(subset)
#         return subset
#
#     # return the class of each vector
#     @staticmethod
#     def __get_class(data):
#         num_columns = len(data)
#         return data[num_columns - 1]
#
#
# def main():
#     class PIE_COLUMNS(Enum):
#         NO_ATTRIBUTE = -1
#         ID = 0
#         CRUST_SIZE = 1
#         SHAPE = 2
#         FILLING_SIZE = 3
#         CLASS = 4
#
#     # data must be in order from crust size, shape, filling size and class, according to the Enum
#     pie_data = [
#         ["1", "big", "circle", "small", "pos"],
#         ["2", "small", "circle", "small", "pos"],
#         ["3", "big", "square", "small", "neg"],
#         ["4", "big", "triangle", "small", "neg"],
#         ["5", "big", "square", "big", "pos"],
#         ["6", "small", "square", "small", "neg"],
#         ["7", "small", "square", "big", "pos"],
#         ["8", "big", "circle", "big", "pos"],
#     ]
#
#     best_pie_attribute_data = DtreeMethods.find_best_attribute(pie_data)
#     print("best attribute in pies domain to split on:", PIE_COLUMNS(best_pie_attribute_data[0]).name, "\n")
#     print("pie domain attribute value entropies:")
#     for attribute_value_tuple in best_pie_attribute_data[1]:
#         print(PIE_COLUMNS(attribute_value_tuple[0]).name, attribute_value_tuple[1],
#               best_pie_attribute_data[1][attribute_value_tuple])
#     print()
#     print("pie domain attribute entropies:")
#     for attribute in best_pie_attribute_data[2]:
#         print(PIE_COLUMNS(attribute).name, best_pie_attribute_data[2][attribute])
#     print()
#     print("pie domain attribute information gains:")
#     for attribute in best_pie_attribute_data[3]:
#         print(PIE_COLUMNS(attribute).name, best_pie_attribute_data[3][attribute])
#     print()
#
#     class CHESS_COLUMNS(Enum):
#         NO_ATTRIBUTE = -1
#         ID = 0
#         WHITE_KING_FILE = 1
#         WHITE_KING_RANK = 2
#         WHITE_ROOK_FILE = 3
#         WHITE_ROOK_RANK = 4
#         BLACK_KING_FILE = 5
#         BLACK_KING_RANK = 6
#         CLASS = 7
#
#     # attributes are in order by the Enum
#     chess_data = [
#         ["1", "d", "1", "f", "3", "e", "4", "draw"],
#         ["2", "a", "1", "f", "3", "g", "3", "draw"],
#         ["3", "c", "2", "d", "6", "a", "1", "one"],
#         ["4", "d", "2", "e", "8", "a", "1", "four"],
#         ["5", "c", "3", "e", "8", "c", "1", "two"],
#         ["6", "c", "3", "d", "4", "e", "1", "eight"],
#         ["7", "d", "3", "a", "8", "f", "3", "nine"],
#         ["8", "d", "3", "e", "2", "b", "1", "four"],
#         ["9", "d", "3", "b", "8", "b", "1", "three"],
#     ]
#
#     best_chess_attribute_data = DtreeMethods.find_best_attribute(chess_data)
#     print("best attribute in chess domain to split on:", CHESS_COLUMNS(best_chess_attribute_data[0]).name, "\n")
#     print("chess domain attribute value entropies:")
#     for attribute_value_tuple in best_chess_attribute_data[1]:
#         print(CHESS_COLUMNS(attribute_value_tuple[0]).name, attribute_value_tuple[1],
#               best_chess_attribute_data[1][attribute_value_tuple])
#     print()
#     print("chess domain attribute entropies:")
#     for attribute in best_chess_attribute_data[2]:
#         print(CHESS_COLUMNS(attribute).name, best_chess_attribute_data[2][attribute])
#     print()
#     print("chess domain attribute information gains:")
#     for attribute in best_chess_attribute_data[3]:
#         print(CHESS_COLUMNS(attribute).name, best_chess_attribute_data[3][attribute])
#     print()
#
#     # test divide_set_by_attribute
#     list_of_subset = DtreeMethods.divide_set_by_attribute(1, chess_data)
#     for subset in list_of_subset:
#         print("subset by : " ,subset[0], subset[1])
#         # to test need to change this method to public
#         # print("class for this subset: ", DtreeMethods.get_class(subset[1][0]))
#     # test build tree
#     question_node = DtreeMethods.build_tree(chess_data)
#
#
# if __name__ == "__main__":
#     main()
>>>>>>> d6f978a74bcfc1ea95dbd79ea406d1a3f7e3082b
