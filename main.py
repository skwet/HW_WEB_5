import aiohttp
import asyncio
import json
from datetime import datetime, timedelta
import platform
import sys

url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='

class PBAPI:
    async def fetch_url(self, url, date):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f'{url}{date}') as response:
                    return await response.json()
            except aiohttp.ClientConnectionError as err:
                print(f'Сталася помилка: {err}')

    async def all_currency_rates(self, url, days):
        tasks = []
        
        for day in range(days):
            date = (datetime.today() - timedelta(days=day)).strftime('%d.%m.%Y')
            task = self.fetch_url(url, date)
            tasks.append(task)
        
        return await asyncio.gather(*tasks)

class CurrencyConverter:
    def __init__(self, data):
        self.data = data

    def convert_to_dict(self):
        currencies = {}
        
        for rate in self.data['exchangeRate']:
            if rate['currency'] in ['USD', 'EUR']:
                currencies[rate['currency']] = {
                    'sale': rate['saleRate'],
                    'purchase': rate['purchaseRate']
                }
        
        return currencies

async def main():
    try:
        days = int(sys.argv[1])

        if days > 10:
            print("Дані можна отримати лише протягом 10 днів!")
            return

        fetcher = PBAPI()
        currency_data = await fetcher.all_currency_rates(url, days)

        result = []
        for response in currency_data:
            converter = CurrencyConverter(response)
            currency_dict = converter.convert_to_dict()
            date = response['date']
            result.append({date: currency_dict})

        print(result)
    except ValueError:
        print('Введіть число,не букви!')
    except IndexError:
        print('Ви забули ввести число!')

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())




