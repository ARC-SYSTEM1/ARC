import sqlite3, time
DB = "arc_events.db"
def log_sale(amount=0):
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS sales (timestamp REAL, amount REAL)")
    c.execute("INSERT INTO sales VALUES (?, ?)", (time.time(), amount))
    conn.commit(); conn.close()
def get_revenue_last_hour():
    conn = sqlite3.connect(DB); c = conn.cursor()
    one_hour = time.time() - 3600
    c.execute("SELECT SUM(amount) FROM sales WHERE timestamp > ?", (one_hour,))
    result = c.fetchone()[0]; conn.close()
    return result or 0
def get_total_revenue():
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM sales")
    result = c.fetchone()[0]; conn.close()
    return result or 0
