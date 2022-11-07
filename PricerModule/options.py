import logging_config
from abc import ABC, abstractmethod
import PricerModule.engine as engine
import globalattributes as ga

logger = logging_config.logging.getLogger(__name__)


class Option(ABC):
    # Use abstract base class with this (do you need abstractmethod???)
    def __init__(self, strike, expiry_dt):
        logger.info(f"Created option at strike {strike} on expiry {expiry_dt}")
        self.strike = strike
        self.expiry_dt = expiry_dt

    @abstractmethod
    def pricing_type(self):
        pass

    def price(self, spot, vol, rfr, pricing_dt) -> float:
        return ga.engine.engine_price(
            spot=spot, vol=vol, rfr=rfr,
            time_to_maturity=self.time_to_maturity(pricing_dt=pricing_dt), strike=self.strike
        )

    def time_to_maturity(self, pricing_dt) -> float:
        return (self.expiry_dt - pricing_dt).days / 365

    def delta(self, spot, vol, rfr, bump_level, pricing_dt) -> float:
        logger.info(f"{ga.option_type}Option.delta processing with the following information: "
                    f"spot {spot}, rfr {rfr}, vol {vol}, bump_level {bump_level}")
        spot_up, spot_dn = spot * (1 + bump_level), spot * (1 - bump_level)
        return (self.price(spot_up, vol, rfr, pricing_dt) - self.price(spot_dn, vol, rfr, pricing_dt)) / (
                spot_up - spot_dn)


class EuropeanBS(Option):
    def pricing_type(self, call_or_put):
        ga.option_type = call_or_put
        ga.engine = engine.BlackScholes()


class EuropeanMC(Option):
    def pricing_type(self, call_or_put, steps=100, num_path=1000):
        ga.option_type = call_or_put
        ga.engine = engine.MonteCarlo(steps=steps, num_path=num_path)


class American(Option):
    def pricing_type(self, call_or_put, steps=100):
        ga.option_type = call_or_put
        ga.engine = engine.BinomialTree(steps=steps)
