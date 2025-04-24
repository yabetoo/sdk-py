from pydantic import BaseModel
from .payment import PaymentMethodData

class CreateDisbursementRequest(BaseModel):
    amount: float
    currency: str
    first_name: str
    last_name: str
    payment_method_data: PaymentMethodData