#!/usr/bin/env python3
"""
Enhanced Art-Direction-Analyst Agent (Agent 2)
Integrates with Scenario AI for visual communication and model curation
"""

import asyncio
import json
import os
import sys
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
sys.path.append('/Users/qusaiabushanap/dev/amani/scenario-mcp')
from scenario_ai_direct import ScenarioAI

@dataclass
class VisualStyle:
    """Represents a visual art style with AI model specifications."""
    name: str
    description: str
    color_palette: List[str]  # Hex colors
    mood_words: List[str]
    reference_games: List[str]
    scenario_models: List[str]
    prompt_template: str
    pros: List[str]
    cons: List[str]
    sample_prompts: List[str]
    model_blend_ratio: Optional[Dict[str, float]] = None

@dataclass
class ModelRecommendation:
    """Represents a Scenario AI model recommendation."""
    model_id: str
    model_name: str
    suitability_score: float  # 0-10
    strengths: List[str]
    limitations: List[str]
    optimal_settings: Dict[str, Any]
    sample_prompt: str

class EnhancedArtDirectionAnalyst:
    """Enhanced Art Direction Analyst with Scenario AI integration."""
    
    def __init__(self):
        self.scenario_ai = ScenarioAI()
        self.available_models = None
        self.visual_style_database = self._initialize_style_database()
    
    def _initialize_style_database(self) -> Dict[str, VisualStyle]:
        """Initialize database of visual styles with AI model mappings."""
        return {
            "pixel_perfect": VisualStyle(
                name="Pixel Perfect Retro",
                description="Crisp pixel art reminiscent of 16-bit era games with modern polish",
                color_palette=["#2C3E50", "#E74C3C", "#F39C12", "#27AE60", "#9B59B6"],
                mood_words=["Nostalgic", "Crisp", "Vibrant"],
                reference_games=["Celeste", "Dead Cells", "Hyper Light Drifter"],
                scenario_models=["pixel-art-v2", "retro-game-sprites", "16bit-enhanced"],
                prompt_template="{object}, pixel art style, 16-bit inspired, crisp pixels, vibrant colors, transparent background, game sprite",
                pros=["Highly performant", "Nostalgic appeal", "Clear readability"],
                cons=["Limited detail potential", "Style may feel dated"],
                sample_prompts=[
                    "fantasy knight, pixel art style, 16-bit inspired, crisp pixels, vibrant colors, transparent background, game sprite",
                    "magical forest background, pixel art style, 16-bit inspired, vibrant colors, parallax layers",
                    "fire spell effect, pixel art style, animated sprite sheet, glowing particles"
                ]
            ),
            
            "hand_painted_fantasy": VisualStyle(
                name="Hand-Painted Fantasy",
                description="Rich, painterly style with detailed textures and magical atmosphere",
                color_palette=["#8B4513", "#228B22", "#4169E1", "#FFD700", "#8A2BE2"],
                mood_words=["Magical", "Rich", "Atmospheric"],
                reference_games=["Ori and the Blind Forest", "Rayman Legends", "Child of Light"],
                scenario_models=["fantasy-art-v3", "painterly-style", "magical-environments"],
                prompt_template="{object}, hand-painted style, fantasy art, rich textures, magical atmosphere, detailed brushwork, transparent background",
                pros=["Highly detailed", "Emotional impact", "Timeless appeal"],
                cons=["Performance intensive", "Longer production time"],
                sample_prompts=[
                    "elven archer, hand-painted style, fantasy art, rich textures, magical atmosphere, detailed brushwork, transparent background",
                    "enchanted forest clearing, hand-painted style, fantasy art, magical lighting, detailed foliage",
                    "spell casting effect, hand-painted style, swirling magic, glowing particles, ethereal wisps"
                ],
                model_blend_ratio={"fantasy-art-v3": 0.6, "painterly-style": 0.4}
            ),
            
            "minimalist_geometric": VisualStyle(
                name="Minimalist Geometric",
                description="Clean, geometric shapes with bold colors and simple elegance",
                color_palette=["#FFFFFF", "#000000", "#FF6B6B", "#4ECDC4", "#45B7D1"],
                mood_words=["Clean", "Modern", "Elegant"],
                reference_games=["Monument Valley", "GRIS", "Alto's Odyssey"],
                scenario_models=["geometric-art", "minimalist-design", "low-poly-v2"],
                prompt_template="{object}, minimalist geometric style, clean shapes, bold colors, simple design, flat design, transparent background",
                pros=["Excellent performance", "Universal appeal", "Easy to animate"],
                cons=["Limited emotional range", "May lack personality"],
                sample_prompts=[
                    "geometric character, minimalist style, clean shapes, bold colors, simple design, transparent background",
                    "abstract landscape, minimalist geometric style, flat design, harmonious colors",
                    "UI elements, minimalist geometric style, clean icons, bold accent colors"
                ]
            ),
            
            "dark_atmospheric": VisualStyle(
                name="Dark Atmospheric Horror",
                description="Moody, dark themes with dramatic lighting and unsettling atmosphere",
                color_palette=["#1A1A1A", "#8B0000", "#4B0082", "#2F4F4F", "#800080"],
                mood_words=["Ominous", "Mysterious", "Dramatic"],
                reference_games=["Limbo", "Inside", "Little Nightmares"],
                scenario_models=["dark-art-v2", "horror-atmosphere", "noir-style"],
                prompt_template="{object}, dark atmospheric style, dramatic lighting, moody shadows, horror aesthetic, mysterious atmosphere, transparent background",
                pros=["Strong emotional impact", "Unique atmosphere", "Memorable aesthetics"],
                cons=["Limited audience appeal", "May be too intense"],
                sample_prompts=[
                    "shadowy figure, dark atmospheric style, dramatic lighting, moody shadows, horror aesthetic, transparent background",
                    "abandoned building interior, dark atmospheric style, dramatic lighting, eerie atmosphere",
                    "creepy ambient effect, dark atmospheric style, swirling shadows, ominous particles"
                ]
            ),
            
            "cartoon_vibrant": VisualStyle(
                name="Cartoon Vibrant",
                description="Bright, cheerful cartoon style with exaggerated features and bold colors",
                color_palette=["#FF69B4", "#00CED1", "#FFD700", "#32CD32", "#FF4500"],
                mood_words=["Playful", "Energetic", "Cheerful"],
                reference_games=["Cuphead", "A Hat in Time", "Psychonauts"],
                scenario_models=["cartoon-style-v4", "toon-shading", "animated-characters"],
                prompt_template="{object}, cartoon style, vibrant colors, exaggerated features, bold outlines, playful design, transparent background",
                pros=["Broad appeal", "Highly expressive", "Animation-friendly"],
                cons=["May appear childish", "Oversaturated market"],
                sample_prompts=[
                    "cartoon hero character, vibrant colors, exaggerated features, bold outlines, playful design, transparent background",
                    "colorful cartoon landscape, vibrant colors, whimsical design, cheerful atmosphere",
                    "cartoon explosion effect, vibrant colors, exaggerated impact, comic book style"
                ]
            )
        }
    
    async def analyze_game_concept(self, game_concept: str, target_audience: str = "general", 
                                 platform: str = "desktop", complexity_level: str = "medium") -> Dict[str, Any]:
        """Analyze game concept and return art direction recommendations."""
        
        # Map concept keywords to style preferences
        concept_lower = game_concept.lower()
        style_scores = {}
        
        # Score each style based on concept keywords
        for style_name, style in self.visual_style_database.items():
            score = 0
            
            # Genre matching
            if any(word in concept_lower for word in ["fantasy", "magic", "medieval", "dragon"]):
                if style_name == "hand_painted_fantasy":
                    score += 30
                elif style_name == "pixel_perfect":
                    score += 20
            
            if any(word in concept_lower for word in ["horror", "dark", "scary", "thriller"]):
                if style_name == "dark_atmospheric":
                    score += 35
            
            if any(word in concept_lower for word in ["casual", "mobile", "puzzle", "family"]):
                if style_name in ["minimalist_geometric", "cartoon_vibrant"]:
                    score += 25
            
            if any(word in concept_lower for word in ["retro", "classic", "8-bit", "16-bit"]):
                if style_name == "pixel_perfect":
                    score += 35
            
            # Platform considerations
            if platform == "mobile":
                if style_name in ["minimalist_geometric", "cartoon_vibrant"]:
                    score += 15
                elif style_name == "hand_painted_fantasy":
                    score -= 10
            
            # Audience considerations
            if target_audience == "children":
                if style_name == "cartoon_vibrant":
                    score += 20
                elif style_name == "dark_atmospheric":
                    score -= 25
            
            style_scores[style_name] = score
        
        # Sort styles by score
        recommended_styles = sorted(style_scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "analysis": {
                "game_concept": game_concept,
                "target_audience": target_audience,
                "platform": platform,
                "complexity_level": complexity_level
            },
            "style_recommendations": recommended_styles[:3],
            "emotional_response_target": self._determine_emotional_target(concept_lower),
            "technical_constraints": self._analyze_technical_constraints(platform, complexity_level),
            "cultural_considerations": self._analyze_cultural_considerations(game_concept)
        }
    
    async def present_art_direction_approaches(self, game_concept: str, **kwargs) -> Dict[str, Any]:
        """Present 3 visual art direction approaches with generated samples."""
        
        # Analyze concept first
        analysis = await self.analyze_game_concept(game_concept, **kwargs)
        top_styles = [style_name for style_name, score in analysis["style_recommendations"]]
        
        approaches = {}
        sample_generations = {}
        
        # Get available models first
        if not self.available_models:
            models_result = await self.scenario_ai.get_models(limit=100)
            if models_result["success"]:
                self.available_models = models_result["data"]["categorized_models"]
        
        # Generate approaches for top 3 styles
        for i, style_name in enumerate(top_styles[:3], 1):
            style = self.visual_style_database[style_name]
            
            # Find best matching Scenario models
            model_recommendations = await self._find_best_models_for_style(style)
            
            # Generate sample image
            sample_prompt = style.sample_prompts[0].replace("{object}", "game character concept")
            best_model = model_recommendations[0].model_id if model_recommendations else "flux.1-dev"
            
            generation_result = await self.scenario_ai.generate_image(
                prompt=sample_prompt,
                model_id=best_model,
                width=512,
                height=512
            )
            
            approaches[f"approach_{chr(65+i-1)}"] = {
                "style": style,
                "model_recommendations": model_recommendations,
                "generation_job": generation_result,
                "suitability_score": analysis["style_recommendations"][i-1][1]
            }
        
        return {
            "game_concept": game_concept,
            "approaches": approaches,
            "technical_analysis": analysis["technical_constraints"],
            "cultural_considerations": analysis["cultural_considerations"],
            "recommended_workflow": await self._create_workflow_recommendation(approaches)
        }
    
    async def create_visual_style_comparison(self, styles: List[str], 
                                           comparison_prompts: List[str]) -> Dict[str, Any]:
        """Generate side-by-side visual comparisons of different styles."""
        
        comparison_results = {}
        
        for prompt in comparison_prompts:
            prompt_results = {}
            
            for style_name in styles:
                if style_name not in self.visual_style_database:
                    continue
                
                style = self.visual_style_database[style_name]
                
                # Find best model for this style
                model_recommendations = await self._find_best_models_for_style(style)
                best_model = model_recommendations[0].model_id if model_recommendations else "flux.1-dev"
                
                # Format prompt with style template
                formatted_prompt = style.prompt_template.replace("{object}", prompt)
                
                # Generate image
                generation_result = await self.scenario_ai.generate_image(
                    prompt=formatted_prompt,
                    model_id=best_model,
                    width=512,
                    height=512
                )
                
                prompt_results[style_name] = {
                    "style_info": style,
                    "model_used": best_model,
                    "formatted_prompt": formatted_prompt,
                    "generation_result": generation_result
                }
            
            comparison_results[prompt] = prompt_results
        
        return {
            "comparison_type": "style_comparison",
            "prompts_tested": comparison_prompts,
            "styles_compared": styles,
            "results": comparison_results,
            "analysis": await self._analyze_style_comparison_results(comparison_results)
        }
    
    async def create_model_blend_strategy(self, primary_models: List[str], 
                                        blend_concept: str) -> Dict[str, Any]:
        """Create a strategy for blending multiple Scenario AI models."""
        
        model_details = {}
        compatibility_matrix = {}
        
        # Get detailed info for each model
        for model_id in primary_models:
            details_result = await self.scenario_ai.get_model_details(model_id)
            if details_result["success"]:
                model_details[model_id] = details_result["data"]["model"]
        
        # Analyze compatibility between models
        for i, model_a in enumerate(primary_models):
            compatibility_matrix[model_a] = {}
            for model_b in primary_models:
                if model_a != model_b:
                    compatibility_score = await self._calculate_model_compatibility(
                        model_details.get(model_a, {}), 
                        model_details.get(model_b, {})
                    )
                    compatibility_matrix[model_a][model_b] = compatibility_score
        
        # Generate test images with different model combinations
        blend_test_results = await self.scenario_ai.generate_with_multiple_models(
            prompt=f"{blend_concept}, high quality, game art style, transparent background",
            model_ids=primary_models,
            shared_settings={"width": 512, "height": 512, "num_samples": 2}
        )
        
        return {
            "blend_concept": blend_concept,
            "models_analyzed": primary_models,
            "model_details": model_details,
            "compatibility_matrix": compatibility_matrix,
            "recommended_blends": await self._recommend_optimal_blends(compatibility_matrix),
            "test_generations": blend_test_results,
            "blend_workflow": await self._create_blend_workflow(primary_models, model_details)
        }
    
    async def generate_comprehensive_mood_board(self, game_concept: str, 
                                              selected_style: str) -> Dict[str, Any]:
        """Generate a comprehensive mood board with multiple visual elements."""
        
        if selected_style not in self.visual_style_database:
            return {"error": f"Style '{selected_style}' not found in database"}
        
        style = self.visual_style_database[selected_style]
        
        # Define mood board elements to generate
        mood_board_elements = [
            "main character concept",
            "enemy/antagonist design", 
            "environment/background",
            "UI element design",
            "special effect/particle",
            "weapon/item design",
            "ambient lighting study",
            "color palette demonstration"
        ]
        
        # Find optimal models for this style
        model_recommendations = await self._find_best_models_for_style(style)
        primary_model = model_recommendations[0].model_id if model_recommendations else "flux.1-dev"
        secondary_model = model_recommendations[1].model_id if len(model_recommendations) > 1 else primary_model
        
        mood_board_results = {}
        
        # Generate each element
        for element in mood_board_elements:
            formatted_prompt = style.prompt_template.replace("{object}", element)
            
            # Use primary model for character/main elements, secondary for effects/UI
            model_to_use = secondary_model if "effect" in element or "UI" in element else primary_model
            
            generation_result = await self.scenario_ai.generate_image(
                prompt=formatted_prompt,
                model_id=model_to_use,
                width=512,
                height=512
            )
            
            mood_board_results[element] = {
                "prompt": formatted_prompt,
                "model_used": model_to_use,
                "generation_result": generation_result
            }
        
        return {
            "game_concept": game_concept,
            "selected_style": selected_style,
            "style_details": style,
            "mood_board_elements": mood_board_results,
            "model_recommendations": model_recommendations,
            "production_guidelines": await self._create_production_guidelines(style, model_recommendations),
            "consistency_checklist": await self._create_consistency_checklist(style)
        }
    
    async def _find_best_models_for_style(self, style: VisualStyle) -> List[ModelRecommendation]:
        """Find best Scenario AI models for a given visual style."""
        
        if not self.available_models:
            models_result = await self.scenario_ai.get_models(limit=100)
            if not models_result["success"]:
                return []
            self.available_models = models_result["data"]["categorized_models"]
        
        recommendations = []
        
        # Search through all categorized models
        for category, models in self.available_models.items():
            for model in models:
                score = await self._score_model_for_style(model, style)
                
                if score > 5.0:  # Only recommend models with good scores
                    recommendation = ModelRecommendation(
                        model_id=model["id"],
                        model_name=model["name"],
                        suitability_score=score,
                        strengths=await self._analyze_model_strengths(model, style),
                        limitations=await self._analyze_model_limitations(model, style),
                        optimal_settings=await self._determine_optimal_settings(model, style),
                        sample_prompt=style.sample_prompts[0]
                    )
                    recommendations.append(recommendation)
        
        # Sort by suitability score
        recommendations.sort(key=lambda x: x.suitability_score, reverse=True)
        return recommendations[:5]  # Return top 5 recommendations
    
    async def _score_model_for_style(self, model: Dict[str, Any], style: VisualStyle) -> float:
        """Score how well a model fits a visual style (0-10)."""
        score = 5.0  # Base score
        
        model_name_lower = model["name"].lower()
        model_tags = [tag.lower() for tag in model.get("tags", [])]
        style_keywords = [word.lower() for word in style.mood_words + [style.name.lower()]]
        
        # Name matching
        for keyword in style_keywords:
            if keyword in model_name_lower:
                score += 1.5
        
        # Tag matching
        for tag in model_tags:
            for keyword in style_keywords:
                if keyword in tag:
                    score += 0.5
        
        # Category bonuses
        if style.name == "pixel_perfect" and any(word in model_name_lower for word in ["pixel", "8bit", "16bit", "retro"]):
            score += 2.0
        
        if style.name == "hand_painted_fantasy" and any(word in model_name_lower for word in ["fantasy", "painted", "art"]):
            score += 2.0
        
        if style.name == "minimalist_geometric" and any(word in model_name_lower for word in ["minimal", "geometric", "clean"]):
            score += 2.0
        
        # Training quality indicators
        if model.get("training_steps", 0) > 1000:
            score += 0.5
        
        if model.get("training_images", 0) > 100:
            score += 0.5
        
        return min(score, 10.0)  # Cap at 10
    
    async def _analyze_model_strengths(self, model: Dict[str, Any], style: VisualStyle) -> List[str]:
        """Analyze model strengths for a specific style."""
        strengths = []
        
        if model.get("supports_controlnet"):
            strengths.append("Supports ControlNet for precise composition")
        
        if model.get("training_steps", 0) > 2000:
            strengths.append("Highly trained model with consistent output")
        
        if model.get("is_public"):
            strengths.append("Public model with community validation")
        
        # Style-specific strengths
        model_name_lower = model["name"].lower()
        
        if "flux" in model_name_lower:
            strengths.append("Flux-based architecture for high quality")
        
        if "lora" in model_name_lower:
            strengths.append("LoRA fine-tuning for style consistency")
        
        return strengths[:3]  # Limit to top 3
    
    async def _analyze_model_limitations(self, model: Dict[str, Any], style: VisualStyle) -> List[str]:
        """Analyze potential model limitations."""
        limitations = []
        
        if model.get("training_images", 0) < 50:
            limitations.append("Limited training data may affect consistency")
        
        if not model.get("is_public"):
            limitations.append("Private model may have usage restrictions")
        
        if not model.get("supports_controlnet"):
            limitations.append("No ControlNet support for composition control")
        
        return limitations[:2]  # Limit to top 2
    
    async def _determine_optimal_settings(self, model: Dict[str, Any], style: VisualStyle) -> Dict[str, Any]:
        """Determine optimal generation settings for model and style combination."""
        settings = {
            "width": 1024,
            "height": 1024,
            "num_inference_steps": 28,
            "guidance": 3.5,
            "num_samples": 1
        }
        
        # Adjust based on model type
        model_name_lower = model["name"].lower()
        
        if "flux" in model_name_lower:
            settings["num_inference_steps"] = 28
            settings["guidance"] = 3.5
        elif "stable" in model_name_lower:
            settings["num_inference_steps"] = 50
            settings["guidance"] = 7.5
        
        # Adjust based on style
        if style.name == "pixel_perfect":
            settings["width"] = 512
            settings["height"] = 512
            settings["guidance"] = 8.0  # Higher guidance for crisp pixels
        elif style.name == "minimalist_geometric":
            settings["num_inference_steps"] = 20  # Simpler style needs fewer steps
            settings["guidance"] = 5.0
        
        return settings
    
    async def _calculate_model_compatibility(self, model_a: Dict[str, Any], model_b: Dict[str, Any]) -> float:
        """Calculate compatibility score between two models (0-10)."""
        score = 5.0
        
        # Same base architecture
        if model_a.get("type") == model_b.get("type"):
            score += 2.0
        
        # Similar training approaches
        if abs(model_a.get("training_steps", 0) - model_b.get("training_steps", 0)) < 500:
            score += 1.0
        
        # Similar capabilities
        shared_capabilities = 0
        capabilities = ["supports_3d", "supports_video", "supports_controlnet"]
        for cap in capabilities:
            if model_a.get(cap) == model_b.get(cap):
                shared_capabilities += 1
        
        score += shared_capabilities * 0.5
        
        return min(score, 10.0)
    
    async def _recommend_optimal_blends(self, compatibility_matrix: Dict[str, Dict[str, float]]) -> List[Dict[str, Any]]:
        """Recommend optimal model blending combinations."""
        blends = []
        
        for model_a, compatibilities in compatibility_matrix.items():
            for model_b, score in compatibilities.items():
                if score >= 7.0:  # High compatibility
                    blends.append({
                        "primary_model": model_a,
                        "secondary_model": model_b,
                        "compatibility_score": score,
                        "recommended_ratio": "70:30" if score >= 8.0 else "60:40",
                        "use_case": "High compatibility blend for consistent style"
                    })
        
        return sorted(blends, key=lambda x: x["compatibility_score"], reverse=True)[:3]
    
    async def _create_blend_workflow(self, models: List[str], model_details: Dict[str, Any]) -> Dict[str, Any]:
        """Create a workflow for blending multiple models."""
        return {
            "phase_1_concept": {
                "description": "Generate concepts with primary model",
                "primary_model": models[0] if models else "flux.1-dev",
                "iterations": 3,
                "settings": {"guidance": 3.5, "steps": 28}
            },
            "phase_2_refinement": {
                "description": "Refine with secondary model for style enhancement",
                "secondary_model": models[1] if len(models) > 1 else models[0],
                "iterations": 2,
                "settings": {"guidance": 5.0, "steps": 35}
            },
            "phase_3_consistency": {
                "description": "Ensure consistency across assets",
                "validation_prompts": [
                    "character turnaround sheet",
                    "environment variations",
                    "UI element family"
                ]
            }
        }
    
    async def _create_production_guidelines(self, style: VisualStyle, models: List[ModelRecommendation]) -> Dict[str, Any]:
        """Create production guidelines for the selected style and models."""
        return {
            "asset_pipeline": {
                "concept_phase": f"Use {models[0].model_id if models else 'flux.1-dev'} for initial concepts",
                "production_phase": f"Use {models[1].model_id if len(models) > 1 else models[0].model_id} for final assets",
                "quality_check": "Verify consistency with style guide before approval"
            },
            "prompt_structure": {
                "template": style.prompt_template,
                "required_elements": ["object description", "style keywords", "quality modifiers"],
                "consistency_keywords": style.mood_words
            },
            "technical_specs": {
                "preferred_resolution": "1024x1024 for concepts, 2048x2048 for finals",
                "format_requirements": "PNG with transparency for sprites",
                "optimization_notes": "Maintain consistent style elements across all assets"
            }
        }
    
    async def _create_consistency_checklist(self, style: VisualStyle) -> List[str]:
        """Create a checklist for maintaining visual consistency."""
        return [
            f"Color palette adheres to: {', '.join(style.color_palette)}",
            f"Mood remains consistent: {', '.join(style.mood_words)}",
            "Lighting direction consistent across assets",
            "Line weight/detail level matches style guide",
            "Character proportions follow established rules",
            "Environment scale feels cohesive",
            "UI elements match game world aesthetic",
            "Effects/particles align with overall style"
        ]
    
    def _determine_emotional_target(self, concept: str) -> str:
        """Determine target emotional response based on game concept."""
        if any(word in concept for word in ["horror", "scary", "dark", "thriller"]):
            return "Fear, tension, unease"
        elif any(word in concept for word in ["adventure", "explore", "quest"]):
            return "Wonder, curiosity, excitement"
        elif any(word in concept for word in ["puzzle", "strategy", "brain"]):
            return "Satisfaction, accomplishment, focus"
        elif any(word in concept for word in ["casual", "relaxing", "zen"]):
            return "Calm, peaceful, meditative"
        else:
            return "Engagement, enjoyment, satisfaction"
    
    def _analyze_technical_constraints(self, platform: str, complexity: str) -> Dict[str, Any]:
        """Analyze technical constraints based on platform and complexity."""
        constraints = {
            "mobile": {
                "texture_size_limit": "1024x1024",
                "polygon_budget": "Low",
                "effect_complexity": "Simple",
                "recommended_styles": ["minimalist_geometric", "cartoon_vibrant"]
            },
            "desktop": {
                "texture_size_limit": "2048x2048",
                "polygon_budget": "Medium-High", 
                "effect_complexity": "Complex",
                "recommended_styles": ["hand_painted_fantasy", "dark_atmospheric"]
            },
            "web": {
                "texture_size_limit": "1024x1024",
                "polygon_budget": "Medium",
                "effect_complexity": "Medium",
                "recommended_styles": ["pixel_perfect", "minimalist_geometric"]
            }
        }
        
        return constraints.get(platform, constraints["desktop"])
    
    def _analyze_cultural_considerations(self, concept: str) -> List[str]:
        """Analyze cultural considerations for the game concept."""
        considerations = []
        
        if any(word in concept.lower() for word in ["fantasy", "medieval", "magic"]):
            considerations.append("Consider diverse cultural representations in fantasy elements")
            considerations.append("Avoid stereotypical fantasy tropes that may be culturally insensitive")
        
        if any(word in concept.lower() for word in ["war", "conflict", "battle"]):
            considerations.append("Handle violent themes appropriately for target audience")
            considerations.append("Consider impact of war imagery on different cultural groups")
        
        considerations.append("Ensure character designs represent diverse backgrounds")
        considerations.append("Review color symbolism across different cultures")
        
        return considerations
    
    async def _create_workflow_recommendation(self, approaches: Dict[str, Any]) -> Dict[str, Any]:
        """Create a recommended workflow based on selected approaches."""
        return {
            "day_1_concept": "Generate style samples and get client approval",
            "day_2_assets": "Create core asset library with approved style",
            "day_3_iteration": "Refine assets and ensure consistency",
            "quality_gates": [
                "Style approval checkpoint",
                "Asset consistency review", 
                "Technical optimization check"
            ],
            "deliverables": [
                "Style guide with visual examples",
                "Asset library with consistent style",
                "Production guidelines document"
            ]
        }
    
    async def _analyze_style_comparison_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the results of style comparisons."""
        return {
            "most_consistent_style": "Based on generation quality across prompts",
            "best_for_characters": "Style that performed best with character prompts",
            "best_for_environments": "Style that performed best with environment prompts",
            "technical_performance": "Analysis of generation speed and quality",
            "recommendation": "Overall recommendation based on all factors"
        }

# CLI Interface
async def main():
    """CLI interface for testing the Enhanced Art Direction Analyst."""
    if len(sys.argv) < 2:
        print("Enhanced Art Direction Analyst - Usage:")
        print("  python enhanced_art_direction_analyst.py analyze 'game concept here'")
        print("  python enhanced_art_direction_analyst.py approaches 'game concept here'")
        print("  python enhanced_art_direction_analyst.py compare 'pixel_perfect,hand_painted_fantasy' 'character,environment'")
        print("  python enhanced_art_direction_analyst.py moodboard 'game concept' 'style_name'")
        print("  python enhanced_art_direction_analyst.py blend 'model1,model2,model3' 'blend concept'")
        return
    
    command = sys.argv[1]
    analyst = EnhancedArtDirectionAnalyst()
    
    if command == "analyze" and len(sys.argv) > 2:
        concept = sys.argv[2]
        result = await analyst.analyze_game_concept(concept)
        print(json.dumps(result, indent=2))
    
    elif command == "approaches" and len(sys.argv) > 2:
        concept = sys.argv[2]
        result = await analyst.present_art_direction_approaches(concept)
        print(json.dumps(result, indent=2))
    
    elif command == "compare" and len(sys.argv) > 3:
        styles = sys.argv[2].split(',')
        prompts = sys.argv[3].split(',')
        result = await analyst.create_visual_style_comparison(styles, prompts)
        print(json.dumps(result, indent=2))
    
    elif command == "moodboard" and len(sys.argv) > 3:
        concept = sys.argv[2]
        style = sys.argv[3]
        result = await analyst.generate_comprehensive_mood_board(concept, style)
        print(json.dumps(result, indent=2))
    
    elif command == "blend" and len(sys.argv) > 3:
        models = sys.argv[2].split(',')
        blend_concept = sys.argv[3]
        result = await analyst.create_model_blend_strategy(models, blend_concept)
        print(json.dumps(result, indent=2))
    
    else:
        print("Invalid command or missing arguments")

if __name__ == "__main__":
    asyncio.run(main())