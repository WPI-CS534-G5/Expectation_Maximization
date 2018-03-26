import random


class Cluster(object):
    """docstring for ."""
    def __init__(self, mu=None, sig=None, probabilities=None):
        self.mu = mu
        self.sig = sig
        self.probabilities = probabilities

        if not mu:
            self. mu = random.random()
        if not sig:
            self.sig = random.random()