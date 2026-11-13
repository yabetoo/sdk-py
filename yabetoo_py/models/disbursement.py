from pydantic import BaseModel, Field
from .payment import PaymentMethodData
from datetime import datetime
from typing import Optional
class CreateDisbursementRequest(BaseModel):
    amount: float
    currency: str
    first_name: str
    last_name: str
    payment_method_data: PaymentMethodData
    



class Disbursement(BaseModel):
    # The create response carries only the first fields; retrieve returns them all.
    id: str
    amount: float
    currency: str
    status: str
    transaction_id: Optional[str] = Field(None, alias="transactionId")
    financial_transaction_id: Optional[str] = Field(None, alias="financialTransactionId")
    failure_code: Optional[str] = Field(None, alias="failureCode")
    failure_message: Optional[str] = Field(None, alias="failureMessage")
    executed_at: Optional[datetime] = Field(None, alias="executedAt")
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    operator_name: Optional[str] = Field(None, alias="operatorName")
    country: Optional[str] = None
    phone: Optional[str] = None
    object: Optional[str] = None
    type: Optional[int] = None
    should_executed_at: Optional[datetime] = Field(None, alias="shouldExecutedAt")
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

    class Config:
        populate_by_name = True
        use_enum_values = True
