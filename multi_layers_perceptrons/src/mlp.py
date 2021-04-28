import math
import numpy as np
from random import uniform
from data import get_vectors
import sys
import confmatrix as cfm


class mlp:
    def __init__(self, n_hidden_nodes, n_outputs, data):
        self.__n_inputs = len(data[0]) - 2
        # self.__n_inputs = n_inputs
        self.__n_outputs = n_outputs
        self.__n_hidden_nodes = n_hidden_nodes
        # initial weights 
        self.hidden_layer_weight = [[uniform(-1.0, 1.0)  for i in range(self.__n_inputs)] for i in range(self.__n_hidden_nodes)]
        self.output_layer_weight = [[uniform(-1.0, 1.0)  for i in range(self.__n_hidden_nodes)] for i in range(self.__n_outputs)]
        self.initial_weights = [self.hidden_layer_weight, self.output_layer_weight]

        # number of epochs
        self.n_epochs = 0
        # multipercentron weights after training
        self.training_weights = self.__train(data)
        # correct class count
        self.correct_class = 0


    # return the classification of each test example
    def get_classification(self, example):
        return self.__get_classification(example)

   # prints the initial and final weights of the hidden and output nodes
    def print_weights(self):

        print("--------Initial hidden layer weight-----------")
        for i in range(len(self.initial_weights[0])):
            print("Initial weights of hidden node", i, ":\n", self.initial_weights[0][i], "\n")
        print("\n--------Initial output layer weight-----------")
        for i in range(len(self.initial_weights[1])):
            print("Initial weights of output node", i, ":\n", self.initial_weights[1][i], "\n")

        print("\n-------Final hidden layer weight------------")
        for i in range(len(self.hidden_layer_weight)):
            print("Final weights of hidden node", i, ":\n", self.hidden_layer_weight[i], "\n")
        print("\n-------Final output layer weight -----------")
        for i in range(len(self.output_layer_weight)):
            print("Final weights of output node", i, ":\n", self.output_layer_weight[i], "\n")

    # prints the number of epochs
    def print_epochs(self):
        print("-------Epochs------------")
        print(self.n_epochs)

    # return the multiperceptron weights
    def __train(self, dataset):
        for example in dataset:       
            attribute_vector = example[1:len(example)-1]
            # target vector for each example follows 80% 20% 
            target_vector = self.__getTarget_vec(example) 

            # perform forward propagation
            hidden_layer_neurons, output_layer_neurons = self.__forward_prop(self.hidden_layer_weight, self.output_layer_weight, attribute_vector)
            prev_hidden_layer_weight = self.hidden_layer_weight
            prev_output_layer_weight = self.output_layer_weight
            # perform backpropagation erorr
            self.hidden_layer_weight, self.output_layer_weight = self.__backprop(self.hidden_layer_weight, self.output_layer_weight, 
                       
                                                                output_layer_neurons,target_vector , hidden_layer_neurons, attribute_vector)
        self.n_epochs += 1

        while  not (self.__is_change_negligible(prev_hidden_layer_weight, self.hidden_layer_weight) and
                        self.__is_change_negligible(prev_output_layer_weight, self.output_layer_weight)):
            
            ##stuck in stagnation -- exceed the allowable running time 
            # if(self.n_epochs == 100):
            #     self.hidden_layer_weight = [[uniform(-1.0, 1.0)  for i in range(self.__n_inputs)] for i in range(self.__n_hidden_nodes)]
            #     self.output_layer_weight = [[uniform(-1.0, 1.0)  for i in range(self.__n_hidden_nodes)] for i in range(self.__n_outputs)]
    
            # works as expected
            if(self.n_epochs == 800):
                break
            self.__train(dataset)
           
        
        return self.hidden_layer_weight, self.output_layer_weight

    
    # return true when all weights get ~0 
    def __is_change_negligible(self, old_weights, new_weights): 
        difference = abs(old_weights - new_weights)
        # print(difference)
        for row in difference:
            for el in row: 
                if el > sys.float_info.epsilon :
                    return False
        return True



    # Return the label of each example

    def __get_label(self, example):
        return example[len(example)-1]

    # Return target vector of each example vector using 80% 20%
    def __getTarget_vec(self, example):
        target_vec = [0 for i in range(0, 8)]
        example_label = self.__get_label(example)
        target_vec[example_label] = 0.8
        for i in range(len(target_vec)): 
            if target_vec[i] == 0:
                target_vec[i] = 0.2
        

        return target_vec

    # Return hidden and ouput neurons of multi_percentrons
    def __forward_prop(self, hidden_layer, output_layer, attribute_vector):
        hidden_layer_output = []
        output_layer_output = []

        # go through each hidden layer node
        for hidden_node in hidden_layer:
            # print("hidden node ", hidden_node)
            swixi = 0
            # go through each attribute
            for i in range(len(attribute_vector)):
                swixi += attribute_vector[i] * hidden_node[i]

            # keep track of the output of the hidden layer
            hidden_layer_output.append(self.__sigmoid(swixi))

        # go through each output layer node
        for output_node in output_layer:
            swixi = 0
            # go through each hidden node's output
            for i in range(len(hidden_layer)):
                swixi += hidden_layer_output[i] * output_node[i]

            # keep track of the output of the output layer
            output_layer_output.append(self.__sigmoid(swixi))

        return hidden_layer_output, output_layer_output

    # logistic function
    def __sigmoid(self, swixi):
        return 1/(1 + math.pow(math.e, -swixi))


    #performs the backpropagation
    def __backprop(self, hidden_layer_weight, output_layer_weight, output_layer_neurons, target_vector, hidden_layer_neurons, attribute_vector, eta=0.1):
        hidden_layer_weight = np.array(hidden_layer_weight, dtype=np.float)
        output_layer_weight = np.array(output_layer_weight, dtype=np.float)
        output_layer_neurons = np.array(output_layer_neurons, dtype=np.float)
        target_vector = np.array(target_vector, dtype=np.float)
        hidden_layer_neurons = np.array(hidden_layer_neurons, dtype=np.float)
        attribute_vector = np.array(attribute_vector, dtype=np.float)
    
        num_hid = hidden_layer_neurons.size
        num_in = self.__n_inputs 
        
        output_responsibility = np.multiply(np.multiply(output_layer_neurons, (1 - output_layer_neurons)), (target_vector - output_layer_neurons))
        hidden_responsibility = np.multiply(np.multiply(hidden_layer_neurons, (1 - hidden_layer_neurons)), output_responsibility.dot(output_layer_weight))
        # print('hidden_responsibility ', hidden_responsibility)

        output_layer_weight = output_layer_weight + eta*np.multiply(np.array([output_responsibility,]*num_hid).transpose(), hidden_layer_neurons)
        # print('output_layer_weight ', output_layer_weight)

        hidden_layer_weight = hidden_layer_weight + eta*np.multiply(np.array([hidden_responsibility,]*num_in).transpose(), attribute_vector)

        return hidden_layer_weight, output_layer_weight

    
    # return classification for the example
    def __get_classification(self,example):
        matrix = self.__build_conf_matrix()
        # total count in each label
        example_label = self.__get_label(example)
        matrix[example_label].total += 1


        # classifier chooses the class whose output neuron has return the highest value 
        [hidden_neurons, output_neurons] = self.__forward_prop(self.training_weights[0], self.training_weights[1], example[1:len(example)-2])
        
        # classifier return correct label
        if output_neurons.index(max(output_neurons)) == self.__get_label(example):
            self.correct_class += 1
            matrix[example_label].tp += 1
        
        # classifier return wrong label
        else:
            matrix[example_label].fp += 1
        
        # classifer return true negative -- return ????
        for mx in matrix: 
            if mx.classname != self.__get_label(example):
                mx.fp += 1
            else: 
                mx.fn += 1
                
                
        
        print("classification for this example is  ", output_neurons.index(max(output_neurons)))

        return output_neurons.index(max(output_neurons))

    # return the accuracy of the 
    def get_accuracy(self, dataset):
        return self.correct_class / len(dataset)


    # return confusion matrix for each label
    def __build_conf_matrix(self, classname):
        matrix = []
        for i in range(8):
            matrix.append(cfm(i))
        return matrix

# if __name__ == "__main__":
#     # Testing forward propagation
#     # Example from book, table 5.1. slighty off due to rounding i think, but it shouldn't matter
#     hidden_layer_weight = [
#         [-1.0, 0.5],
#         [0.1, 0.7]
#     ]

#     output_layer_weight = [
#         [0.9, 0.5],
#         [-0.3, -0.1]
#     ]

#     attribute_vector = [0.8, 0.1]

    # MLP = mlp(2,2)
    # forward_prop_results =  MLP._forward_prop(hidden_layer_weight, output_layer_weight, attribute_vector)
    # # Hidden node outputs
    # print(forward_prop_results[0])
    # # Output node outputs
    # print(forward_prop_results[1])

    # # Testing backpropagation
    # # Example from Table 5.3 in Kubat
    # hidden_layer = [ [-1.0, 1.0],
    #                  [1.0, 1.0] ]

    # output_layer = [ [1.0, 1.0],
    #                  [-1.0, 1.0] ]

    # output_vector = [0.65, 0.59]
    # target_vector = [1.0, 0.0]
    # hidden_vector = [0.12, 0.5]
    # attribute_vector = [1.0, -1.0]

    # backprop_results = MLP._backprop(hidden_layer, output_layer, output_vector, target_vector, hidden_vector, attribute_vector)
    # # Hidden node outputs/weights
    # print("hidden nodes: " ,backprop_results[0])
    # # Output node outputs/weights
    # print("output nodes: ", backprop_results[1])

 
   
    # # test mlp()
    # # data = [100, 53, 69, 43, 86, 63, 0, 57, 12, 52, 44, 2]
    # MLP = mlp(2, 8)
    
    
    # print(MLP.get_classification(data))


    
