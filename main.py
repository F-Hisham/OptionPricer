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
        self.strike = strike
        self.pricing_dt = pricing_dt
        self.expiry_dt = expiry_dt
        self.time_to_maturity = (expiry_dt-pricing_dt).days/365
        logger.info(f"Created option at strike {strike} on expiry {expiry_dt}")

    def d1d2(self, spot, rfr, vol) -> tuple:
        d1 = (np.log(spot / self.strike) + (rfr + vol ** 2 / 2) * self.time_to_maturity) / (
                vol * np.sqrt(self.time_to_maturity))
        d2 = d1 - vol * np.sqrt(self.time_to_maturity)
        return d1, d2

    @abstractmethod
    def price(self, spot, vol, rfr) -> float:
        time_to_maturity = self.expiry_dt - self.pricing_dt
        pass

    @abstractmethod
    def delta(self, spot, vol, rfr, bump_level) -> float:
        pass


class PutOption(Option):
    # No init and minial information needed
    def __init__(self, strike, pricing_dt, expiry_dt):
        super().__init__(strike, pricing_dt, expiry_dt)

    def price(self, spot, vol, rfr):
        d_param = self.d1d2(spot, rfr, vol)
        d1, d2 = d_param[0], d_param[1]
        return norm.cdf(-d2) * self.strike * np.exp(-rfr * self.time_to_maturity) - norm.cdf(-d1) * spot

    def delta(self, spot, vol, rfr, bump_level):
        # return self.d1d2(spot, rfr, vol)[0] - 1
        spot_up = spot * (1+bump_level)
        spot_dn = spot * (1-bump_level)
        return (self.price(spot_up, vol, rfr) - self.price(spot_dn, vol, rfr)) / (spot_up-spot_dn)

class CallOption(Option):
    # No init and minial information needed
    def __init__(self, strike, pricing_dt, expiry_dt):
        super().__init__(strike, pricing_dt, expiry_dt)

    def price(self, spot, vol, rfr):
        d_param = self.d1d2(spot, rfr, vol)
        d1, d2 = d_param[0], d_param[1]
        return norm.cdf(d1) * spot - norm.cdf(d2) * self.strike * np.exp(-rfr * self.time_to_maturity)

    def delta(self, spot, vol, rfr, bump_level):
        # return self.d1d2(spot, rfr, vol)[0]
        spot_up = spot * (1+bump_level)
        spot_dn = spot * (1-bump_level)
        return (self.price(spot_up, vol, rfr) - self.price(spot_dn, vol, rfr)) / (spot_up-spot_dn)

def main():
    obj = PutOption(strike=100, pricing_dt=datetime.date(2022, 10, 11), expiry_dt=datetime.date(2023, 10, 11))
    obj2 = CallOption(strike=100, pricing_dt=datetime.date(2022, 10, 11), expiry_dt=datetime.date(2023, 10, 11))
    print(obj.price(spot=100, vol=0.2, rfr=0.05))
    print(obj.delta(spot=100, vol=0.2, rfr=0.05, bump_level=0.01))
    print(obj2.price(spot=100, vol=0.2, rfr=0.05))
    print(obj2.delta(spot=100, vol=0.2, rfr=0.05, bump_level=0.01))

if __name__ == "__main__":
    main()
