import requests
import logging
from config import Config
from datetime import datetime

logger = logging.getLogger(__name__)

class CurrencyAPI:
    """Handle currency exchange rate API calls"""
    
    def __init__(self):
        self.base_url = Config.CURRENCY_API_URL
        self.cache = {}
        self.cache_time = {}
        self.cache_duration = 3600  # 1 hour in seconds
    
    def get_exchange_rates(self, base_currency: str = 'USD') -> dict:
        """
        Fetch exchange rates for a given base currency
        
        Args:
            base_currency: Base currency code (default: USD)
        
        Returns:
            dict: Exchange rates or empty dict on failure
        """
        try:
            url = f"{self.base_url}/{base_currency}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"✓ Fetched exchange rates for {base_currency}")
            return data.get('rates', {})
        
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Failed to fetch exchange rates: {str(e)}")
            return {}
    
    def convert_currency(self, amount: float, from_currency: str, 
                        to_currency: str) -> float:
        """
        Convert amount from one currency to another
        
        Args:
            amount: Amount to convert
            from_currency: Source currency code
            to_currency: Target currency code
        
        Returns:
            float: Converted amount
        """
        try:
            rates = self.get_exchange_rates(from_currency)
            if to_currency in rates:
                return amount * rates[to_currency]
            else:
                logger.warning(f"Currency {to_currency} not found in rates")
                return amount
        
        except Exception as e:
            logger.error(f"Conversion failed: {str(e)}")
            return amount
    
    def get_supported_currencies(self) -> list:
        """Get list of supported currencies"""
        try:
            rates = self.get_exchange_rates('USD')
            return sorted(list(rates.keys()))
        except Exception as e:
            logger.error(f"Failed to get supported currencies: {str(e)}")
            return []

currency_api = CurrencyAPI()

def get_currency_api():
    """Get currency API instance"""
    return currency_api
