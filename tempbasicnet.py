import numpy as np
import tensorflow.keras.datasets.mnist as mnist

np.random.seed(10)

(x_train, y_train), (x_test, y_test) = mnist.load_data(path='mnist.npz')

x_train = x_train.reshape(len(x_train), 784)


# dot product m1 (rows) x n1 (cols) by m2 x n2 --> n1 and m2 have to be the same


def sigmoid(x, derivative=False):
    if derivative:
        return (np.exp(-x))/((np.exp(-x)+1)**2)
    return 1 / (1 + np.exp(-x))


def snairsoftmax(array):
    vectorizedEx = np.vectorize(lambda x: np.exp(x))
    numerator = vectorizedEx(array)
    denominator = np.sum(numerator)
    return numerator/denominator


vectorizeSigmoid = np.vectorize(sigmoid)


def sigmoid(x, derivative=False):
    if derivative:
        return (np.exp(-x))/((np.exp(-x)+1)**2)
    return 1/(1 + np.exp(-x))


def xadf(x, derivative=False):
    # Numerically stable with large exponentials
    exps = np.exp(x - x.max())
    if derivative:
        return exps / np.sum(exps, axis=0) * (1 - exps / np.sum(exps, axis=0))
    return exps / np.sum(exps, axis=0)


def softmax(array, derivative=False):
    # Numerically stable with large exponentials
    n = np.e**(array)
    d = sum(n)
    if derivative:
        return n*(d-n) / d**2
    return n / d


def relu(array, derivative=False):
    if derivative:
        s = []
        for x in array:
            if x < 0:
                s.append(0)
            else:
                s.append(1)
        return s
    return [max(0, x) for x in array]


INPUT = 784
LAYER_1 = 128
LAYER_2 = 64
OUTPUT = 10
LEARNING_RATE = 0.01

# costtracker = []
numCorrect = 0

# a0 = x_train.reshape()  # input shape(784,)

w1 = np.random.randn(LAYER_1, INPUT, )  # shape(128,784)
b1 = np.random.randn(LAYER_1)  # shape(128)
w2 = np.random.randn(LAYER_2, LAYER_1)  # shape(64, 128)
b2 = np.random.randn(LAYER_2)  # shape(64)
w3 = np.random.randn(OUTPUT, LAYER_2)  # shape (10, 64)
b3 = np.random.randn(OUTPUT)  # shape (10)


for index, a0 in enumerate(x_train):
    # a0 = a0.reshape(784)
    a0 = np.divide(a0, 255)

    z1 = np.add(np.dot(w1, a0), b1)  # shape(128,784) ----- dotified
    a1 = vectorizeSigmoid(z1)  # shape(128,784)
    z2 = np.add(np.dot(w2, a1), b2)  # shape(128,784) ----- dotified
    a2 = vectorizeSigmoid(z2)  # shape(128,784)

    z3 = np.add(np.dot(w3, a2), b3)
    prediction = softmax(z3)
    # prediction = snairsoftmax(z3)
    valueOfPrediction = np.argmax(prediction)
    # print(prediction, )  # prints all 1

    actualArray = np.zeros(OUTPUT)
    actual = y_train[index]
    actualArray[actual] = 1

    # print("prediction {0} actual {1}".format(valueOfPrediction, actual), end="\n")
    if actual == valueOfPrediction:
        numCorrect += 1

    # cost = (prediction.index(max(prediction)) - actual) ** 2

    # # costtracker.append(cost)
    # prediction - actual = shape(10)
    # softmax z3 = shape(10)

    e3 = softmax(z3, derivative=True)*(prediction-actualArray)*2
    dcw3 = np.outer(e3, a2)
    dca3 = np.dot(w3.T, e3)
    # dca3 = np.dot(e3,w3)
    w3 -= dcw3
    b3 -= e3

    e2 = sigmoid(z2, derivative=True)*dca3
    dcw2 = np.outer(e2, a1)
    dca2 = np.dot(w2.T, e2)
    # dca2 = np.dot(e2,w2)
    w2 -= dcw2
    b2 -= e2

    e1 = sigmoid(z1, derivative=True)*dca2
    dcw1 = np.outer(e1, a0)
    # dca1 = np.dot(w1.T,e1)
    # dca1 = np.dot(e1,w1)
    w1 -= dcw1
    b1 -= e1

    # print(sum((prediction-actualArray)**2))

print(numCorrect/60000)
# costtracker = np.array(costtracker)
# x = [range(0,len(costtracker))]
# y = costtracker
# plt.plot(x, y, color="red")
# plt.show()
