from dataclasses import dataclass
from PricerModule import engine


@dataclass
class OptionTypes:
    put = "Put"
    call = "Call"

