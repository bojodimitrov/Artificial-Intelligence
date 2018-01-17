"""
Simple perceptron network
"""
import random
import pattern
import activation_functions as f
import perceptron
import single_hidden_layer_network as n_n

def train_batch(perc):
    """
    Trains perceptron
    """
    for _ in range(1000):
        a = random.randint(0, 1)
        b = random.randint(0, 1)
        result = a & b
        perc.train([a, b], result)

def test_batch(perc):
    """
    Tests AND/OR perceptron
    """
    right = 0
    wrong = 0
    for _ in range(10000):
        a = random.randint(0, 1)
        b = random.randint(0, 1)
        correct = a & b
        result = perc.feed_forward([a, b], f.step_function)[0]
        if correct == result:
            right += 1
        else:
            wrong += 1
    return right / (right + wrong)

def train_network_xor(network):
    """
    Trains network
    """
    for _ in range(50000):
        a = random.randint(0, 1)
        b = random.randint(0, 1)
        result = a ^ b
        network.backpropagation([a, b], [result])


def train_pattern_recognizer(network):
    """
    Trains network to recognise symbol patterns using matrixes as pixels
    """
    for _ in range(10000):
        pat = random.randint(0, 7)
        symbol = pattern.get_symbol(pat)
        network.backpropagation(pattern.get_pattern(symbol)[0], pattern.get_pattern(symbol)[1])

PERC = perceptron.Perceptron(2, 1)
#train_batch(PERC)
#print(test_batch(PERC))

NEURAL_NETWORK = n_n.SingleHiddenLayerNetwork(2, 3, 1, 2)
train_network_xor(NEURAL_NETWORK)

#print('Pure pattern: \ = [0 0 0]')
#print(NEURAL_NETWORK.feed_forward(pattern.get_pattern(pattern.get_symbol(0))[0], f.sigmoid))
#print('Pure pattern: / = [0 0 1]')
#print(NEURAL_NETWORK.feed_forward(pattern.get_pattern(pattern.get_symbol(1))[0], f.sigmoid))
#print('Pure pattern: - = [0 1 0]')
#print(NEURAL_NETWORK.feed_forward(pattern.get_pattern(pattern.get_symbol(2))[0], f.sigmoid))
#print('Pure pattern: | = [0 1 1]')
#print(NEURAL_NETWORK.feed_forward(pattern.get_pattern(pattern.get_symbol(3))[0], f.sigmoid))
#print('Pure pattern: : = [1 0 0]')
#print(NEURAL_NETWORK.feed_forward(pattern.get_pattern(pattern.get_symbol(4))[0], f.sigmoid))
#print('Pure pattern: O = [1 0 1]')
#print(NEURAL_NETWORK.feed_forward(pattern.get_pattern(pattern.get_symbol(5))[0], f.sigmoid))
#print('Pure pattern: * = [1 1 0]')
#print(NEURAL_NETWORK.feed_forward(pattern.get_pattern(pattern.get_symbol(6))[0], f.sigmoid))
#print('Pure pattern: " = [1 1 1]')
#print(NEURAL_NETWORK.feed_forward(pattern.get_pattern(pattern.get_symbol(7))[0], f.sigmoid))
#print('Corrupted pattern: O = [1 0 1]')
#print(NEURAL_NETWORK.feed_forward(
#    [0, 0, 1, 0,
#     1, 0, 0, 1,
#     1, 0, 0, 1,
#     0, 1, 1, 0], f.sigmoid))

print(NEURAL_NETWORK.feed_forward([0, 0], f.sigmoid))
print(NEURAL_NETWORK.feed_forward([0, 1], f.sigmoid))
print(NEURAL_NETWORK.feed_forward([1, 0], f.sigmoid))
print(NEURAL_NETWORK.feed_forward([1, 1], f.sigmoid))
