from models.checkout import CheckoutItem, CreateCheckoutSession
from yabetoo import YabetooSDK


sdk = YabetooSDK("")
produits = [
    {"id": "prod_01", "nom": "Ordinateur", "quantite": 1, "prix": 300000},
    {"id": "prod_02", "nom": "Souris", "quantite": 2, "prix": 5000}
]

items = [
    CheckoutItem(
        product_id=p["id"],
        product_name=p["nom"],
        quantity=p["quantite"],
        price=p["prix"]
    )
    for p in produits
]

total = sum(item.quantity * item.price for item in items)

session_data = CreateCheckoutSession(
    account_id="",
    total=total,
    currency="xaf",
    success_url="https://site.com/ok",
    cancel_url="https://site.com/ko",
    items=items
)

check_session = sdk.sessions.create(session_data)
print(f"session {check_session}")
