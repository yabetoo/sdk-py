from typing import Optional
from http_client import HttpClient, HttpClientOptions
from resources.disbursements import Disbursements
from resources.payments import Payments
from resources.remittances import Remittances
from resources.sessions import Sessions
from config import YabetooConfig


class YabetooSDK:
    """
    Yabetoo SDK for  Payment API
    """
    
    def __init__(
        self, 
        secret_key: str, 
        options: Optional[HttpClientOptions] = None
    ):
        """
        Initialize the Yabetoo SDK
        
        Args:
            secret_key: Your Yabetoo secret key
            options: HTTP client configuration options
        """
        
        options = options or HttpClientOptions()
        
        config = YabetooConfig(secret_key)
        
        checkout_client = HttpClient(
            secret_key=config.secret_key,
            base_url=config.base_urls.get('checkout'),
            options=options
        )
        
        payment_client = HttpClient(
            secret_key=secret_key,
            base_url=config.base_urls.get('payment'),
            options=options
        )
        
        self.payments = Payments(payment_client)
        self.sessions = Sessions(checkout_client)
        self.disbursements = Disbursements(payment_client)
        self.remittances = Remittances(payment_client)
        