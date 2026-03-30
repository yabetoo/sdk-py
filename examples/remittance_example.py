from yabetoo_py import Yabetoo, CreateRemittanceRequest, PaymentMethodData, MomoData

# Initialize SDK
sdk = Yabetoo("your_secret_key")

# Create remittance request
remittance_data = CreateRemittanceRequest(
    amount=10000,
    currency="xaf",
    first_name="John",
    last_name="Doe",
    payment_method_data=PaymentMethodData(
        type="momo",
        momo=MomoData(
            country="cg",
            msisdn="+242XXXXXXXXX",
            operator_name="mtn"
        )
    ),
    metadata={"reference": "REM123"}
)

# Create remittance
remittance = sdk.remittances.create(remittance_data)
print(f"Created remittance: {remittance.id}")

# Retrieve remittance status
status = sdk.remittances.retrieve(remittance.id)
print(f"Remittance status: {status.status}")