"""Authentication utilities for Scenario API."""

import asyncio
import aiohttp
import structlog
from typing import Optional, Dict, Any
from ..config import ScenarioMCPConfig
from ..exceptions import AuthenticationError

logger = structlog.get_logger(__name__)


class AuthenticationManager:
    """Manages authentication for Scenario API."""
    
    def __init__(self, config: ScenarioMCPConfig):
        self.config = config
        self._validated = False
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def validate_credentials(self) -> bool:
        """Validate API credentials with Scenario API."""
        try:
            if not self.config.scenario_api_key or not self.config.scenario_api_secret:
                logger.warning("No API credentials provided")
                return False
            
            # Test authentication with a simple API call
            headers = self._get_auth_headers()
            timeout = aiohttp.ClientTimeout(total=10.0)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                # Try to access the models endpoint to validate auth
                async with session.get(
                    f"{self.config.scenario_api_base_url}/models",
                    headers=headers,
                    params={"limit": 1}
                ) as response:
                    if response.status == 200:
                        self._validated = True
                        logger.info("API credentials validated successfully")
                        return True
                    elif response.status == 401:
                        logger.error("Invalid API credentials")
                        return False
                    else:
                        logger.warning(f"Unexpected response during auth validation: {response.status}")
                        # Assume valid if not explicitly unauthorized
                        self._validated = True
                        return True
        
        except asyncio.TimeoutError:
            logger.error("Timeout during credential validation")
            raise AuthenticationError("Authentication validation timed out")
        except Exception as e:
            logger.error(f"Error during credential validation: {str(e)}")
            raise AuthenticationError(f"Failed to validate credentials: {str(e)}")
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        return {
            "Authorization": self.config.auth_header,
            "Content-Type": "application/json",
            "User-Agent": "scenario-mcp/1.0.0"
        }
    
    def require_auth(self, func):
        """Decorator to require authentication for operations."""
        async def wrapper(*args, **kwargs):
            if not self._validated:
                # Try to validate if not already done
                if not await self.validate_credentials():
                    raise AuthenticationError("Valid authentication required")
            return await func(*args, **kwargs)
        return wrapper
    
    async def get_authenticated_session(self) -> aiohttp.ClientSession:
        """Get an authenticated HTTP session."""
        if not self._validated and not await self.validate_credentials():
            raise AuthenticationError("Authentication required")
        
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(
                limit=self.config.connection_pool_size,
                limit_per_host=5,
                ttl_dns_cache=300,
                use_dns_cache=True
            )
            
            timeout = aiohttp.ClientTimeout(total=self.config.request_timeout)
            
            self._session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers=self._get_auth_headers()
            )
        
        return self._session
    
    async def close(self):
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None
    
    @property
    def is_authenticated(self) -> bool:
        """Check if credentials are validated."""
        return self._validated