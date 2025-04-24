from typing import Dict
from models.remittance import CreateRemittanceRequest, RemittanceResponse
from resources.base import ResourceBase


class Remittances(ResourceBase):
    """Remittances resource"""
    
    def create(self, data: CreateRemittanceRequest) -> RemittanceResponse:
        """
        Create a remittance
        
        Args:
            data: Remittance data
            
        Returns:
            Remittance details
        """
        return self._client.request('POST', '/remittances', data)
    
    def retrieve(self, remittance_id: str) -> Dict:
        """
        Get a remittance by ID
        
        Args:
            remittance_id: Remittance ID
            
        Returns:
            Remittance details
        """
        return self._client.request('GET', f'/remittances/{remittance_id}')