from fetcher import get_rates
from graph import build_graph, find_arbitrage_cycle
import os

def main():
    API_KEY = input("Enter your ExchangeRate-API key: ").strip()

    print(API_KEY)

###################


    base_currency = "USD"
    print(f"Fetching rates from base: {base_currency}...")
    rates = get_rates(API_KEY, base_currency)

    EXCLUDED_CURRENCIES = {"ARS", "LYD", "SSP", "SYP", "VES", "YER", "ZWL"}
    rates = {k: v for k, v in rates.items() if k not in EXCLUDED_CURRENCIES}

    if not rates:
        print("Failed to fetch rates. Exiting.")
        return

    print("Building graph...")
    graph = build_graph(rates)

    print("Searching for arbitrage opportunities...")
    cycle = find_arbitrage_cycle(graph, base_currency)

    if cycle:
        print("Arbitrage cycle found:")
        print(" → ".join(cycle + [cycle[0]]))
    else:
        print("No arbitrage opportunity found.")

if __name__ == "__main__":
    main()
