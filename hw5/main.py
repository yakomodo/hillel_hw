# ───── Price Class ─────
class Price:
    def __init__(self, amount: float, currency: str):
        self.amount = amount
        self.currency = currency.upper()

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot add prices with different currencies")
        return Price(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot subtract prices with different currencies")
        return Price(self.amount - other.amount, self.currency)

    def __str__(self):
        return f"{self.amount} {self.currency}"

    def __repr__(self):
        return f"Price({self.amount}, '{self.currency}')"


# ───── Auth Decorator ─────
users = [
    {"username": "john", "password": "john123"},
    {"username": "admin", "password": "adminpass"},
]

_authenticated_user = None  # глобальна змінна для кешування


def auth(func):
    def wrapper(*args, **kwargs):
        global _authenticated_user

        # Якщо вже авторизований, не питаємо ще раз
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
if __name__ == "__main__":
    print("💼 HW5 Console (type 'exit' to quit)\n")

    # Тест Price
    a = Price(100, "USD")
    b = Price(150, "USD")
    print("Example Price Add:", a + b)
    print("Example Price Sub:", b - a)

    # Тест auth
    while user_input := input("\nType command payload: "):
        if user_input.lower() in ("exit", "quit"):
            break
        command(user_input)