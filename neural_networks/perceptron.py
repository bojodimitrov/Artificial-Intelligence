"""
Implementation of perceptron
"""
import random
import units
import activation_functions as f

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
            self.inputs.append(units.InputNeuron(0))
        for _ in range(number_of_outputs):
            rand_weights = []
            for _ in range(number_of_inputs):
                rand_weights.append(random.uniform(-1, 1))
            self.outputs.append(units.Neuron(rand_weights))

    def feed_forward(self, inputs, activation):
        """
        Feeds forward the input values
        """
        for i, value in enumerate(inputs):
            self.inputs[i].set_value(value)

        for output_neuron in self.outputs:
            output_neuron.calculate(
                [input_neuron.get_value() for input_neuron in self.inputs], activation, self.bias)
        return [output_neuron.get_value() for output_neuron in self.outputs]

    def train(self, trial, desired):
        """
        Correcting the weights
        """
        self.feed_forward(trial, f.step_function)
        for output_neuron in self.outputs:
            error = desired - output_neuron.get_value()
            corrections = []
            for _, neuron in enumerate(self.inputs):
                corrections.append(self.learning_rate * error * neuron.get_value())
            output_neuron.update_weights(corrections)
