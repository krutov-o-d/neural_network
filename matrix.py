import numpy as np
import random
import lab1 as generator
import copy

debug = False


def loadData(path_to_input):
    pass


def normalize_data(X):
    tmparr = []
    tmparr = np.array(tmparr)
    for i in range(len(X)):
        tmparr = np.append(tmparr, X[i].coords)
    # print(tmparr.len())
    mean = np.mean(tmparr)
    std = np.std(tmparr)
    for i in range(len(X)):
        X[i].coords = (X[i].coords - mean) / std
    return X


def encode(answer, class_number):
    ans = [0 for index in range(class_number)]
    ans[answer] = 1
    return ans


def sigm(x):
    return 1 / (1 + np.exp(-x))


def dsigm(x):
    return sigm(x) * (1 - sigm(x))


def getAnswer(answer):  # [a1, a2]
    max_value = max(answer)
    return [1 if max_value == el else 0 for el in answer]


def loss(out, true_out):
    # print (out)
    # print (true_out)
    eps = 1e-10
    size = len(out)
    out = np.clip(out, eps, 1 - eps)
    s = [true_out[index] * np.log(out[index]) + (1 - true_out[index]) * (np.log(1 - out[index])) for index in
         range(size)]
    s = -1 * sum(s) / size
    # print (s)
    return s


class Layer:

    def __init__(self,
                 w,  # weight vector          [[w01, w12, w02], [w10, w11, w12]]
                 b,  # cont input vector      [[b0], [b1]]
                 ):
        self.W = np.array(w, dtype=float)
        self.B = np.array(b, dtype=float)

    def doForward(self,
                  x  # input vector           [[x0],[x1],[x2]]
                  ):
        self.X = np.array(x, dtype=float)
        self.Z = self.W.dot(self.X) + self.B
        # self.A = np.array([[sigm(el)] for el in self.Z])
        self.A = sigm(self.Z)
        # print ('A {}'.format(self.A))
        return self.A

    def doBackward(self,
                   grad  # grad from next layer
                   ):

        # print ('self.Z '.format(self.Z))
        # print ('***')
        # print ('grad: {}'.format(grad))
        # print ('***')
        dadz = np.array([dsigm(self.Z) * grad]).transpose()
        # print('dadz: {}'.format(dadz))

        # if debug: print('dw:\n{}'.format(self.dw))
        self.db = dadz.sum()  ###
        # if debug: print('db:\n{}'.format(self.db))
        # print ('dadz {}'.format(dadz))

        if len(self.X.shape) == 1:
            self.X = self.X.reshape(self.X.shape[0], 1)
        else:
            self.X = np.transpose(self.X)

        # print ('X {}'.format(self.X))
        self.dw = dadz.dot(self.X.transpose())
        # print ('***')
        # print (self.dw)
        # print ('dick: {}'.format(np.dot(np.transpose(self.W),dadz).transpose()))
        # if debug: print('dw:\n{}'.format(self.dw))
        # print ('***')
        return np.dot(np.transpose(self.W), dadz).transpose()[0]

        # if debug: print('back grad: {}'.format(grad))
        # if debug: print('trans: {}'.format(w.transpose()))

        # if debug: print('back ans: {}'.format(grad.dot(dadz)))

        # return np.array(grad.dot(dadz)) #dot(w.transpose()))


class Net:
    def __init__(self,
                 layers,  # [num of neurons] (first - num of inputs)
                 speed  # learning rate
                 ):
        self.loss_g = []
        self.layers = []
        self.speed = speed
        for l in range(1, len(layers)):
            lines = []  # make W
            for cur in range(layers[l]):
                line = []
                for prev in range(layers[l - 1]):
                    line.append(random.random())
                lines.append(line)
            b = []
            for index in range(layers[l]):
                b.append(0)
            self.layers.append(Layer(lines, b))

    def forward(self,
                sample
                ):
        for l in self.layers:
            sample = copy.deepcopy(l.doForward(sample))
        return sample

    def backward(self,
                 grad
                 ):
        for l in range(len(self.layers)):
            # print ('###')
            # print (grad)
            # print ('###')
            grad = copy.deepcopy(self.layers[len(self.layers) - 1 - l].doBackward(grad))
        # print ('###')
        # print (grad)
        # print ('###')

    def update(self):
        for l in self.layers:
            # print ('----')
            # print('W\n{}'.format(l.W))
            # print('dw\n{}'.format(l.dw))
            l.W = l.W - l.dw * self.speed
            # print('W\n{}'.format(l.W))
            l.B = l.B - l.db * self.speed
            # print ('----')

    def predict(self,
                input
                ):
        return self.forward(input)

    def teach(self,
              input,
              output
              ):
        eps = 1e-5
        ans = getAnswer(self.predict(input))
        true_ans = np.array(encode(output, len(ans)))
        # true_ans = np.array([[el] for el in true_ans])
        A1 = np.array(self.layers[-1].A, dtype=float)
        self.loss_g.append(loss(A1, true_ans))

        # print (loss(getAnswer(A1), encode(output,len(A1))))
        A1 = np.clip(A1, eps, 1 - eps)
        da1 = - true_ans / A1 + (1 - true_ans) / (1 - A1)
        # print ('teach')
        # print (da1)
        # print ('teach')
        self.backward(da1)
        self.update()


if __name__ == '__main__':
    # layer0 = Layer([[1,2,3,4],[4,3,2,1]],[[1],[1]])
    # layer1 = Layer([[1,2], [2, 1]], [[2],[2]])
    # predict = getAnswer(layer1.doForward(layer0.doForward([[1],[2],[3],[4]])))

    # true_ans = np.array(encode(0,2), dtype=float)
    # A1 = np.array(layer1.A, dtype=float)

    # l = loss(predict, true_ans) #  for graph
    # true_ans = np.array([[el] for el in true_ans])

    # if debug: print('true ans: {}'.format(true_ans))
    # if debug: print('A1: {}'.format(A1))
    # if debug: print('1 - true ans: {}'.format(1 - true_ans))
    # if debug: print('1 - A: {}'.format(1 - A1))

    # da1 = - true_ans / A1 + (1-true_ans) / (1-A1)

    # if debug: print('da1: {}'.format(da1))

    # da0 = layer1.doBackward(da1)
    # if debug: print('d0:\n{}'.format(da0))

    # layer1.doBackward()
    net = Net([2,5,4], 0.1)
    # for l in net.layers:
    #     print ('---')
    #     print (l.W.shape)
    classes = generator.generate_classes(4)
    classes=normalize_data(classes)

    for q in range(100):
        for j in range(classes[0].coords.__len__()):
            for i in range(classes.__len__()):
                net.teach(classes[i].coords[j],i)
    generator.draw_classes(classes)
    for i in range(classes.__len__()):
        for j in range(10):
            print(net.predict(classes[i].coords[j]))
            print("got {} , true {}".format(getAnswer(net.predict(classes[i].coords[j])),i))