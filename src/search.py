from typing import List, Dict, Optional
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import Tool
import requests

class CryptoSearch:
    def __init__(self):
        self.news_api_url = "https://min-api.cryptocompare.com/data/v2/news/"
        self.price_api_url = "https://min-api.cryptocompare.com/data/pricemultifull"

    def get_crypto_news(self, coin: Optional[str] = None) -> str:
        """Get latest cryptocurrency news."""
        try:
            params = {}
            if coin:
                params['categories'] = coin.lower()
            
            response = requests.get(self.news_api_url, params=params)
            response.raise_for_status()
            
            news_data = response.json()
            if news_data.get('Data'):
                news_items = news_data['Data'][:5]  # Get top 5 news items
                formatted_news = []
                for item in news_items:
                    formatted_news.append(f"- {item['title']}\n  Source: {item['source']}")
                return "\n".join(formatted_news)
            return "No news found."
            
        except Exception as e:
            return f"Error fetching crypto news: {str(e)}"

    def get_crypto_price(self, __arg1: str) -> str:
        """Get current price data for specified cryptocurrencies."""
        try:
            coins = __arg1
            coin_list = [c.strip().upper() for c in [coins]] # Single coin for now
            fsyms = ','.join(coin_list)
            
            params = {
                'fsyms': fsyms,
                'tsyms': 'USD'
            }
            
            response = requests.get(self.price_api_url, params=params)
            response.raise_for_status()
            
            price_data = response.json()
            if price_data.get('RAW'):
                results = []
                for coin in coin_list:
                    if coin in price_data['RAW']:
                        data = price_data['RAW'][coin]['USD']
                        results.append(
                            f"{coin}/USD:"
                            f"\n  Price: ${data['PRICE']:,.2f}"
                            f"\n  24h Change: {data['CHANGEPCT24HOUR']:.2f}%"
                            f"\n  24h Volume: ${data['VOLUME24HOUR']:,.2f}"
                        )
                return "\n".join(results)
            return "No price data found."
            
        except Exception as e:
            return f"Error fetching crypto prices: {str(e)}"

def get_crypto_tools() -> List[Tool]:
    """Get list of crypto-related tools."""
    search = CryptoSearch()
    
    return [
        Tool(
            name="crypto_news",
            description="Get latest cryptocurrency news. Optionally specify a coin name.",
            func=search.get_crypto_news,
        ),
        Tool(
            name="crypto_price",
            description="Get current price data for cryptocurrencies. Input should be comma-separated coin symbols (e.g., 'BTC,ETH')",
            func=search.get_crypto_price,
        ),
    ]
