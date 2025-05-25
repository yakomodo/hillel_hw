class Price:
    # Фіксовані курси обміну до CHF
    exchange_rates = {
        "USD": 0.91,  # 1 USD = 0.91 CHF
        "EUR": 0.98,  # 1 EUR = 0.98 CHF
        "CHF": 1.0,   # Базова валюта
    }

    def init(self, amount: float, currency: str):
        self.amount = amount
        self.currency = currency.upper()
        if self.currency not in self.exchange_rates:
            raise ValueError(f"Unsupported currency: {self.currency}")

    def to_chf(self) -> float:
        return self.amount * self.exchange_rates[self.currency]

    @classmethod
    def from_chf(cls, amount_chf: float, target_currency: str):
        target_currency = target_currency.upper()
        if target_currency not in cls.exchange_rates:
            raise ValueError(f"Unsupported currency: {target_currency}")
        return cls(amount_chf / cls.exchange_rates[target_currency], target_currency)

    def add(self, other):
        if not isinstance(other, Price):
            return NotImplemented
        amount_chf = self.to_chf() + other.to_chf()
        return Price.from_chf(amount_chf, self.currency)

    def sub(self, other):
        if not isinstance(other, Price):
            return NotImplemented
        amount_chf = self.to_chf() - other.to_chf()
        return Price.from_chf(amount_chf, self.currency)

    def str(self):
        return f"{self.amount:.2f} {self.currency}"

    def repr(self):
        return f"Price({self.amount:.2f}, '{self.currency}')"


# ───── Auth Decorator ─────
users = [
    {"username": "john", "password": "john123"},
    {"username": "admin", "password": "adminpass"},
]

_authenticated_user = None  # глобальна змінна для кешування


def auth(func):
    def wrapper(*args, **kwargs):
        global _authenticated_user

        if _authenticated_user:
            return func(*args, **kwargs)

        while True:
            username = input("Enter username: ")
            password = input("Enter password: ")

            for user in users:
                if user["username"] == username and user["password"] == password:
                    _authenticated_user = username
                    print(f"✅ Welcome, {username}!")
                    return func(*args, **kwargs)

            print("❌ Invalid credentials. Try again.")
    return wrapper


# ───── Command Function ─────
@auth
def command(payload):
    print(f"\n🟢 Executing command by authorized user.\nPayload: {payload}")


# ───── CLI ─────
if name == "main":
    print("💼 'exit' to quit \n")

    x = Price(100, "USD")
    y = Price(100, "EUR")
    print("Different currency add (USD + EUR):", x + y)
    print("Different currency sub (EUR - USD):", y - x)

    while user_input := input("\nType command payload: "):
        if user_input.lower() in ("exit", "quit"):
            break
        command(user_input)