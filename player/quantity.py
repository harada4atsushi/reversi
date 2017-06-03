class Quantity:
    def __init__(self, alpha, gamma, initial_q = 1):
        self._initial_q = initial_q
        self._values = {}
        self._alpha = alpha
        self._gamma = gamma

    def get(self, state, act):
        if self._values.get((state, act)) is None:
            # self._values[(state, act)] = self._initial_q
            return self._initial_q
        return self._values.get((state, act))

    def set(self, s, a, q_value):
        self._values[s, a] = q_value

    def update(self, s, a, r, max_q):
        # print(a)
        pQ = self.get(s, a)
        new_q = pQ + self._alpha * ((r + self._gamma * max_q) - pQ)
        # print(new_q)
        self.set(s, a, new_q)
