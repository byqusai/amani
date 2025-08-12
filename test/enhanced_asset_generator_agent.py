#!/usr/bin/env python3
"""
Enhanced Scenario-AI-Asset-Generator Agent (Agent 4)
Integrates with Scenario AI for comprehensive game asset generation
"""

import asyncio
import json
import os
import sys
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
sys.path.append('/Users/qusaiabushanap/dev/amani/scenario-mcp')
from scenario_ai_direct import ScenarioAI

@dataclass
class AssetCategory:
    """Represents a game asset category with generation specifications."""
    name: str
    description: str
    asset_types: List[str]
    recommended_models: List[str]
    default_settings: Dict[str, Any]
    prompt_templates: Dict[str, str]
    quality_requirements: Dict[str, Any]
    batch_size_recommendation: int
    consistency_keywords: List[str]

@dataclass
class AssetGenerationPlan:
    """Represents a complete asset generation plan."""
    project_name: str
    categories: List[str]
    total_assets: int
    estimated_time: str
    model_assignments: Dict[str, str]
    batch_schedule: List[Dict[str, Any]]
    quality_checkpoints: List[str]
    delivery_timeline: Dict[str, str]

@dataclass
class AssetBatch:
    """Represents a batch of assets to be generated."""
    batch_id: str
    category: str
    asset_list: List[str]
    model_id: str
    settings: Dict[str, Any]
    priority: int
    dependencies: List[str]

class EnhancedAssetGenerator:
    """Enhanced Asset Generator with Scenario AI integration."""
    
    def __init__(self):
        self.scenario_ai = ScenarioAI()
        self.available_models = None
        self.asset_categories = self._initialize_asset_categories()
        self.generation_history = []
        self.consistency_tracker = {}
    
    def _initialize_asset_categories(self) -> Dict[str, AssetCategory]:
        """Initialize comprehensive asset category database."""
        return {
            "characters": AssetCategory(
                name="Characters & NPCs",
                description="Player characters, NPCs, enemies, and creatures",
                asset_types=[
                    "player_character_idle", "player_character_walk", "player_character_attack",
                    "npc_merchant", "npc_guard", "npc_villager", "npc_quest_giver",
                    "enemy_basic", "enemy_boss", "enemy_flying", "enemy_ranged",
                    "creature_friendly", "creature_hostile", "creature_neutral"
                ],
                recommended_models=["character-design-v3", "fantasy-characters", "game-sprites-v2"],
                default_settings={
                    "width": 512, "height": 512, "num_samples": 2,
                    "num_inference_steps": 35, "guidance": 6.0
                },
                prompt_templates={
                    "player_character": "{character_type}, game character design, {art_style}, full body, action pose, detailed features, transparent background, high quality",
                    "npc": "{npc_type}, friendly NPC, {art_style}, welcoming expression, detailed clothing, transparent background",
                    "enemy": "{enemy_type}, hostile creature, {art_style}, menacing appearance, battle-ready pose, transparent background",
                    "creature": "{creature_type}, fantasy creature, {art_style}, detailed anatomy, natural pose, transparent background"
                },
                quality_requirements={
                    "resolution_min": "512x512",
                    "background": "transparent",
                    "detail_level": "high",
                    "consistency_check": True
                },
                batch_size_recommendation=8,
                consistency_keywords=["character", "game art", "consistent style"]
            ),
            
            "environments": AssetCategory(
                name="Environments & Backgrounds",
                description="Game world backgrounds, levels, and environmental assets",
                asset_types=[
                    "forest_background", "cave_background", "castle_background", "village_background",
                    "dungeon_corridor", "throne_room", "marketplace", "tavern_interior",
                    "mountain_landscape", "ocean_view", "desert_scene", "swamp_area",
                    "sky_day", "sky_night", "sky_storm", "sky_sunset"
                ],
                recommended_models=["environment-art-v4", "landscape-generator", "fantasy-backgrounds"],
                default_settings={
                    "width": 1024, "height": 512, "num_samples": 1,
                    "num_inference_steps": 30, "guidance": 5.5
                },
                prompt_templates={
                    "outdoor": "{environment_type}, game background, {art_style}, atmospheric lighting, detailed landscape, panoramic view",
                    "indoor": "{interior_type}, game interior, {art_style}, ambient lighting, detailed architecture, room layout",
                    "sky": "{sky_type}, game skybox, {art_style}, atmospheric perspective, cloud details, horizon line",
                    "abstract": "{abstract_type}, game background, {art_style}, stylized environment, atmospheric mood"
                },
                quality_requirements={
                    "resolution_min": "1024x512",
                    "aspect_ratio": "2:1 or 16:9",
                    "detail_level": "medium-high",
                    "parallax_ready": True
                },
                batch_size_recommendation=6,
                consistency_keywords=["environment", "background", "atmospheric"]
            ),
            
            "ui_elements": AssetCategory(
                name="UI & Interface Elements",
                description="User interface components, buttons, icons, and HUD elements",
                asset_types=[
                    "button_normal", "button_hover", "button_pressed", "button_disabled",
                    "icon_health", "icon_mana", "icon_coin", "icon_experience",
                    "panel_inventory", "panel_settings", "panel_stats", "panel_quest",
                    "bar_health", "bar_mana", "bar_experience", "bar_loading",
                    "frame_portrait", "frame_item", "frame_skill", "frame_achievement"
                ],
                recommended_models=["ui-design-v3", "game-interface", "icon-generator"],
                default_settings={
                    "width": 256, "height": 256, "num_samples": 3,
                    "num_inference_steps": 25, "guidance": 7.0
                },
                prompt_templates={
                    "button": "{button_type} button, game UI, {art_style}, clean design, readable text area, transparent background",
                    "icon": "{icon_type} icon, game UI, {art_style}, simple design, recognizable symbol, transparent background",
                    "panel": "{panel_type} panel, game UI, {art_style}, organized layout, frame design, semi-transparent",
                    "bar": "{bar_type} progress bar, game UI, {art_style}, clear indication, gradient fill, border design"
                },
                quality_requirements={
                    "resolution_min": "256x256",
                    "scalability": "vector-ready",
                    "readability": "high contrast",
                    "consistency": "ui_family"
                },
                batch_size_recommendation=12,
                consistency_keywords=["UI", "interface", "clean design"]
            ),
            
            "items_equipment": AssetCategory(
                name="Items & Equipment",
                description="Weapons, armor, consumables, and collectible items",
                asset_types=[
                    "weapon_sword", "weapon_bow", "weapon_staff", "weapon_dagger",
                    "armor_helmet", "armor_chest", "armor_legs", "armor_boots",
                    "potion_health", "potion_mana", "potion_strength", "potion_speed",
                    "gem_ruby", "gem_emerald", "gem_sapphire", "gem_diamond",
                    "scroll_spell", "key_gold", "key_silver", "treasure_chest"
                ],
                recommended_models=["item-design-v2", "fantasy-equipment", "game-assets"],
                default_settings={
                    "width": 256, "height": 256, "num_samples": 2,
                    "num_inference_steps": 30, "guidance": 6.5
                },
                prompt_templates={
                    "weapon": "{weapon_type}, game weapon, {art_style}, detailed craftsmanship, isometric view, transparent background",
                    "armor": "{armor_type}, game armor, {art_style}, protective design, detailed materials, transparent background",
                    "consumable": "{consumable_type}, game item, {art_style}, attractive design, recognizable function, transparent background",
                    "treasure": "{treasure_type}, valuable item, {art_style}, precious appearance, detailed gems, transparent background"
                },
                quality_requirements={
                    "resolution_min": "256x256",
                    "view_angle": "isometric_preferred",
                    "detail_level": "high",
                    "material_clarity": True
                },
                batch_size_recommendation=10,
                consistency_keywords=["item", "equipment", "detailed"]
            ),
            
            "effects_particles": AssetCategory(
                name="Effects & Particles",
                description="Spell effects, particle systems, and visual feedback elements",
                asset_types=[
                    "spell_fire", "spell_ice", "spell_lightning", "spell_healing",
                    "particle_smoke", "particle_sparkles", "particle_dust", "particle_blood",
                    "impact_sword", "impact_arrow", "impact_magic", "impact_explosion",
                    "aura_divine", "aura_dark", "aura_elemental", "aura_protective",
                    "trail_weapon", "trail_magic", "trail_movement", "trail_projectile"
                ],
                recommended_models=["effect-generator", "particle-fx", "magic-effects"],
                default_settings={
                    "width": 512, "height": 512, "num_samples": 1,
                    "num_inference_steps": 28, "guidance": 4.5
                },
                prompt_templates={
                    "spell": "{spell_type} spell effect, magical energy, {art_style}, glowing particles, dynamic motion, transparent background",
                    "particle": "{particle_type} particle system, {art_style}, scattered elements, natural physics, transparent background",
                    "impact": "{impact_type} impact effect, {art_style}, explosive energy, debris scatter, transparent background",
                    "aura": "{aura_type} energy aura, {art_style}, radiating power, subtle glow, transparent background"
                },
                quality_requirements={
                    "resolution_min": "512x512",
                    "alpha_channel": "required",
                    "animation_ready": True,
                    "layering_support": True
                },
                batch_size_recommendation=4,
                consistency_keywords=["effect", "magical", "energy"]
            ),
            
            "tiles_props": AssetCategory(
                name="Tiles & Props",
                description="Level building tiles, decorative props, and interactive objects",
                asset_types=[
                    "tile_grass", "tile_stone", "tile_water", "tile_lava",
                    "prop_tree", "prop_rock", "prop_flower", "prop_mushroom",
                    "object_door", "object_chest", "object_lever", "object_altar",
                    "decoration_banner", "decoration_statue", "decoration_fountain", "decoration_torch"
                ],
                recommended_models=["tileset-generator", "prop-design", "environment-objects"],
                default_settings={
                    "width": 256, "height": 256, "num_samples": 1,
                    "num_inference_steps": 25, "guidance": 5.0
                },
                prompt_templates={
                    "tile": "{tile_type} tile, tileable texture, {art_style}, seamless edges, game asset, top-down view",
                    "prop": "{prop_type} prop, game object, {art_style}, environmental detail, natural placement, transparent background",
                    "interactive": "{object_type} interactive object, game asset, {art_style}, clear function, detailed design, transparent background",
                    "decoration": "{decoration_type} decorative object, game asset, {art_style}, atmospheric detail, transparent background"
                },
                quality_requirements={
                    "resolution_min": "256x256",
                    "tileable": "when_applicable",
                    "seamless_edges": True,
                    "optimization": "game_ready"
                },
                batch_size_recommendation=16,
                consistency_keywords=["tile", "prop", "environmental"]
            )
        }
    
    async def analyze_asset_requirements(self, gdd_content: str, art_style: str = "fantasy") -> Dict[str, Any]:
        """Analyze GDD content and determine comprehensive asset requirements."""
        
        # Parse GDD content for asset mentions
        content_lower = gdd_content.lower()
        detected_assets = {}
        
        for category_name, category in self.asset_categories.items():
            category_assets = []
            
            for asset_type in category.asset_types:
                # Check if asset type is mentioned in GDD
                asset_keywords = asset_type.split('_')
                if any(keyword in content_lower for keyword in asset_keywords):
                    category_assets.append(asset_type)
            
            if category_assets:
                detected_assets[category_name] = category_assets
        
        # Estimate generation requirements
        total_assets = sum(len(assets) for assets in detected_assets.values())
        estimated_time = self._estimate_generation_time(total_assets)
        
        # Get optimal models for each category
        model_assignments = {}
        for category_name in detected_assets.keys():
            optimal_models = await self._find_optimal_models_for_category(category_name, art_style)
            model_assignments[category_name] = optimal_models[0]["id"] if optimal_models else "flux.1-dev"
        
        return {
            "analysis_timestamp": datetime.now().isoformat(),
            "art_style": art_style,
            "detected_categories": list(detected_assets.keys()),
            "asset_breakdown": detected_assets,
            "total_assets": total_assets,
            "estimated_generation_time": estimated_time,
            "model_assignments": model_assignments,
            "priority_categories": self._determine_priority_categories(detected_assets),
            "production_phases": await self._create_production_phases(detected_assets, model_assignments),
            "quality_standards": self._define_quality_standards(art_style),
            "batch_recommendations": await self._create_batch_recommendations(detected_assets)
        }
    
    async def create_comprehensive_asset_plan(self, requirements: Dict[str, Any]) -> AssetGenerationPlan:
        """Create a comprehensive asset generation plan."""
        
        # Create batch schedule
        batch_schedule = []
        batch_id = 1
        
        for category, assets in requirements["asset_breakdown"].items():
            category_info = self.asset_categories[category]
            batch_size = category_info.batch_size_recommendation
            
            # Split assets into batches
            for i in range(0, len(assets), batch_size):
                batch_assets = assets[i:i + batch_size]
                batch = AssetBatch(
                    batch_id=f"batch_{batch_id:03d}",
                    category=category,
                    asset_list=batch_assets,
                    model_id=requirements["model_assignments"][category],
                    settings=category_info.default_settings.copy(),
                    priority=self._calculate_batch_priority(category, batch_assets),
                    dependencies=self._determine_batch_dependencies(category, batch_assets)
                )
                
                batch_schedule.append({
                    "batch_id": batch.batch_id,
                    "category": batch.category,
                    "assets": batch.asset_list,
                    "model": batch.model_id,
                    "priority": batch.priority,
                    "estimated_time": f"{len(batch_assets) * 2}min"
                })
                batch_id += 1
        
        # Sort batches by priority
        batch_schedule.sort(key=lambda x: x["priority"], reverse=True)
        
        return AssetGenerationPlan(
            project_name=f"Asset_Generation_{datetime.now().strftime('%Y%m%d')}",
            categories=list(requirements["asset_breakdown"].keys()),
            total_assets=requirements["total_assets"],
            estimated_time=requirements["estimated_generation_time"],
            model_assignments=requirements["model_assignments"],
            batch_schedule=batch_schedule,
            quality_checkpoints=[
                "Initial batch review (after 25% completion)",
                "Mid-project consistency check (at 50% completion)", 
                "Pre-delivery quality assurance (at 90% completion)"
            ],
            delivery_timeline={
                "phase_1_core": "Days 1-2: Characters and UI elements",
                "phase_2_world": "Days 3-4: Environments and props", 
                "phase_3_polish": "Days 5-6: Effects and final assets",
                "phase_4_delivery": "Day 7: Quality review and delivery"
            }
        )
    
    async def execute_asset_generation_batch(self, batch: Dict[str, Any], 
                                           art_style: str = "fantasy") -> Dict[str, Any]:
        """Execute generation for a specific asset batch."""
        
        category = batch["category"]
        assets = batch["assets"]
        model_id = batch["model"]
        
        if category not in self.asset_categories:
            return {"error": f"Unknown category: {category}"}
        
        category_info = self.asset_categories[category]
        generation_results = {}
        successful_generations = 0
        failed_generations = []
        
        # Process each asset in the batch
        for asset_type in assets:
            try:
                # Determine the appropriate prompt template
                template_key = self._determine_template_key(asset_type, category_info.prompt_templates.keys())
                prompt_template = category_info.prompt_templates.get(template_key, list(category_info.prompt_templates.values())[0])
                
                # Format the prompt
                formatted_prompt = prompt_template.format(
                    **self._extract_prompt_variables(asset_type, art_style)
                )
                
                # Add consistency keywords
                formatted_prompt += f", {', '.join(category_info.consistency_keywords)}"
                
                # Generate the asset
                generation_result = await self.scenario_ai.generate_image(
                    prompt=formatted_prompt,
                    model_id=model_id,
                    **category_info.default_settings
                )
                
                if generation_result["success"]:
                    generation_results[asset_type] = {
                        "status": "success",
                        "job_id": generation_result["data"]["job_id"],
                        "prompt": formatted_prompt,
                        "model": model_id,
                        "settings": category_info.default_settings,
                        "timestamp": datetime.now().isoformat()
                    }
                    successful_generations += 1
                else:
                    failed_generations.append({
                        "asset": asset_type,
                        "error": generation_result["message"]
                    })
                    generation_results[asset_type] = {
                        "status": "failed",
                        "error": generation_result["message"]
                    }
                
            except Exception as e:
                failed_generations.append({
                    "asset": asset_type,
                    "error": str(e)
                })
                generation_results[asset_type] = {
                    "status": "error",
                    "error": str(e)
                }
        
        # Update generation history
        self.generation_history.append({
            "batch_id": batch["batch_id"],
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "assets_attempted": len(assets),
            "assets_successful": successful_generations,
            "success_rate": successful_generations / len(assets) if assets else 0
        })
        
        return {
            "batch_id": batch["batch_id"],
            "category": category,
            "total_assets": len(assets),
            "successful": successful_generations,
            "failed": len(failed_generations),
            "success_rate": f"{(successful_generations / len(assets) * 100):.1f}%",
            "results": generation_results,
            "failed_assets": failed_generations,
            "estimated_completion_time": f"{successful_generations * 2}min",
            "next_steps": await self._generate_next_steps(generation_results, category)
        }
    
    async def perform_quality_consistency_check(self, generated_assets: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive quality and consistency checks on generated assets."""
        
        consistency_report = {
            "overall_score": 0.0,
            "category_scores": {},
            "issues_found": [],
            "recommendations": [],
            "regeneration_suggestions": []
        }
        
        category_scores = []
        
        # Analyze each category for consistency
        for category, assets in generated_assets.items():
            if category not in self.asset_categories:
                continue
            
            category_info = self.asset_categories[category]
            successful_assets = [a for a in assets.values() if a.get("status") == "success"]
            
            # Calculate category consistency score
            category_score = await self._calculate_category_consistency(successful_assets, category_info)
            category_scores.append(category_score)
            consistency_report["category_scores"][category] = category_score
            
            # Check for specific issues
            issues = await self._identify_category_issues(successful_assets, category_info)
            consistency_report["issues_found"].extend(issues)
            
            # Generate recommendations
            recommendations = await self._generate_category_recommendations(successful_assets, category_info)
            consistency_report["recommendations"].extend(recommendations)
        
        # Calculate overall score
        consistency_report["overall_score"] = sum(category_scores) / len(category_scores) if category_scores else 0
        
        # Generate regeneration suggestions for low-quality assets
        if consistency_report["overall_score"] < 7.0:
            regeneration_suggestions = await self._suggest_regenerations(generated_assets, consistency_report)
            consistency_report["regeneration_suggestions"] = regeneration_suggestions
        
        return consistency_report
    
    async def generate_asset_variations(self, base_asset: str, variation_count: int = 3,
                                      variation_type: str = "color") -> Dict[str, Any]:
        """Generate variations of a base asset."""
        
        variation_prompts = {
            "color": [
                "red color scheme variant",
                "blue color scheme variant", 
                "green color scheme variant",
                "purple color scheme variant"
            ],
            "style": [
                "more detailed version",
                "simplified version",
                "weathered/worn version",
                "pristine/new version"
            ],
            "pose": [
                "different action pose",
                "idle stance variant",
                "defensive pose",
                "aggressive pose"
            ],
            "lighting": [
                "dramatic lighting",
                "soft ambient lighting",
                "backlit silhouette",
                "multiple light sources"
            ]
        }
        
        if variation_type not in variation_prompts:
            return {"error": f"Unknown variation type: {variation_type}"}
        
        base_prompt = f"{base_asset}, game asset, high quality, transparent background"
        variations = {}
        
        for i in range(min(variation_count, len(variation_prompts[variation_type]))):
            variation_modifier = variation_prompts[variation_type][i]
            variation_prompt = f"{base_prompt}, {variation_modifier}"
            
            generation_result = await self.scenario_ai.generate_image(
                prompt=variation_prompt,
                model_id="flux.1-dev",  # Use default model for variations
                width=512,
                height=512
            )
            
            variations[f"variation_{i+1}"] = {
                "modifier": variation_modifier,
                "prompt": variation_prompt,
                "generation_result": generation_result
            }
        
        return {
            "base_asset": base_asset,
            "variation_type": variation_type,
            "variations": variations,
            "generation_timestamp": datetime.now().isoformat()
        }
    
    async def create_asset_optimization_report(self, generated_assets: Dict[str, Any]) -> Dict[str, Any]:
        """Create optimization recommendations for generated assets."""
        
        optimization_report = {
            "file_size_analysis": {},
            "resolution_recommendations": {},
            "format_suggestions": {},
            "compression_settings": {},
            "performance_impact": {},
            "mobile_optimization": {}
        }
        
        for category, assets in generated_assets.items():
            if category not in self.asset_categories:
                continue
            
            category_info = self.asset_categories[category]
            successful_assets = [a for a in assets.values() if a.get("status") == "success"]
            
            # File size analysis
            optimization_report["file_size_analysis"][category] = {
                "estimated_size_per_asset": self._estimate_file_size(category_info.default_settings),
                "total_category_size": f"{len(successful_assets) * self._estimate_file_size(category_info.default_settings)}MB",
                "compression_potential": "30-50% with proper optimization"
            }
            
            # Resolution recommendations
            optimization_report["resolution_recommendations"][category] = await self._get_resolution_recommendations(category_info)
            
            # Format suggestions
            optimization_report["format_suggestions"][category] = self._get_format_suggestions(category)
            
            # Compression settings
            optimization_report["compression_settings"][category] = self._get_compression_settings(category)
        
        # Performance impact analysis
        optimization_report["performance_impact"] = await self._analyze_performance_impact(generated_assets)
        
        # Mobile optimization
        optimization_report["mobile_optimization"] = await self._create_mobile_optimization_plan(generated_assets)
        
        return optimization_report
    
    # Helper methods
    async def _find_optimal_models_for_category(self, category: str, art_style: str) -> List[Dict[str, Any]]:
        """Find optimal Scenario AI models for a specific asset category."""
        
        if not self.available_models:
            models_result = await self.scenario_ai.get_models(limit=100)
            if models_result["success"]:
                self.available_models = models_result["data"]["categorized_models"]
        
        category_info = self.asset_categories.get(category)
        if not category_info:
            return []
        
        optimal_models = []
        
        # Search through all model categories
        for model_category, models in self.available_models.items():
            for model in models:
                score = await self._score_model_for_category(model, category_info, art_style)
                
                if score > 6.0:  # Good compatibility threshold
                    optimal_models.append({
                        "id": model["id"],
                        "name": model["name"],
                        "score": score,
                        "category": model_category,
                        "specialization": await self._determine_model_specialization(model, category)
                    })
        
        # Sort by score and return top models
        optimal_models.sort(key=lambda x: x["score"], reverse=True)
        return optimal_models[:3]
    
    async def _score_model_for_category(self, model: Dict[str, Any], 
                                      category_info: AssetCategory, art_style: str) -> float:
        """Score how well a model fits an asset category."""
        score = 5.0  # Base score
        
        model_name_lower = model["name"].lower()
        model_tags = [tag.lower() for tag in model.get("tags", [])]
        
        # Category-specific scoring
        category_keywords = category_info.name.lower().split() + category_info.consistency_keywords
        
        for keyword in category_keywords:
            if keyword in model_name_lower:
                score += 1.0
            for tag in model_tags:
                if keyword in tag:
                    score += 0.3
        
        # Art style compatibility
        if art_style.lower() in model_name_lower:
            score += 1.5
        
        # Asset type specific bonuses
        if category_info.name == "Characters & NPCs":
            if any(word in model_name_lower for word in ["character", "person", "npc", "creature"]):
                score += 2.0
        elif category_info.name == "Environments & Backgrounds":
            if any(word in model_name_lower for word in ["environment", "landscape", "background", "scene"]):
                score += 2.0
        elif category_info.name == "UI & Interface Elements":
            if any(word in model_name_lower for word in ["ui", "interface", "icon", "button"]):
                score += 2.0
        
        # Quality indicators
        if model.get("training_steps", 0) > 1500:
            score += 0.5
        if model.get("is_public"):
            score += 0.3
        
        return min(score, 10.0)
    
    def _estimate_generation_time(self, asset_count: int) -> str:
        """Estimate total generation time for assets."""
        # Rough estimate: 2 minutes per asset including processing
        total_minutes = asset_count * 2
        
        if total_minutes < 60:
            return f"{total_minutes} minutes"
        else:
            hours = total_minutes // 60
            minutes = total_minutes % 60
            return f"{hours}h {minutes}min"
    
    def _determine_priority_categories(self, detected_assets: Dict[str, List[str]]) -> List[str]:
        """Determine priority order for asset categories."""
        priority_order = [
            "characters",      # Core gameplay elements first
            "ui_elements",     # Interface elements for user interaction
            "environments",    # World building
            "items_equipment", # Game content
            "tiles_props",     # Level details
            "effects_particles" # Polish elements
        ]
        
        return [cat for cat in priority_order if cat in detected_assets]
    
    async def _create_production_phases(self, detected_assets: Dict[str, List[str]], 
                                       model_assignments: Dict[str, str]) -> Dict[str, Any]:
        """Create production phases based on detected assets."""
        return {
            "phase_1_foundation": {
                "description": "Core game elements (characters, UI)",
                "categories": [cat for cat in ["characters", "ui_elements"] if cat in detected_assets],
                "timeline": "Days 1-2",
                "priority": "high"
            },
            "phase_2_world_building": {
                "description": "Game world and environment",
                "categories": [cat for cat in ["environments", "tiles_props"] if cat in detected_assets],
                "timeline": "Days 3-4", 
                "priority": "medium-high"
            },
            "phase_3_content": {
                "description": "Items and equipment",
                "categories": [cat for cat in ["items_equipment"] if cat in detected_assets],
                "timeline": "Day 5",
                "priority": "medium"
            },
            "phase_4_polish": {
                "description": "Effects and visual polish",
                "categories": [cat for cat in ["effects_particles"] if cat in detected_assets],
                "timeline": "Day 6",
                "priority": "low"
            }
        }
    
    def _define_quality_standards(self, art_style: str) -> Dict[str, Any]:
        """Define quality standards based on art style."""
        base_standards = {
            "resolution_minimum": "256x256",
            "format_required": "PNG with alpha channel",
            "consistency_check": True,
            "color_accuracy": "high",
            "detail_level": "appropriate_for_style"
        }
        
        style_specific = {
            "pixel": {
                "pixel_perfect": True,
                "anti_aliasing": False,
                "color_limit": "palette_based"
            },
            "fantasy": {
                "detail_level": "high",
                "color_richness": "saturated",
                "texture_detail": "visible"
            },
            "minimalist": {
                "clean_edges": True,
                "color_simplicity": "limited_palette",
                "geometric_precision": True
            }
        }
        
        if art_style.lower() in style_specific:
            base_standards.update(style_specific[art_style.lower()])
        
        return base_standards
    
    async def _create_batch_recommendations(self, detected_assets: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Create batch processing recommendations."""
        recommendations = []
        
        for category, assets in detected_assets.items():
            if category in self.asset_categories:
                category_info = self.asset_categories[category]
                batch_size = category_info.batch_size_recommendation
                
                num_batches = (len(assets) + batch_size - 1) // batch_size
                
                recommendations.append({
                    "category": category,
                    "total_assets": len(assets),
                    "recommended_batch_size": batch_size,
                    "number_of_batches": num_batches,
                    "processing_strategy": "sequential" if category == "characters" else "parallel"
                })
        
        return recommendations
    
    def _calculate_batch_priority(self, category: str, assets: List[str]) -> int:
        """Calculate priority score for a batch (1-10, higher is more important)."""
        category_priorities = {
            "characters": 10,
            "ui_elements": 9,
            "environments": 7,
            "items_equipment": 6,
            "tiles_props": 4,
            "effects_particles": 3
        }
        
        base_priority = category_priorities.get(category, 5)
        
        # Adjust based on asset types
        critical_assets = ["player_character", "main_menu", "health_bar"]
        if any(critical in asset for asset in assets for critical in critical_assets):
            base_priority += 2
        
        return min(base_priority, 10)
    
    def _determine_batch_dependencies(self, category: str, assets: List[str]) -> List[str]:
        """Determine what other batches this batch depends on."""
        dependencies = []
        
        # UI elements depend on having the art style established by characters
        if category == "ui_elements":
            dependencies.append("characters")
        
        # Effects often need to match character/environment styles
        if category == "effects_particles":
            dependencies.extend(["characters", "environments"])
        
        # Props should match environment style
        if category == "tiles_props":
            dependencies.append("environments")
        
        return dependencies
    
    def _determine_template_key(self, asset_type: str, available_keys: List[str]) -> str:
        """Determine which prompt template to use for an asset type."""
        asset_parts = asset_type.split('_')
        
        # Direct match
        for key in available_keys:
            if key in asset_type:
                return key
        
        # Partial match
        for key in available_keys:
            if any(part in key for part in asset_parts):
                return key
        
        # Fallback to first available template
        return list(available_keys)[0]
    
    def _extract_prompt_variables(self, asset_type: str, art_style: str) -> Dict[str, str]:
        """Extract variables for prompt formatting."""
        parts = asset_type.split('_')
        
        variables = {
            "art_style": art_style,
            "character_type": parts[1] if len(parts) > 1 and parts[0] == "character" else "character",
            "npc_type": parts[1] if len(parts) > 1 and parts[0] == "npc" else "friendly character",
            "enemy_type": parts[1] if len(parts) > 1 and parts[0] == "enemy" else "hostile creature",
            "creature_type": parts[1] if len(parts) > 1 and parts[0] == "creature" else "fantasy creature",
            "environment_type": parts[1] if len(parts) > 1 and parts[0] in ["forest", "cave", "castle"] else "landscape",
            "interior_type": parts[1] if len(parts) > 1 and "interior" in asset_type else "room",
            "sky_type": parts[1] if len(parts) > 1 and parts[0] == "sky" else "cloudy sky",
            "abstract_type": parts[1] if len(parts) > 1 else "abstract background",
            "button_type": parts[1] if len(parts) > 1 and parts[0] == "button" else "interactive",
            "icon_type": parts[1] if len(parts) > 1 and parts[0] == "icon" else "game",
            "panel_type": parts[1] if len(parts) > 1 and parts[0] == "panel" else "interface",
            "bar_type": parts[1] if len(parts) > 1 and parts[0] == "bar" else "progress",
            "weapon_type": parts[1] if len(parts) > 1 and parts[0] == "weapon" else "sword",
            "armor_type": parts[1] if len(parts) > 1 and parts[0] == "armor" else "protective gear",
            "consumable_type": parts[1] if len(parts) > 1 and parts[0] in ["potion", "scroll"] else "magical item",
            "treasure_type": parts[1] if len(parts) > 1 and parts[0] in ["gem", "key", "treasure"] else "valuable item",
            "spell_type": parts[1] if len(parts) > 1 and parts[0] == "spell" else "magical energy",
            "particle_type": parts[1] if len(parts) > 1 and parts[0] == "particle" else "floating particles",
            "impact_type": parts[1] if len(parts) > 1 and parts[0] == "impact" else "collision effect",
            "aura_type": parts[1] if len(parts) > 1 and parts[0] == "aura" else "energy field",
            "tile_type": parts[1] if len(parts) > 1 and parts[0] == "tile" else "ground texture",
            "prop_type": parts[1] if len(parts) > 1 and parts[0] == "prop" else "environmental object",
            "object_type": parts[1] if len(parts) > 1 and parts[0] == "object" else "interactive item",
            "decoration_type": parts[1] if len(parts) > 1 and parts[0] == "decoration" else "ornamental object"
        }
        
        return variables
    
    async def _generate_next_steps(self, generation_results: Dict[str, Any], category: str) -> List[str]:
        """Generate recommended next steps after batch completion."""
        next_steps = []
        
        successful_count = sum(1 for result in generation_results.values() if result.get("status") == "success")
        total_count = len(generation_results)
        success_rate = successful_count / total_count if total_count > 0 else 0
        
        if success_rate < 0.7:
            next_steps.append("Review failed generations and regenerate with adjusted prompts")
        
        if success_rate >= 0.8:
            next_steps.append("Proceed to quality consistency check")
            next_steps.append("Consider generating variations of best assets")
        
        next_steps.append(f"Begin next priority batch or move to {category} optimization")
        
        return next_steps
    
    async def _calculate_category_consistency(self, assets: List[Dict[str, Any]], 
                                           category_info: AssetCategory) -> float:
        """Calculate consistency score for a category (0-10)."""
        if not assets:
            return 0.0
        
        # This would typically involve image analysis
        # For now, return a simulated score based on successful generations
        base_score = 7.0
        
        # Bonus for having recommended batch size
        if len(assets) >= category_info.batch_size_recommendation * 0.8:
            base_score += 1.0
        
        # Consistency keywords bonus (simulated)
        base_score += 1.0
        
        return min(base_score, 10.0)
    
    async def _identify_category_issues(self, assets: List[Dict[str, Any]], 
                                      category_info: AssetCategory) -> List[str]:
        """Identify potential issues in a category."""
        issues = []
        
        if len(assets) < category_info.batch_size_recommendation * 0.5:
            issues.append(f"Low asset count in {category_info.name} category")
        
        # Simulated issue detection
        issues.append("Some assets may need color consistency review")
        
        return issues
    
    async def _generate_category_recommendations(self, assets: List[Dict[str, Any]], 
                                               category_info: AssetCategory) -> List[str]:
        """Generate recommendations for a category."""
        recommendations = []
        
        if len(assets) < category_info.batch_size_recommendation:
            recommendations.append(f"Consider generating additional {category_info.name.lower()}")
        
        recommendations.append(f"Review {category_info.name.lower()} against quality requirements")
        
        return recommendations
    
    async def _suggest_regenerations(self, generated_assets: Dict[str, Any], 
                                   consistency_report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest assets that should be regenerated."""
        suggestions = []
        
        for category, score in consistency_report["category_scores"].items():
            if score < 6.0:
                suggestions.append({
                    "category": category,
                    "reason": "Low consistency score",
                    "recommended_action": "Regenerate with more specific prompts"
                })
        
        return suggestions
    
    async def _determine_model_specialization(self, model: Dict[str, Any], category: str) -> str:
        """Determine what the model specializes in for this category."""
        model_name_lower = model["name"].lower()
        
        specializations = {
            "characters": ["portraits", "full body", "creatures", "people"],
            "environments": ["landscapes", "interiors", "backgrounds", "scenes"],
            "ui_elements": ["icons", "buttons", "interface", "symbols"],
            "items_equipment": ["objects", "weapons", "armor", "items"],
            "effects_particles": ["effects", "magic", "particles", "energy"],
            "tiles_props": ["textures", "props", "objects", "tiles"]
        }
        
        category_specs = specializations.get(category, [])
        for spec in category_specs:
            if spec in model_name_lower:
                return spec.title()
        
        return "General"
    
    def _estimate_file_size(self, settings: Dict[str, Any]) -> float:
        """Estimate file size in MB based on generation settings."""
        width = settings.get("width", 512)
        height = settings.get("height", 512)
        
        # Rough estimate: 4 bytes per pixel for RGBA PNG
        pixels = width * height
        estimated_mb = (pixels * 4) / (1024 * 1024)
        
        return round(estimated_mb, 2)
    
    async def _get_resolution_recommendations(self, category_info: AssetCategory) -> Dict[str, str]:
        """Get resolution recommendations for a category."""
        return {
            "development": f"{category_info.default_settings['width']}x{category_info.default_settings['height']}",
            "production": "2x development resolution for high-DPI displays",
            "optimization": "Consider multiple resolutions for different platforms"
        }
    
    def _get_format_suggestions(self, category: str) -> Dict[str, str]:
        """Get format suggestions for a category."""
        format_map = {
            "characters": "PNG with alpha channel for transparency",
            "environments": "JPG for backgrounds, PNG for foreground elements",
            "ui_elements": "PNG with alpha channel, consider SVG for scalability",
            "items_equipment": "PNG with alpha channel",
            "effects_particles": "PNG with alpha channel, consider animated formats",
            "tiles_props": "PNG for objects, consider tileable formats for tiles"
        }
        
        return {
            "recommended": format_map.get(category, "PNG with alpha channel"),
            "alternatives": "WebP for smaller file sizes, AVIF for modern browsers"
        }
    
    def _get_compression_settings(self, category: str) -> Dict[str, Any]:
        """Get compression settings for a category."""
        return {
            "png_quality": "85-95% for final assets",
            "jpg_quality": "80-90% for backgrounds",
            "webp_quality": "80-90% for web deployment",
            "optimization_tools": ["OptiPNG", "TinyPNG", "ImageOptim"]
        }
    
    async def _analyze_performance_impact(self, generated_assets: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance impact of generated assets."""
        total_assets = sum(len(assets) for assets in generated_assets.values())
        estimated_memory = total_assets * 2  # MB estimate
        
        return {
            "total_asset_count": total_assets,
            "estimated_memory_usage": f"{estimated_memory}MB",
            "loading_time_estimate": f"{total_assets * 0.1:.1f}s",
            "optimization_priority": "high" if estimated_memory > 100 else "medium"
        }
    
    async def _create_mobile_optimization_plan(self, generated_assets: Dict[str, Any]) -> Dict[str, Any]:
        """Create mobile optimization plan."""
        return {
            "resolution_scaling": "50-75% of desktop resolution",
            "format_optimization": "WebP where supported, PNG fallback",
            "loading_strategy": "Progressive loading with low-res previews",
            "memory_management": "Asset pooling and unloading of off-screen elements"
        }


# CLI Interface
async def main():
    """CLI interface for the Enhanced Asset Generator."""
    if len(sys.argv) < 2:
        print("Enhanced Asset Generator - Usage:")
        print("  python enhanced_asset_generator_agent.py analyze 'GDD content here' [art_style]")
        print("  python enhanced_asset_generator_agent.py plan 'requirements_json_file'")
        print("  python enhanced_asset_generator_agent.py generate_batch 'batch_json_file' [art_style]")
        print("  python enhanced_asset_generator_agent.py quality_check 'assets_json_file'")
        print("  python enhanced_asset_generator_agent.py variations 'base_asset' [count] [type]")
        print("  python enhanced_asset_generator_agent.py optimize 'assets_json_file'")
        return
    
    command = sys.argv[1]
    generator = EnhancedAssetGenerator()
    
    if command == "analyze" and len(sys.argv) > 2:
        gdd_content = sys.argv[2]
        art_style = sys.argv[3] if len(sys.argv) > 3 else "fantasy"
        result = await generator.analyze_asset_requirements(gdd_content, art_style)
        print(json.dumps(result, indent=2))
    
    elif command == "plan" and len(sys.argv) > 2:
        with open(sys.argv[2], 'r') as f:
            requirements = json.load(f)
        result = await generator.create_comprehensive_asset_plan(requirements)
        # Convert dataclass to dict for JSON serialization
        plan_dict = {
            "project_name": result.project_name,
            "categories": result.categories,
            "total_assets": result.total_assets,
            "estimated_time": result.estimated_time,
            "model_assignments": result.model_assignments,
            "batch_schedule": result.batch_schedule,
            "quality_checkpoints": result.quality_checkpoints,
            "delivery_timeline": result.delivery_timeline
        }
        print(json.dumps(plan_dict, indent=2))
    
    elif command == "generate_batch" and len(sys.argv) > 2:
        with open(sys.argv[2], 'r') as f:
            batch_data = json.load(f)
        art_style = sys.argv[3] if len(sys.argv) > 3 else "fantasy"
        result = await generator.execute_asset_generation_batch(batch_data, art_style)
        print(json.dumps(result, indent=2))
    
    elif command == "quality_check" and len(sys.argv) > 2:
        with open(sys.argv[2], 'r') as f:
            assets_data = json.load(f)
        result = await generator.perform_quality_consistency_check(assets_data)
        print(json.dumps(result, indent=2))
    
    elif command == "variations" and len(sys.argv) > 2:
        base_asset = sys.argv[2]
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        variation_type = sys.argv[4] if len(sys.argv) > 4 else "color"
        result = await generator.generate_asset_variations(base_asset, count, variation_type)
        print(json.dumps(result, indent=2))
    
    elif command == "optimize" and len(sys.argv) > 2:
        with open(sys.argv[2], 'r') as f:
            assets_data = json.load(f)
        result = await generator.create_asset_optimization_report(assets_data)
        print(json.dumps(result, indent=2))
    
    else:
        print("Invalid command or missing arguments")

if __name__ == "__main__":
    asyncio.run(main())