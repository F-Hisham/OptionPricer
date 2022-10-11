import scipy.stats
import numpy as np


class OptionPricer:
    def __init__(self, s, k, r, t, sigma):
        self.spot = s
        self.strike = k
        self.rate = r
        self.time = t
        self.sigma = sigma

    def discounting(self) -> float:
        return np.exp(-self.rate * self.time)

    def black_scholes(self, c_p: True):
        n = scipy.stats.norm.cdf
        d1 = (np.log(self.spot / self.strike) + (self.rate + self.sigma ** 2 / 2) * self.time) / (
                self.sigma * np.sqrt(self.time))
        d2 = d1 - self.sigma * np.sqrt(self.time)
        # c = n(d1) * self.spot - n(d2) * self.strike * np.exp(-self.rate * self.time)
        # p = c + self.strike * np.exp(-self.rate * self.time) - self.spot
        if c_p:
            return n(d1) * self.spot - n(d2) * self.strike * np.exp(-self.rate * self.time)
        else:
            return n(-d2) * self.strike * np.exp(-self.rate * self.time) - n(-d1) * self.spot

    def monte_carlo(self, c_p: True, steps, paths):
        dt = self.time / steps
        path = np.exp(np.log(self.spot) +
                      np.cumsum(((self.rate - self.sigma ** 2 / 2) * dt +
                                 self.sigma * np.sqrt(dt) * np.random.normal(size=(steps, paths))), axis=0))
        if c_p:
            return np.mean(np.maximum(path[-1] - self.strike, 0)) * self.discounting()
        else:
            np.mean(np.maximum(self.strike - path[-1], 0)) * self.discounting()
