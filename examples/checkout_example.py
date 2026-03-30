from yabetoo_py import Yabetoo, CreateCheckoutSession, CheckoutItem

# Initialize SDK
sdk = Yabetoo("your_secret_key")

# Create product list
products = [
    {"id": "prod_01", "name": "Premium T-Shirt", "quantity": 2, "price": 15000},
    {"id": "prod_02", "name": "Classic Cap", "quantity": 1, "price": 8000}
]

# Create checkout items
items = [
    CheckoutItem(
        product_id=product["id"],
        product_name=product["name"],
        quantity=product["quantity"],
        price=product["price"]
    )
    for product in products
]

# Calculate total
total = sum(item.quantity * item.price for item in items)

# Create checkout session
session_data = CreateCheckoutSession(
    account_id="acc_123",
    total=total,
    currency="xaf",
    success_url="https://your-website.com/success",
    cancel_url="https://your-website.com/cancel",
    items=items,
    metadata={
        "order_reference": "ORD-123",
        "customer_email": "customer@example.com"
    }
)

# Create session
session = sdk.sessions.create(session_data)

print(f"Checkout session created!")
print(f"Session ID: {session.session_id}")
print(f"Order ID: {session.order_id}")
print(f"Checkout URL: {session.url}")
print(f"Expires at: {session.expires_at}")