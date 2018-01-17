"""
Implementation of neural network with one hidden layer
"""
import random
import units
import activation_functions as f

class SingleHiddenLayerNetwork:
    """
    Represents neural network with just one hidden layer
    """
    def __init__(self, number_of_inputs, number_of_hidden_neurons,
                 number_of_outputs, learning_rate):
        self.learning_rate = learning_rate
        self.inputs = {'bias': [], 'neurons': []}
        self.outputs = []
        self.hidden_layer = {'bias': [], 'neurons': []}

        for _ in range(number_of_inputs):
            self.inputs['neurons'].append(units.InputNeuron(0))
        for _ in range(number_of_hidden_neurons):
            rand_weights = []
            for _ in range(number_of_inputs):
                rand_weights.append(random.uniform(0, 1))
            self.hidden_layer['neurons'].append(units.Neuron(rand_weights))
            self.inputs['bias'].append(random.uniform(0, 1))

        for _ in range(number_of_outputs):
            rand_weights = []
            for _ in range(number_of_hidden_neurons):
                rand_weights.append(random.uniform(0, 1))
            self.outputs.append(units.Neuron(rand_weights))
            self.hidden_layer['bias'].append(random.uniform(0, 1))

    def feed_forward(self, inputs, activation):
        """
        Feeds forward the input values
        """
        for i, value in enumerate(inputs):
            self.inputs['neurons'][i].set_value(value)

        for i, hidden_neuron in enumerate(self.hidden_layer['neurons']):
            hidden_neuron.calculate(
                [input_neuron.get_value() for input_neuron in self.inputs['neurons']],
                activation, self.inputs['bias'][i])

        for i, output_neuron in enumerate(self.outputs):
            output_neuron.calculate(
                [hidden_neuron.get_value() for hidden_neuron in self.hidden_layer['neurons']],
                activation, self.hidden_layer['bias'][i])
        return [output_neuron.get_value() for output_neuron in self.outputs]

    def backpropagation(self, inputs, desired):
        """
        Applies backpropagation algorithm for correcting weights and biases of the network
        """
        self.feed_forward(inputs, f.sigmoid)

        output_layer_corrections = {}
        for i, output in enumerate(self.outputs):
            delta_output = -(desired[i] - output.get_value()) * f.sigmoid_derivative(output.get_value())
            output_layer_corrections[i] = []
            for hidden_neuron in self.hidden_layer['neurons']:
                output_layer_corrections[i].append(
                    -self.learning_rate * delta_output * hidden_neuron.get_value())
            self.hidden_layer['bias'][i] -= delta_output * self.learning_rate

        hidden_layer_corrections = {}
        for i, hidden_neuron in enumerate(self.hidden_layer['neurons']):
            hidden_layer_corrections[i] = []
            delta_total = 0
            for j, _ in enumerate(hidden_neuron.get_weights()):
                delta_hidden = 0
                #sum of the output deltas
                for k, output_neuron  in enumerate(self.outputs):
                    delta_hidden += -(desired[k] - output_neuron.get_value()) * f.sigmoid_derivative(output_neuron.get_value()) * output_neuron.get_weights()[i]
                delta_total = delta_hidden * f.sigmoid_derivative(hidden_neuron.get_value())
                total_error_derivative = delta_total * self.inputs['neurons'][j].get_value()
                hidden_layer_corrections[i].append(-self.learning_rate * total_error_derivative)
            self.inputs['bias'][i] -= delta_total * self.learning_rate

        for i, output_neuron in enumerate(self.outputs):
            output_neuron.update_weights(output_layer_corrections[i])
        for i, hidden_neuron in enumerate(self.hidden_layer['neurons']):
            hidden_neuron.update_weights(hidden_layer_corrections[i])
