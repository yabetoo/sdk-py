from yabetoo_py import Yabetoo, CreateIntentRequest, ConfirmIntentRequest, PaymentMethodData, MomoData

# Initialize SDK with your secret key
sdk = Yabetoo("your_secret_key")

# Create a payment intent
intent_data = CreateIntentRequest(
    amount=5000,
    currency="xaf",
    description="Example payment",
    metadata={"order_id": "ORDER123"}
)

intent = sdk.payments.create(intent_data)
print(f"Created payment intent: {intent.id}")

# Confirm the payment intent
confirm_data = ConfirmIntentRequest(
    client_secret=intent.client_secret,
    payment_method_data=PaymentMethodData(
        type='momo',
        momo=MomoData(
            country='cg',
            msisdn='+242XXXXXXXXX',
            operator_name="mtn"
        )
    )
)

result = sdk.payments.confirm(intent.id, confirm_data)
print(f"Payment confirmed: {result.status}")