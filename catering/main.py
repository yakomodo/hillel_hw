from datetime import datetime, timedelta
import queue
import threading
import time
import random

OrderRequestBody = tuple[str, datetime]

storage = {
    "users": [],
    "dishes": [
        {"id": 1, "name": "Salad", "value": 1099, "restaurant": "Silpo"},
        {"id": 2, "name": "Soda", "value": 199, "restaurant": "Silpo"},
        {"id": 3, "name": "Pizza", "value": 599, "restaurant": "Kvadrat"},
    ],
    "delivery_providers": ["uklon", "uber"]
}


class Scheduler:
    def __init__(self, delivery_queue: queue.Queue):
        self.orders: queue.Queue[OrderRequestBody] = queue.Queue()
        self.delivery_queue = delivery_queue

    def process_orders(self) -> None:
        print("SCHEDULER PROCESSING...")
        while True:
            order = self.orders.get(True)
            time_to_wait = order[1] - datetime.now()
            if time_to_wait.total_seconds() > 0:
                self.orders.put(order)
                time.sleep(0.5)
            else:
                print(f"\n\t{order[0]} READY FOR DELIVERY")
                # додати у чергу доставки
                self.delivery_queue.put(order)


    def add_order(self, order: OrderRequestBody) -> None:
        self.orders.put(order)
        print(f"\n\t{order[0]} ADDED FOR PROCESSING")


class DeliveryHandler:
    def __init__(self):
        self.delivery_queue: queue.Queue[OrderRequestBody] = queue.Queue()

    def process_deliveries(self) -> None:
        print("DELIVERY HANDLER PROCESSING...")
        while True:
            order = self.delivery_queue.get(True)
            provider = random.choice(storage["delivery_providers"])
            print(f"\n\t{order[0]} PICKED UP BY {provider.upper()}")

            if provider == "uklon":
                time.sleep(5)
            elif provider == "uber":
                time.sleep(3)

            print(f"\n\t{order[0]} DELIVERED BY {provider.upper()}")


def main():
    delivery_handler = DeliveryHandler()
    scheduler = Scheduler(delivery_handler.delivery_queue)

    scheduler_thread = threading.Thread(target=scheduler.process_orders, daemon=True)
    delivery_thread = threading.Thread(target=delivery_handler.process_deliveries, daemon=True)

    scheduler_thread.start()
    delivery_thread.start()

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
