import logging_config
import numpy as np
import globalattributes as ga
from abc import ABC, abstractmethod
from scipy.stats import norm as norm

logger = logging_config.logging.getLogger(__name__)


class Engine(ABC):

    @abstractmethod
    def engine_price(self, spot, strike, rfr, time_to_maturity, vol) -> float:
        pass


class BlackScholes(Engine):

    def __init__(self):
        pass

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

    def engine_price(self, spot, strike, rfr, time_to_maturity, vol) -> float:
        logger.info(
            f"BS method processing using the following parameters: "
            f"spot {spot}, rfr {rfr}, vol {vol}, time_to_maturity {time_to_maturity} and strike {strike}")
        d1 = self.d1(spot=spot, rfr=rfr, vol=vol, strike=strike, time_to_maturity=time_to_maturity)
        d2 = self.d2(spot=spot, rfr=rfr, vol=vol, strike=strike, time_to_maturity=time_to_maturity)
        if ga.option_type == "Call":
            return norm.cdf(d1) * spot - norm.cdf(d2) * strike * np.exp(-rfr * time_to_maturity)
        else:
            return norm.cdf(-d2) * strike * np.exp(-rfr * time_to_maturity) - norm.cdf(-d1) * spot

    def iv_newtonraphson(self, spot, strike, vol, rfr, pricing_dt, nb_loop, market_price, time_to_maturity) -> float:
        sigma = 0.5
        for i in range(nb_loop):

            bs_price = self.engine_price(spot=spot, vol=vol, rfr=rfr, pricing_dt=pricing_dt)
            diff = market_price - bs_price
            vega = spot * self.d1(spot=spot, rfr=rfr, vol=vol, strike=strike, time_to_maturity=time_to_maturity) * np.sqrt(self.time)
            if abs(diff) < 0.01:
                return sigma
            sigma += diff / vega
        return sigma

class MonteCarlo(Engine):
    def __init__(self, steps, num_path):
        self.steps = steps
        self.num_path = num_path

    def paths(self, spot, rfr, time_to_maturity, vol) -> np.ndarray:
        dt = time_to_maturity / self.steps
        return np.exp(np.log(spot) +
                      np.cumsum(((rfr - vol ** 2 / 2) * dt +
                                 vol * np.sqrt(dt) * np.random.normal(size=(self.steps, self.num_path))), axis=0))

    def engine_price(self, spot, strike, rfr, time_to_maturity, vol) -> float:
        logger.info(
            f"MC method processing using the following parameters: "
            f"spot {spot}, rfr {rfr}, vol {vol}, time_to_maturity {time_to_maturity}, "
            f"strike {strike}, steps {self.steps} and num_path {self.num_path}")
        paths = self.paths(
            spot=spot, rfr=rfr, time_to_maturity=time_to_maturity, vol=vol
        )
        if ga.option_type == "Call":
            return np.mean(np.maximum(paths[-1] - strike, 0)) * np.exp(-rfr * time_to_maturity)
        else:
            return np.mean(np.maximum(strike - paths[-1], 0)) * np.exp(-rfr * time_to_maturity)


class BinomialTree:
    def __init__(self, steps):
        self.steps = steps

    def engine_price(self, spot, strike, rfr, time_to_maturity, vol) -> float:
        logger.info(
            f"BT method processing using the following parameters: "
            f"spot {spot}, rfr {rfr}, vol {vol}, time_to_maturity {time_to_maturity}, "
            f"strike {strike}, steps {self.steps}")
        dt = time_to_maturity / self.steps
        u, d = np.exp(vol * np.sqrt(dt)), np.exp(-vol * np.sqrt(dt))  # upward and downward movements
        p = (np.exp(rfr * dt) - d) / (u - d)  # risk neutral probability up
        payoff = np.zeros(self.steps + 1)  # creation of the payoffs table

        spot_diffusion = np.array([spot * u ** i * d ** (self.steps - i) for i in range(self.steps + 1)])
        payoff[:] = np.maximum(spot_diffusion - strike, 0) if ga.option_type == "Call" else np.maximum(strike - spot_diffusion, 0)

        for i in range(self.steps):
            payoff[:-1] = np.exp(-rfr * dt) * (p * payoff[1:] + (1 - p) * payoff[:-1])
            spot_diffusion = spot_diffusion * u
            # print(spot_diffusion)

        return np.maximum(payoff, spot_diffusion - strike)[0] if ga.option_type == "Call" else np.maximum(payoff, strike-spot_diffusion)[0]


