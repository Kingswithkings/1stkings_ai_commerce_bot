import sqlite3
from pathlib import Path

DB_PATH = Path("store.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS businesses (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        channel TEXT NOT NULL,
        provider TEXT NOT NULL,
        bot_key TEXT,
        welcome_message TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_id INTEGER NOT NULL,
        phone TEXT NOT NULL,
        name TEXT,
        UNIQUE(business_id, phone)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS carts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_id INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'open',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cart_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER NOT NULL,
        sku TEXT NOT NULL,
        name TEXT NOT NULL,
        qty INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        line_total REAL NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_id INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        total REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        delivery_address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_id INTEGER NOT NULL,
        phone TEXT NOT NULL,
        direction TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    INSERT OR IGNORE INTO businesses (id, name, channel, provider, bot_key, welcome_message)
    VALUES (
        1,
        'Najeebullah Store',
        'whatsapp',
        'sendpulse',
        'najeebullah_main',
        'Welcome to Najeebullah Store 👋'
    )
    """)

    conn.commit()
    conn.close()