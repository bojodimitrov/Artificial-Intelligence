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

    def get_weights(self):
        """
        Returns weights
        """
        return self.weights

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
    def __init__(self, number_of_inputs, number_of_hidden_neurons, number_of_outputs, learning_rate):
        self.learning_rate = learning_rate
        self.inputs = {'bias': [], 'neurons': []}
        self.outputs = []
        self.hidden_layer = {'bias': [], 'neurons': []}

        for _ in range(number_of_inputs):
            self.inputs['neurons'].append(InputNeuron(0))
        for _ in range(number_of_hidden_neurons):
            rand_weights = []
            for _ in range(number_of_inputs):
                rand_weights.append(random.uniform(0, 1))
            self.hidden_layer['neurons'].append(Neuron(rand_weights))
            self.inputs['bias'].append(random.uniform(0, 1))

        for _ in range(number_of_outputs):
            rand_weights = []
            for _ in range(number_of_hidden_neurons):
                rand_weights.append(random.uniform(0, 1))
            self.outputs.append(Neuron(rand_weights))
            self.hidden_layer['bias'].append(random.uniform(0,1))

    def feed_forward(self, inputs, activation):
        """
        Feeds forward the input values
        """
        for i, value in enumerate(inputs):
            self.inputs['neurons'][i].set_value(value)

        for i, hidden_neuron in enumerate(self.hidden_layer['neurons']):
            hidden_neuron.calculate([input_neuron.get_value() for input_neuron in self.inputs['neurons']], activation, self.inputs['bias'][i])

        for i, output_neuron in enumerate(self.outputs):
            output_neuron.calculate([hidden_neuron.get_value() for hidden_neuron in self.hidden_layer['neurons']], activation, self.hidden_layer['bias'][i])
        return [output_neuron.get_value() for output_neuron in self.outputs]

    def backpropagation(self, inputs, desired):
        """
        Applies backpropagation algorithm for correcting weights of the network
        """
        self.feed_forward(inputs, sigmoid)

        output_layer_corrections = {}
        for i, output in enumerate(self.outputs):
            delta_output = -(desired[i] - output.get_value()) * sigmoid_derivative(output.get_value())
            output_layer_corrections[i] = []
            for hidden_neuron in self.hidden_layer['neurons']:
                output_layer_corrections[i].append(-self.learning_rate * delta_output * hidden_neuron.get_value())
            self.hidden_layer['bias'][i] -= delta_output * self.learning_rate

        hidden_layer_corrections = {}
        for i, hidden_neuron in enumerate(self.hidden_layer['neurons']):
            hidden_layer_corrections[i] = []
            delta_total = 0
            for j, _ in enumerate(hidden_neuron.get_weights()):
                delta_hidden = 0
                #sum of the output deltas
                for k, output_neuron  in enumerate(self.outputs):
                    delta_hidden += -(desired[k] - output_neuron.get_value()) * sigmoid_derivative(output_neuron.get_value()) * output_neuron.get_weights()[i]
                delta_total = delta_hidden * sigmoid_derivative(hidden_neuron.get_value()) 
                total_error_derivative = delta_total * self.inputs['neurons'][j].get_value()
                hidden_layer_corrections[i].append(-self.learning_rate * total_error_derivative)
            self.inputs['bias'][i] -= delta_total * self.learning_rate

        for i, output_neuron in enumerate(self.outputs):
            output_neuron.update_weights(output_layer_corrections[i])
        for i, hidden_neuron in enumerate(self.hidden_layer['neurons']):
            hidden_neuron.update_weights(hidden_layer_corrections[i])


class Perceptron:
    """
    Simple perceptron
    """
    def __init__(self, number_of_inputs, number_of_outputs):
        self.bias = 1
        self.learning_rate = 0.2
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
                corrections.append(self.learning_rate * error * neuron.get_value())
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

def train_network_batch(network):
    """
    Trains network
    """
    for _ in range(50000):
        a = random.randint(0, 1)
        b = random.randint(0, 1)
        result = a ^ b
        network.backpropagation([a, b], [result])


#PERC = Perceptron(2, 1)
#train_batch(PERC)
#print(test_batch(PERC))

NEURAL_NETWORK = SingleHiddenLayerNetwork(2, 2, 1, 2)
train_network_batch(NEURAL_NETWORK)
print(NEURAL_NETWORK.feed_forward([0, 0], sigmoid))
print(NEURAL_NETWORK.feed_forward([0, 1], sigmoid))
print(NEURAL_NETWORK.feed_forward([1, 0], sigmoid))
print(NEURAL_NETWORK.feed_forward([1, 1], sigmoid))
