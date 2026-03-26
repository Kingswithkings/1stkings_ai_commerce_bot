from app.db import get_conn
from app.services.cart_service import get_cart, get_cart_total, get_cart_items_text, clear_cart


def get_checkout_session(phone: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT phone, step, customer_name, address, delivery_time
        FROM checkout_sessions
        WHERE phone = ?
    """, (phone,))
    row = cur.fetchone()
    conn.close()
    return row


def start_checkout(phone: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO checkout_sessions (phone, step)
        VALUES (?, ?)
        ON CONFLICT(phone) DO UPDATE SET
            step = excluded.step,
            customer_name = NULL,
            address = NULL,
            delivery_time = NULL,
            updated_at = CURRENT_TIMESTAMP
    """, (phone, "awaiting_name"))

    conn.commit()
    conn.close()

    return "Please enter your name."


def update_checkout_name(phone: str, name: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE checkout_sessions
        SET customer_name = ?, step = ?, updated_at = CURRENT_TIMESTAMP
        WHERE phone = ?
    """, (name, "awaiting_address", phone))
    conn.commit()
    conn.close()

    return "Please enter your delivery address."


def update_checkout_address(phone: str, address: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE checkout_sessions
        SET address = ?, step = ?, updated_at = CURRENT_TIMESTAMP
        WHERE phone = ?
    """, (address, "awaiting_delivery_time", phone))
    conn.commit()
    conn.close()

    return "Please enter your preferred delivery time."


def update_checkout_delivery_time(phone: str, delivery_time: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE checkout_sessions
        SET delivery_time = ?, step = ?, updated_at = CURRENT_TIMESTAMP
        WHERE phone = ?
    """, (delivery_time, "ready_to_save", phone))
    conn.commit()
    conn.close()

    return save_order(phone)


def save_order(phone: str):
    session = get_checkout_session(phone)
    if not session:
        return "Checkout session not found. Type checkout again."

    cart_rows = get_cart(phone)
    if not cart_rows:
        delete_checkout_session(phone)
        return "Your cart is empty. Add products before checkout."

    items_text = get_cart_items_text(phone)
    total = get_cart_total(phone)

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO orders (
            phone, customer_name, address, delivery_time, items, total, status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        phone,
        session["customer_name"],
        session["address"],
        session["delivery_time"],
        items_text,
        total,
        "pending",
    ))
    order_id = cur.lastrowid
    conn.commit()
    conn.close()

    clear_cart(phone)
    delete_checkout_session(phone)

    return (
        f"✅ Order placed successfully!\n\n"
        f"Order ID: {order_id}\n"
        f"Name: {session['customer_name']}\n"
        f"Address: {session['address']}\n"
        f"Delivery time: {session['delivery_time']}\n\n"
        f"Items:\n{items_text}\n\n"
        f"Total: £{total:.2f}"
    )


def delete_checkout_session(phone: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM checkout_sessions WHERE phone = ?", (phone,))
    conn.commit()
    conn.close()


def get_latest_orders(limit: int = 20):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, phone, customer_name, address, delivery_time, items, total, status, created_at
        FROM orders
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows