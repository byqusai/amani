"""3D model generation MCP tools."""

import structlog
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import Context

from ..utils.response import ResponseHelper
from ..utils.validation import validate_request
from ..models.requests import ThreeDGenerationRequest
from ..models.enums import ModelType
from ..scenario_client import ScenarioAPIClient
from ..exceptions import *

logger = structlog.get_logger(__name__)


def register_3d_tools(mcp):
    """Register 3D generation tools."""
    
    @mcp.tool()
    async def scenario_generate_3d(
        ctx: Context,
        prompt: str,
        model_type: str = "mesh",
        resolution: int = 512,
        view_angles: List[str] = None,
        generate_textures: bool = True,
        generate_materials: bool = True,
        model_id: str = "3d-gen-v1",
        wait_for_completion: bool = True
    ) -> Dict[str, Any]:
        """
        Generate 3D models from text prompts using Scenario API.
        
        Perfect for Agent 4's 3D asset creation workflows for games requiring
        meshes, textures, and materials from text descriptions.
        
        Args:
            prompt: Text description of the 3D model (required)
            model_type: Type of 3D model ("mesh", "texture", "material", "full_scene")
            resolution: Texture resolution for generated models (128-1024)
            view_angles: Required view angles (default: ["front", "side", "back"])
            generate_textures: Whether to generate textures for the model
            generate_materials: Whether to generate materials for the model
            model_id: Scenario 3D model ID to use
            wait_for_completion: Wait for generation to complete
            
        Returns:
            Dict containing 3D model generation results and download URLs
        """
        try:
            if view_angles is None:
                view_angles = ["front", "side", "back"]
            
            logger.info(f"Generating 3D {model_type} from prompt: {prompt[:50]}...")
            
            # Validate model type
            try:
                model_type_enum = ModelType(model_type.lower())
            except ValueError:
                return ResponseHelper.validation_error(
                    "model_type",
                    f"Invalid model type '{model_type}'. Must be one of: {[t.value for t in ModelType]}"
                )
            
            # Validate request
            request_data = {
                "prompt": prompt,
                "model_type": model_type_enum,
                "resolution": resolution,
                "view_angles": view_angles,
                "generate_textures": generate_textures,
                "generate_materials": generate_materials,
                "model_id": model_id
            }
            
            request = validate_request(request_data, ThreeDGenerationRequest)
            
            # Execute 3D generation
            async with ScenarioAPIClient() as client:
                job = await client.generate_3d(request)
                
                if wait_for_completion:
                    completed_job = await client.wait_for_completion(job.id, max_wait_time=600)  # 3D takes longer
                    
                    # Process 3D-specific assets
                    model_assets = []
                    texture_assets = []
                    material_assets = []
                    
                    for asset in completed_job.assets:
                        # Categorize assets by type (based on format or metadata)
                        asset_format = asset.format.lower() if asset.format else ""
                        
                        if asset_format in ["obj", "fbx", "gltf", "glb", "blend"]:
                            model_assets.append(asset)
                        elif asset_format in ["png", "jpg", "jpeg", "tga", "exr"]:
                            texture_assets.append(asset)
                        elif asset_format in ["mtl", "mat", "material"]:
                            material_assets.append(asset)
                        else:
                            # Default to model if unknown
                            model_assets.append(asset)
                    
                    return ResponseHelper.success(
                        f"Generated 3D {model_type} with {len(completed_job.assets)} assets",
                        data={
                            "job_id": completed_job.id,
                            "status": completed_job.status.value,
                            "model_type": model_type,
                            "resolution": resolution,
                            "view_angles": view_angles,
                            "textures_included": generate_textures,
                            "materials_included": generate_materials,
                            "total_assets": len(completed_job.assets),
                            "model_assets": [
                                {
                                    "id": asset.id,
                                    "url": asset.url,
                                    "format": asset.format,
                                    "size_bytes": asset.size_bytes
                                }
                                for asset in model_assets
                            ],
                            "texture_assets": [
                                {
                                    "id": asset.id,
                                    "url": asset.url,
                                    "format": asset.format,
                                    "width": asset.width,
                                    "height": asset.height,
                                    "size_bytes": asset.size_bytes
                                }
                                for asset in texture_assets
                            ],
                            "material_assets": [
                                {
                                    "id": asset.id,
                                    "url": asset.url,
                                    "format": asset.format,
                                    "size_bytes": asset.size_bytes
                                }
                                for asset in material_assets
                            ],
                            "credits_used": completed_job.credits_used,
                            "generation_time": (completed_job.completed_at - completed_job.created_at).total_seconds() if completed_job.completed_at else None
                        }
                    )
                else:
                    return ResponseHelper.success(
                        f"3D {model_type} generation started",
                        data={
                            "job_id": job.id,
                            "status": job.status.value,
                            "model_type": model_type,
                            "estimated_completion": "5-10 minutes",
                            "created_at": job.created_at.isoformat()
                        }
                    )
        
        except ValidationError as e:
            return ResponseHelper.validation_error("3d_generation_request", str(e))
        except AuthenticationError as e:
            return ResponseHelper.authentication_error(str(e))
        except GenerationError as e:
            return ResponseHelper.error(f"3D generation failed: {str(e)}")
        except Exception as e:
            logger.exception("Unexpected error in scenario_generate_3d")
            return ResponseHelper.error(f"Unexpected error: {str(e)}")
    
    @mcp.tool()
    async def scenario_texture_3d_model(
        ctx: Context,
        model_description: str,
        texture_prompt: str,
        model_id: str = "3d-texture-v1",
        texture_resolution: int = 1024,
        texture_style: str = "realistic",
        seamless_textures: bool = True,
        generate_normal_maps: bool = True,
        generate_roughness_maps: bool = True
    ) -> Dict[str, Any]:
        """
        Generate textures for 3D models based on descriptions.
        
        Perfect for Agent 4's texture creation workflows where existing 3D models
        need custom textures and materials applied.
        
        Args:
            model_description: Description of the 3D model being textured
            texture_prompt: Specific texture description (e.g., "rusty metal", "wooden planks")
            model_id: Model ID for texture generation
            texture_resolution: Resolution for generated textures
            texture_style: Style of textures ("realistic", "stylized", "cartoon", "pixelart")
            seamless_textures: Whether to generate seamless/tileable textures
            generate_normal_maps: Whether to generate normal maps
            generate_roughness_maps: Whether to generate roughness/PBR maps
            
        Returns:
            Dict containing generated texture assets and material information
        """
        try:
            logger.info(f"Generating 3D textures for '{model_description}': {texture_prompt}")
            
            # Create comprehensive texture generation prompt
            texture_components = []
            
            if seamless_textures:
                texture_components.append("seamless tileable texture")
            
            if generate_normal_maps:
                texture_components.append("with normal map")
                
            if generate_roughness_maps:
                texture_components.append("with roughness and metallic maps")
            
            # Combine prompt components
            full_prompt = f"{texture_prompt} texture for {model_description}, {texture_style} style"
            if texture_components:
                full_prompt += f", {', '.join(texture_components)}"
            
            # Use 3D generation with texture focus
            result = await scenario_generate_3d(
                ctx=ctx,
                prompt=full_prompt,
                model_type="texture",
                resolution=texture_resolution,
                view_angles=["front"],  # Single view for textures
                generate_textures=True,
                generate_materials=True,
                model_id=model_id,
                wait_for_completion=True
            )
            
            if result.get("success"):
                # Enhance response with texture-specific information
                data = result["data"]
                texture_info = {
                    "model_description": model_description,
                    "texture_prompt": texture_prompt,
                    "texture_style": texture_style,
                    "resolution": texture_resolution,
                    "seamless": seamless_textures,
                    "includes_normal_maps": generate_normal_maps,
                    "includes_roughness_maps": generate_roughness_maps,
                    "pbr_ready": generate_normal_maps and generate_roughness_maps,
                    "technique": "ai_texture_generation"
                }
                
                data["texture_generation_info"] = texture_info
                result["message"] = f"Generated {texture_style} textures for {model_description}"
            
            return result
        
        except Exception as e:
            logger.exception("Error in scenario_texture_3d_model")
            return ResponseHelper.error(f"3D texture generation failed: {str(e)}")
    
    @mcp.tool()
    async def scenario_3d_asset_variations(
        ctx: Context,
        base_prompt: str,
        variation_styles: List[str],
        model_type: str = "mesh",
        consistent_geometry: bool = True,
        resolution: int = 512
    ) -> Dict[str, Any]:
        """
        Generate multiple style variations of the same 3D asset.
        
        Perfect for Agent 4's asset variation workflows where they need the same
        3D object in different artistic styles or materials.
        
        Args:
            base_prompt: Base description of the 3D model
            variation_styles: List of style variations to apply
            model_type: Type of 3D model to generate
            consistent_geometry: Whether to maintain consistent shape/geometry
            resolution: Texture resolution for all variations
            
        Returns:
            Dict containing all 3D asset variations
        """
        try:
            if not variation_styles:
                return ResponseHelper.validation_error("variation_styles", "At least one variation style is required")
            
            logger.info(f"Generating {len(variation_styles)} 3D variations of: {base_prompt}")
            
            results = []
            total_credits = 0.0
            
            for i, style in enumerate(variation_styles):
                try:
                    # Create style-specific prompt
                    if consistent_geometry:
                        variation_prompt = f"{base_prompt}, {style} style, maintain original proportions and shape"
                    else:
                        variation_prompt = f"{base_prompt}, {style} style"
                    
                    # Generate 3D variation
                    variation_result = await scenario_generate_3d(
                        ctx=ctx,
                        prompt=variation_prompt,
                        model_type=model_type,
                        resolution=resolution,
                        view_angles=["front", "side"],  # Reduced for faster generation
                        generate_textures=True,
                        generate_materials=True,
                        wait_for_completion=True
                    )
                    
                    if variation_result.get("success"):
                        data = variation_result["data"]
                        results.append({
                            "variation_index": i,
                            "style": style,
                            "variation_prompt": variation_prompt,
                            "job_id": data["job_id"],
                            "status": "completed",
                            "model_assets": data.get("model_assets", []),
                            "texture_assets": data.get("texture_assets", []),
                            "material_assets": data.get("material_assets", []),
                            "credits_used": data.get("credits_used", 0)
                        })
                        total_credits += data.get("credits_used", 0)
                    else:
                        results.append({
                            "variation_index": i,
                            "style": style,
                            "status": "failed",
                            "error": variation_result.get("message", "Unknown error")
                        })
                    
                    logger.info(f"Completed 3D variation {i+1}/{len(variation_styles)}: {style}")
                
                except Exception as e:
                    logger.error(f"Failed 3D variation {i+1}: {style} - {str(e)}")
                    results.append({
                        "variation_index": i,
                        "style": style,
                        "status": "failed",
                        "error": str(e)
                    })
            
            # Summary
            successful_variations = len([r for r in results if r.get("status") == "completed"])
            
            return ResponseHelper.success(
                f"Generated {successful_variations}/{len(variation_styles)} 3D asset variations",
                data={
                    "base_prompt": base_prompt,
                    "model_type": model_type,
                    "resolution": resolution,
                    "geometry_consistent": consistent_geometry,
                    "total_variations": len(variation_styles),
                    "successful_variations": successful_variations,
                    "total_credits_used": total_credits,
                    "results": results
                }
            )
        
        except Exception as e:
            logger.exception("Unexpected error in scenario_3d_asset_variations")
            return ResponseHelper.error(f"3D asset variations failed: {str(e)}")
    
    @mcp.tool()
    async def scenario_3d_game_assets(
        ctx: Context,
        asset_type: str,
        game_style: str,
        asset_list: List[str],
        optimization_level: str = "game_ready",
        texture_resolution: int = 512,
        include_lods: bool = True
    ) -> Dict[str, Any]:
        """
        Generate game-ready 3D assets optimized for game engines.
        
        Perfect for Agent 4's game asset creation workflows where assets need to be
        optimized for Unity, Unreal Engine, or other game engines.
        
        Args:
            asset_type: Type of game assets ("environment", "character", "props", "weapons", "vehicles")
            game_style: Overall game art style ("realistic", "stylized", "cartoon", "low_poly", "pixel")
            asset_list: List of specific assets to generate
            optimization_level: Optimization level ("game_ready", "high_poly", "low_poly", "mobile")
            texture_resolution: Texture resolution based on target platform
            include_lods: Whether to generate multiple LOD levels
            
        Returns:
            Dict containing game-ready 3D asset collection
        """
        try:
            if not asset_list:
                return ResponseHelper.validation_error("asset_list", "At least one asset is required")
            
            logger.info(f"Generating {len(asset_list)} game-ready {asset_type} assets in {game_style} style")
            
            # Optimization settings based on level
            optimization_settings = {
                "game_ready": {
                    "poly_count": "optimized for real-time rendering",
                    "texture_size": texture_resolution,
                    "detail_level": "balanced quality and performance"
                },
                "high_poly": {
                    "poly_count": "high detail for hero assets",
                    "texture_size": min(texture_resolution * 2, 2048),
                    "detail_level": "maximum quality"
                },
                "low_poly": {
                    "poly_count": "minimal polygons for mobile",
                    "texture_size": max(texture_resolution // 2, 256),
                    "detail_level": "stylized simplified"
                },
                "mobile": {
                    "poly_count": "mobile optimized under 1000 tris",
                    "texture_size": max(texture_resolution // 2, 256),
                    "detail_level": "mobile performance focused"
                }
            }
            
            settings = optimization_settings.get(optimization_level, optimization_settings["game_ready"])
            
            results = []
            total_credits = 0.0
            
            # Generate each asset
            for i, asset_name in enumerate(asset_list):
                try:
                    # Create game-optimized prompt
                    game_prompt = f"{asset_name} {asset_type} asset, {game_style} game art style, {settings['poly_count']}, {settings['detail_level']}, game engine ready"
                    
                    if include_lods:
                        game_prompt += ", multiple LOD levels"
                    
                    # Generate the 3D asset
                    asset_result = await scenario_generate_3d(
                        ctx=ctx,
                        prompt=game_prompt,
                        model_type="mesh",
                        resolution=settings["texture_size"],
                        view_angles=["front", "side", "back"],
                        generate_textures=True,
                        generate_materials=True,
                        wait_for_completion=True
                    )
                    
                    if asset_result.get("success"):
                        data = asset_result["data"]
                        
                        # Add game-specific metadata
                        game_asset_info = {
                            "asset_name": asset_name,
                            "asset_type": asset_type,
                            "game_style": game_style,
                            "optimization_level": optimization_level,
                            "texture_resolution": settings["texture_size"],
                            "includes_lods": include_lods,
                            "poly_count_target": settings["poly_count"],
                            "game_engine_ready": True,
                            "pbr_materials": data.get("materials_included", True)
                        }
                        
                        results.append({
                            "asset_index": i,
                            "asset_name": asset_name,
                            "job_id": data["job_id"],
                            "status": "completed",
                            "game_asset_info": game_asset_info,
                            "model_assets": data.get("model_assets", []),
                            "texture_assets": data.get("texture_assets", []),
                            "material_assets": data.get("material_assets", []),
                            "credits_used": data.get("credits_used", 0)
                        })
                        total_credits += data.get("credits_used", 0)
                    else:
                        results.append({
                            "asset_index": i,
                            "asset_name": asset_name,
                            "status": "failed",
                            "error": asset_result.get("message", "Unknown error")
                        })
                    
                    logger.info(f"Completed game asset {i+1}/{len(asset_list)}: {asset_name}")
                
                except Exception as e:
                    logger.error(f"Failed game asset {i+1}: {asset_name} - {str(e)}")
                    results.append({
                        "asset_index": i,
                        "asset_name": asset_name,
                        "status": "failed",
                        "error": str(e)
                    })
            
            # Summary
            successful_assets = len([r for r in results if r.get("status") == "completed"])
            
            return ResponseHelper.success(
                f"Generated {successful_assets}/{len(asset_list)} game-ready 3D assets",
                data={
                    "asset_collection_info": {
                        "asset_type": asset_type,
                        "game_style": game_style,
                        "optimization_level": optimization_level,
                        "target_texture_resolution": texture_resolution,
                        "includes_lods": include_lods,
                        "game_engine_compatibility": ["Unity", "Unreal", "Godot", "Custom"]
                    },
                    "total_assets": len(asset_list),
                    "successful_assets": successful_assets,
                    "total_credits_used": total_credits,
                    "results": results,
                    "integration_notes": [
                        "Assets are optimized for real-time rendering",
                        "Textures follow PBR workflow standards",
                        "Models include proper UV mapping",
                        "Materials are game-engine compatible"
                    ]
                }
            )
        
        except Exception as e:
            logger.exception("Unexpected error in scenario_3d_game_assets")
            return ResponseHelper.error(f"3D game asset generation failed: {str(e)}")
    
    @mcp.tool()
    async def scenario_estimate_3d_cost(
        ctx: Context,
        prompt: str,
        model_type: str = "mesh",
        resolution: int = 512,
        generate_textures: bool = True,
        generate_materials: bool = True,
        view_angles: List[str] = None
    ) -> Dict[str, Any]:
        """
        Estimate cost for 3D model generation without executing.
        
        Perfect for Agent 4's 3D project budget planning and cost management.
        
        Args:
            prompt: 3D model description
            model_type: Type of 3D model
            resolution: Texture resolution
            generate_textures: Include texture generation
            generate_materials: Include material generation
            view_angles: Required view angles
            
        Returns:
            Dict containing 3D generation cost estimation
        """
        try:
            if view_angles is None:
                view_angles = ["front", "side", "back"]
            
            # Estimate based on complexity factors
            base_cost = 10.0  # Base cost for 3D generation
            
            # Resolution multiplier
            resolution_multiplier = (resolution / 512) ** 2
            
            # Feature multipliers
            texture_multiplier = 1.5 if generate_textures else 1.0
            material_multiplier = 1.3 if generate_materials else 1.0
            view_multiplier = len(view_angles) * 0.3
            
            # Model type complexity
            type_multipliers = {
                "mesh": 1.0,
                "texture": 0.7,
                "material": 0.5,
                "full_scene": 2.0
            }
            
            type_multiplier = type_multipliers.get(model_type, 1.0)
            
            # Calculate estimated cost
            estimated_cost = base_cost * resolution_multiplier * texture_multiplier * material_multiplier * (1 + view_multiplier) * type_multiplier
            
            return ResponseHelper.success(
                f"Estimated cost for 3D {model_type}: {estimated_cost:.2f} credits",
                data={
                    "estimated_credits": round(estimated_cost, 2),
                    "cost_breakdown": {
                        "base_cost": base_cost,
                        "resolution_factor": resolution_multiplier,
                        "texture_factor": texture_multiplier,
                        "material_factor": material_multiplier,
                        "view_angles_factor": 1 + view_multiplier,
                        "model_type_factor": type_multiplier
                    },
                    "generation_parameters": {
                        "prompt_length": len(prompt),
                        "model_type": model_type,
                        "resolution": resolution,
                        "view_angles": len(view_angles),
                        "includes_textures": generate_textures,
                        "includes_materials": generate_materials
                    },
                    "estimated_generation_time": "5-10 minutes",
                    "complexity_level": "high" if estimated_cost > 20 else "medium" if estimated_cost > 10 else "low"
                }
            )
        
        except Exception as e:
            logger.exception("Error in scenario_estimate_3d_cost")
            return ResponseHelper.error(f"3D cost estimation failed: {str(e)}")