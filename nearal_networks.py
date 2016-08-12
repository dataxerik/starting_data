import math
from linear_algebra import dot


# Preceptron: a simple neural network which approximate a single neuron with n binary inputs
def step_function(x):
    return 1 if x >= 0 else 0


def perceptron_output(weights, bias, x):
    """returns 1 if the perceptron 'fires', 0 if not"""
    calculation = dot(weights, x) + bias
    return step_function(calculation)


def sigmoid(t):
    return 1 / (1 + math.exp(-t))


def neuron_output(weight, inputs):
    return sigmoid(dot(weight, inputs))


def feed_forward(neural_network, input_vector):
    """takes in a neural network
    (represented as a lists of list of weights)
    and returns the output from forward-propagating the input"""

    outputs = []

    # process one layer at a time
    for layer in neural_network:
        input_with_bias = input_vector + [1]  # add a bias input
        output = [neuron_output(neuron, input_with_bias)  # compute the output
                  for neuron in layer]
        outputs.append(output)

        # then the input to the next layer is the output of this one
        input_vector = output

    return outputs


def backpropagate(network, input_vector, targets):
    hidden_outputs, outputs = feed_forward(network, input_vector)

    # the output * (1 - output) is from the derivative of sigmoid
    output_deltas = [output * (1 - output) * (output - target)
                     for output, target in zip(outputs, targets)]

    # adjust weights for output layer, one neuron at a time
    for i, outputs_neuron in enumerate(network[-1]):
        # focus on the ith output layer neuron
        for j, hidden_outputs in enumerate(hidden_outputs + [1]):
            # adjust the jth weight based on both
            # this neuron's delta and its jth output
            outputs_neuron[j] -= output_deltas[i] * hidden_outputs
