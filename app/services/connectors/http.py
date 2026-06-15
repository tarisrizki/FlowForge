import httpx
from typing import Dict, Any
from app.services.connectors.base import BaseConnector

class HttpConnector(BaseConnector):
    async def execute(self, config: Dict[str, Any], params: Dict[str, Any], context_data: Dict[str, Any]) -> Any:
        method = params.get("method", "GET").upper()
        url = params.get("url")
        
        if not url:
            raise ValueError("HTTP connector requires 'url' in params")

        # Config might have base auth headers
        headers = config.get("headers", {})
        # Merge with param headers
        headers.update(params.get("headers", {}))

        # Payload
        json_payload = params.get("json", {})

        async with httpx.AsyncClient() as client:
            request = client.build_request(method, url, headers=headers, json=json_payload if json_payload else None)
            response = await client.send(request)
            response.raise_for_status()
            
            try:
                return response.json()
            except:
                return response.text

http_connector = HttpConnector()
