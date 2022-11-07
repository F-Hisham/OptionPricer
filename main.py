import datetime
from PricerModule import engine, options


def main():
    # Creation of the attributes used as parameters
    pricing_dt = datetime.date(2022, 10, 11)
    expiry_dt = datetime.date(2023, 10, 11)

    eur = options.EuropeanBS(strike=100, expiry_dt=expiry_dt)
    eur.pricing_type(call_or_put='Call')  # init global attributes. Better way to do?
    print(f'call bs price is {eur.price(spot=120, vol=0.2, rfr=0.05, pricing_dt=pricing_dt)}')
    print(f'call bs delta is {eur.delta(spot=120, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt)}')

    eur = options.EuropeanMC(strike=100, expiry_dt=expiry_dt)
    eur.pricing_type(call_or_put='Call')  # init global attributes. Better way to do?
    print(f'call mc price is {eur.price(spot=120, vol=0.2, rfr=0.05, pricing_dt=pricing_dt)}')
    print(f'call mc delta is {eur.delta(spot=120, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt)}')

    eur = options.EuropeanMC(strike=100, expiry_dt=expiry_dt)
    eur.pricing_type(call_or_put='Call')  # init global attributes. Better way to do?
    print(f'call amer price is {eur.price(spot=120, vol=0.2, rfr=0.05, pricing_dt=pricing_dt)}')
    print(f'call amer delta is {eur.delta(spot=120, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt)}')


if __name__ == "__main__":
    main()
