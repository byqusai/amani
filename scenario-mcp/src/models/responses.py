"""Pydantic response models for Scenario API responses."""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field
from .enums import GenerationStatus, ModelCategory


class AssetInfo(BaseModel):
    """Information about a generated asset."""
    
    id: str = Field(..., description="Unique asset ID")
    url: Optional[str] = Field(None, description="Download URL")
    width: Optional[int] = Field(None, description="Image width")
    height: Optional[int] = Field(None, description="Image height")
    format: Optional[str] = Field(None, description="File format")
    size_bytes: Optional[int] = Field(None, description="File size in bytes")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")


class GenerationJob(BaseModel):
    """Information about a generation job."""
    
    id: str = Field(..., description="Unique job ID")
    status: GenerationStatus = Field(..., description="Current job status")
    progress: Optional[float] = Field(None, ge=0.0, le=1.0, description="Progress percentage")
    estimated_time_remaining: Optional[int] = Field(None, description="ETA in seconds")
    created_at: datetime = Field(..., description="Job creation time")
    completed_at: Optional[datetime] = Field(None, description="Job completion time")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    assets: List[AssetInfo] = Field(default_factory=list, description="Generated assets")
    credits_used: Optional[float] = Field(None, description="Credits consumed")


class ModelInfo(BaseModel):
    """Information about a Scenario model."""
    
    id: str = Field(..., description="Unique model ID")
    name: str = Field(..., description="Model name")
    description: Optional[str] = Field(None, description="Model description")
    category: ModelCategory = Field(..., description="Model category")
    tags: List[str] = Field(default_factory=list, description="Model tags")
    created_by: Optional[str] = Field(None, description="Model creator")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    is_public: bool = Field(default=False, description="Is publicly available")
    supports_controlnet: bool = Field(default=False, description="Supports ControlNet")
    supports_3d: bool = Field(default=False, description="Supports 3D generation")
    supports_video: bool = Field(default=False, description="Supports video generation")
    recommended_settings: Dict[str, Any] = Field(default_factory=dict, description="Recommended parameters")


class CostEstimate(BaseModel):
    """Cost estimation for generation request."""
    
    estimated_credits: float = Field(..., description="Estimated credit cost")
    breakdown: Dict[str, float] = Field(default_factory=dict, description="Cost breakdown by operation")
    current_balance: Optional[float] = Field(None, description="Current account balance")
    sufficient_credits: bool = Field(..., description="Whether account has sufficient credits")


class BatchResult(BaseModel):
    """Result of batch generation operation."""
    
    batch_id: str = Field(..., description="Unique batch ID")
    total_jobs: int = Field(..., description="Total number of jobs in batch")
    completed_jobs: int = Field(default=0, description="Number of completed jobs")
    failed_jobs: int = Field(default=0, description="Number of failed jobs")
    progress: float = Field(default=0.0, ge=0.0, le=1.0, description="Overall batch progress")
    jobs: List[GenerationJob] = Field(default_factory=list, description="Individual job results")
    total_credits_used: Optional[float] = Field(None, description="Total credits consumed")
    started_at: datetime = Field(..., description="Batch start time")
    completed_at: Optional[datetime] = Field(None, description="Batch completion time")


class AssetDownloadResult(BaseModel):
    """Result of asset download operation."""
    
    downloaded_assets: List[Dict[str, Any]] = Field(default_factory=list, description="Successfully downloaded assets")
    failed_downloads: List[Dict[str, str]] = Field(default_factory=list, description="Failed downloads with error messages")
    download_path: str = Field(..., description="Base download path")
    total_size_bytes: int = Field(default=0, description="Total size of downloaded files")
    organization_structure: Dict[str, List[str]] = Field(default_factory=dict, description="File organization structure")


class StandardResponse(BaseModel):
    """Standard response format for MCP tools."""
    
    success: bool = Field(..., description="Whether operation was successful")
    message: str = Field(..., description="Human-readable message")
    data: Optional[Union[Dict[str, Any], List[Any], str, int, float]] = Field(None, description="Response data")
    error_details: Optional[Dict[str, Any]] = Field(None, description="Error details if operation failed")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }