"""Response formatting utilities."""

from typing import Any, Dict, Optional
from datetime import datetime
from models.responses import StandardResponse


class ResponseHelper:
    """Helper class for standardized response formatting."""
    
    @staticmethod
    def success(message: str, data: Any = None) -> Dict[str, Any]:
        """Create a successful response."""
        response = StandardResponse(
            success=True,
            message=message,
            data=data,
            timestamp=datetime.now()
        )
        return response.model_dump()
    
    @staticmethod
    def error(message: str, error_details: Optional[Dict[str, Any]] = None, 
              data: Any = None) -> Dict[str, Any]:
        """Create an error response."""
        response = StandardResponse(
            success=False,
            message=message,
            data=data,
            error_details=error_details,
            timestamp=datetime.now()
        )
        return response.model_dump()
    
    @staticmethod
    def validation_error(field: str, error: str) -> Dict[str, Any]:
        """Create a validation error response."""
        return ResponseHelper.error(
            f"Validation error for field '{field}'",
            error_details={
                "field": field,
                "error": error,
                "type": "validation_error"
            }
        )
    
    @staticmethod
    def api_error(status_code: int, message: str, 
                  response_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create an API error response."""
        return ResponseHelper.error(
            f"Scenario API error: {message}",
            error_details={
                "status_code": status_code,
                "api_response": response_data,
                "type": "api_error"
            }
        )
    
    @staticmethod
    def authentication_error(message: str = "Authentication failed") -> Dict[str, Any]:
        """Create an authentication error response."""
        return ResponseHelper.error(
            message,
            error_details={
                "type": "authentication_error",
                "suggestion": "Check SCENARIO_API_KEY and SCENARIO_API_SECRET environment variables"
            }
        )
    
    @staticmethod
    def rate_limit_error(retry_after: Optional[int] = None) -> Dict[str, Any]:
        """Create a rate limit error response."""
        message = "Rate limit exceeded"
        error_details = {"type": "rate_limit_error"}
        
        if retry_after:
            message += f". Retry after {retry_after} seconds"
            error_details["retry_after"] = retry_after
            
        return ResponseHelper.error(message, error_details)
    
    @staticmethod
    def timeout_error(operation: str) -> Dict[str, Any]:
        """Create a timeout error response."""
        return ResponseHelper.error(
            f"Operation timed out: {operation}",
            error_details={
                "type": "timeout_error",
                "operation": operation
            }
        )
    
    @staticmethod
    def batch_partial_success(completed: int, failed: int, 
                            results: Dict[str, Any]) -> Dict[str, Any]:
        """Create a partial success response for batch operations."""
        total = completed + failed
        success_rate = (completed / total) * 100 if total > 0 else 0
        
        return ResponseHelper.success(
            f"Batch completed: {completed}/{total} successful ({success_rate:.1f}%)",
            data={
                "completed": completed,
                "failed": failed,
                "total": total,
                "success_rate": success_rate,
                "results": results
            }
        )