import requests

class ExchangeRateProvider:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_currency = "CHF"
        self.cache = {}

    def get_to_chf_rate(self, currency: str) -> float:
        currency = currency.upper()

        if currency == "CHF":
            return 1.0

        if currency in self.cache:
            return self.cache[currency]

        print(f"📡 Отримую курс {currency} до CHF з AlphaVantage...")

        url = f"https://www.alphavantage.co/query"
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": currency,
            "to_currency": self.base_currency,
            "apikey": self.api_key
        }

        response = requests.get(url, params=params)
        data = response.json()

        try:
            rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
            self.cache[currency] = rate
            return rate
        except (KeyError, ValueError):
            raise RuntimeError(f"❌ Не вдалося отримати курс для {currency} -> {self.base_currency}")

    def convert_to_chf(self, amount: float, currency: str) -> float:
        rate = self.get_to_chf_rate(currency)
        return amount * rate

    def convert_from_chf(self, amount_chf: float, target_currency: str) -> float:
        rate = self.get_to_chf_rate(target_currency)
        return amount_chf / rate


# ───── Клас Price ─────
class Price:
    def __init__(self, amount: float, currency: str, rate_provider: ExchangeRateProvider):
        self.amount = amount
        self.currency = currency.upper()
        self.rates = rate_provider

    def __add__(self, other):
        if not isinstance(other, Price):
            return NotImplemented

        self_chf = self.rates.convert_to_chf(self.amount, self.currency)
        other_chf = self.rates.convert_to_chf(other.amount, other.currency)

        result_chf = self_chf + other_chf
        result_amount = self.rates.convert_from_chf(result_chf, self.currency)

        return Price(result_amount, self.currency, self.rates)

    def __sub__(self, other):
        if not isinstance(other, Price):
            return NotImplemented

        self_chf = self.rates.convert_to_chf(self.amount, self.currency)
        other_chf = self.rates.convert_to_chf(other.amount, other.currency)

        result_chf = self_chf - other_chf
        result_amount = self.rates.convert_from_chf(result_chf, self.currency)

        return Price(result_amount, self.currency, self.rates)

    def __str__(self):
        return f"{self.amount:.2f} {self.currency}"

    def __repr__(self):
        return f"Price({self.amount:.2f}, '{self.currency}')"


if __name__ == "__main__":
    API_KEY = "03IIBLM637F8PK13"
    rate_provider = ExchangeRateProvider(API_KEY)

    print("💰 Демонстрація роботи з класом Price\n")

    p1 = Price(100, "USD", rate_provider)
    p2 = Price(200, "EUR", rate_provider)

    print(f"Ціна 1: {p1}")
    print(f"Ціна 2: {p2}")

    total = p1 + p2
    diff = p1 - p2

    print(f"\n📈 Сума (в валюті першого об'єкта): {total}")
    print(f"📉 Різниця (в валюті першого об'єкта): {diff}")