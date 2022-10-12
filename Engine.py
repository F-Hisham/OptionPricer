import logging_config
import scipy.stats
import numpy as np
from abc import ABC, abstractmethod
from scipy.stats import norm as norm

logger = logging_config.logging.getLogger(__name__)


class Engine(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def engine_price(self, spot, strike, rfr, time_to_maturity, vol, call_or_put, steps=100, num_path=10000) -> float:
        pass


class BlackScholes(Engine):
    def d1(self, spot, rfr, vol, strike, time_to_maturity) -> float:
        logger.info(
            f"d1 computed with following parameters: "
            f"spot {spot}, rfr {rfr}, vol {vol}, time_to_maturity {time_to_maturity} and strike {strike}")
        return (np.log(spot / strike) + (rfr + vol ** 2 / 2) * time_to_maturity) / (vol * np.sqrt(time_to_maturity))

    def d2(self, spot, rfr, vol, strike, time_to_maturity) -> float:
        logger.info(
            f"d2 computed with following parameters: "
            f"spot {spot}, rfr {rfr}, vol {vol}, time_to_maturity {time_to_maturity} and strike {strike}")
        return self.d1(spot=spot, rfr=rfr, vol=vol, strike=strike, time_to_maturity=time_to_maturity) - vol * np.sqrt(
            time_to_maturity)

    def engine_price(self, spot, strike, rfr, time_to_maturity, vol, call_or_put, steps=100, num_path=10000) -> float:
        logger.info(
            f"BS method processing using the following parameters: "
            f"spot {spot}, rfr {rfr}, vol {vol}, time_to_maturity {time_to_maturity} and strike {strike}")
        d1 = self.d1(spot=spot, rfr=rfr, vol=vol, strike=strike, time_to_maturity=time_to_maturity)
        d2 = self.d2(spot=spot, rfr=rfr, vol=vol, strike=strike, time_to_maturity=time_to_maturity)
        if call_or_put == "call":
            return norm.cdf(d1) * spot - norm.cdf(d2) * strike * np.exp(-rfr * time_to_maturity)
        else:
            return norm.cdf(-d2) * strike * np.exp(-rfr * time_to_maturity) - norm.cdf(-d1) * spot


class MonteCarlo(Engine):
    def paths(self, spot, strike, rfr, time_to_maturity, vol, steps=100, num_path=10000) -> np.ndarray:
        dt = time_to_maturity / steps
        return np.exp(np.log(spot) +
                      np.cumsum(((rfr - vol ** 2 / 2) * dt +
                                 vol * np.sqrt(dt) * np.random.normal(size=(steps, num_path))), axis=0))

    def engine_price(self, spot, strike, rfr, time_to_maturity, vol, call_or_put, steps=100, num_path=10000) -> float:
        logger.info(
            f"MC method processing using the following parameters: "
            f"spot {spot}, rfr {rfr}, vol {vol}, time_to_maturity {time_to_maturity}, "
            f"strike {strike}, steps {steps} and num_path {num_path}")
        paths = self.paths(
                spot=spot, strike=strike, rfr=rfr, time_to_maturity=time_to_maturity, vol=vol, steps=steps,
                num_path=num_path
            )
        if call_or_put == "call":
            return np.mean(np.maximum(paths[-1] - strike, 0)) * np.exp(-rfr * time_to_maturity)
        else:
            return np.mean(np.maximum(strike - paths[-1], 0)) * np.exp(-rfr * time_to_maturity)
