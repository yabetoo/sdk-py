# Yabetoo Python SDK

Official Python SDK for integrating with the Yabetoo Payment API. This library provides a simple interface for processing Mobile Money payments, creating checkout sessions, managing disbursements and money transfers in Central Africa.

## Features

- **Mobile Money Payments** - Accept payments via MTN Mobile Money and Airtel Money
- **Checkout Sessions** - Create hosted payment pages with redirect
- **Disbursements** - Send money to Mobile Money accounts
- **Remittances** - Manage international money transfers
- **Sandbox/Production Environments** - Automatically switch based on your API key
- **Error Handling** - Typed errors with detailed codes and messages
- **Automatic Retry** - Configurable retries for failed requests

## Installation

```bash
pip install yabetoo-sdk
```

## Prerequisites

- Python 3.9+
- Yabetoo API key (get yours at [yabetoopay.com](https://yabetoopay.com))

## Quick Start

```python
from yabetoo_py import Yabetoo, CreateIntentRequest, ConfirmIntentRequest, PaymentMethodData, MomoData

# Initialize the SDK with your secret key
# Use sk_test_xxx for sandbox, sk_live_xxx for production
yabetoo = Yabetoo("sk_test_your_secret_key")

# Create a payment intent
intent = yabetoo.payments.create(CreateIntentRequest(
    amount=1000,
    currency="XAF",
    description="Product purchase",
    metadata={"order_id": "123"}
))

# Confirm the payment with Mobile Money details
result = yabetoo.payments.confirm(intent.id, ConfirmIntentRequest(
    client_secret=intent.client_secret,
    payment_method_data=PaymentMethodData(
        type="momo",
        momo=MomoData(
            country="cg",
            msisdn="+242XXXXXXXXX",
            operator_name="mtn"
        )
    )
))
```

## Documentation

### Initialization

```python
from yabetoo_py import Yabetoo
from yabetoo_py.models.common import HttpClientOptions

yabetoo = Yabetoo(
    secret_key="sk_test_your_secret_key",
    options=HttpClientOptions(
        timeout=30,           # Timeout in seconds
        max_retries=3,        # Number of retries
        retry_delay=1,        # Delay between retries
        verify_ssl=True,      # SSL verification
        custom_headers={}     # Custom headers
    )
)
```

### Payments

```python
from yabetoo_py import CreateIntentRequest, ConfirmIntentRequest, PaymentMethodData, MomoData

# Create a payment intent
intent = yabetoo.payments.create(CreateIntentRequest(
    amount=5000,
    currency="XAF",
    description="Online purchase"
))

# Confirm the payment
payment = yabetoo.payments.confirm(intent.id, ConfirmIntentRequest(
    client_secret=intent.client_secret,
    payment_method_data=PaymentMethodData(
        type="momo",
        momo=MomoData(
            country="cg",
            msisdn="+242XXXXXXXXX",
            operator_name="mtn"  # or "airtel"
        )
    )
))

# Retrieve a payment
payment = yabetoo.payments.retrieve("pi_xxx")

# List payments with pagination
payments = yabetoo.payments.get_page(page=1, per_page=10)
```

### Checkout Sessions

```python
from yabetoo_py import CreateCheckoutSession, CheckoutItem

# Create a hosted checkout session
session = yabetoo.sessions.create(CreateCheckoutSession(
    account_id="acc_xxx",
    total=10000,
    currency="XAF",
    success_url="https://your-site.com/success",
    cancel_url="https://your-site.com/cancel",
    items=[
        CheckoutItem(
            product_id="prod_123",
            product_name="T-shirt",
            quantity=2,
            price=5000
        )
    ]
))

# Redirect the user to session.url
```

### Disbursements

```python
from yabetoo_py import CreateDisbursementRequest, PaymentMethodData, MomoData

# Send money to a Mobile Money account
disbursement = yabetoo.disbursements.create(CreateDisbursementRequest(
    amount=5000,
    currency="XAF",
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
))
```

### Remittances

```python
from yabetoo_py import CreateRemittanceRequest, PaymentMethodData, MomoData

# Create a money transfer
remittance = yabetoo.remittances.create(CreateRemittanceRequest(
    amount=5000,
    currency="XAF",
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
))
```

## Error Handling

```python
from yabetoo_py import YabetooError

try:
    payment = yabetoo.payments.retrieve("invalid_id")
except YabetooError as e:
    print(f"Error: {e.message}")
    if e.code:
        print(f"Error code: {e.code}")
    if e.errors:
        print("Validation errors:", e.errors)
```

## Supported Countries and Operators

| Country | Code | Operators |
|---------|------|-----------|
| Congo-Brazzaville | `cg` | MTN, Airtel |
| France | `fr` | - |

## Environments

The SDK automatically detects the environment based on your API key:

- `sk_test_xxx` → Sandbox (`https://pay.sandbox.yabetoopay.com/v1`)
- `sk_live_xxx` → Production (`https://pay.api.yabetoopay.com/v1`)

## Development

```bash
# Clone the repository
git clone https://github.com/yabetoo/sdk-py.git

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy .

# Format code
black .
isort .
```

## Examples

See the [examples/](examples/) folder for complete examples:

- [payments_example.py](examples/payments_example.py) - Mobile Money payments
- [checkout_example.py](examples/checkout_example.py) - Checkout sessions
- [disbursement_example.py](examples/disbursement_example.py) - Disbursements
- [remittance_example.py](examples/remittance_example.py) - Remittances
- [error_handling_example.py](examples/error_handling_example.py) - Error handling

## License

MIT License - see LICENSE file for details.
