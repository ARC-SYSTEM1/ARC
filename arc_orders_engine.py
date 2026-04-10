import sqlite3
import time
from datetime import datetime, date

DB = "/home/chadj0085/ARC/arc_orders.db"

def _conn():
    return sqlite3.connect(DB)

def init_orders_db():
    con = _conn()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        quantity INTEGER,
        price REAL,
        total REAL,
        status TEXT,
        ts INTEGER
    )
    """)
    con.commit()
    con.close()

def add_order(item, quantity, price, status="paid"):
    quantity = int(quantity)
    price = float(price)
    total = quantity * price
    ts = int(time.time())

    con = _conn()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO orders (item, quantity, price, total, status, ts) VALUES (?,?,?,?,?,?)",
        (item, quantity, price, total, status, ts)
    )
    con.commit()
    con.close()

    return {"status":"ok","item":item,"quantity":quantity,"total":total}

def orders_today():
    start = int(datetime.combine(date.today(), datetime.min.time()).timestamp())

    con = _conn()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*), COALESCE(SUM(total),0) FROM orders WHERE ts >= ?", (start,))
    count, revenue = cur.fetchone()
    con.close()

    return {"orders_today": count, "revenue_today": revenue}

def order_stats():
    con = _conn()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*), COALESCE(SUM(total),0), COALESCE(AVG(total),0) FROM orders")
    count, revenue, avg_ticket = cur.fetchone()
    con.close()

    return {
        "total_orders": count,
        "total_revenue": revenue,
        "average_ticket": round(avg_ticket,2)
    }
