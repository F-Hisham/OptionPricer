import datetime
from PricerModule import engine, options
import globalattributes as ga


def main():
    # Creation of the attributes used as parameters
    pricing_dt = datetime.date(2022, 10, 11)
    expiry_dt = datetime.date(2023, 10, 11)

# ------------------BS
    # Call
    # Instantiate Black and Scholes object and initialisate the global attributes (engine, option type and number of steps if necessary)
    callbs = options.CallBS(strike=100, expiry_dt=expiry_dt)
    callbs.pricing_type()  # init global attributes. Better way to do?

    # call price and delta functions from the parent (Options) class
    print(f'call bs price is {callbs.price(spot=120, vol=0.2, rfr=0.05, pricing_dt=pricing_dt)}')
    print(f'call bs delta is {callbs.delta(spot=120, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt)}')

    # Put
    putbs = options.PutBS(strike=100, expiry_dt=expiry_dt)
    putbs.pricing_type()
    print(f'put bs price is {putbs.price(spot=120, vol=0.2, rfr=0.05, pricing_dt=pricing_dt)}')
    print(f'put bs delta is {putbs.delta(spot=120, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt)}')

# ------------------MC
    # Call
    callmc = options.CallMC(strike=100, expiry_dt=expiry_dt)
    callmc.pricing_type(path_steps=10000)
    print(f'call mc price is {callmc.price(spot=120, vol=0.2, rfr=0.05, pricing_dt=pricing_dt)}')
    print(f'call mc delta is {callmc.delta(spot=120, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt)}')

    # Put
    putmc = options.PutMC(strike=100, expiry_dt=expiry_dt)
    putmc.pricing_type(path_steps=10000)
    print(f'put mc price is {putmc.price(spot=120, vol=0.2, rfr=0.05, pricing_dt=pricing_dt)}')
    print(f'put mc delta is {putmc.delta(spot=120, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt)}')


# ------------------BT
    # Call
    callbt = options.CallMC(strike=100, expiry_dt=expiry_dt)
    callbt.pricing_type(path_steps=100)
    print(f'call bt price is {callbt.price(spot=120, vol=0.2, rfr=0.05, pricing_dt=pricing_dt)}')
    print(f'call bt delta is {callbt.delta(spot=120, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt)}')

    # Put
    putbt = options.PutMC(strike=100, expiry_dt=expiry_dt)
    putbt.pricing_type(path_steps=100)
    print(f'put bt price is {putbt.price(spot=120, vol=0.2, rfr=0.05, pricing_dt=pricing_dt)}')
    print(f'put bt delta is {putbt.delta(spot=120, vol=0.2, rfr=0.05, bump_level=0.01, pricing_dt=pricing_dt)}')

if __name__ == "__main__":
    main()
