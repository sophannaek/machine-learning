

hidden_layer_weight = [[-1.0, 0.5],[0.1,.7]]
output_layer_weight = [[0.9,0.5],[-0.3, -0.1]]
attibute_vec = [0.8, 0.1]
target_vec = [1, 0]
output_vec = [0.65,0.59]
learning_rate = 0.1 



def test_forwardProp(hidden_layer_weight,output_layer_weight, attribute_vec ): 
    print("testing forward prop...")
    hidden_layer, output_layer = forward_prop(hidden_layer_weight, output_layer_weight, attribute_vec)



def test_backProp(output_vec, target_vec): 
    print("testing backprop... ")
    hidden_layer, output_layer = backpropagation(output_vec, target_vec)


def test_train_neural_networks():
    # TO DO