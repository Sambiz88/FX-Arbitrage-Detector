import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Loads .env file with API_KEY




def get_rates(API_KEY, base_currency="USD"):
    """
    Fetch exchange rates from ExchangeRate-API for a given base currency.

    Returns:
        dict: A mapping of currency codes to exchange rates.
    """
    BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"
    
    url = BASE_URL + base_currency
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("result") != "success":
            raise ValueError(f"API error: {data.get('error-type', 'Unknown error')}")

        return data["conversion_rates"]  # dict of {currency: rate}
    
    except requests.RequestException as e:
        print(f"[ERROR] Network or HTTP error: {e}")
        return {}
    except Exception as e:
        print(f"[ERROR] Failed to fetch rates: {e}")
        return {}
