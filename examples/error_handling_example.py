from yabetoo import YabetooSDK, YabetooError
from models.payment import CreateIntentRequest, PaymentMethodData, MomoData
from errors import ValidationError, APIError, NetworkError

# Initialize SDK
sdk = YabetooSDK("your_secret_key")

def handle_validation_error(e: YabetooError):
    print("Validation Error:")
    for error in e.errors:
        print(f"- Field '{error.get('field')}': {error.get('message')}")

def handle_api_error(e: APIError):
    print(f"API Error: {e.message}")
    if e.code:
        print(f"Error code: {e.code}")

def handle_network_error(e: NetworkError):
    print(f"Network Error: {e.message}")

try:
    # Try creating a payment with invalid amount
    intent_data = CreateIntentRequest(
        amount=-100,  # Invalid negative amount
        currency="xaf",
        description="Test payment"
    )
    
    payment = sdk.payments.create(intent_data)

except ValidationError as e:
    handle_validation_error(e)

try:
    # Try confirming with invalid payment method
    confirm_data = PaymentMethodData(
        type="invalid_type",
        momo=MomoData(
            country="invalid",
            msisdn="invalid",
            operator_name="invalid"
        )
    )
    
    sdk.payments.confirm("invalid_id", confirm_data)

except APIError as e:
    handle_api_error(e)

try:
    # Try retrieving non-existent payment
    sdk.payments.retrieve("non_existent_id")

except YabetooError as e:
    print(f"General Error: {e.message}")