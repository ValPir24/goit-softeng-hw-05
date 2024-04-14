import asyncio
import aiohttp
from datetime import datetime, timedelta


class CurrencyRates:
    def __init__(self):
        self.base_url = 'https://api.privatbank.ua/p24api/exchange_rates'
        self.headers = {'Content-Type': 'application/json'}

    async def fetch_currency_rate(self, date: str):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(f'{self.base_url}?json&date={date}') as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    return None

    async def get_currency_rates(self, days: int):
        currency_rates = []
        today = datetime.now()
        for i in range(days):
            date = (today - timedelta(days=i)).strftime('%d.%m.%Y')
            data = await self.fetch_currency_rate(date)
            if data:
                rates = {}
                for currency in data['exchangeRate']:
                    if currency['currency'] in ['EUR', 'USD']:
                        rates[currency['currency']] = {'sale': currency['saleRate'], 'purchase': currency['purchaseRate']}
                currency_rates.append({date: rates})
        return currency_rates


async def main(days: int):
    currency_rates = CurrencyRates()
    rates = await currency_rates.get_currency_rates(days)
    return rates


if __name__ == '__main__':
    import sys
    import json

    if len(sys.argv) != 2:
        print("Usage: python main.py <days>")
        sys.exit(1)

    try:
        days = int(sys.argv[1])
    except ValueError:
        print("Number of days must be an integer")
        sys.exit(1)

    if days > 10:
        print("Number of days cannot exceed 10")
        sys.exit(1)

    result = asyncio.run(main(days))
    print(json.dumps(result, indent=2))
