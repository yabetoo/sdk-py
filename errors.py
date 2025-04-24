"""
Error classes for Yabetoo SDK
"""

from typing import Dict, List, Optional, Any

class YabetooError(Exception):
    
    def __init__(
        self, 
        message: str, 
        code: Optional[str] = None, 
        errors: Optional[List[Dict[str, Any]]] = None
    ):
        
        self.message = message
        self.code = code
        self.errors = errors or []
        super().__init__(self.message)
        
    def __str__(self) -> str:
        
        result = self.message
        if self.code:
            result = f"{result} (Code: {self.code})"
        
        if self.errors:
            errors_str = "\n".join([f"- {e.get('field', '')}: {e.get('message', '')}" for e in self.errors])
            result = f"{result}\nValidation errors:\n{errors_str}"
            
        return result

class ValidationError(YabetooError):
    """Error raised when request validation fails"""
    pass

class APIError(YabetooError):
    """Error raised when API returns an error response"""
    pass

class NetworkError(YabetooError):
    """Error raised when network communication fails"""
    pass

class AuthenticationError(YabetooError):
    """Error raised when authentication fails"""
    pass