def handle_text(phone: str, message: str) -> str:
    text = (message or "").strip().lower()

    # Greeting
    if text in {"hi", "hello", "hey", "start"}:
        return (
            "👋 Welcome to 1stkings AI Commerce.\n\n"
            "Type:\n"
            "🛒 products - see items\n"
            "📦 cart - view cart\n"
            "✅ checkout - place order\n"
        )

    # Products
    elif "product" in text:
        return (
            "🛒 Available products:\n"
            "1. Rice - £10\n"
            "2. Beans - £8\n"
            "3. Oil - £5\n\n"
            "Type 'add rice' or 'add beans'"
        )

    # Add to cart (simple version)
    elif "add rice" in text:
        return "✅ Rice added to cart"

    elif "add beans" in text:
        return "✅ Beans added to cart"

    # Cart
    elif "cart" in text:
        return "🛒 Your cart:\n- Rice\n- Beans"

    # Checkout
    elif "checkout" in text:
        return "✅ Order placed successfully!"

    # Default
    return "❓ I didn’t understand. Type 'products' to begin."