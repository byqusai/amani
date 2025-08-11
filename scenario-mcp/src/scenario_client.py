"""Scenario API client with full feature support."""

import asyncio
import aiohttp
import structlog
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

from .config import config
from .utils.auth import AuthenticationManager
from .utils.async_utils import RetryableHTTPClient, poll_until_complete
from .models.requests import *
from .models.responses import *
from .exceptions import *

logger = structlog.get_logger(__name__)


class ScenarioAPIClient:
    """Comprehensive Scenario API client."""
    
    def __init__(self):
        self.config = config
        self.auth_manager = AuthenticationManager(self.config)
        self.http_client: Optional[RetryableHTTPClient] = None
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def initialize(self):
        """Initialize the client."""
        await self.auth_manager.validate_credentials()
        self._session = await self.auth_manager.get_authenticated_session()
        self.http_client = RetryableHTTPClient(self._session)
        logger.info("Scenario API client initialized")
    
    async def close(self):
        """Close the client and cleanup resources."""
        await self.auth_manager.close()
        if self._session and not self._session.closed:
            await self._session.close()
        logger.info("Scenario API client closed")
    
    # GENERATION METHODS
    
    async def text_to_image(self, request: TextToImageRequest) -> GenerationJob:
        """Generate images from text prompt."""
        try:
            logger.info(f"Starting text-to-image generation: {request.prompt[:50]}...")
            
            # Prepare request payload
            payload = {
                "prompt": request.prompt,
                "modelId": request.model_id,
                "numSamples": request.num_samples,
                "width": request.width,
                "height": request.height,
                "guidance": request.guidance,
                "numInferenceSteps": request.num_inference_steps,
                "scheduler": request.scheduler.value
            }
            
            if request.negative_prompt:
                payload["negativePrompt"] = request.negative_prompt
            if request.seed is not None:
                payload["seed"] = request.seed
            
            # Submit generation request
            response = await self.http_client.post_json(
                f"{self.config.scenario_api_base_url}/generate/txt2img",
                payload
            )
            
            # Parse response
            job_id = response.get("inference", {}).get("id")
            if not job_id:
                raise GenerationError("No job ID returned from API")
            
            logger.info(f"Text-to-image job submitted: {job_id}")
            
            # Return initial job info
            return GenerationJob(
                id=job_id,
                status=GenerationStatus.PENDING,
                created_at=datetime.now(),
                assets=[]
            )
        
        except Exception as e:
            logger.error(f"Text-to-image generation failed: {str(e)}")
            raise GenerationError(f"Generation failed: {str(e)}")
    
    async def image_to_image(self, request: ImageToImageRequest) -> GenerationJob:
        """Generate images from input image and text prompt."""
        try:
            logger.info(f"Starting image-to-image generation: {request.prompt[:50]}...")
            
            payload = {
                "prompt": request.prompt,
                "image": request.input_image,
                "strength": request.strength,
                "modelId": request.model_id,
                "guidance": request.guidance,
                "numInferenceSteps": request.num_inference_steps
            }
            
            if request.negative_prompt:
                payload["negativePrompt"] = request.negative_prompt
            if request.seed is not None:
                payload["seed"] = request.seed
            
            response = await self.http_client.post_json(
                f"{self.config.scenario_api_base_url}/generate/img2img",
                payload
            )
            
            job_id = response.get("inference", {}).get("id")
            if not job_id:
                raise GenerationError("No job ID returned from API")
            
            logger.info(f"Image-to-image job submitted: {job_id}")
            
            return GenerationJob(
                id=job_id,
                status=GenerationStatus.PENDING,
                created_at=datetime.now(),
                assets=[]
            )
        
        except Exception as e:
            logger.error(f"Image-to-image generation failed: {str(e)}")
            raise GenerationError(f"Generation failed: {str(e)}")
    
    async def controlnet_generate(self, request: ControlNetRequest) -> GenerationJob:
        """Generate images with ControlNet guidance."""
        try:
            logger.info(f"Starting ControlNet generation ({request.control_type}): {request.prompt[:50]}...")
            
            payload = {
                "prompt": request.prompt,
                "controlImage": request.control_image,
                "controlType": request.control_type.value,
                "modelId": request.model_id,
                "strength": request.strength,
                "guidance": request.guidance,
                "numInferenceSteps": request.num_inference_steps
            }
            
            if request.negative_prompt:
                payload["negativePrompt"] = request.negative_prompt
            
            response = await self.http_client.post_json(
                f"{self.config.scenario_api_base_url}/generate/controlnet",
                payload
            )
            
            job_id = response.get("inference", {}).get("id")
            if not job_id:
                raise GenerationError("No job ID returned from API")
            
            logger.info(f"ControlNet job submitted: {job_id}")
            
            return GenerationJob(
                id=job_id,
                status=GenerationStatus.PENDING,
                created_at=datetime.now(),
                assets=[]
            )
        
        except Exception as e:
            logger.error(f"ControlNet generation failed: {str(e)}")
            raise GenerationError(f"Generation failed: {str(e)}")
    
    async def generate_video(self, request: VideoGenerationRequest) -> GenerationJob:
        """Generate video from text prompt."""
        try:
            logger.info(f"Starting video generation: {request.prompt[:50]}...")
            
            payload = {
                "prompt": request.prompt,
                "duration": request.duration,
                "fps": request.fps,
                "width": request.width,
                "height": request.height,
                "modelId": request.model_id,
                "guidance": request.guidance
            }
            
            if request.seed is not None:
                payload["seed"] = request.seed
            
            response = await self.http_client.post_json(
                f"{self.config.scenario_api_base_url}/generate/video",
                payload
            )
            
            job_id = response.get("inference", {}).get("id")
            if not job_id:
                raise GenerationError("No job ID returned from API")
            
            logger.info(f"Video generation job submitted: {job_id}")
            
            return GenerationJob(
                id=job_id,
                status=GenerationStatus.PENDING,
                created_at=datetime.now(),
                assets=[]
            )
        
        except Exception as e:
            logger.error(f"Video generation failed: {str(e)}")
            raise GenerationError(f"Generation failed: {str(e)}")
    
    async def generate_3d(self, request: ThreeDGenerationRequest) -> GenerationJob:
        """Generate 3D model from text prompt."""
        try:
            logger.info(f"Starting 3D generation: {request.prompt[:50]}...")
            
            payload = {
                "prompt": request.prompt,
                "modelType": request.model_type.value,
                "resolution": request.resolution,
                "viewAngles": request.view_angles,
                "generateTextures": request.generate_textures,
                "generateMaterials": request.generate_materials,
                "modelId": request.model_id
            }
            
            response = await self.http_client.post_json(
                f"{self.config.scenario_api_base_url}/generate/3d-model",
                payload
            )
            
            job_id = response.get("inference", {}).get("id")
            if not job_id:
                raise GenerationError("No job ID returned from API")
            
            logger.info(f"3D generation job submitted: {job_id}")
            
            return GenerationJob(
                id=job_id,
                status=GenerationStatus.PENDING,
                created_at=datetime.now(),
                assets=[]
            )
        
        except Exception as e:
            logger.error(f"3D generation failed: {str(e)}")
            raise GenerationError(f"Generation failed: {str(e)}")
    
    # STATUS AND MONITORING
    
    async def get_generation_status(self, job_id: str) -> GenerationJob:
        """Get status of a generation job."""
        try:
            response = await self.http_client.get_json(
                f"{self.config.scenario_api_base_url}/generations/{job_id}"
            )
            
            # Parse job status
            status_str = response.get("status", "pending").lower()
            if status_str == "completed":
                status = GenerationStatus.COMPLETED
            elif status_str in ["processing", "running"]:
                status = GenerationStatus.PROCESSING
            elif status_str in ["failed", "error"]:
                status = GenerationStatus.FAILED
            else:
                status = GenerationStatus.PENDING
            
            # Parse assets
            assets = []
            asset_data = response.get("images", []) or response.get("assets", [])
            for asset in asset_data:
                assets.append(AssetInfo(
                    id=asset.get("id", ""),
                    url=asset.get("url"),
                    width=asset.get("width"),
                    height=asset.get("height"),
                    format=asset.get("format"),
                    size_bytes=asset.get("size")
                ))
            
            return GenerationJob(
                id=job_id,
                status=status,
                progress=response.get("progress", 0.0),
                created_at=datetime.fromisoformat(response.get("createdAt", datetime.now().isoformat())),
                completed_at=datetime.fromisoformat(response.get("completedAt")) if response.get("completedAt") else None,
                error_message=response.get("errorMessage"),
                assets=assets,
                credits_used=response.get("creditsUsed")
            )
        
        except Exception as e:
            logger.error(f"Failed to get generation status for {job_id}: {str(e)}")
            raise GenerationError(f"Status check failed: {str(e)}")
    
    async def wait_for_completion(self, job_id: str, 
                                max_wait_time: int = 300) -> GenerationJob:
        """Wait for generation job to complete."""
        logger.info(f"Waiting for completion of job: {job_id}")
        
        async def check_status():
            return await self.get_generation_status(job_id)
        
        try:
            result = await poll_until_complete(
                check_status,
                check_interval=2.0,
                max_attempts=max_wait_time // 2
            )
            return result
        except TimeoutError:
            logger.error(f"Job {job_id} did not complete within {max_wait_time} seconds")
            raise GenerationError(f"Generation timed out after {max_wait_time} seconds")
    
    # MODEL MANAGEMENT
    
    async def list_models(self, category: Optional[str] = None, 
                         search_term: Optional[str] = None,
                         limit: int = 50) -> List[ModelInfo]:
        """List available models."""
        try:
            params = {"limit": limit}
            if category:
                params["category"] = category
            if search_term:
                params["search"] = search_term
            
            response = await self.http_client.get_json(
                f"{self.config.scenario_api_base_url}/models",
                params=params
            )
            
            models = []
            for model_data in response.get("models", []):
                models.append(ModelInfo(
                    id=model_data.get("id", ""),
                    name=model_data.get("name", ""),
                    description=model_data.get("description"),
                    category=ModelCategory(model_data.get("category", "public")),
                    tags=model_data.get("tags", []),
                    created_by=model_data.get("createdBy"),
                    is_public=model_data.get("isPublic", False),
                    supports_controlnet=model_data.get("supportsControlNet", False),
                    supports_3d=model_data.get("supports3D", False),
                    supports_video=model_data.get("supportsVideo", False),
                    recommended_settings=model_data.get("recommendedSettings", {})
                ))
            
            logger.info(f"Retrieved {len(models)} models")
            return models
        
        except Exception as e:
            logger.error(f"Failed to list models: {str(e)}")
            raise ScenarioAPIError(f"Model listing failed: {str(e)}")
    
    async def get_model_info(self, model_id: str) -> ModelInfo:
        """Get detailed information about a specific model."""
        try:
            response = await self.http_client.get_json(
                f"{self.config.scenario_api_base_url}/models/{model_id}"
            )
            
            return ModelInfo(
                id=response.get("id", ""),
                name=response.get("name", ""),
                description=response.get("description"),
                category=ModelCategory(response.get("category", "public")),
                tags=response.get("tags", []),
                created_by=response.get("createdBy"),
                is_public=response.get("isPublic", False),
                supports_controlnet=response.get("supportsControlNet", False),
                supports_3d=response.get("supports3D", False),
                supports_video=response.get("supportsVideo", False),
                recommended_settings=response.get("recommendedSettings", {})
            )
        
        except Exception as e:
            logger.error(f"Failed to get model info for {model_id}: {str(e)}")
            raise ScenarioAPIError(f"Model info retrieval failed: {str(e)}")
    
    # COST ESTIMATION
    
    async def estimate_cost(self, generation_params: Dict[str, Any]) -> CostEstimate:
        """Estimate cost for generation request."""
        try:
            # Add dryRun parameter to estimate cost without executing
            params = {**generation_params, "dryRun": True}
            
            # Use txt2img endpoint for estimation (works for most generation types)
            response = await self.http_client.post_json(
                f"{self.config.scenario_api_base_url}/generate/txt2img",
                params
            )
            
            estimated_credits = response.get("estimatedCredits", 0.0)
            breakdown = response.get("costBreakdown", {})
            
            return CostEstimate(
                estimated_credits=estimated_credits,
                breakdown=breakdown,
                sufficient_credits=True  # We don't have balance info from dry run
            )
        
        except Exception as e:
            logger.error(f"Cost estimation failed: {str(e)}")
            raise ScenarioAPIError(f"Cost estimation failed: {str(e)}")
    
    # ASSET MANAGEMENT
    
    async def list_assets(self, filter_by: Optional[Dict[str, Any]] = None,
                         sort_by: str = "created_at", limit: int = 50) -> List[AssetInfo]:
        """List user's generated assets."""
        try:
            params = {"limit": limit, "sort": sort_by}
            if filter_by:
                params.update(filter_by)
            
            response = await self.http_client.get_json(
                f"{self.config.scenario_api_base_url}/assets",
                params=params
            )
            
            assets = []
            for asset_data in response.get("assets", []):
                assets.append(AssetInfo(
                    id=asset_data.get("id", ""),
                    url=asset_data.get("url"),
                    width=asset_data.get("width"),
                    height=asset_data.get("height"),
                    format=asset_data.get("format"),
                    size_bytes=asset_data.get("size"),
                    created_at=datetime.fromisoformat(asset_data.get("createdAt", datetime.now().isoformat()))
                ))
            
            logger.info(f"Retrieved {len(assets)} assets")
            return assets
        
        except Exception as e:
            logger.error(f"Failed to list assets: {str(e)}")
            raise AssetError(f"Asset listing failed: {str(e)}")