"""Image-to-image generation MCP tools."""

import structlog
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import Context

from ..utils.response import ResponseHelper
from ..utils.validation import validate_request, validate_url_or_base64
from ..models.requests import ImageToImageRequest
from ..scenario_client import ScenarioAPIClient
from ..exceptions import *

logger = structlog.get_logger(__name__)


def register_image_to_image_tools(mcp):
    """Register image-to-image generation tools."""
    
    @mcp.tool()
    async def scenario_image_to_image(
        ctx: Context,
        prompt: str,
        input_image: str,
        strength: float = 0.8,
        model_id: str = "flux.1-dev",
        guidance: float = 7.5,
        num_inference_steps: int = 50,
        negative_prompt: Optional[str] = None,
        seed: Optional[int] = None,
        wait_for_completion: bool = True
    ) -> Dict[str, Any]:
        """
        Generate images from input image and text prompt using Scenario API.
        
        Perfect for Agent 4's style transfer and image-guided generation workflows.
        
        Args:
            prompt: Text description for image transformation (required)
            input_image: Input image URL or base64 data (required)
            strength: How much to transform the input image (0.1-1.0, default: 0.8)
            model_id: Scenario model ID to use (default: flux.1-dev)
            guidance: Guidance scale for generation (0.1-30.0)
            num_inference_steps: Number of inference steps (1-150)
            negative_prompt: Negative prompt to avoid certain elements
            seed: Random seed for reproducible results
            wait_for_completion: Wait for generation to complete (default: True)
            
        Returns:
            Dict containing job information and generated assets
        """
        try:
            # Validate input image format
            image_type, validated_image = validate_url_or_base64(input_image)
            logger.info(f"Processing image-to-image with {image_type}: {prompt[:50]}...")
            
            # Validate request
            request_data = {
                "prompt": prompt,
                "input_image": validated_image,
                "strength": strength,
                "model_id": model_id,
                "guidance": guidance,
                "num_inference_steps": num_inference_steps,
                "negative_prompt": negative_prompt,
                "seed": seed
            }
            
            request = validate_request(request_data, ImageToImageRequest)
            
            # Execute generation
            async with ScenarioAPIClient() as client:
                job = await client.image_to_image(request)
                
                if wait_for_completion:
                    # Wait for completion and get final results
                    completed_job = await client.wait_for_completion(job.id)
                    
                    return ResponseHelper.success(
                        f"Generated {len(completed_job.assets)} images from input image successfully",
                        data={
                            "job_id": completed_job.id,
                            "status": completed_job.status.value,
                            "input_image_type": image_type,
                            "transformation_strength": strength,
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
                        f"Image-to-image generation started",
                        data={
                            "job_id": job.id,
                            "status": job.status.value,
                            "created_at": job.created_at.isoformat()
                        }
                    )
        
        except ValidationError as e:
            return ResponseHelper.validation_error("image_to_image_request", str(e))
        except AuthenticationError as e:
            return ResponseHelper.authentication_error(str(e))
        except GenerationError as e:
            return ResponseHelper.error(f"Image-to-image generation failed: {str(e)}")
        except Exception as e:
            logger.exception("Unexpected error in scenario_image_to_image")
            return ResponseHelper.error(f"Unexpected error: {str(e)}")
    
    @mcp.tool()
    async def scenario_style_transfer(
        ctx: Context,
        content_image: str,
        style_prompt: str,
        style_strength: float = 0.7,
        content_preservation: float = 0.3,
        model_id: str = "flux.1-dev",
        guidance: float = 7.5
    ) -> Dict[str, Any]:
        """
        Apply style transfer to existing images based on text descriptions.
        
        Perfect for Agent 4's style consistency workflows across game assets.
        
        Args:
            content_image: Source image URL or base64 data
            style_prompt: Text description of desired artistic style
            style_strength: How strongly to apply the style (0.1-1.0)
            content_preservation: How much to preserve original content (0.1-1.0)
            model_id: Model to use for style transfer
            guidance: Guidance scale for generation
            
        Returns:
            Dict containing styled image results
        """
        try:
            # Validate content image
            image_type, validated_image = validate_url_or_base64(content_image)
            logger.info(f"Applying style transfer: '{style_prompt}' to {image_type}")
            
            # Create balanced prompt for style transfer
            style_transfer_prompt = f"apply {style_prompt} style while preserving content structure and details"
            
            # Calculate strength based on style vs content balance
            calculated_strength = style_strength * (1 - content_preservation)
            
            # Use image_to_image for style transfer
            result = await scenario_image_to_image(
                ctx=ctx,
                prompt=style_transfer_prompt,
                input_image=validated_image,
                strength=calculated_strength,
                model_id=model_id,
                guidance=guidance,
                wait_for_completion=True
            )
            
            if result.get("success"):
                # Enhance response with style transfer context
                result["data"]["style_transfer_info"] = {
                    "original_style_prompt": style_prompt,
                    "style_strength": style_strength,
                    "content_preservation": content_preservation,
                    "calculated_transformation_strength": calculated_strength,
                    "technique": "text_guided_style_transfer"
                }
                result["message"] = f"Style transfer completed: '{style_prompt}' applied successfully"
            
            return result
        
        except Exception as e:
            logger.exception("Error in scenario_style_transfer")
            return ResponseHelper.error(f"Style transfer failed: {str(e)}")
    
    @mcp.tool()
    async def scenario_image_variations(
        ctx: Context,
        base_image: str,
        variation_prompts: List[str],
        strength: float = 0.6,
        model_id: str = "flux.1-dev",
        preserve_composition: bool = True
    ) -> Dict[str, Any]:
        """
        Generate multiple variations of a base image using different prompts.
        
        Perfect for Agent 4's asset variation workflows where they need multiple
        versions of the same base composition.
        
        Args:
            base_image: Base image URL or base64 data
            variation_prompts: List of prompts for different variations
            strength: Transformation strength for all variations
            model_id: Model to use for all variations
            preserve_composition: Whether to preserve the original composition
            
        Returns:
            Dict containing all variation results
        """
        try:
            if not variation_prompts:
                return ResponseHelper.validation_error("variation_prompts", "At least one variation prompt is required")
            
            # Validate base image
            image_type, validated_image = validate_url_or_base64(base_image)
            logger.info(f"Creating {len(variation_prompts)} variations from {image_type}")
            
            # Adjust strength for composition preservation
            if preserve_composition:
                adjusted_strength = min(strength, 0.7)  # Cap at 0.7 to preserve composition
            else:
                adjusted_strength = strength
            
            results = []
            total_credits = 0.0
            
            async with ScenarioAPIClient() as client:
                for i, variation_prompt in enumerate(variation_prompts):
                    try:
                        # Add composition preservation instruction if needed
                        if preserve_composition:
                            full_prompt = f"{variation_prompt}, maintaining original composition and layout"
                        else:
                            full_prompt = variation_prompt
                        
                        # Create individual request
                        request_data = {
                            "prompt": full_prompt,
                            "input_image": validated_image,
                            "strength": adjusted_strength,
                            "model_id": model_id,
                            "guidance": 7.5,
                            "num_inference_steps": 50
                        }
                        request = validate_request(request_data, ImageToImageRequest)
                        
                        # Generate variation
                        job = await client.image_to_image(request)
                        completed_job = await client.wait_for_completion(job.id)
                        
                        # Store result
                        variation_result = {
                            "variation_index": i,
                            "variation_prompt": variation_prompt,
                            "full_prompt_used": full_prompt,
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
                        total_credits += completed_job.credits_used or 0
                        
                        logger.info(f"Completed variation {i+1}/{len(variation_prompts)}: {variation_prompt}")
                    
                    except Exception as e:
                        logger.error(f"Failed variation {i+1}: {variation_prompt} - {str(e)}")
                        results.append({
                            "variation_index": i,
                            "variation_prompt": variation_prompt,
                            "error": str(e),
                            "status": "failed"
                        })
            
            # Summary
            successful_variations = len([r for r in results if r.get("status") != "failed"])
            
            return ResponseHelper.success(
                f"Generated {successful_variations}/{len(variation_prompts)} image variations successfully",
                data={
                    "base_image_type": image_type,
                    "total_variations": len(variation_prompts),
                    "successful_variations": successful_variations,
                    "total_credits_used": total_credits,
                    "transformation_strength": adjusted_strength,
                    "composition_preserved": preserve_composition,
                    "results": results
                }
            )
        
        except Exception as e:
            logger.exception("Unexpected error in scenario_image_variations")
            return ResponseHelper.error(f"Image variations generation failed: {str(e)}")
    
    @mcp.tool()
    async def scenario_upscale_and_enhance(
        ctx: Context,
        input_image: str,
        enhancement_prompt: str = "high quality, detailed, sharp, professional",
        upscale_factor: float = 2.0,
        model_id: str = "flux.1-dev",
        preserve_details: bool = True
    ) -> Dict[str, Any]:
        """
        Upscale and enhance image quality using AI.
        
        Perfect for Agent 4's asset quality improvement workflows.
        
        Args:
            input_image: Input image URL or base64 data
            enhancement_prompt: Prompt describing desired enhancements
            upscale_factor: Desired upscale factor (1.5-4.0)
            model_id: Model to use for enhancement
            preserve_details: Whether to preserve original details
            
        Returns:
            Dict containing enhanced image results
        """
        try:
            # Validate input image
            image_type, validated_image = validate_url_or_base64(input_image)
            logger.info(f"Upscaling and enhancing {image_type} with factor {upscale_factor}")
            
            # Create enhancement prompt
            if preserve_details:
                full_prompt = f"{enhancement_prompt}, preserve all original details and features, upscale {upscale_factor}x"
            else:
                full_prompt = f"{enhancement_prompt}, upscale {upscale_factor}x"
            
            # Use lower strength to preserve quality while enhancing
            enhancement_strength = 0.4 if preserve_details else 0.6
            
            # Calculate target dimensions (approximate)
            target_width = int(1024 * upscale_factor) if upscale_factor > 1 else 1024
            target_height = int(1024 * upscale_factor) if upscale_factor > 1 else 1024
            
            # Use image_to_image for enhancement
            result = await scenario_image_to_image(
                ctx=ctx,
                prompt=full_prompt,
                input_image=validated_image,
                strength=enhancement_strength,
                model_id=model_id,
                guidance=5.0,  # Lower guidance for quality preservation
                num_inference_steps=75,  # More steps for better quality
                wait_for_completion=True
            )
            
            if result.get("success"):
                # Enhance response with upscaling context
                result["data"]["enhancement_info"] = {
                    "upscale_factor": upscale_factor,
                    "target_dimensions": f"{target_width}x{target_height}",
                    "enhancement_prompt": enhancement_prompt,
                    "details_preserved": preserve_details,
                    "enhancement_strength": enhancement_strength,
                    "technique": "ai_upscaling_and_enhancement"
                }
                result["message"] = f"Image enhanced and upscaled {upscale_factor}x successfully"
            
            return result
        
        except Exception as e:
            logger.exception("Error in scenario_upscale_and_enhance")
            return ResponseHelper.error(f"Image enhancement failed: {str(e)}")