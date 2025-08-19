import uuid
from dataclasses import dataclass
import random
import abc
import queue
import threading
import time
from datetime import datetime, timedelta
from typing import Literal

CHECK_ORDER_DELAY = 2  # перевірка кожні 2 сек

OrderRequestBody = tuple[str, datetime]
DeliveryProvider = Literal["Uklon", "Uber"]
OrderDeliveryStatus = Literal["ongoing", "finished", "archived"]

storage = {
    "delivery": {},  # id: [provider, status, delivered_at]
    "users": [],
    "dishes": [
        {"id": 1, "name": "Salad", "value": 1099, "restaurant": "Silpo"},
        {"id": 2, "name": "Soda", "value": 199, "restaurant": "Silpo"},
        {"id": 3, "name": "Pizza", "value": 599, "restaurant": "Kvadrat"},
    ],
}


@dataclass
class DeliveryOrder:
    order_name: str
    number: uuid.UUID | None = None


class DeliveryService(abc.ABC):
    def __init__(self, order: DeliveryOrder):
        self._order: DeliveryOrder = order

    @abc.abstractmethod
    def ship(self) -> None:
        pass

    @classmethod
    def _process_delivery(cls) -> None:
        print("DELIVERY PROCESSING...")

        while True:
            filtered = {
                k: v for k, v in storage["delivery"].items()
                if v[1] in ("ongoing", "finished")
            }

            for order_id, value in filtered.items():
                provider, status, *delivered_at = value

                if status == "ongoing":
                    continue

                if status == "finished":
                    delivered_time = delivered_at[0] if delivered_at else None
                    if delivered_time and (datetime.now() - delivered_time).total_seconds() > 10:
                        storage["delivery"][order_id][1] = "archived"
                        print(f"\n\t📦 Order {order_id} ARCHIVED after 10s")

            time.sleep(CHECK_ORDER_DELAY)

    def _ship(self, delay: float):
        def _callback():
            time.sleep(delay)
            storage["delivery"][self._order.number] = (
                self.__class__.__name__, "finished", datetime.now()
            )
            print(f"🚚 DELIVERED {self._order}")

        thread = threading.Thread(target=_callback)
        thread.start()


class Uklon(DeliveryService):
    def ship(self) -> None:
        provider_name = self.__class__.__name__
        self._order.number = uuid.uuid4()
        storage["delivery"][self._order.number] = [provider_name, "ongoing", None]
        delay: float = random.randint(1, 3)
        print(f"\n\t🚚 {provider_name} Shipping {self._order} with {delay}s delay")
        self._ship(delay)


class Uber(DeliveryService):
    def ship(self) -> None:
        provider_name = self.__class__.__name__
        self._order.number = uuid.uuid4()
        storage["delivery"][self._order.number] = [provider_name, "ongoing", None]
        delay: float = random.randint(3, 5)
        print(f"\n\t🚚 {provider_name} Shipping {self._order} with {delay}s delay")
        self._ship(delay)


class Scheduler:
    def __init__(self):
        self.orders: queue.Queue[OrderRequestBody] = queue.Queue()

    @staticmethod
    def _service_dispatcher() -> type[DeliveryService]:
        random_provider: DeliveryProvider = random.choice(("Uklon", "Uber"))

        match random_provider:
            case "Uklon":
                return Uklon
            case "Uber":
                return Uber

    def ship_order(self, order_name: str) -> None:
        ConcreteDeliveryService: type[DeliveryService] = self._service_dispatcher()
        instance = ConcreteDeliveryService(order=DeliveryOrder(order_name=order_name))
        instance.ship()

    def add_order(self, order: OrderRequestBody) -> None:
        self.orders.put(order)
        print(f"\n\t{order[0]} ADDED FOR PROCESSING")

    def process_orders(self) -> None:
        print("ORDERS PROCESSING...")

        while True:
            order = self.orders.get(True)
            time_to_wait = order[1] - datetime.now()

            if time_to_wait.total_seconds() > 0:
                self.orders.put(order)
                time.sleep(0.5)
            else:
                self.ship_order(order[0])


def main():
    scheduler = Scheduler()

    process_orders_thread = threading.Thread(
        target=scheduler.process_orders, daemon=True
    )
    process_delivery_thread = threading.Thread(
        target=DeliveryService._process_delivery, daemon=True
    )

    process_orders_thread.start()
    process_delivery_thread.start()

    while True:
        order_details = input("Enter order details: ")
        data = order_details.split(" ")
        order_name = data[0]
        delay = datetime.now() + timedelta(seconds=int(data[1]))
        scheduler.add_order(order=(order_name, delay))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        raise SystemExit(0)
