import Engine
import Options
import datetime


def main():
    # Creation of the attributes used as parameters
    pricing_dt = datetime.date(2022, 10, 11)
    expiry_dt = datetime.date(2023, 10, 11)
    # mc_engine = Engine.MonteCarlo(num_path=100000)
    # bs_engine = Engine.BlackScholes()
    bt_engine = Engine.BinomialTree(steps=10)

    # Creation of the objects
    # callbs = Options.CallOption(strike=100, expiry_dt=expiry_dt, engine=bs_engine)
    # putbs = Options.PutOption(strike=100, expiry_dt=expiry_dt, engine=bs_engine)
    # callmc = Options.CallOption(strike=100, expiry_dt=expiry_dt, engine=mc_engine)
    # putmc = Options.PutOption(strike=100, expiry_dt=expiry_dt, engine=mc_engine)
    callbt = Options.CallOption(strike=100, expiry_dt=expiry_dt, engine=bt_engine)
    putbt = Options.PutOption(strike=100, expiry_dt=expiry_dt, engine=bt_engine)

    # Call the methods
    # print(callbs.price(spot=100, vol=0.2, rfr=0.05, pricing_dt=pricing_dt))
    # print(callbs.delta(spot=100, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt))
    # print(putbs.price(spot=100, vol=0.2, rfr=0.05, pricing_dt=pricing_dt))
    # print(putbs.delta(spot=100, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt))
    # print(callmc.price(spot=100, vol=0.2, rfr=0.05, pricing_dt=pricing_dt))
    # print(callmc.delta(spot=100, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt))
    # print(putmc.price(spot=100, vol=0.2, rfr=0.05, pricing_dt=pricing_dt))
    # print(putmc.delta(spot=100, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt))
    print(callbt.price(spot=120, vol=0.2, rfr=0.05, pricing_dt=pricing_dt))
    print(callbt.delta(spot=120, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt))
    print(putbt.price(spot=120, vol=0.2, rfr=0.05, pricing_dt=pricing_dt))
    print(putbt.delta(spot=120, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt))

if __name__ == "__main__":
    main()
