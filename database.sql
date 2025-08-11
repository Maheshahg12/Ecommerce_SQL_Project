PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Products (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE,
    Price REAL NOT NULL CHECK (Price > 0),
    Quantity INTEGER NOT NULL CHECK (Quantity >= 0),
    CreatedAt DATETIME DEFAULT (datetime('now','localtime'))
);
