import numpy as np
import logging_config
import datetime
from scipy.stats import norm as norm
from abc import ABC, abstractmethod

logger = logging_config.logging.getLogger(__name__)


# 1) Implement classes below
# 2) Stick to Black Scholes
# 3) It should fail if you try to make an Option (must be call or put)
# 4) Use datetimes to define time (don't just use floats)
# 5) Use typing on all methods/functions
# 6) Include USEFUL logging

class Option(ABC):
    # Use abstract base class with this (do you need abstractmethod???)
    def __init__(self, strike, expiry_dt):
        logger.info(f"Created option at strike {strike} on expiry {expiry_dt}")
        self.strike = strike
        self.expiry_dt = expiry_dt

    @property
    @abstractmethod
    def option_type(self):
        pass

    @abstractmethod
    def price(self, spot, vol, rfr, pricing_dt) -> float:
        pass

    def time_to_maturity(self, pricing_dt) -> float:
        return (self.expiry_dt - pricing_dt).days / 365

    def d1(self, spot, rfr, vol, pricing_dt) -> float:
        logger.info(
            f"d1 computed with following parameters: spot {spot}, rfr {rfr}, vol {vol}, pricing_dt {pricing_dt}")
        return (
                (np.log(spot / self.strike) + (rfr + vol ** 2 / 2) * self.time_to_maturity(pricing_dt)) /
                (vol * np.sqrt(self.time_to_maturity(pricing_dt)))
        )

    def d2(self, spot, rfr, vol, pricing_dt) -> float:
        logger.info(
            f"d2 computed with following parameters: spot {spot}, rfr {rfr}, vol {vol}, pricing_dt {pricing_dt}")
        return self.d1(spot, rfr, vol, pricing_dt) - vol * np.sqrt(self.time_to_maturity(pricing_dt))

    def delta(self, spot, vol, rfr, bump_level, pricing_dt) -> float:
        logger.info(f"{self.option_type}Option.delta processing with the following information: "
                    f"spot {spot}, rfr {rfr}, vol {vol}, bump_level {bump_level}")
        spot_up, spot_dn = spot * (1 + bump_level), spot * (1 - bump_level)
        return (self.price(spot_up, vol, rfr, pricing_dt) - self.price(spot_dn, vol, rfr, pricing_dt)) / (
                    spot_up - spot_dn)


class PutOption(Option):
    @property
    def option_type(self):
        return "Put"

    def price(self, spot, vol, rfr, pricing_dt) -> float:
        logger.info(f"PutOption.price processing with the following information: spot {spot}, rfr {rfr}, vol {vol} and pricing_dt {pricing_dt}")
        d1, d2 = self.d1(spot, rfr, vol, pricing_dt), self.d2(spot, rfr, vol, pricing_dt)
        return norm.cdf(-d2) * self.strike * np.exp(-rfr * self.time_to_maturity(pricing_dt)) - norm.cdf(-d1) * spot


class CallOption(Option):
    @property
    def option_type(self):
        return "Call"

    def price(self, spot, vol, rfr, pricing_dt) -> float:
        logger.info(f"CallOption.price processing with the following information: spot {spot}, rfr {rfr}, vol {vol} and pricing_dt {pricing_dt}")
        d1, d2 = self.d1(spot, rfr, vol, pricing_dt), self.d2(spot, rfr, vol, pricing_dt)
        return norm.cdf(d1) * spot - norm.cdf(d2) * self.strike * np.exp(-rfr * self.time_to_maturity(pricing_dt))


def main():
    pricing_dt = datetime.date(2022, 10, 11)
    expiry_dt = datetime.date(2023, 10, 11)
    obj = PutOption(strike=100, expiry_dt=expiry_dt)
    obj2 = CallOption(strike=100, expiry_dt=expiry_dt)
    print(obj.price(spot=100, vol=0.2, rfr=0.05, pricing_dt=pricing_dt))
    print(obj.delta(spot=100, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt))
    print(obj2.price(spot=100, vol=0.2, rfr=0.05, pricing_dt=pricing_dt))
    print(obj2.delta(spot=100, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt))


if __name__ == "__main__":
    main()
