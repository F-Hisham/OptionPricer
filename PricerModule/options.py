import globalattributes
import logging_config
from abc import ABC, abstractmethod
import PricerModule.engine as engine
import globalattributes as ga
from numpy import sqrt

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


class CallBS(Option):
    def pricing_type(self):
        ga.option_type = 'Call'
        ga.engine = engine.BlackScholes()


class PutBS(Option):
    def pricing_type(self):
        ga.option_type = 'Put'
        ga.engine = engine.BlackScholes()


class CallMC(Option):
    def pricing_type(self, path_steps:int):
        ga.option_type = 'Call'
        ga.path_steps = path_steps
        ga.engine = engine.MonteCarlo(num_path=ga.path_steps)


class PutMC(Option):
    def pricing_type(self, path_steps:int):
        ga.option_type = 'Put'
        ga.path_steps = path_steps
        ga.engine = engine.MonteCarlo(num_path=ga.path_steps)


class CallBT(Option):
    def pricing_type(self, path_steps:int):
        ga.option_type = 'Call'
        ga.path_steps = path_steps
        ga.engine = engine.engine.BinomialTree(steps=ga.path_steps)


class PutBT(Option):
    def pricing_type(self, path_steps:int):
        ga.option_type = 'Put'
        ga.path_steps = path_steps
        ga.engine = engine.engine.BinomialTree(steps=ga.path_steps)
