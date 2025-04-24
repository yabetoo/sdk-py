from pydantic import BaseModel
from typing import Union , Optional, Dict, Any
from datetime import datetime 
from .payment import PaymentMethodData

class CreateRemittanceRequest(BaseModel):
    amount: Union[int, str]
    currency: str
    first_name: str
    last_name: str
    payment_method_data: PaymentMethodData
    metadata: Optional[Dict[str, Any]] = None

class RemittanceResponse(BaseModel):
    id: str
    amount: int
    currency: str
    status: str
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime
    metadata: Optional[Dict[str, Any]] = None