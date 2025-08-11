"""Text-to-image generation MCP tools."""

import structlog
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import Context

from ..utils.response import ResponseHelper
from ..utils.validation import validate_request
from ..models.requests import TextToImageRequest
from ..scenario_client import ScenarioAPIClient
from ..exceptions import *

logger = structlog.get_logger(__name__)


def register_text_to_image_tools(mcp):
    """Register text-to-image generation tools."""
    
    @mcp.tool()
    async def scenario_text_to_image(
        ctx: Context,
        prompt: str,
        model_id: str = "flux.1-dev",
        num_samples: int = 1,
        width: int = 1024,
        height: int = 1024,
        guidance: float = 3.5,
        num_inference_steps: int = 28,
        scheduler: str = "EulerAncestralDiscrete",
        negative_prompt: Optional[str] = None,
        seed: Optional[int] = None,
        wait_for_completion: bool = True
    ) -> Dict[str, Any]:
        """
        Generate images from text prompts using Scenario API.
        
        Perfect for Agent 4's text-to-image generation workflows.
        
        Args:
            prompt: Text description for image generation (required)
            model_id: Scenario model ID to use (default: flux.1-dev)
            num_samples: Number of images to generate (1-10)
            width: Image width in pixels, must be multiple of 64 (64-2048)
            height: Image height in pixels, must be multiple of 64 (64-2048)
            guidance: Guidance scale for generation (0.1-30.0)
            num_inference_steps: Number of inference steps (1-150)
            scheduler: Sampling scheduler type
            negative_prompt: Negative prompt to avoid certain elements
            seed: Random seed for reproducible results
            wait_for_completion: Wait for generation to complete (default: True)
            
        Returns:
            Dict containing job information and generated assets
        """
        try:
            # Validate request
            request_data = {
                "prompt": prompt,
                "model_id": model_id,
                "num_samples": num_samples,
                "width": width,
                "height": height,
                "guidance": guidance,
                "num_inference_steps": num_inference_steps,
                "scheduler": scheduler,
                "negative_prompt": negative_prompt,
                "seed": seed
            }
            
            request = validate_request(request_data, TextToImageRequest)
            
            # Execute generation
            async with ScenarioAPIClient() as client:
                job = await client.text_to_image(request)
                
                if wait_for_completion:
                    # Wait for completion and get final results
                    completed_job = await client.wait_for_completion(job.id)
                    
                    return ResponseHelper.success(
                        f"Generated {len(completed_job.assets)} images successfully",
                        data={
                            "job_id": completed_job.id,
                            "status": completed_job.status.value,
                            "assets": [
                                {
                                    "id": asset.id,
                                    "url": asset.url,
                                    "width": asset.width,
                                    "height": asset.height,
                                    "format": asset.format
                                }
                                for asset in completed_job.assets
                            ],
                            "credits_used": completed_job.credits_used,
                            "generation_time": (completed_job.completed_at - completed_job.created_at).total_seconds() if completed_job.completed_at else None
                        }
                    )
                else:
                    # Return job ID for monitoring
                    return ResponseHelper.success(
                        f"Text-to-image generation started",
                        data={
                            "job_id": job.id,
                            "status": job.status.value,
                            "created_at": job.created_at.isoformat()
                        }
                    )
        
        except ValidationError as e:
            return ResponseHelper.validation_error("text_to_image_request", str(e))
        except AuthenticationError as e:
            return ResponseHelper.authentication_error(str(e))
        except GenerationError as e:
            return ResponseHelper.error(f"Generation failed: {str(e)}")
        except Exception as e:
            logger.exception("Unexpected error in scenario_text_to_image")
            return ResponseHelper.error(f"Unexpected error: {str(e)}")
    
    @mcp.tool()
    async def scenario_text_to_image_variations(
        ctx: Context,
        base_prompt: str,
        variations: List[str],
        model_id: str = "flux.1-dev",
        shared_settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate multiple variations of a base prompt efficiently.
        
        Perfect for Agent 4's prompt variation workflows.
        
        Args:
            base_prompt: Base text prompt
            variations: List of prompt variations or additions
            model_id: Model to use for all generations
            shared_settings: Shared generation settings for all variations
            
        Returns:
            Dict containing results for all variations
        """
        try:
            if not variations:
                return ResponseHelper.validation_error("variations", "At least one variation is required")
            
            default_settings = {
                "width": 1024,
                "height": 1024,
                "guidance": 3.5,
                "num_inference_steps": 28,
                "scheduler": "EulerAncestralDiscrete",
                "num_samples": 1
            }
            
            if shared_settings:
                default_settings.update(shared_settings)
            
            results = []
            total_assets = 0
            total_credits = 0.0
            
            async with ScenarioAPIClient() as client:
                for i, variation in enumerate(variations):
                    try:
                        # Combine base prompt with variation
                        if variation.startswith('+'):
                            # Additive variation: "base prompt, additional element"
                            full_prompt = f"{base_prompt}, {variation[1:].strip()}"
                        elif variation.startswith('='):
                            # Replacement variation: use variation as full prompt
                            full_prompt = variation[1:].strip()
                        else:
                            # Default: append variation to base
                            full_prompt = f"{base_prompt} {variation}"
                        
                        # Create request
                        request_data = {
                            "prompt": full_prompt,
                            "model_id": model_id,
                            **default_settings
                        }
                        request = validate_request(request_data, TextToImageRequest)
                        
                        # Generate and wait for completion
                        job = await client.text_to_image(request)
                        completed_job = await client.wait_for_completion(job.id)
                        
                        # Store result
                        variation_result = {
                            "variation_index": i,
                            "original_variation": variation,
                            "full_prompt": full_prompt,
                            "job_id": completed_job.id,
                            "status": completed_job.status.value,
                            "assets": [
                                {
                                    "id": asset.id,
                                    "url": asset.url,
                                    "width": asset.width,
                                    "height": asset.height
                                }
                                for asset in completed_job.assets
                            ],
                            "credits_used": completed_job.credits_used or 0
                        }
                        
                        results.append(variation_result)
                        total_assets += len(completed_job.assets)
                        total_credits += completed_job.credits_used or 0
                        
                        logger.info(f"Completed variation {i+1}/{len(variations)}: {variation}")
                    
                    except Exception as e:
                        logger.error(f"Failed variation {i+1}: {variation} - {str(e)}")
                        results.append({
                            "variation_index": i,
                            "original_variation": variation,
                            "error": str(e),
                            "status": "failed"
                        })
            
            # Summary
            successful_variations = len([r for r in results if r.get("status") != "failed"])
            
            return ResponseHelper.success(
                f"Generated {successful_variations}/{len(variations)} variations successfully",
                data={
                    "base_prompt": base_prompt,
                    "total_variations": len(variations),
                    "successful_variations": successful_variations,
                    "total_assets_generated": total_assets,
                    "total_credits_used": total_credits,
                    "results": results,
                    "shared_settings": default_settings
                }
            )
        
        except Exception as e:
            logger.exception("Unexpected error in scenario_text_to_image_variations")
            return ResponseHelper.error(f"Variations generation failed: {str(e)}")
    
    @mcp.tool()
    async def scenario_estimate_text_to_image_cost(
        ctx: Context,
        prompt: str,
        model_id: str = "flux.1-dev",
        num_samples: int = 1,
        width: int = 1024,
        height: int = 1024,
        num_inference_steps: int = 28
    ) -> Dict[str, Any]:
        """
        Estimate cost for text-to-image generation without executing.
        
        Perfect for Agent 4's cost planning and budget management.
        
        Args:
            prompt: Text prompt for generation
            model_id: Model ID to use
            num_samples: Number of images to generate
            width: Image width
            height: Image height
            num_inference_steps: Number of inference steps
            
        Returns:
            Dict containing cost estimation details
        """
        try:
            generation_params = {
                "prompt": prompt,
                "modelId": model_id,
                "numSamples": num_samples,
                "width": width,
                "height": height,
                "numInferenceSteps": num_inference_steps
            }
            
            async with ScenarioAPIClient() as client:
                cost_estimate = await client.estimate_cost(generation_params)
                
                return ResponseHelper.success(
                    f"Estimated cost: {cost_estimate.estimated_credits} credits",
                    data={
                        "estimated_credits": cost_estimate.estimated_credits,
                        "cost_breakdown": cost_estimate.breakdown,
                        "generation_parameters": {
                            "prompt_length": len(prompt),
                            "model_id": model_id,
                            "num_samples": num_samples,
                            "dimensions": f"{width}x{height}",
                            "inference_steps": num_inference_steps
                        },
                        "sufficient_credits": cost_estimate.sufficient_credits
                    }
                )
        
        except Exception as e:
            logger.exception("Error in scenario_estimate_text_to_image_cost")
            return ResponseHelper.error(f"Cost estimation failed: {str(e)}")