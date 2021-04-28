from mlp import mlp
from data import get_vectors, trainingSet, training


def main():
    print("***EXECUTION INITIATED***")
    # train the data
    training_data = get_vectors()['training1and2']
    # create MLP with 12 hidden nodes and 8 output nodes
    MLP = mlp(12, 8, training_data)
    # test the holdout set
    holdout_data = get_vectors()['holdout']
    for example in holdout_data:
        MLP.get_classification(example)

    print()
    # printing the weights and the epochs
    MLP.print_weights()
    MLP.print_epochs()
        
    #Validation
    print("----------Validation----------")
    accuracy_rate = MLP.get_accuracy(holdout_data)
    error_rate = 1 - accuracy_rate
    print("Accuracy rate =", accuracy_rate)
    print("Error rate =", error_rate)

if __name__ == "__main__":
    main()