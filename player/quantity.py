class Quantity:
    def __init__(self, initial_q = 1):
        self._initial_q = initial_q
        self._values = {}

    def get(self, state, act):
        if self._values.get((state, act)) is None:
            self._values[(state, act)] = self._initial_q
        return self._values.get((state, act))

    def set(self, s, a, q_value):
        self._values[s, a] = q_value
