"""Pydantic request models for Scenario API calls."""

from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from .enums import SchedulerType, ControlNetType, ModelType, AssetOrganization


class TextToImageRequest(BaseModel):
    """Request model for text-to-image generation."""
    
    prompt: str = Field(..., min_length=1, max_length=2000, description="Text prompt for generation")
    model_id: str = Field(default="flux.1-dev", description="Model ID to use for generation")
    num_samples: int = Field(default=1, ge=1, le=10, description="Number of images to generate")
    width: int = Field(default=1024, ge=64, le=2048, description="Image width")
    height: int = Field(default=1024, ge=64, le=2048, description="Image height")
    guidance: float = Field(default=3.5, ge=0.1, le=30.0, description="Guidance scale")
    num_inference_steps: int = Field(default=28, ge=1, le=150, description="Number of inference steps")
    scheduler: SchedulerType = Field(default=SchedulerType.EULER_ANCESTRAL_DISCRETE, description="Sampling scheduler")
    negative_prompt: Optional[str] = Field(None, max_length=1000, description="Negative prompt")
    seed: Optional[int] = Field(None, description="Random seed for reproducibility")
    
    @validator('prompt')
    def validate_prompt(cls, v):
        if not v.strip():
            raise ValueError("Prompt cannot be empty or whitespace only")
        return v.strip()
    
    @validator('width', 'height')
    def validate_dimensions(cls, v):
        if v % 64 != 0:
            raise ValueError("Dimensions must be multiples of 64")
        return v


class ImageToImageRequest(BaseModel):
    """Request model for image-to-image generation."""
    
    prompt: str = Field(..., min_length=1, max_length=2000)
    input_image: str = Field(..., description="Input image URL or base64 string")
    strength: float = Field(default=0.8, ge=0.1, le=1.0, description="Transformation strength")
    model_id: str = Field(default="flux.1-dev")
    guidance: float = Field(default=7.5, ge=0.1, le=30.0)
    num_inference_steps: int = Field(default=50, ge=1, le=150)
    negative_prompt: Optional[str] = Field(None, max_length=1000)
    seed: Optional[int] = None


class ControlNetRequest(BaseModel):
    """Request model for ControlNet generation."""
    
    prompt: str = Field(..., min_length=1, max_length=2000)
    control_image: str = Field(..., description="Control image URL or base64")
    control_type: ControlNetType = Field(..., description="Type of control")
    model_id: str = Field(..., description="Model ID with ControlNet support")
    strength: float = Field(default=1.0, ge=0.1, le=2.0, description="Control strength")
    guidance: float = Field(default=7.5, ge=0.1, le=30.0)
    num_inference_steps: int = Field(default=50, ge=1, le=150)
    negative_prompt: Optional[str] = Field(None, max_length=1000)


class VideoGenerationRequest(BaseModel):
    """Request model for video generation."""
    
    prompt: str = Field(..., min_length=1, max_length=2000)
    duration: int = Field(default=3, ge=1, le=30, description="Duration in seconds")
    fps: int = Field(default=24, ge=8, le=60, description="Frames per second")
    model_id: str = Field(default="video-gen-v1")
    width: int = Field(default=512, ge=256, le=1024)
    height: int = Field(default=512, ge=256, le=1024)
    guidance: float = Field(default=7.5, ge=0.1, le=30.0)
    seed: Optional[int] = None


class ThreeDGenerationRequest(BaseModel):
    """Request model for 3D model generation."""
    
    prompt: str = Field(..., min_length=1, max_length=2000)
    model_type: ModelType = Field(default=ModelType.MESH)
    resolution: int = Field(default=512, ge=128, le=1024, description="Texture resolution")
    view_angles: List[str] = Field(default=["front", "side", "back"], description="Required view angles")
    generate_textures: bool = Field(default=True)
    generate_materials: bool = Field(default=True)
    model_id: str = Field(default="3d-gen-v1")


class BatchGenerationRequest(BaseModel):
    """Request model for batch generation."""
    
    prompts: List[str] = Field(..., min_items=1, max_items=50, description="List of prompts to process")
    model_id: str = Field(..., description="Model ID for all generations")
    batch_settings: Dict[str, Any] = Field(default_factory=dict, description="Shared settings for all generations")
    max_concurrent: int = Field(default=5, ge=1, le=10, description="Maximum concurrent requests")
    
    @validator('prompts')
    def validate_prompts(cls, v):
        cleaned = []
        for prompt in v:
            if not prompt.strip():
                continue
            cleaned.append(prompt.strip())
        if not cleaned:
            raise ValueError("At least one valid prompt is required")
        return cleaned


class AssetDownloadRequest(BaseModel):
    """Request model for asset download."""
    
    asset_ids: List[str] = Field(..., min_items=1, description="List of asset IDs to download")
    download_path: str = Field(..., description="Local path for downloads")
    organize_by: AssetOrganization = Field(default=AssetOrganization.DATE)
    create_metadata: bool = Field(default=True, description="Create JSON metadata files")
    overwrite_existing: bool = Field(default=False, description="Overwrite existing files")


class ModelTrainingRequest(BaseModel):
    """Request model for custom model training."""
    
    model_name: str = Field(..., min_length=1, max_length=100)
    training_images: List[str] = Field(..., min_items=5, max_items=100, description="URLs or paths to training images")
    base_model: str = Field(..., description="Base model to fine-tune")
    training_config: Dict[str, Any] = Field(default_factory=dict)
    description: Optional[str] = Field(None, max_length=500)
    tags: List[str] = Field(default_factory=list, max_items=10)
    
    @validator('model_name')
    def validate_model_name(cls, v):
        # Only allow alphanumeric, hyphens, underscores
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError("Model name can only contain letters, numbers, hyphens, and underscores")
        return v