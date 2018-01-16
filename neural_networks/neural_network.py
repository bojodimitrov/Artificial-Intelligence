"""
Simple perceptron network
"""
import random
import math

class Neuron:
    """
    Basic structural unit of networks
    """
    def __init__(self, weights):
        self.weights = list(weights)
        self.value = 0

    def calculate(self, inputs, activation_function, bias):
        """
        Calculates its value
        """
        if len(inputs) != len(self.weights):
            raise ValueError('Different number of inputs and weights')
        neuron_base_value = 0
        for i, value in enumerate(inputs):
            neuron_base_value += value * self.weights[i]
        self.value = activation_function(neuron_base_value + bias)

    def get_value(self):
        """
        Returns neuron value
        """
        return self.value

    def update_weights(self, corrections):
        """
        Adds each weights_sum to each weight
        """
        for i, value in enumerate(corrections):
            self.weights[i] += value

class InputNeuron(Neuron):
    """
    Input neuron
    """
    def __init__(self, value):
        super(InputNeuron, self).__init__([])
        self.value = value

    def set_value(self, value):
        """
        Sets value
        """
        self.value = value

class SingleHiddenLayerNetwork:
    """
    Represents neural network with just one hidden layer
    """
    def __init__(self, number_of_inputs, number_of_hidden_neurons, number_of_outputs):
        self.training_constant = 0.2
        self.inputs = {'bias': 1, 'neurons': []}
        self.outputs = []
        self.hidden_layer = {'bias': 1, 'neurons': []}

        for _ in range(number_of_inputs):
            self.inputs['neurons'].append(InputNeuron(0))
        for _ in range(number_of_hidden_neurons):
            rand_weights = []
            for _ in range(number_of_inputs):
                rand_weights.append(random.uniform(-1, 1))
            self.hidden_layer['neurons'].append(Neuron(rand_weights))

        for _ in range(number_of_outputs):
            rand_weights = []
            for _ in range(number_of_hidden_neurons):
                rand_weights.append(random.uniform(-1, 1))
            self.outputs.append(Neuron(rand_weights))

    def feed_forward(self, inputs, activation):
        """
        Feeds forward the input values
        """
        for i, value in enumerate(inputs):
            self.inputs['neurons'][i].set_value(value)

        for hidden_neuron in self.hidden_layer['neurons']:
            hidden_neuron.calculate([input_neuron.get_value() for input_neuron in self.inputs['neurons']], activation, self.inputs['bias'])

        for output_neuron in self.outputs:
            output_neuron.calculate([hidden_neuron.get_value() for hidden_neuron in self.hidden_layer['neurons']], activation, self.hidden_layer['bias'])
        return [output_neuron.get_value() for output_neuron in self.outputs]

    def backpropagation(self, inputs, desired):
        """
        Applies backpropagation algorithm for correcting weights of the network
        """
        outputs = self.feed_forward(inputs, sigmoid)
        for i, output in enumerate(outputs):
            error = (desired[i] - outputs)





class Perceptron:
    """
    Simple perceptron
    """
    def __init__(self, number_of_inputs, number_of_outputs):
        self.bias = 1
        self.training_constant = 0.2
        self.inputs = []
        self.outputs = []

        for _ in range(number_of_inputs):
            self.inputs.append(InputNeuron(0))
        for _ in range(number_of_outputs):
            rand_weights = []
            for _ in range(number_of_inputs):
                rand_weights.append(random.uniform(-1, 1))
            self.outputs.append(Neuron(rand_weights))

    def feed_forward(self, inputs, activation):
        """
        Feeds forward the input values
        """
        for i, value in enumerate(inputs):
            self.inputs[i].set_value(value)

        for output_neuron in self.outputs:
            output_neuron.calculate([input_neuron.get_value() for input_neuron in self.inputs], activation, self.bias)
        return [output_neuron.get_value() for output_neuron in self.outputs]

    def train(self, trial, desired):
        """
        Correcting the weights
        """
        self.feed_forward(trial, step_function)
        for output_neuron in self.outputs:
            error = desired - output_neuron.get_value()
            corrections = []
            for _, neuron in enumerate(self.inputs):
                corrections.append(self.training_constant * error * neuron.get_value())
            output_neuron.update_weights(corrections)


def step_function(value):
    """
    Step function
    """
    if value >= 1:
        return 1
    else:
        return 0

def sigmoid(value):
    """
    Implementation of sigmoid function
    """
    return 1 / (1 + math.exp(-value))

def sigmoid_derivative(value):
    """
    Returns value of the derivative of the sigmoid function
    """
    return value * (1 - value)

def train_batch(perceptron):
    """
    Trains perceptron
    """
    for _ in range(1000):
        a = random.randint(0, 1)
        b = random.randint(0, 1)
        result = a & b
        perceptron.train([a, b], result)

def test_batch(perceptron):
    """
    Tests AND/OR perceptron
    """
    right = 0
    wrong = 0
    for _ in range(10000):
        a = random.randint(0, 1)
        b = random.randint(0, 1)
        correct = a & b
        result = perceptron.feed_forward([a, b], step_function)[0]
        if correct == result:
            right += 1
        else:
            wrong += 1
    return right / (right + wrong)

#PERC = Perceptron(2, 1)
#train_batch(PERC)
#print(test_batch(PERC))

NEURAL_NETWORK = SingleHiddenLayerNetwork(2, 2, 1)
print(NEURAL_NETWORK.feed_forward([0, 0], sigmoid))

