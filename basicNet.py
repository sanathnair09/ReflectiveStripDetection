import math
# from tkinter import NE
import numpy as np


class Network():
    def __init__(self, input: np.ndarray):
        self.input = input
        self.inputSize = input.size

        self.layer1Activations = np.zeros(16)
        self.layer1Weights = np.random.randn(16, self.inputSize)
        self.layer1Biases = np.random.randn(self.inputSize)

    def train(self):

        pass

    # take input multiply with weights -> add bias -> squishify -> continue for number of layer
    # start with 784 -> 16 -> 10
    #           input layer1 output
    def feedForward(self, activation, weight, biases):
        vectorizeReLU = np.vectorize(Network.relu)
        vectorizeSigmoid = np.vectorize(Network.sigmoid)

        return vectorizeSigmoid(self, Network.computeWeightedSum(
            self, activation=activation, weight=weight, bias=biases))

    def backProp(self, learningRate=0.01):

        pass

    def computeWeightedSum(self,  weight, activation, bias):
        return np.add(np.dot(activation, weight), bias)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def relu(self, a):
        return max(0, a)

    def computeCost(self, prediction, actual):
        square = np.vectorize(x**2)
        return square(np.subtract(prediction, actual))

    def computeCostDerivative(self, prediction, actual):
        return 2 * (prediction - actual)


input = np.random.randn(784, 1)

net = Network(input=input)
net.feedForward()
