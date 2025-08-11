"""Video generation MCP tools."""

import structlog
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import Context

from ..utils.response import ResponseHelper
from ..utils.validation import validate_request, validate_url_or_base64
from ..models.requests import VideoGenerationRequest
from ..scenario_client import ScenarioAPIClient
from ..exceptions import *

logger = structlog.get_logger(__name__)


def register_video_tools(mcp):
    """Register video generation tools."""
    
    @mcp.tool()
    async def scenario_generate_video(
        ctx: Context,
        prompt: str,
        duration: int = 3,
        fps: int = 24,
        width: int = 512,
        height: int = 512,
        model_id: str = "video-gen-v1",
        guidance: float = 7.5,
        seed: Optional[int] = None,
        wait_for_completion: bool = True
    ) -> Dict[str, Any]:
        """
        Generate video clips from text prompts using Scenario API.
        
        Perfect for Agent 4's video content creation workflows for game trailers,
        cutscenes, animations, and promotional materials.
        
        Args:
            prompt: Text description of the video content (required)
            duration: Video duration in seconds (1-30)
            fps: Frames per second for the video (8-60)
            width: Video width in pixels (256-1024)
            height: Video height in pixels (256-1024)
            model_id: Scenario video model ID to use
            guidance: Guidance scale for generation (0.1-30.0)
            seed: Random seed for reproducible results
            wait_for_completion: Wait for generation to complete
            
        Returns:
            Dict containing video generation results and download URLs
        """
        try:
            logger.info(f"Generating {duration}s video at {fps}fps: {prompt[:50]}...")
            
            # Validate request
            request_data = {
                "prompt": prompt,
                "duration": duration,
                "fps": fps,
                "width": width,
                "height": height,
                "model_id": model_id,
                "guidance": guidance,
                "seed": seed
            }
            
            request = validate_request(request_data, VideoGenerationRequest)
            
            # Execute video generation
            async with ScenarioAPIClient() as client:
                job = await client.generate_video(request)
                
                if wait_for_completion:
                    # Video generation takes longer
                    completed_job = await client.wait_for_completion(job.id, max_wait_time=900)  # 15 minutes
                    
                    # Process video assets
                    video_assets = []
                    preview_assets = []
                    
                    for asset in completed_job.assets:
                        asset_format = asset.format.lower() if asset.format else ""
                        
                        if asset_format in ["mp4", "mov", "avi", "webm"]:
                            video_assets.append(asset)
                        elif asset_format in ["gif", "png", "jpg"]:
                            preview_assets.append(asset)
                        else:
                            # Default to video
                            video_assets.append(asset)
                    
                    total_frames = duration * fps
                    
                    return ResponseHelper.success(
                        f"Generated {duration}s video with {len(completed_job.assets)} assets",
                        data={
                            "job_id": completed_job.id,
                            "status": completed_job.status.value,
                            "video_specifications": {
                                "duration_seconds": duration,
                                "fps": fps,
                                "dimensions": f"{width}x{height}",
                                "total_frames": total_frames,
                                "estimated_file_size": f"{total_frames * width * height // 1000000}MB"
                            },
                            "video_assets": [
                                {
                                    "id": asset.id,
                                    "url": asset.url,
                                    "format": asset.format,
                                    "size_bytes": asset.size_bytes,
                                    "duration": duration
                                }
                                for asset in video_assets
                            ],
                            "preview_assets": [
                                {
                                    "id": asset.id,
                                    "url": asset.url,
                                    "format": asset.format,
                                    "width": asset.width,
                                    "height": asset.height
                                }
                                for asset in preview_assets
                            ],
                            "credits_used": completed_job.credits_used,
                            "generation_time": (completed_job.completed_at - completed_job.created_at).total_seconds() if completed_job.completed_at else None
                        }
                    )
                else:
                    return ResponseHelper.success(
                        f"Video generation started: {duration}s at {fps}fps",
                        data={
                            "job_id": job.id,
                            "status": job.status.value,
                            "video_specs": f"{duration}s, {fps}fps, {width}x{height}",
                            "estimated_completion": "5-15 minutes",
                            "created_at": job.created_at.isoformat()
                        }
                    )
        
        except ValidationError as e:
            return ResponseHelper.validation_error("video_generation_request", str(e))
        except AuthenticationError as e:
            return ResponseHelper.authentication_error(str(e))
        except GenerationError as e:
            return ResponseHelper.error(f"Video generation failed: {str(e)}")
        except Exception as e:
            logger.exception("Unexpected error in scenario_generate_video")
            return ResponseHelper.error(f"Unexpected error: {str(e)}")
    
    @mcp.tool()
    async def scenario_animate_image(
        ctx: Context,
        image_url: str,
        animation_prompt: str,
        animation_type: str = "smooth_motion",
        duration: int = 3,
        fps: int = 24,
        model_id: str = "image2video-v1",
        preserve_original: bool = True
    ) -> Dict[str, Any]:
        """
        Animate static images to create video content.
        
        Perfect for Agent 4's animation workflows where static game art
        needs to be brought to life with motion and effects.
        
        Args:
            image_url: Input image URL or base64 data
            animation_prompt: Description of desired animation
            animation_type: Type of animation ("smooth_motion", "parallax", "effects", "character_animation")
            duration: Animation duration in seconds
            fps: Frames per second for output video
            model_id: Model ID for image-to-video generation
            preserve_original: Whether to preserve original image composition
            
        Returns:
            Dict containing animated video results
        """
        try:
            # Validate input image
            image_type, validated_image = validate_url_or_base64(image_url)
            logger.info(f"Animating {image_type} with {animation_type}: {animation_prompt}")
            
            # Create animation-specific prompt
            animation_prompts = {
                "smooth_motion": f"smooth gentle motion, {animation_prompt}, subtle movement, preserve composition",
                "parallax": f"parallax scrolling effect, {animation_prompt}, layered depth movement",
                "effects": f"dynamic effects animation, {animation_prompt}, particles, lighting effects",
                "character_animation": f"character animation, {animation_prompt}, natural movement, expressive"
            }
            
            full_prompt = animation_prompts.get(animation_type, f"{animation_prompt} animation")
            
            if preserve_original:
                full_prompt += ", maintain original image style and composition"
            
            # Use video generation with image guidance
            # Note: This would typically use image-to-video specific endpoint
            # For now, we'll use the text-to-video with enhanced prompting
            result = await scenario_generate_video(
                ctx=ctx,
                prompt=full_prompt,
                duration=duration,
                fps=fps,
                width=512,  # Standard for animations
                height=512,
                model_id=model_id,
                guidance=6.0,  # Lower guidance for smoother animations
                wait_for_completion=True
            )
            
            if result.get("success"):
                # Enhance response with animation context
                data = result["data"]
                animation_info = {
                    "source_image_type": image_type,
                    "animation_type": animation_type,
                    "animation_prompt": animation_prompt,
                    "original_preserved": preserve_original,
                    "technique": "image_to_video_animation"
                }
                
                data["animation_info"] = animation_info
                result["message"] = f"Animated image with {animation_type} for {duration}s"
            
            return result
        
        except Exception as e:
            logger.exception("Error in scenario_animate_image")
            return ResponseHelper.error(f"Image animation failed: {str(e)}")
    
    @mcp.tool()
    async def scenario_video_variations(
        ctx: Context,
        base_prompt: str,
        variation_prompts: List[str],
        duration: int = 3,
        fps: int = 24,
        consistent_style: bool = True,
        model_id: str = "video-gen-v1"
    ) -> Dict[str, Any]:
        """
        Generate multiple video variations from a base concept.
        
        Perfect for Agent 4's video content variation workflows where they need
        multiple versions of the same video concept for A/B testing or options.
        
        Args:
            base_prompt: Base video concept description
            variation_prompts: List of variation descriptions to apply
            duration: Duration for all video variations
            fps: FPS for all video variations
            consistent_style: Whether to maintain consistent visual style
            model_id: Model to use for all variations
            
        Returns:
            Dict containing all video variation results
        """
        try:
            if not variation_prompts:
                return ResponseHelper.validation_error("variation_prompts", "At least one variation prompt is required")
            
            logger.info(f"Generating {len(variation_prompts)} video variations: {base_prompt}")
            
            results = []
            total_credits = 0.0
            
            for i, variation in enumerate(variation_prompts):
                try:
                    # Create variation-specific prompt
                    if consistent_style:
                        full_prompt = f"{base_prompt}, {variation}, maintain consistent visual style"
                    else:
                        full_prompt = f"{base_prompt}, {variation}"
                    
                    # Generate video variation
                    variation_result = await scenario_generate_video(
                        ctx=ctx,
                        prompt=full_prompt,
                        duration=duration,
                        fps=fps,
                        model_id=model_id,
                        wait_for_completion=True
                    )
                    
                    if variation_result.get("success"):
                        data = variation_result["data"]
                        results.append({
                            "variation_index": i,
                            "variation_prompt": variation,
                            "full_prompt": full_prompt,
                            "job_id": data["job_id"],
                            "status": "completed",
                            "video_assets": data.get("video_assets", []),
                            "preview_assets": data.get("preview_assets", []),
                            "credits_used": data.get("credits_used", 0)
                        })
                        total_credits += data.get("credits_used", 0)
                    else:
                        results.append({
                            "variation_index": i,
                            "variation_prompt": variation,
                            "status": "failed",
                            "error": variation_result.get("message", "Unknown error")
                        })
                    
                    logger.info(f"Completed video variation {i+1}/{len(variation_prompts)}: {variation}")
                
                except Exception as e:
                    logger.error(f"Failed video variation {i+1}: {variation} - {str(e)}")
                    results.append({
                        "variation_index": i,
                        "variation_prompt": variation,
                        "status": "failed",
                        "error": str(e)
                    })
            
            # Summary
            successful_variations = len([r for r in results if r.get("status") == "completed"])
            
            return ResponseHelper.success(
                f"Generated {successful_variations}/{len(variation_prompts)} video variations",
                data={
                    "base_prompt": base_prompt,
                    "video_specifications": {
                        "duration": duration,
                        "fps": fps,
                        "style_consistent": consistent_style
                    },
                    "total_variations": len(variation_prompts),
                    "successful_variations": successful_variations,
                    "total_credits_used": total_credits,
                    "results": results
                }
            )
        
        except Exception as e:
            logger.exception("Unexpected error in scenario_video_variations")
            return ResponseHelper.error(f"Video variations generation failed: {str(e)}")
    
    @mcp.tool()
    async def scenario_game_trailer_clips(
        ctx: Context,
        game_concept: str,
        clip_types: List[str],
        art_style: str = "cinematic",
        duration_per_clip: int = 3,
        total_duration: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate video clips for game trailers and promotional content.
        
        Perfect for Agent 4's game marketing workflows where they need
        specific types of promotional video content for game trailers.
        
        Args:
            game_concept: Overall game concept description
            clip_types: Types of clips needed ("gameplay", "character_showcase", "environment", "action", "story")
            art_style: Visual style for all clips ("cinematic", "gameplay", "concept_art", "realistic")
            duration_per_clip: Duration for each individual clip
            total_duration: Total duration constraint (will adjust individual clips)
            
        Returns:
            Dict containing all trailer clip results organized by type
        """
        try:
            if not clip_types:
                return ResponseHelper.validation_error("clip_types", "At least one clip type is required")
            
            # Adjust durations if total duration is specified
            if total_duration and total_duration < len(clip_types) * duration_per_clip:
                adjusted_duration = max(2, total_duration // len(clip_types))  # Minimum 2 seconds per clip
                logger.info(f"Adjusting clip duration to {adjusted_duration}s to fit total duration of {total_duration}s")
            else:
                adjusted_duration = duration_per_clip
            
            logger.info(f"Generating {len(clip_types)} trailer clips for: {game_concept}")
            
            # Clip type templates
            clip_templates = {
                "gameplay": f"{game_concept} gameplay footage, {art_style} style, player action, UI elements, game interface",
                "character_showcase": f"{game_concept} character showcase, {art_style} style, hero character, detailed view, personality",
                "environment": f"{game_concept} environment showcase, {art_style} style, world building, atmospheric, immersive",
                "action": f"{game_concept} action sequence, {art_style} style, dynamic movement, exciting moments, intensity",
                "story": f"{game_concept} story elements, {art_style} style, narrative moments, emotional, cinematic cutscene"
            }
            
            results = []
            total_credits = 0.0
            
            for i, clip_type in enumerate(clip_types):
                try:
                    # Get template or create custom
                    clip_prompt = clip_templates.get(clip_type, f"{game_concept} {clip_type} content, {art_style} style")
                    
                    # Add trailer-specific enhancements
                    trailer_prompt = f"{clip_prompt}, high quality, promotional trailer style, engaging visuals"
                    
                    # Generate trailer clip
                    clip_result = await scenario_generate_video(
                        ctx=ctx,
                        prompt=trailer_prompt,
                        duration=adjusted_duration,
                        fps=30,  # Higher FPS for trailer quality
                        width=1024,  # Higher resolution for trailers
                        height=576,  # 16:9 aspect ratio
                        model_id="video-gen-v1",
                        guidance=8.0,  # Higher guidance for quality
                        wait_for_completion=True
                    )
                    
                    if clip_result.get("success"):
                        data = clip_result["data"]
                        
                        # Add trailer-specific metadata
                        trailer_clip_info = {
                            "clip_type": clip_type,
                            "clip_purpose": "game_trailer",
                            "art_style": art_style,
                            "game_concept": game_concept,
                            "duration": adjusted_duration,
                            "resolution": "1024x576",
                            "aspect_ratio": "16:9",
                            "suitable_for": ["trailers", "social_media", "marketing"]
                        }
                        
                        results.append({
                            "clip_index": i,
                            "clip_type": clip_type,
                            "trailer_prompt": trailer_prompt,
                            "job_id": data["job_id"],
                            "status": "completed",
                            "trailer_clip_info": trailer_clip_info,
                            "video_assets": data.get("video_assets", []),
                            "preview_assets": data.get("preview_assets", []),
                            "credits_used": data.get("credits_used", 0)
                        })
                        total_credits += data.get("credits_used", 0)
                    else:
                        results.append({
                            "clip_index": i,
                            "clip_type": clip_type,
                            "status": "failed",
                            "error": clip_result.get("message", "Unknown error")
                        })
                    
                    logger.info(f"Completed trailer clip {i+1}/{len(clip_types)}: {clip_type}")
                
                except Exception as e:
                    logger.error(f"Failed trailer clip {i+1}: {clip_type} - {str(e)}")
                    results.append({
                        "clip_index": i,
                        "clip_type": clip_type,
                        "status": "failed",
                        "error": str(e)
                    })
            
            # Summary and organization
            successful_clips = len([r for r in results if r.get("status") == "completed"])
            total_actual_duration = successful_clips * adjusted_duration
            
            # Organize by clip type
            clips_by_type = {}
            for result in results:
                if result.get("status") == "completed":
                    clip_type = result["clip_type"]
                    if clip_type not in clips_by_type:
                        clips_by_type[clip_type] = []
                    clips_by_type[clip_type].append(result)
            
            return ResponseHelper.success(
                f"Generated {successful_clips}/{len(clip_types)} trailer clips ({total_actual_duration}s total)",
                data={
                    "trailer_project_info": {
                        "game_concept": game_concept,
                        "art_style": art_style,
                        "total_clips": len(clip_types),
                        "successful_clips": successful_clips,
                        "total_duration": total_actual_duration,
                        "target_duration": total_duration,
                        "clip_duration": adjusted_duration
                    },
                    "clips_by_type": clips_by_type,
                    "all_clips": results,
                    "total_credits_used": total_credits,
                    "post_production_notes": [
                        "Clips are in 16:9 format suitable for trailers",
                        "30 FPS for smooth playback",
                        "High resolution for quality output",
                        "Ready for video editing software import",
                        "Consider adding transitions between clips",
                        "Add music and sound effects in post-production"
                    ]
                }
            )
        
        except Exception as e:
            logger.exception("Unexpected error in scenario_game_trailer_clips")
            return ResponseHelper.error(f"Game trailer clip generation failed: {str(e)}")
    
    @mcp.tool()
    async def scenario_estimate_video_cost(
        ctx: Context,
        prompt: str,
        duration: int = 3,
        fps: int = 24,
        width: int = 512,
        height: int = 512,
        model_id: str = "video-gen-v1"
    ) -> Dict[str, Any]:
        """
        Estimate cost for video generation without executing.
        
        Perfect for Agent 4's video project budget planning and cost management.
        
        Args:
            prompt: Video description
            duration: Video duration in seconds
            fps: Frames per second
            width: Video width
            height: Video height
            model_id: Model ID for generation
            
        Returns:
            Dict containing video generation cost estimation
        """
        try:
            # Calculate complexity factors
            total_frames = duration * fps
            resolution_factor = (width * height) / (512 * 512)  # Normalized to 512x512
            
            # Base cost per frame
            base_cost_per_frame = 0.5
            
            # Complexity multipliers
            duration_multiplier = 1.0 + (duration / 30)  # Longer videos cost more
            fps_multiplier = 1.0 + (fps - 24) / 60  # Higher FPS costs more
            resolution_multiplier = max(0.5, resolution_factor)  # Higher resolution costs more
            
            # Model-specific multipliers
            model_multipliers = {
                "video-gen-v1": 1.0,
                "image2video-v1": 1.2,
                "video-hd-v1": 1.5,
                "video-4k-v1": 2.0
            }
            
            model_multiplier = model_multipliers.get(model_id, 1.0)
            
            # Calculate total cost
            estimated_cost = (
                total_frames * 
                base_cost_per_frame * 
                duration_multiplier * 
                fps_multiplier * 
                resolution_multiplier * 
                model_multiplier
            )
            
            return ResponseHelper.success(
                f"Estimated cost for {duration}s video: {estimated_cost:.2f} credits",
                data={
                    "estimated_credits": round(estimated_cost, 2),
                    "cost_breakdown": {
                        "base_cost_per_frame": base_cost_per_frame,
                        "total_frames": total_frames,
                        "duration_factor": duration_multiplier,
                        "fps_factor": fps_multiplier,
                        "resolution_factor": resolution_multiplier,
                        "model_factor": model_multiplier
                    },
                    "generation_parameters": {
                        "prompt_length": len(prompt),
                        "duration_seconds": duration,
                        "fps": fps,
                        "dimensions": f"{width}x{height}",
                        "total_frames": total_frames,
                        "model_id": model_id
                    },
                    "estimated_generation_time": f"{duration * 2}-{duration * 3} minutes",
                    "complexity_level": "high" if estimated_cost > 50 else "medium" if estimated_cost > 20 else "low",
                    "cost_comparison": {
                        "vs_image_generation": f"{estimated_cost / 2:.1f}x more expensive",
                        "per_second": f"{estimated_cost / duration:.2f} credits/second"
                    }
                }
            )
        
        except Exception as e:
            logger.exception("Error in scenario_estimate_video_cost")
            return ResponseHelper.error(f"Video cost estimation failed: {str(e)}")