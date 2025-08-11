"""
DatabaseHandler: handles all SQLite operations for the project.
"""
import sqlite3
from sqlite3 import Connection
from typing import List, Tuple, Optional

class DatabaseHandler:
    def __init__(self, db_name: str = "ecommerce.db"):
        self.db_name = db_name

    def _connect(self) -> Connection:
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def initialize_db(self) -> None:
        """Create tables and load schema from database.sql if not present."""
        schema = None
        try:
            with open("database.sql", "r", encoding="utf-8") as f:
                schema = f.read()
        except FileNotFoundError:
            # fallback: create table with built-in SQL
            schema = (
                "CREATE TABLE IF NOT EXISTS Products ("
                "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                "Name TEXT NOT NULL UNIQUE,"
                "Price REAL NOT NULL CHECK (Price > 0),"
                "Quantity INTEGER NOT NULL CHECK (Quantity >= 0),"
                "CreatedAt DATETIME DEFAULT (datetime('now','localtime'))"
                ");"
            )

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.executescript(schema)
            conn.commit()

    def add_product(self, name: str, price: float, quantity: int) -> int:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Products (Name, Price, Quantity) VALUES (?, ?, ?)",
                (name.strip(), float(price), int(quantity)),
            )
            conn.commit()
            return cursor.lastrowid

    def get_products(self, limit: Optional[int] = None, offset: int = 0) -> List[Tuple]:
        q = "SELECT ID, Name, Price, Quantity, CreatedAt FROM Products ORDER BY ID"
        if limit:
            q += f" LIMIT {int(limit)} OFFSET {int(offset)}"
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(q)
            return cursor.fetchall()

    def find_products_by_name(self, term: str) -> List[Tuple]:
        like = f"%{term.strip()}%"
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT ID, Name, Price, Quantity, CreatedAt FROM Products WHERE Name LIKE ? ORDER BY Name",
                (like,),
            )
            return cursor.fetchall()

    def filter_products(self, min_price: Optional[float], max_price: Optional[float]) -> List[Tuple]:
        q = "SELECT ID, Name, Price, Quantity, CreatedAt FROM Products WHERE 1=1"
        params = []
        if min_price is not None:
            q += " AND Price >= ?"
            params.append(float(min_price))
        if max_price is not None:
            q += " AND Price <= ?"
            params.append(float(max_price))
        q += " ORDER BY Price"
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(q, tuple(params))
            return cursor.fetchall()

    def update_product(self, product_id: int, name: Optional[str], price: Optional[float], quantity: Optional[int]) -> bool:
        updates = []
        params = []
        if name is not None:
            updates.append("Name = ?")
            params.append(name.strip())
        if price is not None:
            updates.append("Price = ?")
            params.append(float(price))
        if quantity is not None:
            updates.append("Quantity = ?")
            params.append(int(quantity))
        if not updates:
            return False
        params.append(int(product_id))
        q = f"UPDATE Products SET {', '.join(updates)} WHERE ID = ?"
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(q, tuple(params))
            conn.commit()
            return cursor.rowcount > 0

    def delete_product(self, product_id: int) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Products WHERE ID = ?", (int(product_id),))
            conn.commit()
            return cursor.rowcount > 0

    def get_product(self, product_id: int) -> Optional[Tuple]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ID, Name, Price, Quantity, CreatedAt FROM Products WHERE ID = ?", (int(product_id),))
            return cursor.fetchone()