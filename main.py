from yabetoo import YabetooSDK
from models.remittance import CreateRemittanceRequest
from models.payment import MomoData, PaymentMethodData



yabetoo = YabetooSDK("")

create_data = CreateRemittanceRequest(
    amount=100,
    currency="xaf",
    first_name="Scoty",
    last_name="Loumbou",
    payment_method_data=PaymentMethodData(
        type="momo",
        momo=MomoData(
            country="cg",
            msisdn="+242066594470",
            operator_name="mtn"
        )
    ),
    metadata={"orderId": "ABC123XYZ"}
)

created_remittance = yabetoo.remittances.create(create_data)
print(f"✅ Remittance created: {created_remittance.id}")

# 2. Récupération de la remittance par ID
retrieved_remittance = yabetoo.remittances.retrieve(created_remittance.id)
print("🔍 Retrieved remittance:")
print(f"Amount: {retrieved_remittance.amount}")
print(f"Name: {retrieved_remittance.first_name} {retrieved_remittance.last_name}")
print(f"Status: {retrieved_remittance.status}")
print(f"Created at: {retrieved_remittance.created_at}")
# first_page = yabetoo.payments.get_page(page=1, per_page=2)

# for payment in first_page.items:
#     print(f"Payment ID: {payment.id}, Amount: {payment.amount} {payment.currency}")
    
#     if payment.status == "succeeded":
#         print(f"  Payment succeeded at: {payment.created_at}")
    
#     if payment.metadata and "customer_id" in payment.metadata:
#         print(f"  Customer ID: {payment.metadata['customer_id']}")
# data = CreateIntentRequest(print(f"payment {payment.model_dump_json()}")
#     amount=20000,  
#     currency="xaf",
#     description="une description test",
#     metadata={"orderId": "skljqfmsd"}
# )

# intent = sdk.payments.create(data)

# confirm_intent_data = ConfirmIntentRequest(
#     client_secret=intent.client_secret,
#     payment_method_data=PaymentMethodData(
#         type='momo',
#         momo=MomoData(
#             country='cg',
#             msisdn='+242065607129',
#             operator_name="mtn"
#         )
#     )
# )

# confirm_intent = sdk.payments.confirm(intent.id, confirm_intent_data)

# print(f"confirm intent: {confirm_intent.model_dump(mode='json')}")


# produits = [
#     {"id": "prod_01", "nom": "Ordinateur", "quantite": 1, "prix": 300000},
#     {"id": "prod_02", "nom": "Souris", "quantite": 2, "prix": 5000}
# ]

# items = [
#     CheckoutItem(
#         product_id=p["id"],
#         product_name=p["nom"],
#         quantity=p["quantite"],
#         price=p["prix"]
#     )
#     for p in produits
# ]

# total = sum(item.quantity * item.price for item in items)

# session_data = CreateCheckoutSession(
#     account_id="",
#     total=total,
#     currency="xaf",
#     success_url="https://site.com/ok",
#     cancel_url="https://site.com/ko",
#     items=items
# )

# check_session = sdk.sessions.create(session_data)

# print(f"url {check_session.url}")
