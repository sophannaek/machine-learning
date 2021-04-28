"""
Ensemble.py - Class that encapsulates all functions needed to create a Dtree Ensemble.
Provides a constructor for creating a Dtree Ensemble and functions to operate on the
Dtree Ensemble.

Dennis La - Dennis.La@student.csulb.edu
Melissa Hazlewood - Melissa.Hazlewood@student.csulb.edu
Rowan Herbert - Rowan.Herbert@student.csulb.edu
Sophanna Ek - Sophanna.Ek@student.csulb.edu
"""
import random
from enum import Enum
import parse
from Dtree import Dtree
from second_tree import from_misclassified


class DtreeEnsemble:
    def __init__(self):
        """
        Constructor for DtreeEnsemble. Creates a list of trees that will hold all the trees in
        the ensemble
        """
        # list of trees
        self.__list_of_dtrees = []

    def add_dtree_to_ensemble(self, dtree_to_add):
        """
        Function that adds a given tree to the ensemble
        :param dtree_to_add: the dtree to be added to the ensemble
        :return:
        """
        self.__list_of_dtrees.append(dtree_to_add)

    def get_voting_results(self, example):
        """
        Returns a label for a given example base on voting of the dtrees
        :param example: the example to classify
        :return: the label of the example that the ensemble assigns
        """
        vote_weight_dict = {}

        # go through each d tree and ask it to classify the example.
        # then create a key with the label it gives for the example
        # store each key (label) with a running total of weights of trees that vote for that label
        for dtree in self.__list_of_dtrees:
            label = dtree.get_classification(example)
            if label in vote_weight_dict:
                vote_weight_dict[label] += dtree.get_voting_weight()
            else:
                vote_weight_dict[label] = dtree.get_voting_weight()

        # find the max voting weight in vote weight dict
        # let the max be a random label
        label_with_max_vote_weight = random.choice(list(vote_weight_dict))
        for label in vote_weight_dict:
            if vote_weight_dict[label] > vote_weight_dict[label_with_max_vote_weight]:
                # found a new max
                label_with_max_vote_weight = label

        return label_with_max_vote_weight

    def get_accuracy(self, dataset):
        """
        Calculates the accuracy of the dtree ensemble
        :param dataset: the testing set
        :return: the accuracy of the ensemble
        """
        correct = 0
        for example in dataset:
            if example[len(dataset[0]) - 1] == self.get_voting_results(example):
                correct += 1
        return correct / len(dataset)


def main():
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

    # test example, this is the first example from csv file. class should be draw
    chess_example1 = ['1', 'd', '1', 'f', '3', 'e', '4', '???']
    # this other example should be class 'five'
    chess_example112 = ['112', 'd', '3', 'c', '4', 'c', '1', '???']

    tree_dict = parse.run()
    dtree1 = Dtree(tree_dict["train"], CHESS_COLUMNS)
    dtree1_acc = dtree1.get_accuracy(tree_dict["holdt"])
    print("Accuracy of dtree1:", dtree1_acc)

    dtree2 = from_misclassified(tree_dict, dtree1)
    dtree2_acc = dtree2.get_accuracy(tree_dict["holdt"])

    print("Accuracy of dtree2:", dtree2_acc)
    dtree_ensemble = DtreeEnsemble()
    dtree1.set_voting_weight(dtree1_acc)
    dtree2.set_voting_weight(dtree2_acc)
    dtree_ensemble.add_dtree_to_ensemble(dtree1)
    dtree_ensemble.add_dtree_to_ensemble(dtree2)

    print()
    print("classification of example 1 from dtree1 is:", dtree1.get_classification(chess_example1))
    #print("classification of example 122 from dtree1 is:", dtree1.get_classification(chess_example112))

    print()
    print("classification of example 1 from dtree2 is:", dtree2.get_classification(chess_example1))
    #print("classification of example 122 from dtree2 is:", dtree2.get_classification(chess_example112))

    print()
    print("classification of example 1 from ensemble is:", dtree_ensemble.get_voting_results(chess_example1))
    #print("classification of example 122 from ensemble is:", dtree_ensemble.get_voting_results(chess_example112))

if __name__ == "__main__":
    main()
