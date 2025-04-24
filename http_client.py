from typing import Optional, Dict
from pydantic import BaseModel
import requests
import json
from errors import YabetooError

class HttpClientOptions(BaseModel):
    """HTTP client configuration options"""
    timeout: int = 30
    max_retries: int = 3
    retry_delay: int = 1
    verify_ssl: bool = True
    follow_redirects: bool = True
    custom_headers: Dict[str, str] = {}

class HttpClient:
    """
    HTTP Client for making API requests
    """
    def __init__(
        self, 
        secret_key: str, 
        base_url: str, 
        options: Optional[HttpClientOptions] = None
    ):
        self.secret_key = secret_key
        self.base_url = base_url
        self.options = options or HttpClientOptions()
        
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.secret_key}',
            **self.options.custom_headers
        }
        
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            max_retries=self.options.max_retries
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
    
    def request(self, method: str, path: str, data: Optional[BaseModel] = None) -> Dict:
        """
        Make HTTP request to API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            data: Request data as Pydantic model
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}{path}"
        print(f"url: {url}")
        
        
        request_params = {
            'headers': self.headers,
            'timeout': self.options.timeout,
            'verify': self.options.verify_ssl,
            'allow_redirects': self.options.follow_redirects
        }
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, **request_params)
            elif method.upper() == 'POST':
               
                json_data = data.model_dump(by_alias=True ) if data else None
                response = self.session.post(url, json=json_data, **request_params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response_data = response.json()
            
            if response.status_code >= 400:
                if 'errors' in response_data:
                    raise YabetooError(
                        message="Validation error",
                        errors=response_data['errors']
                    )
                elif 'error' in response_data:
                    if isinstance(response_data['error'], dict):
                        raise YabetooError(
                            message=response_data['error'].get('message', 'Unknown error'),
                            code=response_data['error'].get('code')
                        )
                    else:
                        raise YabetooError(message=response_data['error'])
                else:
                    raise YabetooError(message=f"Error: {response.status_code}")
                    
            return response_data
            
        except requests.RequestException as e:
            raise YabetooError(message=f"Network error: {str(e)}")
        except json.JSONDecodeError:
            raise YabetooError(message="Invalid JSON response from API")