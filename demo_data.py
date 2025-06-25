def get_sample_rates():
    # Matrix of direct rates between currencies (deliberately inconsistent for arbitrage)
    return {
        "USD": {"USD": 1.0, "EUR": 0.9, "GBP": 0.8},
        "EUR": {"USD": 1.12, "EUR": 1.0, "GBP": 0.89},
        "GBP": {"USD": 1.25, "EUR": 1.1, "GBP": 1.0},
    }