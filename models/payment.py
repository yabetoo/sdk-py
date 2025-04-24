from pydantic import BaseModel, Field
from typing import Dict, Optional, Any, List
from datetime import datetime

class MomoData(BaseModel):
    msisdn: str
    country: str
    operator_name: str

class PaymentMethodData(BaseModel):
    type: str
    momo: MomoData

class CreatePaymentIntentRequest(BaseModel):
    amount: int
    currency: str
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class CreatePaymentIntentResponse(BaseModel):
  id: str
  amount: str
  currency: str
  label: str
  client_secret: str = Field(alias="clientSecret")
  created_at: datetime = Field(alias="createdAt"),
  updated_at: datetime = Field(alias='updatedAt')
  
  class Config:
        validate_by_name = True
        


class ConfirmPaymentIntentRequest(BaseModel):
    client_secret: str
    payment_method_data: PaymentMethodData
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    receipt_email: Optional[str] = None

class ConfirmPaymentResponse(BaseModel):
    charge_id: str = Field(alias='id')
    intent_id: str  = Field(alias='intentId')
    financial_transaction_Id: str = Field(alias='financialTransactionId')
    transaction_id: str = Field("transactionId")
    amount: float
    status: str 
    captured: bool 
    external_id: str = Field(alias="externalId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    payment_method_id: str = Field(alias="paymentMethodId")
    
    class Config:
        validate_by_name = True
        




class Charge(BaseModel):
    id: int
    type: str
    event_id: int = Field(alias="event_id")
    charge_id: str
    financial_transaction_id: str
    transaction_id: str
    amount: float
    captured: bool
    refunded: bool
    disputed: bool
    currency: str
    status: str
    failure_code: Optional[str]
    failure_message: Optional[str]
    external_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        validate_by_name = True
        


class Payout(BaseModel):
    id: int
    type: str
    event_id: int
    payout_id: str
    financial_transaction_id: str
    transaction_id: str
    amount: float
    amount_captured: float
    amount_fee: float
    currency: str
    status: str
    failure_code: Optional[str]
    failure_message: Optional[str]
    external_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        validate_by_name = True
        
        


class PaymentEvent(BaseModel):
    id: int
    intent_id: int
    created_at: datetime
    updated_at: datetime
    charges: List[Charge]
    payouts: List[Payout]

    class Config:
        validate_by_name = True
        


class PaymentIntent(BaseModel):
    id: int
    client_secret: str
    intent_id: str
    currency: str
    amount: float
    payment_method_types: Optional[str]
    payment_method: Optional[str]
    last_payment_error: Optional[str]
    status: str
    metadata: Optional[dict]
    charge_id: Optional[str]
    canceled_at: Optional[datetime]
    description: Optional[str]
    cancellation_reason: Optional[str]
    live_mode: bool
    payout_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    event: PaymentEvent

    class Config:
        validate_by_name = True
        



class Sorting(BaseModel):
    id: str = Field(..., alias="id")
    desc: bool = Field(..., alias="desc")


class PaymentFiltersRequest(BaseModel):
    sorting: Optional[List[Sorting]] = Field(None, alias="sorting")
    per_page: Optional[int] = Field(None, alias="perPage")
    page: Optional[int] = Field(None, alias="page")

    def to_query_params(self) -> dict:
        params = self.model_dump(by_alias=True, exclude_none=True)
        if "sorting" in params:
            params["sorting"] = [s.model_dump(by_alias=True) for s in self.sorting]
        return params
