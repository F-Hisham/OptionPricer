import datetime
from PricerModule import engine, options
import globalattributes as ga


def main():
    # Creation of the attributes used as parameters
    pricing_dt = datetime.date(2022, 10, 11)
    expiry_dt = datetime.date(2023, 10, 11)

    # ga.path_steps = 100
    callbs = options.CallBS(strike=100, expiry_dt=expiry_dt)
    print(callbs.price(spot=120, vol=0.2, rfr=0.05, pricing_dt=pricing_dt))
    print(callbs.delta(spot=100, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt))


if __name__ == "__main__":
    main()
