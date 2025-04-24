from typing import Dict, Optional
from pydantic import BaseModel
from enum import Enum


class HttpClientOptions(BaseModel):
    timeout: int = 30
    max_retries: int = 3
    retry_delay: int = 1
    headers: Dict[str, str] = {}  
    verify_ssl: bool = True  
    proxy: Optional[str] = None  
    connection_timeout: int = 5  
    follow_redirects: bool = True  
    user_agent: Optional[str] = None  
    

class EnvironmentType(str, Enum):
    SANDBOX = 'sandbox'
    PRODUCTION = 'production'
