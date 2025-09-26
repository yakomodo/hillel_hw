from dataclasses import dataclass
from datetime import date
import psycopg

connection_payload = {
    "dbname": "catering",
    "user": "kulinich",
    "password": "pass0327",
    "host": "localhost",
    "port": 5432,
}


class DatabaseConnection:
    def __enter__(self):
        self.conn = psycopg.connect(**connection_payload)
        self.cur = self.conn.cursor()

        return self

    def __exit__(self, exc_type, *_):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()

        self.cur.close()
        self.conn.close()

    def query(self, sql: str, params: tuple | None = None):
        self.cur.execute(sql, params or ())
        return self.cur.fetchall()


@dataclass
class User:
    name: str
    phone: str
    role: str
    id: int | None = None

    @classmethod
    def all(cls) -> list["User"]:
        """return all the users from `users` table."""

        with DatabaseConnection() as db:
            rows = db.query("SELECT name, phone, role, id FROM users")
            return [cls(*row) for row in rows]

    @classmethod
    def filter(cls, **filters) -> list["User"]:
        """return filtered users from `users` table."""

        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            rows = db.query(
                f"SELECT name, phone, role, id FROM users WHERE {conditions}",
                values,
            )
            return [cls(*row) for row in rows]

    def create(self) -> "User":
        with DatabaseConnection() as db:
            db.cur.execute(
                "INSERT INTO users (name, phone, role) VALUES (%s, %s, %s) RETURNING id",
                (self.name, self.phone, self.role),
            )
            # NOTE: actually bad practice to mutate `self` instance from here

            self.id = db.cur.fetchone()[0]

            return self

    def update(self, **payload) -> "User | None":
        fields = ", ".join([f"{key} = %s" for key in payload])
        values = tuple(payload.values())

        # ensure id exists
        if self.id is None:
            raise ValueError("Can not update user without ID")

        with DatabaseConnection() as db:
            db.cur.execute(
                f"UPDATE users SET {fields} WHERE id = %s RETURNING id, name, phone, role",
                (*values, self.id),
            )

            row = db.cur.fetchone()

        if not row:
            return None
        else:
            _, name, phone, role = row
            self.name = name
            self.phone = phone
            self.role = role

            return self

    @classmethod
    def delete_by_filters(cls, **filters) -> bool:
        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            db.cur.execute(f"DELETE FROM users WHERE {conditions}", values)
            return True


@dataclass
class Dish:
    name: str
    price: float
    id: int | None = None

    @classmethod
    def all(cls) -> list["Dish"]:
        with DatabaseConnection() as db:
            rows = db.query("SELECT name, price, id FROM dishes")
            return [cls(*row) for row in rows]

    @classmethod
    def filter(cls, **filters) -> list["Dish"]:
        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            rows = db.query(
                f"SELECT name, price, id FROM dishes WHERE {conditions}",
                values,
            )
            return [cls(*row) for row in rows]

    def create(self) -> "Dish":
        with DatabaseConnection() as db:
            db.cur.execute(
                "INSERT INTO dishes (name, price) VALUES (%s, %s) RETURNING id",
                (self.name, self.price),
            )
            self.id = db.cur.fetchone()[0]
        return self

    def update(self, **payload) -> "Dish | None":
        fields = ", ".join([f"{key} = %s" for key in payload])
        values = tuple(payload.values())
        if self.id is None:
            raise ValueError("Can not update dish without ID")
        with DatabaseConnection() as db:
            db.cur.execute(
                f"UPDATE dishes SET {fields} WHERE id = %s RETURNING id, name, price",
                (*values, self.id),
            )
            row = db.cur.fetchone()
        if not row:
            return None
        else:
            _, name, price = row
            self.name, self.price = name, price
            return self

    @classmethod
    def delete_by_filters(cls, **filters) -> bool:
        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            db.cur.execute(f"DELETE FROM dishes WHERE {conditions}", values)
            return True


@dataclass
class Order:
    date: date
    total: float
    status: str
    user_id: int
    id: int | None = None

    @classmethod
    def all(cls) -> list["Order"]:
        with DatabaseConnection() as db:
            rows = db.query("SELECT date, total, status, user_id, id FROM orders")
            return [cls(*row) for row in rows]

    @classmethod
    def filter(cls, **filters) -> list["Order"]:
        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            rows = db.query(
                f"SELECT date, total, status, user_id, id FROM orders WHERE {conditions}",
                values,
            )
            return [cls(*row) for row in rows]

    def create(self) -> "Order":
        with DatabaseConnection() as db:
            db.cur.execute(
                "INSERT INTO orders (date, total, status, user_id) VALUES (%s, %s, %s, %s) RETURNING id",
                (self.date, self.total, self.status, self.user_id),
            )
            self.id = db.cur.fetchone()[0]
        return self

    def update(self, **payload) -> "Order | None":
        fields = ", ".join([f"{key} = %s" for key in payload])
        values = tuple(payload.values())
        if self.id is None:
            raise ValueError("Can not update order without ID")
        with DatabaseConnection() as db:
            db.cur.execute(
                f"UPDATE orders SET {fields} WHERE id = %s RETURNING id, date, total, status, user_id",
                (*values, self.id),
            )
            row = db.cur.fetchone()
        if not row:
            return None
        else:
            _, date_val, total, status, user_id = row
            self.date, self.total, self.status, self.user_id = (
                date_val,
                total,
                status,
                user_id,
            )
            return self

    @classmethod
    def delete_by_filters(cls, **filters) -> bool:
        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            db.cur.execute(f"DELETE FROM orders WHERE {conditions}", values)
            return True


@dataclass
class OrderItem:
    order_id: int
    dish_id: int
    quantity: int
    price: float
    id: int | None = None

    @classmethod
    def all(cls) -> list["OrderItem"]:
        with DatabaseConnection() as db:
            rows = db.query("SELECT order_id, dish_id, quantity, price, id FROM order_items")
            return [cls(*row) for row in rows]

    @classmethod
    def filter(cls, **filters) -> list["OrderItem"]:
        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            rows = db.query(
                f"SELECT order_id, dish_id, quantity, price, id FROM order_items WHERE {conditions}",
                values,
            )
            return [cls(*row) for row in rows]

    def create(self) -> "OrderItem":
        with DatabaseConnection() as db:
            db.cur.execute(
                "INSERT INTO order_items (order_id, dish_id, quantity, price) VALUES (%s, %s, %s, %s) RETURNING id",
                (self.order_id, self.dish_id, self.quantity, self.price),
            )
            self.id = db.cur.fetchone()[0]
        return self

    def update(self, **payload) -> "OrderItem | None":
        fields = ", ".join([f"{key} = %s" for key in payload])
        values = tuple(payload.values())
        if self.id is None:
            raise ValueError("Can not update order item without ID")
        with DatabaseConnection() as db:
            db.cur.execute(
                f"UPDATE order_items SET {fields} WHERE id = %s RETURNING id, order_id, dish_id, quantity, price",
                (*values, self.id),
            )
            row = db.cur.fetchone()
        if not row:
            return None
        else:
            _, order_id, dish_id, quantity, price = row
            self.order_id, self.dish_id, self.quantity, self.price = order_id, dish_id, quantity, price
            return self

    @classmethod
    def delete_by_filters(cls, **filters) -> bool:
        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            db.cur.execute(f"DELETE FROM order_items WHERE {conditions}", values)
            return True