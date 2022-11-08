import logging_config
from abc import ABC, abstractmethod
import PricerModule.engine as engine
from constants import OptionTypes

logger = logging_config.logging.getLogger(__name__)


class Option(ABC):
    # Use abstract base class with this (do you need abstractmethod???)
    def __init__(self, strike, expiry_dt, **kwargs):
        logger.info(f"Created option at strike {strike} on expiry {expiry_dt}")
        self.strike = strike
        self.expiry_dt = expiry_dt
        self.option_type = kwargs["option_type"]
        self.engine = kwargs["engine"]

    def price(self, spot, vol, rfr, pricing_dt) -> float:
        return self.engine.engine_price(
            spot=spot, vol=vol, rfr=rfr,
            time_to_maturity=self.time_to_maturity(pricing_dt=pricing_dt), strike=self.strike,
            option_type=self.option_type
        )

    def time_to_maturity(self, pricing_dt) -> float:
        return (self.expiry_dt - pricing_dt).days / 365

    def delta(self, spot, vol, rfr, bump_level, pricing_dt) -> float:
        logger.info(f"{self.option_type}Option.delta processing with the following information: "
                    f"spot {spot}, rfr {rfr}, vol {vol}, bump_level {bump_level}")
        spot_up, spot_dn = spot * (1 + bump_level), spot * (1 - bump_level)
        return (self.price(spot_up, vol, rfr, pricing_dt) - self.price(spot_dn, vol, rfr, pricing_dt)) / (
                spot_up - spot_dn)


class EuropeanBS(Option):
    def __init__(self, **kwargs):
        kwargs["engine"] = engine.BlackScholes()
        kwargs["option_type"] = kwargs["option_type"]
        super().__init__(**kwargs)


class EuropeanMC(Option):
    def __init__(self, **kwargs):
        kwargs["engine"] = engine.MonteCarlo(steps=kwargs["steps"], num_path=kwargs["num_path"])
        kwargs["option_type"] = kwargs["option_type"]
        super().__init__(**kwargs)


class American(Option):
    def __init__(self, **kwargs):
        kwargs["engine"] = engine.BinomialTree(steps=kwargs["steps"])
        kwargs["option_type"] = kwargs["option_type"]
        super().__init__(**kwargs)
