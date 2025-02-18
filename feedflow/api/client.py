"""Inoreader API client implementation."""

from typing import Any, Optional
import os
from datetime import datetime

import requests
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class APIConfig(BaseModel):
    """Configuration for the Inoreader API client."""
    
    app_id: str = Field(..., description="Inoreader API App ID")
    app_key: str = Field(..., description="Inoreader API App Key")
    base_url: str = Field(
        default="https://www.inoreader.com/reader/api/0",
        description="Base URL for the Inoreader API"
    )
    zone1_limit: int = Field(
        default=100,
        description="API Zone 1 daily request limit"
    )
    zone2_limit: int = Field(
        default=100,
        description="API Zone 2 daily request limit"
    )

class InoreaderClient:
    """Client for interacting with the Inoreader API."""
    
    def __init__(self) -> None:
        """Initialize the Inoreader API client."""
        self.config = APIConfig(
            app_id=os.getenv("INOREADER_APP_ID", ""),
            app_key=os.getenv("INOREADER_APP_KEY", ""),
            zone1_limit=int(os.getenv("INOREADER_ZONE1_LIMIT", "100")),
            zone2_limit=int(os.getenv("INOREADER_ZONE2_LIMIT", "100"))
        )
        self.session = requests.Session()
        self.session.headers.update({
            "AppId": self.config.app_id,
            "AppKey": self.config.app_key,
            "User-Agent": f"FeedFlow/0.1.0 (https://github.com/trentleslie/feedflow)"
        })
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
        **kwargs: Any
    ) -> requests.Response:
        """Make a request to the Inoreader API.
        
        Args:
            method: HTTP method to use
            endpoint: API endpoint to call
            params: Optional query parameters
            json: Optional JSON body
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Response from the API
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = f"{self.config.base_url}/{endpoint.lstrip('/')}"
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            **kwargs
        )
        response.raise_for_status()
        return response

    def get_user_info(self) -> dict[str, Any]:
        """Get information about the authenticated user.
        
        Returns:
            User information from the API
        """
        response = self._make_request("GET", "/user-info")
        return dict(response.json())

    def get_subscription_list(self) -> dict[str, Any]:
        """Get the list of user's subscriptions.
        
        Returns:
            List of subscriptions from the API
        """
        response = self._make_request("GET", "/subscription/list")
        return dict(response.json())
