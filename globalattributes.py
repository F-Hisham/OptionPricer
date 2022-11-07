from dataclasses import dataclass
from PricerModule import engine


@dataclass
class GlobalAttributes:
    option_type: str
    engine: engine

