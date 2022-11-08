import datetime
from PricerModule import engine, options


def main():
    pricing_dt = datetime.date(2022, 10, 11)
    expiry_dt = datetime.date(2023, 10, 11)

    bs = options.EuropeanBS(strike=100, expiry_dt=expiry_dt, option_type="Call")
    mc = options.EuropeanMC(strike=100, expiry_dt=expiry_dt, option_type="Call", steps=100, num_path=100000)
    amr = options.American(strike=100, expiry_dt=expiry_dt, option_type="Call", steps=100)

    print(f'call bs price is {bs.price(spot=90, vol=0.2, rfr=0.05, pricing_dt=pricing_dt)}')
    print(f'call bs delta is {bs.delta(spot=90, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt)}')
    print(f'call mc price is {mc.price(spot=90, vol=0.2, rfr=0.05, pricing_dt=pricing_dt)}')
    print(f'call mc delta is {mc.delta(spot=90, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt)}')
    print(f'call amr price is {amr.price(spot=90, vol=0.2, rfr=0.05, pricing_dt=pricing_dt)}')
    print(f'call amr delta is {amr.delta(spot=90, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt)}')


if __name__ == "__main__":
    main()
