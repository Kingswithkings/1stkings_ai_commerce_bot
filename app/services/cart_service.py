import csv
from pathlib import Path
from app.db import get_conn

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PRODUCTS_CSV = BASE_DIR / "products.csv"


def load_products():
    products = []
    if not PRODUCTS_CSV.exists():
        return products

    with open(PRODUCTS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append(row)
    return products


def find_product_by_name(name: str):
    name = (name or "").strip().lower()
    for product in load_products():
        if product["name"].strip().lower() == name:
            return product
    return None


def list_products_text():
    products = load_products()
    if not products:
        return "No products available yet."

    lines = ["Available products:"]
    for p in products:
        lines.append(f"- {p['name']} - £{p['price']}")
    return "\n".join(lines)


def add_to_cart(phone: str, product_name: str, quantity: int = 1):
    product = find_product_by_name(product_name)
    if not product:
        return False, f"Product '{product_name}' not found."

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, quantity FROM carts
        WHERE phone = ? AND lower(product_name) = lower(?)
    """, (phone, product["name"]))
    existing = cur.fetchone()

    if existing:
        new_qty = existing["quantity"] + quantity
        cur.execute("""
            UPDATE carts
            SET quantity = ?
            WHERE id = ?
        """, (new_qty, existing["id"]))
    else:
        cur.execute("""
            INSERT INTO carts (phone, product_name, quantity, unit_price)
            VALUES (?, ?, ?, ?)
        """, (phone, product["name"], quantity, float(product["price"])))

    conn.commit()
    conn.close()

    return True, f"✅ Added {quantity} x {product['name']} to cart."


def remove_from_cart(phone: str, product_name: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id FROM carts
        WHERE phone = ? AND lower(product_name) = lower(?)
    """, (phone, product_name))
    existing = cur.fetchone()

    if not existing:
        conn.close()
        return False, f"'{product_name}' is not in your cart."

    cur.execute("DELETE FROM carts WHERE id = ?", (existing["id"],))
    conn.commit()
    conn.close()

    return True, f"🗑️ Removed {product_name} from cart."


def clear_cart(phone: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM carts WHERE phone = ?", (phone,))
    conn.commit()
    conn.close()
    return "🧹 Your cart has been cleared."


def get_cart(phone: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT product_name, quantity, unit_price
        FROM carts
        WHERE phone = ?
    """, (phone,))
    rows = cur.fetchall()
    conn.close()
    return rows


def cart_text(phone: str):
    rows = get_cart(phone)
    if not rows:
        return "🛒 Your cart is empty."

    lines = ["🛒 Your cart:"]
    total = 0.0

    for row in rows:
        line_total = row["quantity"] * row["unit_price"]
        total += line_total
        lines.append(
            f"- {row['product_name']} x {row['quantity']} = £{line_total:.2f}"
        )

    lines.append(f"\nTotal: £{total:.2f}")
    return "\n".join(lines)


def checkout_text(phone: str):
    rows = get_cart(phone)
    if not rows:
        return "Your cart is empty. Add products before checkout."

    message = cart_text(phone) + "\n\n✅ Order placed successfully!"
    clear_cart(phone)
    return message