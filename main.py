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




# import aiohttp
# import asyncio
# import argparse
# from datetime import datetime, timedelta

# class PrivatBankAPI:
#     async def fetch_currency(self, session, date):
#         async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}') as response:
#             return await response.json()

# class CurrencyConverter:
#     def __init__(self, data):
#         self.data = data

#     def convert_to_dict(self):
#         return {
#             'EUR': {
#                 'sale': self.data['exchangeRate'][0]['saleRateNB'],
#                 'purchase': self.data['exchangeRate'][0]['purchaseRateNB']
#             },
#             'USD': {
#                 'sale': self.data['exchangeRate'][1]['saleRateNB'],
#                 'purchase': self.data['exchangeRate'][1]['purchaseRateNB']
#             }
#         }

# class CurrencyRateFetcher:
#     def __init__(self, api):
#         self.api = api

#     async def get_currency_rates(self, days):
#         async with aiohttp.ClientSession() as session:
#             tasks = []
#             for i in range(days):
#                 date = (datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y')
#                 task = self.api.fetch_currency(session, date)
#                 tasks.append(task)
#             responses = await asyncio.gather(*tasks)
#             return responses

# async def main(days):
#     if days > 10:
#         print("Error: Cannot fetch rates for more than 10 days.")
#         return

#     api = PrivatBankAPI()
#     fetcher = CurrencyRateFetcher(api)
#     currency_responses = await fetcher.get_currency_rates(days)

#     currency_rates = []
#     for response in currency_responses:
#         converter = CurrencyConverter(response)
#         currency_rates.append(converter.convert_to_dict())

#     print(currency_rates)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Get currency rates from PrivatBank API.")
#     parser.add_argument("days", type=int, help="Number of days to fetch currency rates")
#     args = parser.parse_args()

#     asyncio.run(main(args.days))

