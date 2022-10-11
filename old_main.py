import option_pricer

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    obj = option_pricer.OptionPricer(100, 105, 0.05, 1, 0.01)
    print(obj.black_scholes(True))
    print(obj.monte_carlo(True, 100, 10000))
