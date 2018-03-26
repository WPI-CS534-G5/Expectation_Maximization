import random


class Cluster(object):
    """docstring for ."""
    def __init__(self, mus=None, sigs=None, probabilities=None, num_dimensions=3):
        self.mus = mus
        self.sigs = sigs
        self.probabilities = probabilities

        if not mus:
            self.mus = []
            self.sigs = []
            for i in range(num_dimensions):
                self.mus.append(random.random())
                self.sigs.append(random.random())