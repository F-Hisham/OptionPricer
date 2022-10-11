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
    def __init__(self, strike, pricing_dt, expiry_dt):
        logger.info(f"Created option at strike {strike} on expiry {expiry_dt}")
        self.strike = strike
        self.pricing_dt = pricing_dt
        self.expiry_dt = expiry_dt
        self.time_to_maturity = (expiry_dt - pricing_dt).days / 365

    def d1d2(self, spot, rfr, vol) -> tuple:
        logger.info(f"d1 and d2 computed with following parameters: spot {spot}, rfr {rfr} and vol {vol}")
        d1 = (
                (np.log(spot / self.strike) + (rfr + vol ** 2 / 2) * self.time_to_maturity) /
                (vol * np.sqrt(self.time_to_maturity))
              )
        d2 = d1 - vol * np.sqrt(self.time_to_maturity)
        return d1, d2

    def delta(self, spot, vol, rfr, bump_level) -> float:
        logger.info(f"Option's delta processing with the following information: "
                    f"spot {spot}, rfr {rfr}, vol {vol}, bump_level {bump_level}")
        spot_up, spot_dn = spot * (1 + bump_level), spot * (1 - bump_level)
        return (self.price(spot_up, vol, rfr) - self.price(spot_dn, vol, rfr)) / (spot_up - spot_dn)

    @abstractmethod
    def price(self, spot, vol, rfr) -> float:
        pass


class PutOption(Option):
    # No init and minial information needed
    def __init__(self, strike, pricing_dt, expiry_dt):
        logger.info(f"PutOption class created: strike {strike}, pricing_dt {pricing_dt}, expiry_dt {expiry_dt}")
        super().__init__(strike, pricing_dt, expiry_dt)

    def price(self, spot, vol, rfr) -> float:
        logger.info(f"PutOption.price processing with the following information: spot {spot}, rfr {rfr}, vol {vol}")
        d1, d2 = self.d1d2(spot, rfr, vol)
        return norm.cdf(-d2) * self.strike * np.exp(-rfr * self.time_to_maturity) - norm.cdf(-d1) * spot

    def delta(self, spot, vol, rfr, bump_level) -> float:
        logger.info(f"PutOption.delta processing with the following information: "
                    f"spot {spot}, rfr {rfr}, vol {vol} and bump_leve {bump_level}")
        return super().delta(spot, vol, rfr, bump_level)  # calling the delta function of the mother class


class CallOption(Option):
    # No init and minial information needed
    def __init__(self, strike, pricing_dt, expiry_dt):
        logger.info(f"CallOption class created: strike {strike}, pricing_dt {pricing_dt}, expiry_dt {expiry_dt}")
        super().__init__(strike, pricing_dt, expiry_dt)

    def price(self, spot, vol, rfr) -> float:
        logger.info(f"CallOption.price processing with the following information: spot {spot}, rfr {rfr}, vol {vol}")
        d1, d2 = self.d1d2(spot, rfr, vol)
        return norm.cdf(d1) * spot - norm.cdf(d2) * self.strike * np.exp(-rfr * self.time_to_maturity)

    def delta(self, spot, vol, rfr, bump_level) -> float:
        logger.info(f"CallOption.delta processing with the following information: "
                    f"spot {spot}, rfr {rfr}, vol {vol} and bump_leve {bump_level}")
        # return self.d1d2(spot, rfr, vol)[0]
        return super().delta(spot, vol, rfr, bump_level)  # calling the delta function of the mother class


def main():
    obj = PutOption(strike=100, pricing_dt=datetime.date(2022, 10, 11), expiry_dt=datetime.date(2023, 10, 11))
    obj2 = CallOption(strike=100, pricing_dt=datetime.date(2022, 10, 11), expiry_dt=datetime.date(2023, 10, 11))
    print(obj.price(spot=100, vol=0.2, rfr=0.05))
    print(obj.delta(spot=100, vol=0.2, rfr=0.05, bump_level=0.01))
    print(obj2.price(spot=100, vol=0.2, rfr=0.05))
    print(obj2.delta(spot=100, vol=0.2, rfr=0.05, bump_level=0.01))


if __name__ == "__main__":
    main()
