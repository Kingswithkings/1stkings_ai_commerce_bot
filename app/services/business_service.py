import re
from app.services.cart_service import (
    list_products_text,
    add_to_cart,
    remove_from_cart,
    cart_text,
    clear_cart,
    checkout_text,
)


def handle_text(phone: str, message: str) -> str:
    text = (message or "").strip().lower()

    if text in {"hi", "hello", "hey", "start"}:
        return (
            "Welcome to 1stkings AI Commerce.\n\n"
            "You can try:\n"
            "- products\n"
            "- add rice\n"
            "- add 2 beans\n"
            "- remove rice\n"
            "- cart\n"
            "- clear cart\n"
            "- checkout\n"
            "- help"
        )

    if text == "help":
        return (
            "Commands:\n"
            "- products\n"
            "- add rice\n"
            "- add 2 beans\n"
            "- remove rice\n"
            "- cart\n"
            "- clear cart\n"
            "- checkout"
        )

    if "product" in text or text == "catalog":
        return list_products_text()

    match_add = re.match(r"add\s+(\d+)?\s*([a-zA-Z ]+)$", text)
    if match_add:
        qty = int(match_add.group(1)) if match_add.group(1) else 1
        product_name = match_add.group(2).strip()
        ok, reply = add_to_cart(phone, product_name, qty)
        return reply

    match_remove = re.match(r"remove\s+([a-zA-Z ]+)$", text)
    if match_remove:
        product_name = match_remove.group(1).strip()
        ok, reply = remove_from_cart(phone, product_name)
        return reply

    if text == "cart":
        return cart_text(phone)

    if text == "clear cart":
        return clear_cart(phone)

    if text == "checkout":
        return checkout_text(phone)

    return "I didn't understand that. Type 'help' or 'products'."