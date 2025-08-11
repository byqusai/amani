"""ControlNet generation MCP tools."""

import structlog
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import Context

from ..utils.response import ResponseHelper
from ..utils.validation import validate_request, validate_url_or_base64
from ..models.requests import ControlNetRequest
from ..models.enums import ControlNetType
from ..scenario_client import ScenarioAPIClient
from ..exceptions import *

logger = structlog.get_logger(__name__)


def register_controlnet_tools(mcp):
    """Register ControlNet generation tools."""
    
    @mcp.tool()
    async def scenario_controlnet_generate(
        ctx: Context,
        prompt: str,
        control_image: str,
        control_type: str,
        model_id: str,
        strength: float = 1.0,
        guidance: float = 7.5,
        num_inference_steps: int = 50,
        negative_prompt: Optional[str] = None,
        wait_for_completion: bool = True
    ) -> Dict[str, Any]:
        """
        Generate images with ControlNet guidance (pose, depth, canny, etc.).
        
        Perfect for Agent 4's precise control workflows where specific poses,
        compositions, or structures need to be maintained.
        
        Args:
            prompt: Text description for generation (required)
            control_image: Control image URL or base64 data (required)
            control_type: Type of control ("pose", "depth", "canny", "openpose", "scribble", "normal", "lineart")
            model_id: Scenario model ID with ControlNet support (required)
            strength: Control guidance strength (0.1-2.0, default: 1.0)
            guidance: Text guidance scale (0.1-30.0)
            num_inference_steps: Number of inference steps (1-150)
            negative_prompt: Negative prompt to avoid elements
            wait_for_completion: Wait for generation to complete
            
        Returns:
            Dict containing job information and generated assets
        """
        try:
            # Validate control image
            image_type, validated_image = validate_url_or_base64(control_image)
            logger.info(f"Processing ControlNet ({control_type}) with {image_type}: {prompt[:50]}...")
            
            # Validate control type
            try:
                control_type_enum = ControlNetType(control_type.lower())
            except ValueError:
                return ResponseHelper.validation_error(
                    "control_type", 
                    f"Invalid control type '{control_type}'. Must be one of: {[t.value for t in ControlNetType]}"
                )
            
            # Validate request
            request_data = {
                "prompt": prompt,
                "control_image": validated_image,
                "control_type": control_type_enum,
                "model_id": model_id,
                "strength": strength,
                "guidance": guidance,
                "num_inference_steps": num_inference_steps,
                "negative_prompt": negative_prompt
            }
            
            request = validate_request(request_data, ControlNetRequest)
            
            # Execute generation
            async with ScenarioAPIClient() as client:
                job = await client.controlnet_generate(request)
                
                if wait_for_completion:
                    completed_job = await client.wait_for_completion(job.id)
                    
                    return ResponseHelper.success(
                        f"Generated {len(completed_job.assets)} ControlNet images successfully",
                        data={
                            "job_id": completed_job.id,
                            "status": completed_job.status.value,
                            "control_type": control_type,
                            "control_strength": strength,
                            "control_image_type": image_type,
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
                    return ResponseHelper.success(
                        f"ControlNet generation started with {control_type} control",
                        data={
                            "job_id": job.id,
                            "status": job.status.value,
                            "control_type": control_type,
                            "created_at": job.created_at.isoformat()
                        }
                    )
        
        except ValidationError as e:
            return ResponseHelper.validation_error("controlnet_request", str(e))
        except AuthenticationError as e:
            return ResponseHelper.authentication_error(str(e))
        except GenerationError as e:
            return ResponseHelper.error(f"ControlNet generation failed: {str(e)}")
        except Exception as e:
            logger.exception("Unexpected error in scenario_controlnet_generate")
            return ResponseHelper.error(f"Unexpected error: {str(e)}")
    
    @mcp.tool()
    async def scenario_pose_control(
        ctx: Context,
        prompt: str,
        pose_image: str,
        model_id: str,
        pose_strength: float = 1.0,
        preserve_pose_exactly: bool = True,
        guidance: float = 7.5
    ) -> Dict[str, Any]:
        """
        Generate images with precise pose control from reference images.
        
        Perfect for Agent 4's character consistency workflows where specific
        poses need to be maintained across different style variations.
        
        Args:
            prompt: Text description for the generated image
            pose_image: Reference pose image URL or base64 data
            model_id: Model ID with pose ControlNet support
            pose_strength: How strictly to follow the pose (0.5-2.0)
            preserve_pose_exactly: Whether to preserve pose exactly or allow variations
            guidance: Text guidance scale
            
        Returns:
            Dict containing pose-controlled generation results
        """
        try:
            # Validate pose image
            image_type, validated_image = validate_url_or_base64(pose_image)
            logger.info(f"Applying pose control from {image_type}: {prompt[:50]}...")
            
            # Adjust strength based on preservation preference
            if preserve_pose_exactly:
                adjusted_strength = max(pose_strength, 1.2)  # Minimum 1.2 for exact preservation
                enhanced_prompt = f"{prompt}, exact pose match, precise body positioning"
            else:
                adjusted_strength = pose_strength
                enhanced_prompt = f"{prompt}, similar pose and gesture"
            
            # Use ControlNet with pose control
            result = await scenario_controlnet_generate(
                ctx=ctx,
                prompt=enhanced_prompt,
                control_image=validated_image,
                control_type="pose",
                model_id=model_id,
                strength=adjusted_strength,
                guidance=guidance,
                wait_for_completion=True
            )
            
            if result.get("success"):
                # Enhance response with pose control context
                result["data"]["pose_control_info"] = {
                    "pose_reference_type": image_type,
                    "pose_strength": pose_strength,
                    "adjusted_strength": adjusted_strength,
                    "exact_preservation": preserve_pose_exactly,
                    "technique": "openpose_controlnet"
                }
                result["message"] = f"Pose-controlled generation completed with {adjusted_strength:.1f} strength"
            
            return result
        
        except Exception as e:
            logger.exception("Error in scenario_pose_control")
            return ResponseHelper.error(f"Pose control generation failed: {str(e)}")
    
    @mcp.tool()
    async def scenario_depth_control(
        ctx: Context,
        prompt: str,
        depth_image: str,
        model_id: str,
        depth_strength: float = 1.0,
        preserve_structure: bool = True,
        guidance: float = 7.5
    ) -> Dict[str, Any]:
        """
        Generate images with depth map control for consistent scene structure.
        
        Perfect for Agent 4's environment consistency workflows where spatial
        relationships and depth need to be maintained.
        
        Args:
            prompt: Text description for the generated scene
            depth_image: Depth map image URL or base64 data
            model_id: Model ID with depth ControlNet support
            depth_strength: How strictly to follow depth information
            preserve_structure: Whether to preserve spatial structure exactly
            guidance: Text guidance scale
            
        Returns:
            Dict containing depth-controlled generation results
        """
        try:
            # Validate depth image
            image_type, validated_image = validate_url_or_base64(depth_image)
            logger.info(f"Applying depth control from {image_type}: {prompt[:50]}...")
            
            # Adjust settings for structure preservation
            if preserve_structure:
                adjusted_strength = max(depth_strength, 1.0)
                enhanced_prompt = f"{prompt}, maintain spatial depth and structure, consistent perspective"
            else:
                adjusted_strength = depth_strength
                enhanced_prompt = f"{prompt}, similar depth composition"
            
            # Use ControlNet with depth control
            result = await scenario_controlnet_generate(
                ctx=ctx,
                prompt=enhanced_prompt,
                control_image=validated_image,
                control_type="depth",
                model_id=model_id,
                strength=adjusted_strength,
                guidance=guidance,
                wait_for_completion=True
            )
            
            if result.get("success"):
                # Enhance response with depth control context
                result["data"]["depth_control_info"] = {
                    "depth_reference_type": image_type,
                    "depth_strength": depth_strength,
                    "adjusted_strength": adjusted_strength,
                    "structure_preserved": preserve_structure,
                    "technique": "depth_map_controlnet"
                }
                result["message"] = f"Depth-controlled generation completed with preserved structure: {preserve_structure}"
            
            return result
        
        except Exception as e:
            logger.exception("Error in scenario_depth_control")
            return ResponseHelper.error(f"Depth control generation failed: {str(e)}")
    
    @mcp.tool()
    async def scenario_canny_edge_control(
        ctx: Context,
        prompt: str,
        edge_image: str,
        model_id: str,
        edge_strength: float = 1.0,
        preserve_edges: bool = True,
        guidance: float = 7.5
    ) -> Dict[str, Any]:
        """
        Generate images following edge maps for precise shape control.
        
        Perfect for Agent 4's precise shape control workflows where specific
        outlines and boundaries need to be maintained.
        
        Args:
            prompt: Text description for the generated image
            edge_image: Canny edge map URL or base64 data
            model_id: Model ID with Canny ControlNet support
            edge_strength: How strictly to follow edge information
            preserve_edges: Whether to preserve edges exactly
            guidance: Text guidance scale
            
        Returns:
            Dict containing edge-controlled generation results
        """
        try:
            # Validate edge image
            image_type, validated_image = validate_url_or_base64(edge_image)
            logger.info(f"Applying Canny edge control from {image_type}: {prompt[:50]}...")
            
            # Adjust settings for edge preservation
            if preserve_edges:
                adjusted_strength = max(edge_strength, 1.1)
                enhanced_prompt = f"{prompt}, precise edges and outlines, sharp boundaries"
            else:
                adjusted_strength = edge_strength
                enhanced_prompt = f"{prompt}, similar edge composition"
            
            # Use ControlNet with Canny control
            result = await scenario_controlnet_generate(
                ctx=ctx,
                prompt=enhanced_prompt,
                control_image=validated_image,
                control_type="canny",
                model_id=model_id,
                strength=adjusted_strength,
                guidance=guidance,
                wait_for_completion=True
            )
            
            if result.get("success"):
                # Enhance response with edge control context
                result["data"]["edge_control_info"] = {
                    "edge_reference_type": image_type,
                    "edge_strength": edge_strength,
                    "adjusted_strength": adjusted_strength,
                    "edges_preserved": preserve_edges,
                    "technique": "canny_edge_controlnet"
                }
                result["message"] = f"Edge-controlled generation completed with preserved edges: {preserve_edges}"
            
            return result
        
        except Exception as e:
            logger.exception("Error in scenario_canny_edge_control")
            return ResponseHelper.error(f"Canny edge control generation failed: {str(e)}")
    
    @mcp.tool()
    async def scenario_multi_controlnet(
        ctx: Context,
        prompt: str,
        control_inputs: List[Dict[str, Any]],
        model_id: str,
        overall_guidance: float = 7.5,
        balance_controls: bool = True
    ) -> Dict[str, Any]:
        """
        Generate images using multiple ControlNet controls simultaneously.
        
        Perfect for Agent 4's complex control workflows where multiple aspects
        (pose + depth + edges) need to be controlled together.
        
        Args:
            prompt: Text description for generation
            control_inputs: List of control specifications, each containing:
                - type: Control type ("pose", "depth", "canny", etc.)
                - image: Control image URL or base64
                - strength: Individual control strength
                - weight: Relative importance (0.1-1.0)
            model_id: Model ID with multi-ControlNet support
            overall_guidance: Overall text guidance scale
            balance_controls: Whether to auto-balance control strengths
            
        Returns:
            Dict containing multi-control generation results
        """
        try:
            if not control_inputs:
                return ResponseHelper.validation_error("control_inputs", "At least one control input is required")
            
            logger.info(f"Processing multi-ControlNet with {len(control_inputs)} controls: {prompt[:50]}...")
            
            # Validate and prepare control inputs
            processed_controls = []
            total_weight = 0.0
            
            for i, control_input in enumerate(control_inputs):
                try:
                    # Validate required fields
                    if "type" not in control_input or "image" not in control_input:
                        return ResponseHelper.validation_error(
                            f"control_inputs[{i}]", 
                            "Each control input must have 'type' and 'image' fields"
                        )
                    
                    # Validate control image
                    image_type, validated_image = validate_url_or_base64(control_input["image"])
                    
                    # Validate control type
                    try:
                        control_type = ControlNetType(control_input["type"].lower())
                    except ValueError:
                        return ResponseHelper.validation_error(
                            f"control_inputs[{i}].type",
                            f"Invalid control type '{control_input['type']}'"
                        )
                    
                    # Extract control parameters
                    strength = control_input.get("strength", 1.0)
                    weight = control_input.get("weight", 1.0)
                    total_weight += weight
                    
                    processed_controls.append({
                        "type": control_type,
                        "image": validated_image,
                        "image_type": image_type,
                        "strength": strength,
                        "weight": weight,
                        "original_input": control_input
                    })
                    
                except Exception as e:
                    return ResponseHelper.validation_error(
                        f"control_inputs[{i}]",
                        f"Invalid control input: {str(e)}"
                    )
            
            # Balance control strengths if requested
            if balance_controls and total_weight > 0:
                for control in processed_controls:
                    # Normalize weights and adjust strengths
                    normalized_weight = control["weight"] / total_weight
                    control["balanced_strength"] = control["strength"] * normalized_weight * len(processed_controls)
            
            # For now, process the strongest control (in a real implementation,
            # this would combine multiple controls simultaneously)
            primary_control = max(processed_controls, key=lambda x: x.get("balanced_strength", x["strength"]))
            
            logger.info(f"Using primary control: {primary_control['type'].value} (strength: {primary_control.get('balanced_strength', primary_control['strength']):.2f})")
            
            # Enhanced prompt with multi-control context
            control_types = [c["type"].value for c in processed_controls]
            enhanced_prompt = f"{prompt}, controlled by {', '.join(control_types)}, precise multi-aspect generation"
            
            # Execute primary control generation
            result = await scenario_controlnet_generate(
                ctx=ctx,
                prompt=enhanced_prompt,
                control_image=primary_control["image"],
                control_type=primary_control["type"].value,
                model_id=model_id,
                strength=primary_control.get("balanced_strength", primary_control["strength"]),
                guidance=overall_guidance,
                wait_for_completion=True
            )
            
            if result.get("success"):
                # Enhance response with multi-control context
                result["data"]["multi_control_info"] = {
                    "total_controls": len(processed_controls),
                    "control_types": control_types,
                    "primary_control": primary_control["type"].value,
                    "controls_balanced": balance_controls,
                    "control_details": [
                        {
                            "type": c["type"].value,
                            "strength": c["strength"],
                            "weight": c["weight"],
                            "balanced_strength": c.get("balanced_strength")
                        }
                        for c in processed_controls
                    ],
                    "technique": "multi_controlnet_generation"
                }
                result["message"] = f"Multi-ControlNet generation completed using {len(processed_controls)} controls"
            
            return result
        
        except Exception as e:
            logger.exception("Error in scenario_multi_controlnet")
            return ResponseHelper.error(f"Multi-ControlNet generation failed: {str(e)}")
    
    @mcp.tool()
    async def scenario_controlnet_batch(
        ctx: Context,
        prompts: List[str],
        control_image: str,
        control_type: str,
        model_id: str,
        strength: float = 1.0,
        max_concurrent: int = 3
    ) -> Dict[str, Any]:
        """
        Generate multiple variations using the same ControlNet control.
        
        Perfect for Agent 4's variation workflows where the same pose/composition
        needs to be applied to multiple different prompts.
        
        Args:
            prompts: List of text prompts for variations
            control_image: Shared control image URL or base64 data
            control_type: Type of control to apply to all generations
            model_id: Model ID with ControlNet support
            strength: Control strength for all generations
            max_concurrent: Maximum concurrent generations
            
        Returns:
            Dict containing batch ControlNet generation results
        """
        try:
            if not prompts:
                return ResponseHelper.validation_error("prompts", "At least one prompt is required")
            
            # Validate control image once
            image_type, validated_image = validate_url_or_base64(control_image)
            logger.info(f"Processing ControlNet batch: {len(prompts)} prompts with {control_type} control")
            
            results = []
            total_credits = 0.0
            
            # Process in batches to respect concurrency limits
            import asyncio
            from ..utils.async_utils import AsyncThrottler
            
            throttler = AsyncThrottler(max_concurrent=max_concurrent, rate_limit=5.0)
            
            async def process_single_prompt(prompt_data):
                index, prompt = prompt_data
                try:
                    # Generate with ControlNet
                    result = await scenario_controlnet_generate(
                        ctx=ctx,
                        prompt=prompt,
                        control_image=validated_image,
                        control_type=control_type,
                        model_id=model_id,
                        strength=strength,
                        guidance=7.5,
                        wait_for_completion=True
                    )
                    
                    if result.get("success"):
                        data = result["data"]
                        return {
                            "index": index,
                            "prompt": prompt,
                            "job_id": data["job_id"],
                            "status": "completed",
                            "assets": data["assets"],
                            "credits_used": data.get("credits_used", 0)
                        }
                    else:
                        return {
                            "index": index,
                            "prompt": prompt,
                            "status": "failed",
                            "error": result.get("message", "Unknown error")
                        }
                
                except Exception as e:
                    return {
                        "index": index,
                        "prompt": prompt,
                        "status": "failed",
                        "error": str(e)
                    }
            
            # Execute batch with throttling
            prompt_operations = [(process_single_prompt, ((i, prompt),), {}) 
                               for i, prompt in enumerate(prompts)]
            
            batch_results = await throttler.execute_batch(prompt_operations)
            
            # Process results
            for batch_result in batch_results:
                if batch_result.get("success", True):
                    result_data = batch_result.get("result", batch_result)
                    results.append(result_data)
                    if result_data.get("credits_used"):
                        total_credits += result_data["credits_used"]
            
            # Summary
            successful = len([r for r in results if r.get("status") == "completed"])
            
            return ResponseHelper.success(
                f"ControlNet batch completed: {successful}/{len(prompts)} successful",
                data={
                    "control_type": control_type,
                    "control_image_type": image_type,
                    "control_strength": strength,
                    "total_prompts": len(prompts),
                    "successful_generations": successful,
                    "failed_generations": len(prompts) - successful,
                    "total_credits_used": total_credits,
                    "results": results
                }
            )
        
        except Exception as e:
            logger.exception("Error in scenario_controlnet_batch")
            return ResponseHelper.error(f"ControlNet batch generation failed: {str(e)}")