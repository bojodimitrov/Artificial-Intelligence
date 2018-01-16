"""
Simple perceptron network
"""
import random

class Perceptron:
    """
    Simple perceptron
    """
    def __init__(self, number_of_inputs, number_of_outputs):
        self.bias = 1
        self.inputs = []
        self.outputs = []
        self.weights = []
        self.traininig_constant = 0.5
        self.number_of_outputs = number_of_outputs
        for i in range(number_of_outputs):
            self.weights.append([])
            for _ in range(number_of_inputs):
                self.weights[i].append(random.uniform(-1, 1))

    def feed_forward(self, inputs, activation):
        """
        Feeds forward the input values
        """
        self.outputs = []
        self.inputs = list(inputs)
        for i in range(self.number_of_outputs):
            neuron_value = 0
            for j in range(len(self.inputs)):
                neuron_value += self.inputs[j]*self.weights[i][j] * self.bias
            self.outputs.append(activation(neuron_value))
        return self.outputs

    def train(self, trial, desired):
        """
        Correcting the weights
        """
        self.feed_forward(trial, activation_function)
        for i in range(len(self.outputs)):
            error = desired - self.outputs[i]
            for j in range(len(self.weights[i])):
                self.weights[i][j] += self.traininig_constant * error * self.inputs[j]


def activation_function(value):
    """
    Step function
    """
    if value > 2:
        return 1
    else:
        return 0

def train_batch(perceptron):
    for _ in range(1000):
        a = random.randint(0, 1)
        b = random.randint(0, 1)
        result = a & b
        perceptron.train([a, b], result)

def test_batch(perceptron):
    right = 0
    wrong = 0
    for _ in range(10000):
        a = random.randint(0, 1)
        b = random.randint(0, 1)
        correct = a & b
        result = perceptron.feed_forward([a, b], activation_function)[0]
        if correct == result:
            right += 1
        else:
            wrong += 1
    return right / (right + wrong)

PERC = Perceptron(2, 1)
train_batch(PERC)
print(test_batch(PERC))
print(PERC.weights)
