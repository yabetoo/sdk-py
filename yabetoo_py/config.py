"""
Configuration module for Yabetoo SDK
"""
from .models.common import EnvironmentType


class YabetooConfig:
    """
    Configuration class for Yabetoo SDK
    
    Attributes:
        secret_key (str): Secret API key for authentication
        http_options (HttpClientOptions): Additional HTTP client options
    """
    
    def __init__(
        self,
        secret_key: str,
    ):
      
     
        if not secret_key:
            raise ValueError("Secret key is required")
        if not secret_key.startswith(("sk_test", "sk_live")):
            raise ValueError('Invalid secret key format. Key must start with "sk_test" or "sk_live"')
        if secret_key.startswith("sk_test"):
            environment = EnvironmentType.SANDBOX
        else:
            environment = EnvironmentType.PRODUCTION
            
        self.secret_key = secret_key
        self.environment = environment
        
        env_prefix = 'api' if environment == EnvironmentType.PRODUCTION else 'sandbox'
        # The checkout API has a single host: the secret key selects the environment.
        self.base_urls = {
            'checkout': "https://buy.api.yabetoopay.com/v1",
            'payment': f"https://pay.{env_prefix}.yabetoopay.com/v1"
        }
        
    