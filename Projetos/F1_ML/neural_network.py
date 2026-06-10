import numpy as np

class NeuralCar:
    def __init__(self, weights=None):
        self.num_inputs = 9
        self.hidden_size = 16

        if weights is None:
            self.w1 = np.random.randn(self.num_inputs, self.hidden_size) * 0.5
            self.b1 = np.zeros(self.hidden_size)
            self.w2 = np.random.randn(self.hidden_size, 2) * 0.5
            self.b2 = np.zeros(2)
        else:
            self.w1 = weights['w1'].copy()
            self.b1 = weights['b1'].copy()
            self.w2 = weights['w2'].copy()
            self.b2 = weights['b2'].copy()

        self.last_hidden = None
        self.last_output = None

    def think(self, inputs):
        x = np.array(inputs)
        self.last_hidden = np.tanh(x @ self.w1 + self.b1)
        self.last_output = np.tanh(self.last_hidden @ self.w2 + self.b2)

        return {
            'steer': self.last_output[0],
            'gas': self.last_output[1]
        }

    def mutate(self, rate):
        self.w1 += np.random.randn(*self.w1.shape) * rate
        self.b1 += np.random.randn(*self.b1.shape) * rate
        self.w2 += np.random.randn(*self.w2.shape) * rate
        self.b2 += np.random.randn(*self.b2.shape) * rate

    def get_weights(self):
        return {'w1': self.w1, 'b1': self.b1, 'w2': self.w2, 'b2': self.b2}