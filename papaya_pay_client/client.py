import requests
import json
from typing import Optional
from .types import Checkout, CheckoutItem
from .errors import PapayaAPIError

class CheckoutsService:
    def __init__(self, client):
        self.client = client
        
    def get(self, checkout_id: str) -> Checkout:
        response = self.client._request('GET', f'/v1/gateway/api/checkouts/{checkout_id}')
        
        # Parsea los items, si vienen como string JSON, los parseamos.
        items_data = response.get('items', [])
        if isinstance(items_data, str):
            try:
                items_data = json.loads(items_data)
            except:
                items_data = []
                
        items = [CheckoutItem(**item) for item in items_data]
        
        return Checkout(
            id=response.get('id', ''),
            app_id=response.get('app_id', ''),
            external_reference=response.get('external_reference', ''),
            amount_ves_cents=response.get('amount_ves_cents', 0),
            amount_usdc_cents=response.get('amount_usdc_cents', 0),
            paid_currency=response.get('paid_currency'),
            status=response.get('status', ''),
            items=items,
            expires_at=response.get('expires_at', 0),
            created_at=response.get('created_at', 0),
        )

class PapayaClient:
    def __init__(self, api_key: str, base_url: str = 'http://localhost:80'):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        })
        
        self.checkouts = CheckoutsService(self)
        
    def _request(self, method: str, path: str, **kwargs) -> dict:
        url = f'{self.base_url}{path}'
        response = self.session.request(method, url, **kwargs)
        
        if not response.ok:
            raise PapayaAPIError(response.status_code, response.text)
            
        return response.json()
