def handle_text(phone: str, message: str) -> str:
    text = (message or "").strip().lower()

    if text in {"hi", "hello", "hey", "start"}:
        return (
            "Welcome to 1stkings AI Commerce.\n\n"
            "You can try:\n"
            "- products\n"
            "- cart\n"
            "- checkout\n"
            "- help"
        )

    if "product" in text or "products" in text or "catalog" in text:
        return "Available products: Rice, Beans, Oil, Bread."

    if "cart" in text:
        return "Your cart is currently empty."

    if "checkout" in text:
        return "Checkout is not set up yet."

    if "help" in text:
        return (
            "Send words like:\n"
            "- products\n"
            "- cart\n"
            "- checkout"
        )

    return f"You said: {message}"