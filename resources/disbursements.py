from typing import Dict
from models.disbursement import CreateDisbursementRequest
from resources.base import ResourceBase


class Disbursements(ResourceBase):
    """Disbursements resource"""
    
    def create(self, data: Dict) -> Dict:
        """
        Create a disbursement
        
        Args:
            data: Disbursement data
            
        Returns:
            Disbursement details
        """
        request = CreateDisbursementRequest(**data)
        return self._client.request('POST', '/disbursements', request)
    
    def retrieve(self, disbursement_id: str) -> Dict:
        """
        Get a disbursement by ID
        
        Args:
            disbursement_id: Disbursement ID
            
        Returns:
            Disbursement details
        """
        return self._client.request('GET', f'/disbursements/{disbursement_id}')