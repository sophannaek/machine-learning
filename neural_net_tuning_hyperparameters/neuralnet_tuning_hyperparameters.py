from mnist import MNIST
import os
from sklearn.model_selection import train_test_split
import numpy as np
from keras import optimizers
from keras import models
from keras import layers
from sklearn.model_selection import GridSearchCV, RepeatedStratifiedKFold
from keras.wrappers.scikit_learn import KerasClassifier
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
import numpy as np



# create model based for each optimizer function
def create_model_sgd(learning_rate):
    # create a model
    model = models.Sequential()
    model.add(layers.Dense(units=32, activation='sigmoid', input_shape=(num_pixels,)))
    model.add(layers.Dense(units=num_labels, activation='softmax'))
    model.compile(optimizer=optimizers.SGD(learning_rate=learning_rate),
                  loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def create_model_rmsprop(learning_rate, rho, epsilon):
    # create a model
    model = models.Sequential()
    model.add(layers.Dense(units=32, activation='sigmoid', input_shape=(num_pixels,)))
    model.add(layers.Dense(units=num_labels, activation='softmax'))
    model.compile(optimizer=optimizers.RMSprop(learning_rate=learning_rate, rho=rho, epsilon=epsilon),
                  loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def create_model_adam(learning_rate, beta_1, beta_2, epsilon):
    # create a model
    model = models.Sequential()
    model.add(layers.Dense(units=32, activation='sigmoid', input_shape=(num_pixels,)))
    model.add(layers.Dense(units=num_labels, activation='softmax'))
    model.compile(optimizer=optimizers.Adam(learning_rate=learning_rate, beta_1=beta_1, beta_2=beta_2, epsilon=epsilon),
                  loss='categorical_crossentropy', metrics=['accuracy'])
    return model



if __name__ == "__main__": 

    # loading training and test sets 
    mndata = MNIST('mnist')
    X_train, y_train = mndata.load_training()
    X_test, y_test = mndata.load_testing()

    # np.shape(X_train)
    # (60000, 784)


    # image of 'zero' for id = 1
    id=1
    image = np.array(X_train[id], dtype='float')
    pixels = image.reshape((28, 28))
    # show image
    # plt.imshow(pixels, cmap='gray')
    # plt.show()


    # convert to numpy array
    X_train = np.array(X_train)
    X_test = np.array(X_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)

    # validation set =  1/6 training set
    # random splits = 10 
    num_splits = 6 
    num_pixels = 784
    num_labels = 10
    batch_size = 5000
    num_epochs = 1
    verbose_level = 1
    num_repeats = 1

    optimizer_scores = dict()
    best_hyperparameters = dict()

    # tuning hyperparameters with sgd optimizer
    model_sgd = KerasClassifier(build_fn=create_model_sgd, epochs=num_epochs, batch_size=batch_size, verbose=verbose_level)
    # define the grid search parameters
    # learning_rate = [0.1, 0.01, 0.001]
    learning_rate=[0.1]
    param_grid = dict(learning_rate=learning_rate)
    cv = RepeatedStratifiedKFold(n_splits=num_splits, n_repeats=num_repeats)
    grid = GridSearchCV(estimator=model_sgd, param_grid=param_grid, n_jobs=-1, cv=cv)
    grid_result = grid.fit(X_train, y_train)
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    optimizer_scores["sgd"] = grid_result.best_score_
    best_hyperparameters["sgd"] = grid_result.best_params_

    # tuning hyperparameters with rmsprop optimizer
    model_rmsprop = KerasClassifier(build_fn=create_model_rmsprop, epochs=num_epochs, batch_size=batch_size, verbose=verbose_level)
    # define the grid search parameters
    learning_rate = [0.1, 0.01, 0.001]
    rho = [0.7, 0.8, 0.9]
    epsilon = [1e-06, 1e-07, 1e-08]
    param_grid = dict(learning_rate=learning_rate, rho=rho, epsilon=epsilon)
    cv = RepeatedStratifiedKFold(n_splits=num_splits, n_repeats=num_repeats)
    grid = GridSearchCV(estimator=model_rmsprop, param_grid=param_grid, n_jobs=-1, cv=cv)
    grid_result = grid.fit(X_train, y_train)
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    optimizer_scores["rmsprop"] = grid_result.best_score_
    best_hyperparameters["rmsprop"] = grid_result.best_params_

    # tuning hyperparameters with adam optimizer 
    model_adam = KerasClassifier(build_fn=create_model_adam, epochs=num_epochs, batch_size=batch_size, verbose=verbose_level)
    # define the grid search parameters
    learning_rate = [0.1, 0.01, 0.001]
    beta_1 = [0.7, 0.8, 0.9]
    beta_2 = [0.777, 0.888, 0.999]
    epsilon = [1e-06, 1e-07, 1e-08]
    param_grid = dict(learning_rate=learning_rate, beta_1=beta_1, beta_2=beta_2, epsilon=epsilon)
    cv = RepeatedStratifiedKFold(n_splits=num_splits, n_repeats=num_repeats)
    grid = GridSearchCV(estimator=model_adam, param_grid=param_grid, n_jobs=-1, cv=cv)
    grid_result = grid.fit(X_train, y_train)
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    optimizer_scores["adam"] = grid_result.best_score_
    best_hyperparameters["adam"] = grid_result.best_params_


    # tuning hyperparameter with adagrad optimizers
    model_adagrad = KerasClassifier(build_fn=create_model_adagrad, epochs=num_epochs, batch_size=batch_size, verbose=verbose_level)
    # define the grid search parameters
    learning_rate = [0.1, 0.01, 0.001]
    initial_accumulator_value = [0.001, 0.01, 0.1]
    epsilon = [1e-06, 1e-07, 1e-08]
    param_grid = dict(learning_rate=learning_rate, initial_accumulator_value=initial_accumulator_value, epsilon=epsilon)
    cv = RepeatedStratifiedKFold(n_splits=num_splits, n_repeats=num_repeats)
    grid = GridSearchCV(estimator=model_adagrad, param_grid=param_grid, n_jobs=-1, cv=cv)
    grid_result = grid.fit(X_train, y_train)
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    optimizer_scores["adagrad"] = grid_result.best_score_
    best_hyperparameters["adagrad"] = grid_result.best_params_

    # find the best optimizer among above optimizers
    for key in optimizer_scores:
        print(key, optimizer_scores[key], best_hyperparameters[key])


    
    for key in optimizer_scores:
        print(key, optimizer_scores[key], best_hyperparameters[key])

    # Train the network with the training dataset (not sub training) with the best hyper-parameters of each optimizer.
    optimizer_test_accuracies = dict()

    # SGD
    model_sgd = create_model_sgd(learning_rate=best_hyperparameters["sgd"]["learning_rate"])
    model_sgd.fit(X_train, to_categorical(y_train), epochs=num_epochs, batch_size=batch_size, verbose=verbose_level)
    loss, acc = model_sgd.evaluate(X_test, to_categorical(y_test))
    optimizer_test_accuracies["sgd"] = acc

    # RMSPROP
    model_rmsprop = create_model_rmsprop(learning_rate=best_hyperparameters["rmsprop"]["learning_rate"],
                                        rho=best_hyperparameters["rmsprop"]["rho"],
                                        epsilon=best_hyperparameters["rmsprop"]["epsilon"])
    model_rmsprop.fit(X_train, to_categorical(y_train), epochs=num_epochs, batch_size=batch_size, verbose=verbose_level)
    loss, acc = model_rmsprop.evaluate(X_test, to_categorical(y_test))
    optimizer_test_accuracies["rmsprop"] = acc

    # ADAM
    model_adam = create_model_adam(learning_rate=best_hyperparameters["adam"]["learning_rate"],
                                beta_1=best_hyperparameters["adam"]["beta_1"],
                                beta_2=best_hyperparameters["adam"]["beta_2"],
                                epsilon=best_hyperparameters["adam"]["epsilon"])
    model_adam.fit(X_train, to_categorical(y_train), epochs=num_epochs, batch_size=batch_size, verbose=verbose_level)
    loss, acc = model_adam.evaluate(X_test, to_categorical(y_test))
    optimizer_test_accuracies["adam"] = acc

    # Adagrad
    model_adagrad = create_model_adagrad(learning_rate=best_hyperparameters["adagrad"]["learning_rate"],
                                initial_accumulator_value=best_hyperparameters["adagrad"]["initial_accumulator_value"],
                                epsilon=best_hyperparameters["adagrad"]["epsilon"])
    model_adagrad.fit(X_train, to_categorical(y_train), epochs=num_epochs, batch_size=batch_size, verbose=verbose_level)
    loss, acc = model_adagrad.evaluate(X_test, to_categorical(y_test))
    optimizer_test_accuracies["adagrad"] = acc


    for key in optimizer_test_accuracies:
        print("Test accuracy of", key, optimizer_test_accuracies[key])

    # select the best optimizer for the neural network 
    best_optimizer = max(optimizer_test_accuracies, key=optimizer_test_accuracies.get)
    print("The best optimizer is", best_optimizer)
    chosen_hyperparameters = best_hyperparameters[best_optimizer]
    print("The best hyperparameters found for", best_optimizer, "are", chosen_hyperparameters)


