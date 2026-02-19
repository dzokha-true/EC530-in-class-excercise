import httpx
from typing import Optional, Dict, Any

class FDAClient:
    """
    A client to interact with the OpenFDA API.
    """
    BASE_URL = "https://api.fda.gov/"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = httpx.AsyncClient(base_url=self.BASE_URL)

    async def fetch_data(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generic method to fetch data from a given FDA API endpoint.
        
        Args:
            endpoint (str): The specific API endpoint (e.g., "drug/event.json").
            params (dict, optional): Query parameters for the request.

        Returns:
            dict: The JSON response from the API.
        """
        if params is None:
            params = {}
        
        if self.api_key:
            params['api_key'] = self.api_key

        try:
            response = await self.client.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            # You might want to handle specific status codes here
            raise Exception(f"FDA API Error: {e.response.text}") from e
        except Exception as e:
            raise Exception(f"An error occurred while fetching data: {str(e)}") from e

    async def close(self):
        """Close the underlying HTTP client."""
        await self.client.aclose()
