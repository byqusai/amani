"""Custom exceptions for Scenario MCP Server."""

from typing import Optional, Dict, Any


class ScenarioMCPError(Exception):
    """Base exception for all Scenario MCP operations."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class AuthenticationError(ScenarioMCPError):
    """Raised when Scenario API authentication fails."""
    pass


class ValidationError(ScenarioMCPError):
    """Raised when request validation fails."""
    pass


class ScenarioAPIError(ScenarioMCPError):
    """Raised when Scenario API returns an error."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, 
                 response_data: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data or {}


class ConnectionError(ScenarioMCPError):
    """Raised when connection to Scenario API fails."""
    pass


class RateLimitError(ScenarioMCPError):
    """Raised when API rate limit is exceeded."""
    
    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(message)
        self.retry_after = retry_after


class GenerationError(ScenarioMCPError):
    """Raised when image generation fails."""
    pass


class AssetError(ScenarioMCPError):
    """Raised when asset operations fail."""
    pass


class BatchProcessingError(ScenarioMCPError):
    """Raised when batch processing fails."""
    
    def __init__(self, message: str, failed_items: Optional[list] = None):
        super().__init__(message)
        self.failed_items = failed_items or []