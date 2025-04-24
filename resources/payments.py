from typing import Dict, Optional
from models.payment import ConfirmPaymentIntentRequest, ConfirmPaymentResponse, CreatePaymentIntentRequest, CreatePaymentIntentResponse, PaymentFiltersRequest, PaymentIntent
from resources.base import ResourceBase


class Payments(ResourceBase):
    """Payments resource for interacting with payment intents"""
    
    def create(self, data: CreatePaymentIntentRequest) -> CreatePaymentIntentResponse:
        """
        Create a payment intent
        
        Args:
            data: Payment intent data
            
        Returns:
            Payment intent details
        """
        response = self._client.request('POST', '/payment-intents', data)
        return CreatePaymentIntentResponse(**response)
        
    
    def confirm(self, payment_id: str, data: ConfirmPaymentIntentRequest) -> ConfirmPaymentResponse:
        """
        Confirm a payment intent
        
        Args:
            payment_id: Payment intent ID
            data: Confirmation data
            
        Returns:
            Confirmed payment intent details
        """
        response = self._client.request('POST', f'/payment-intents/{payment_id}/confirm', payload)
        return ConfirmPaymentResponse(**response)
    
    def retrieve(self, payment_id: str) -> PaymentIntent:
        """
        Get a payment intent by ID
        
        Args:
            payment_id: Payment intent ID
            
        Returns:
            Payment intent details
        """
        response = self._client.request('GET', f'/payment-intents/{payment_id}')
        return PaymentIntent(**response)
    
    def all(self, params: Optional[PaymentFiltersRequest] = None) -> Dict:
        """
        List all payment intents
        
        Args:
            params: Filter parameters
            
        Returns:
            List of payment intents
        """
        return self._client.request('GET', '/payment-intents')