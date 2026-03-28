"""
api_service.py — Fetches live currency exchange rates
using the free Frankfurter API (no API key needed).
Used for multi-currency payroll/invoice reporting.
"""

import requests

FRANKFURTER_BASE = "https://api.frankfurter.app"

def get_exchange_rates(base_currency: str = "USD") -> dict:
    """
    Fetch latest exchange rates relative to a base currency.
    Returns a dict of { currency_code: rate } or error info.
    """
    try:
        url = f"{FRANKFURTER_BASE}/latest?from={base_currency}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            "base": data["base"],
            "date": data["date"],
            "rates": data["rates"]
        }
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please try again."}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e}"}
    except Exception as e:
        return {"error": str(e)}

def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """Convert an amount from one currency to another."""
    try:
        url = f"{FRANKFURTER_BASE}/latest?amount={amount}&from={from_currency}&to={to_currency}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        converted = data["rates"].get(to_currency)
        return {
            "from": from_currency,
            "to": to_currency,
            "original_amount": amount,
            "converted_amount": converted,
            "date": data["date"]
        }
    except Exception as e:
        return {"error": str(e)}
