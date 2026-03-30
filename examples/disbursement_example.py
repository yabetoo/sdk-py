from yabetoo_py import Yabetoo, CreateDisbursementRequest, PaymentMethodData, MomoData

# Initialize SDK
sdk = Yabetoo("your_secret_key")

# Create disbursement request
disbursement_data = CreateDisbursementRequest(
    amount=5000,
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
    )
)

# Create disbursement
disbursement = sdk.disbursements.create(disbursement_data)
print(f"Created disbursement: {disbursement.id}")
print(f"Status: {disbursement.status}")
print(f"Amount: {disbursement.amount} {disbursement.currency}")
print(f"Recipient: {disbursement.first_name} {disbursement.last_name}")
print(f"Operator: {disbursement.operator_name}")

# Retrieve disbursement status
status = sdk.disbursements.retrieve(disbursement.id)
print(f"\nDisbursement status: {status.status}")
print(f"Created at: {status.created_at}")
print(f"Updated at: {status.updated_at}")