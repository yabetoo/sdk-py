from yabetoo import YabetooSDK
from models.payment import PaymentFiltersRequest, Sorting

# Initialize SDK
sdk = YabetooSDK("your_secret_key")

# Example 1: Simple pagination
print("Fetching first page of payments...")
first_page = sdk.payments.get_page(page=1, per_page=5)

print(f"\nFound {first_page.total_count} total payments")
print(f"Showing page {first_page.page} ({len(first_page.items)} items)")

for payment in first_page.items:
    print(f"\nPayment ID: {payment.id}")
    print(f"Amount: {payment.amount} {payment.currency}")
    print(f"Status: {payment.status}")
    print(f"Created: {payment.created_at}")

# Example 2: With sorting
print("\nFetching payments sorted by creation date...")
sorting_params = [
    {"id": "createdAt", "desc": True}
]

sorted_payments = sdk.payments.get_page(
    page=1,
    per_page=5,
    sorting=sorting_params
)

for payment in sorted_payments.items:
    print(f"\nPayment ID: {payment.id}")
    print(f"Amount: {payment.amount} {payment.currency}")
    print(f"Created: {payment.created_at}")

# Example 3: Custom filters
print("\nFetching with custom filters...")
filters = PaymentFiltersRequest(
    page=1,
    per_page=5,
    sorting=[
        Sorting(id="amount", desc=True),
        Sorting(id="createdAt", desc=False)
    ]
)

filtered_payments = sdk.payments.all(filters)

for payment in filtered_payments.items:
    print(f"\nPayment ID: {payment.id}")
    print(f"Amount: {payment.amount} {payment.currency}")
    if payment.metadata:
        print(f"Metadata: {payment.metadata}")