"""Input validation utilities."""

import re
from typing import Any, Dict, List, Optional, Type, TypeVar
from pydantic import BaseModel, ValidationError
from ..exceptions import ValidationError as ScenarioValidationError

T = TypeVar('T', bound=BaseModel)


def validate_request(request_data: Dict[str, Any], model_class: Type[T]) -> T:
    """Validate request data against Pydantic model."""
    try:
        return model_class(**request_data)
    except ValidationError as e:
        # Convert Pydantic ValidationError to our custom exception
        errors = []
        for error in e.errors():
            field = ".".join(str(x) for x in error["loc"])
            message = error["msg"]
            errors.append(f"{field}: {message}")
        
        raise ScenarioValidationError(
            f"Request validation failed: {'; '.join(errors)}",
            details={"validation_errors": e.errors()}
        )


def validate_prompt(prompt: str, max_length: int = 2000) -> str:
    """Validate and clean a text prompt."""
    if not prompt or not prompt.strip():
        raise ScenarioValidationError("Prompt cannot be empty")
    
    cleaned = prompt.strip()
    
    if len(cleaned) > max_length:
        raise ScenarioValidationError(f"Prompt exceeds maximum length of {max_length} characters")
    
    # Check for potentially problematic characters
    if '\x00' in cleaned:
        raise ScenarioValidationError("Prompt contains null characters")
    
    return cleaned


def validate_image_dimensions(width: int, height: int, 
                            min_size: int = 64, max_size: int = 2048) -> tuple[int, int]:
    """Validate image dimensions."""
    if width < min_size or width > max_size:
        raise ScenarioValidationError(f"Width must be between {min_size} and {max_size}")
    
    if height < min_size or height > max_size:
        raise ScenarioValidationError(f"Height must be between {min_size} and {max_size}")
    
    if width % 64 != 0 or height % 64 != 0:
        raise ScenarioValidationError("Dimensions must be multiples of 64")
    
    return width, height


def validate_model_id(model_id: str) -> str:
    """Validate model ID format."""
    if not model_id or not model_id.strip():
        raise ScenarioValidationError("Model ID cannot be empty")
    
    cleaned = model_id.strip()
    
    # Basic validation - alphanumeric, hyphens, dots, underscores
    if not re.match(r'^[a-zA-Z0-9._-]+$', cleaned):
        raise ScenarioValidationError("Model ID contains invalid characters")
    
    return cleaned


def validate_file_path(file_path: str) -> str:
    """Validate file path for security."""
    if not file_path or not file_path.strip():
        raise ScenarioValidationError("File path cannot be empty")
    
    cleaned = file_path.strip()
    
    # Check for path traversal attempts
    if '..' in cleaned or cleaned.startswith('/'):
        raise ScenarioValidationError("Invalid file path - path traversal not allowed")
    
    return cleaned


def validate_url_or_base64(data: str) -> tuple[str, str]:
    """Validate if string is URL or base64 image data."""
    if not data or not data.strip():
        raise ScenarioValidationError("Image data cannot be empty")
    
    cleaned = data.strip()
    
    # Check if it's a URL
    if cleaned.startswith(('http://', 'https://')):
        if not re.match(r'^https?://[^\s/$.?#].[^\s]*$', cleaned):
            raise ScenarioValidationError("Invalid URL format")
        return 'url', cleaned
    
    # Check if it's base64 data
    if cleaned.startswith('data:image/'):
        # Extract base64 part
        if ',' not in cleaned:
            raise ScenarioValidationError("Invalid base64 image format")
        
        header, data_part = cleaned.split(',', 1)
        
        # Validate base64
        import base64
        try:
            base64.b64decode(data_part, validate=True)
            return 'base64', cleaned
        except Exception:
            raise ScenarioValidationError("Invalid base64 image data")
    
    raise ScenarioValidationError("Image data must be a URL or base64 encoded image")


def validate_asset_ids(asset_ids: List[str]) -> List[str]:
    """Validate list of asset IDs."""
    if not asset_ids:
        raise ScenarioValidationError("Asset IDs list cannot be empty")
    
    validated = []
    for asset_id in asset_ids:
        if not asset_id or not asset_id.strip():
            continue
        
        cleaned = asset_id.strip()
        
        # Basic UUID-like validation (common format for asset IDs)
        if not re.match(r'^[a-zA-Z0-9_-]+$', cleaned):
            raise ScenarioValidationError(f"Invalid asset ID format: {cleaned}")
        
        validated.append(cleaned)
    
    if not validated:
        raise ScenarioValidationError("No valid asset IDs provided")
    
    return validated


def validate_batch_size(prompts: List[str], max_batch_size: int = 50) -> int:
    """Validate batch size."""
    if not prompts:
        raise ScenarioValidationError("Batch cannot be empty")
    
    if len(prompts) > max_batch_size:
        raise ScenarioValidationError(f"Batch size exceeds maximum of {max_batch_size}")
    
    return len(prompts)