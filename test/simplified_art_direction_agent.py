#!/usr/bin/env python3
"""
Simplified Art Direction Analyst Agent (Agent 2) - Visual AI Game Studio
Uses existing MCP Scenario AI integration without additional dependencies
"""

import json
import sys
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

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

class SimplifiedArtDirectionAgent:
    """
    Simplified Art Direction Analyst Agent with visual communication focus.
    Uses existing MCP Scenario AI tools for generation.
    """
    
    def __init__(self):
        self.agent_name = "Art-Direction-Analyst"
        self.agent_id = "agent_2"
        self.specialization = "Visual Style Development & AI Asset Generation"
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
                scenario_models=["flux.1-dev"],  # Use available MCP models
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
                scenario_models=["flux.1-dev"],
                prompt_template="{object}, hand-painted style, fantasy art, rich textures, magical atmosphere, detailed brushwork, transparent background",
                pros=["Highly detailed", "Emotional impact", "Timeless appeal"],
                cons=["Performance intensive", "Longer production time"],
                sample_prompts=[
                    "elven archer, hand-painted style, fantasy art, rich textures, magical atmosphere, detailed brushwork, transparent background",
                    "enchanted forest clearing, hand-painted style, fantasy art, magical lighting, detailed foliage",
                    "spell casting effect, hand-painted style, swirling magic, glowing particles, ethereal wisps"
                ]
            ),
            
            "minimalist_geometric": VisualStyle(
                name="Minimalist Geometric",
                description="Clean, geometric shapes with bold colors and simple elegance",
                color_palette=["#FFFFFF", "#000000", "#FF6B6B", "#4ECDC4", "#45B7D1"],
                mood_words=["Clean", "Modern", "Elegant"],
                reference_games=["Monument Valley", "GRIS", "Alto's Odyssey"],
                scenario_models=["flux.1-dev"],
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
                scenario_models=["flux.1-dev"],
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
                scenario_models=["flux.1-dev"],
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
    
    def analyze_game_concept(self, game_concept: str, target_audience: str = "general", 
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
    
    def present_art_direction_approaches(self, game_concept: str, **kwargs) -> Dict[str, Any]:
        """Present 3 visual art direction approaches with detailed specifications."""
        
        # Analyze concept first
        analysis = self.analyze_game_concept(game_concept, **kwargs)
        top_styles = [style_name for style_name, score in analysis["style_recommendations"]]
        
        approaches = {}
        
        # Create approaches for top 3 styles
        for i, style_name in enumerate(top_styles[:3], 1):
            style = self.visual_style_database[style_name]
            
            approaches[f"approach_{chr(65+i-1)}"] = {
                "style": style,
                "suitability_score": analysis["style_recommendations"][i-1][1],
                "scenario_prompt_examples": self._create_scenario_prompts(style, game_concept),
                "production_estimates": self._estimate_production_timeline(style),
                "asset_categories": self._plan_asset_categories(style)
            }
        
        return {
            "game_concept": game_concept,
            "approaches": approaches,
            "technical_analysis": analysis["technical_constraints"],
            "cultural_considerations": analysis["cultural_considerations"],
            "recommended_workflow": self._create_workflow_recommendation(approaches)
        }
    
    def create_comprehensive_mood_board_plan(self, game_concept: str, selected_style: str) -> Dict[str, Any]:
        """Create a comprehensive mood board plan with specific generation instructions."""
        
        if selected_style not in self.visual_style_database:
            return {"error": f"Style '{selected_style}' not found in database"}
        
        style = self.visual_style_database[selected_style]
        
        # Define mood board elements to generate
        mood_board_elements = {
            "main_character": {
                "prompt": style.prompt_template.replace("{object}", f"{game_concept} main character"),
                "priority": 1,
                "settings": {"width": 1024, "height": 1024},
                "description": "Primary protagonist showcasing style and personality"
            },
            "enemy_design": {
                "prompt": style.prompt_template.replace("{object}", f"{game_concept} antagonist"),
                "priority": 2,
                "settings": {"width": 1024, "height": 1024},
                "description": "Primary antagonist demonstrating threat level and style consistency"
            },
            "environment": {
                "prompt": style.prompt_template.replace("{object}", f"{game_concept} environment background"),
                "priority": 1,
                "settings": {"width": 1024, "height": 768},
                "description": "Key environment showcasing world design and atmosphere"
            },
            "ui_elements": {
                "prompt": style.prompt_template.replace("{object}", "game UI elements, health bar, buttons"),
                "priority": 3,
                "settings": {"width": 1024, "height": 512},
                "description": "User interface elements maintaining style consistency"
            },
            "special_effects": {
                "prompt": style.prompt_template.replace("{object}", f"{game_concept} magical effect"),
                "priority": 2,
                "settings": {"width": 512, "height": 512},
                "description": "Key visual effects showcasing style's dynamic elements"
            },
            "color_study": {
                "prompt": f"color palette study, {', '.join(style.color_palette)}, {game_concept} themed",
                "priority": 3,
                "settings": {"width": 1024, "height": 256},
                "description": "Color harmony demonstration for style consistency"
            }
        }
        
        return {
            "game_concept": game_concept,
            "selected_style": selected_style,
            "style_details": style,
            "mood_board_elements": mood_board_elements,
            "generation_sequence": self._create_generation_sequence(mood_board_elements),
            "scenario_mcp_instructions": self._create_mcp_instructions(mood_board_elements),
            "consistency_checklist": self._create_consistency_checklist(style)
        }
    
    def handle_ceo_request(self, request: str, game_concept: str = "", 
                          context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle CEO requests for art direction with visual communication."""
        
        request_lower = request.lower()
        context = context or {}
        
        if any(keyword in request_lower for keyword in ["art style", "visual", "look", "feel", "colors", "aesthetic"]):
            return self._handle_art_style_request(game_concept, context)
        
        elif any(keyword in request_lower for keyword in ["mood board", "concept art", "samples", "examples"]):
            return self._handle_mood_board_request(game_concept, context)
        
        elif any(keyword in request_lower for keyword in ["scenario", "generate", "ai", "samples"]):
            return self._handle_generation_request(game_concept, context)
        
        else:
            return self._handle_general_analysis(game_concept, context)
    
    def _handle_art_style_request(self, game_concept: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle requests for art style direction with visual samples."""
        
        approaches = self.present_art_direction_approaches(game_concept, **context)
        
        return self._format_ceo_response(
            task="Art Style Direction",
            analysis={
                "game_concept": game_concept,
                "approaches_analyzed": len(approaches["approaches"]),
                "technical_constraints": approaches["technical_analysis"],
                "cultural_considerations": approaches["cultural_considerations"]
            },
            options=self._format_art_style_options(approaches["approaches"]),
            recommendation=self._create_art_style_recommendation(approaches),
            next_steps="CEO selects preferred approach → Generate visual samples with Scenario MCP → Create comprehensive mood board",
            mcp_instructions=self._create_art_style_mcp_instructions(approaches)
        )
    
    def _handle_mood_board_request(self, game_concept: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle requests for mood board generation with AI samples."""
        
        selected_style = context.get("selected_style", "hand_painted_fantasy")
        mood_board_plan = self.create_comprehensive_mood_board_plan(game_concept, selected_style)
        
        if "error" in mood_board_plan:
            return self._format_error_response(mood_board_plan["error"])
        
        return self._format_ceo_response(
            task="Mood Board Generation Plan",
            analysis={
                "game_concept": game_concept,
                "selected_style": selected_style,
                "elements_planned": len(mood_board_plan["mood_board_elements"]),
                "total_generations": len(mood_board_plan["mood_board_elements"])
            },
            options=self._format_mood_board_options(mood_board_plan),
            recommendation=self._create_mood_board_recommendation(mood_board_plan),
            next_steps="CEO approves mood board plan → Execute Scenario MCP generations → Review and refine samples",
            mcp_instructions=mood_board_plan["scenario_mcp_instructions"]
        )
    
    def _handle_generation_request(self, game_concept: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle requests for direct Scenario AI generation."""
        
        style_name = context.get("style", "hand_painted_fantasy")
        
        if style_name not in self.visual_style_database:
            style_name = "hand_painted_fantasy"
        
        style = self.visual_style_database[style_name]
        generation_prompts = self._create_scenario_prompts(style, game_concept)
        
        return self._format_ceo_response(
            task="Scenario AI Generation Instructions",
            analysis={
                "game_concept": game_concept,
                "selected_style": style_name,
                "prompts_prepared": len(generation_prompts),
                "estimated_time": f"{len(generation_prompts) * 3} minutes"
            },
            options=self._format_generation_options(generation_prompts),
            recommendation=f"I recommend starting with {generation_prompts[0]['prompt']} to establish the core visual direction",
            next_steps="CEO selects generation priority → Execute with Scenario MCP → Review and iterate",
            mcp_instructions=self._create_direct_generation_instructions(generation_prompts)
        )
    
    def _handle_general_analysis(self, game_concept: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general art direction analysis requests."""
        
        analysis = self.analyze_game_concept(game_concept, **context)
        
        return self._format_ceo_response(
            task="Art Direction Analysis",
            analysis={
                "game_concept": game_concept,
                "top_style_match": analysis["style_recommendations"][0][0],
                "match_score": f"{analysis['style_recommendations'][0][1]}/10",
                "emotional_target": analysis["emotional_response_target"],
                "platform_constraints": analysis["technical_constraints"]
            },
            options=self._format_analysis_options(analysis),
            recommendation=self._create_general_recommendation(analysis),
            next_steps="CEO selects focus area → Deep dive into chosen style → Generate visual validation samples",
            mcp_instructions=self._create_analysis_mcp_instructions(analysis)
        )
    
    # Formatting and utility methods
    def _format_ceo_response(self, task: str, analysis: Dict[str, Any], 
                           options: List[Dict[str, Any]], recommendation: str, 
                           next_steps: str, mcp_instructions: List[str] = None) -> Dict[str, Any]:
        """Format response for CEO decision-making."""
        
        response = {
            "agent": self.agent_name,
            "agent_id": self.agent_id,
            "specialization": self.specialization,
            "task": task,
            "analysis": analysis,
            "ceo_options": options,
            "expert_recommendation": recommendation,
            "next_steps": next_steps,
            "status": "awaiting_ceo_decision",
            "response_format": "visual_presentation_with_ai_samples"
        }
        
        if mcp_instructions:
            response["scenario_mcp_instructions"] = mcp_instructions
        
        return response
    
    def _format_art_style_options(self, approaches: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format art style options for CEO presentation."""
        
        options = []
        
        for approach_key, approach_data in approaches.items():
            style = approach_data["style"]
            
            option = {
                "option_name": f"Option {approach_key[-1]}: {style.name}",
                "description": style.description,
                "visual_philosophy": f"Evokes {', '.join(style.mood_words)} through {style.description.lower()}",
                "color_palette": style.color_palette,
                "mood_words": style.mood_words,
                "reference_games": style.reference_games,
                "suitability_score": f"{approach_data['suitability_score']}/10",
                "pros": style.pros,
                "cons": style.cons,
                "production_timeline": approach_data["production_estimates"],
                "asset_categories": approach_data["asset_categories"],
                "sample_prompts": style.sample_prompts[:2],
                "recommendation_level": self._calculate_recommendation_level(approach_data['suitability_score'])
            }
            
            options.append(option)
        
        return options
    
    def _create_scenario_prompts(self, style: VisualStyle, game_concept: str) -> List[Dict[str, Any]]:
        """Create specific Scenario AI prompts for the style and game concept."""
        
        base_elements = [
            f"{game_concept} main character",
            f"{game_concept} environment",
            f"{game_concept} enemy",
            f"UI elements for {game_concept}",
            f"special effects for {game_concept}"
        ]
        
        prompts = []
        for i, element in enumerate(base_elements):
            prompts.append({
                "element": element,
                "prompt": style.prompt_template.replace("{object}", element),
                "priority": 1 if i < 2 else 2,
                "settings": {
                    "model_id": "flux.1-dev",
                    "width": 1024,
                    "height": 1024 if "character" in element else 768
                }
            })
        
        return prompts
    
    def _create_mcp_instructions(self, mood_board_elements: Dict[str, Any]) -> List[str]:
        """Create step-by-step MCP instructions for generation."""
        
        instructions = []
        
        # Sort by priority
        sorted_elements = sorted(mood_board_elements.items(), 
                               key=lambda x: x[1]["priority"])
        
        for element_name, element_data in sorted_elements:
            instruction = f"mcp__ScenarioMCP__scenario_simple_generate with prompt: '{element_data['prompt']}'"
            if element_data["settings"]:
                instruction += f" and settings: {element_data['settings']}"
            instructions.append(instruction)
        
        return instructions
    
    def _create_generation_sequence(self, mood_board_elements: Dict[str, Any]) -> List[str]:
        """Create optimal generation sequence based on priorities."""
        
        # Group by priority
        priority_groups = {}
        for name, data in mood_board_elements.items():
            priority = data["priority"]
            if priority not in priority_groups:
                priority_groups[priority] = []
            priority_groups[priority].append(name)
        
        # Create sequence
        sequence = []
        for priority in sorted(priority_groups.keys()):
            sequence.extend(priority_groups[priority])
        
        return sequence
    
    def _create_consistency_checklist(self, style: VisualStyle) -> List[str]:
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
    
    # Additional utility methods
    def _estimate_production_timeline(self, style: VisualStyle) -> Dict[str, str]:
        """Estimate production timeline for a visual style."""
        
        timelines = {
            "Pixel Perfect Retro": {"concept": "1 day", "production": "2-3 days", "polish": "1 day"},
            "Minimalist Geometric": {"concept": "1 day", "production": "2-3 days", "polish": "1 day"},
            "Cartoon Vibrant": {"concept": "1-2 days", "production": "3-4 days", "polish": "1-2 days"},
            "Hand-Painted Fantasy": {"concept": "2 days", "production": "4-6 days", "polish": "2 days"},
            "Dark Atmospheric Horror": {"concept": "1-2 days", "production": "3-5 days", "polish": "1-2 days"}
        }
        
        return timelines.get(style.name, {"concept": "1-2 days", "production": "3-4 days", "polish": "1-2 days"})
    
    def _plan_asset_categories(self, style: VisualStyle) -> Dict[str, List[str]]:
        """Plan asset categories for the style."""
        
        return {
            "characters": ["Main character", "NPCs", "Enemies", "Character variations"],
            "environments": ["Backgrounds", "Tilesets", "Props", "Interactive objects"],
            "ui": ["Buttons", "Icons", "Health bars", "Menus", "Tooltips"],
            "effects": ["Particles", "Spell effects", "Impact effects", "Ambient effects"],
            "audio_visual": ["Loading screens", "Cutscene elements", "Transitions"]
        }
    
    def _create_workflow_recommendation(self, approaches: Dict[str, Any]) -> Dict[str, str]:
        """Create workflow recommendations."""
        
        return {
            "phase_1": "Style validation with 3-5 key samples",
            "phase_2": "Core asset production (characters, environments)",
            "phase_3": "Secondary assets (UI, effects)",
            "phase_4": "Polish and consistency pass",
            "quality_gates": "CEO approval at each phase"
        }
    
    def _determine_emotional_target(self, concept: str) -> str:
        """Determine target emotional response."""
        
        if any(word in concept for word in ["horror", "scary", "dark"]):
            return "Fear, tension, unease"
        elif any(word in concept for word in ["adventure", "explore"]):
            return "Wonder, curiosity, excitement"
        elif any(word in concept for word in ["puzzle", "strategy"]):
            return "Satisfaction, accomplishment"
        elif any(word in concept for word in ["casual", "relaxing"]):
            return "Calm, peaceful, meditative"
        else:
            return "Engagement, enjoyment"
    
    def _analyze_technical_constraints(self, platform: str, complexity: str) -> Dict[str, Any]:
        """Analyze technical constraints."""
        
        constraints = {
            "mobile": {"texture_limit": "1024x1024", "poly_budget": "Low"},
            "desktop": {"texture_limit": "2048x2048", "poly_budget": "High"},
            "web": {"texture_limit": "1024x1024", "poly_budget": "Medium"}
        }
        
        return constraints.get(platform, constraints["desktop"])
    
    def _analyze_cultural_considerations(self, concept: str) -> List[str]:
        """Analyze cultural considerations."""
        
        return [
            "Ensure diverse character representation",
            "Review color symbolism across cultures",
            "Consider accessibility in visual design",
            "Validate cultural references for sensitivity"
        ]
    
    def _calculate_recommendation_level(self, score: float) -> str:
        """Calculate recommendation level."""
        
        if score >= 8:
            return "⭐⭐⭐"
        elif score >= 6:
            return "⭐⭐"
        else:
            return "⭐"
    
    # Additional formatting methods for different request types
    def _format_mood_board_options(self, mood_board_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format mood board options."""
        
        elements = mood_board_plan["mood_board_elements"]
        
        return [
            {
                "option_name": "Option A: Complete Mood Board",
                "description": f"Generate all {len(elements)} visual elements",
                "elements": list(elements.keys()),
                "time_estimate": f"{len(elements) * 3} minutes",
                "recommendation_level": "⭐⭐⭐"
            },
            {
                "option_name": "Option B: Priority Elements Only",
                "description": "Generate high-priority elements first",
                "elements": [k for k, v in elements.items() if v["priority"] == 1],
                "time_estimate": "15 minutes",
                "recommendation_level": "⭐⭐"
            }
        ]
    
    def _format_generation_options(self, prompts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format generation options."""
        
        return [
            {
                "option_name": f"Option {i+1}: {prompt['element'].title()}",
                "description": f"Generate {prompt['element']} sample",
                "prompt": prompt["prompt"],
                "settings": prompt["settings"],
                "priority": prompt["priority"],
                "recommendation_level": "⭐⭐⭐" if prompt["priority"] == 1 else "⭐⭐"
            }
            for i, prompt in enumerate(prompts[:3])
        ]
    
    def _format_analysis_options(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format analysis options."""
        
        top_styles = analysis["style_recommendations"][:3]
        
        return [
            {
                "option_name": f"Option {i+1}: {style_name.replace('_', ' ').title()}",
                "description": f"Focus on {style_name} development",
                "score": f"{score}/10",
                "style_details": self.visual_style_database[style_name],
                "recommendation_level": "⭐⭐⭐" if score >= 8 else "⭐⭐"
            }
            for i, (style_name, score) in enumerate(top_styles)
        ]
    
    def _create_art_style_recommendation(self, approaches: Dict[str, Any]) -> str:
        """Create art style recommendation."""
        
        best_approach = max(approaches["approaches"].items(), 
                          key=lambda x: x[1]["suitability_score"])
        
        style = best_approach[1]["style"]
        score = best_approach[1]["suitability_score"]
        
        return f"""I recommend **{style.name}** (Score: {score}/10) because:

1. **Best Concept Match**: Highest alignment with game concept and requirements
2. **Technical Feasibility**: Matches platform and complexity constraints
3. **Market Appeal**: Strong appeal to target audience
4. **Production Efficiency**: Balanced timeline and resource requirements

This style provides optimal visual impact while maintaining practical development constraints."""
    
    def _create_mood_board_recommendation(self, mood_board_plan: Dict[str, Any]) -> str:
        """Create mood board recommendation."""
        
        element_count = len(mood_board_plan["mood_board_elements"])
        
        return f"""I recommend generating the **Complete Mood Board** because:

1. **Comprehensive Coverage**: All {element_count} elements ensure complete style validation
2. **Early Problem Detection**: Multiple elements reveal consistency issues early
3. **Stakeholder Alignment**: Complete visuals reduce miscommunication
4. **Production Planning**: Full coverage enables accurate pipeline planning

Investment in complete mood board saves significant time in later production phases."""
    
    def _create_general_recommendation(self, analysis: Dict[str, Any]) -> str:
        """Create general analysis recommendation."""
        
        top_style = analysis["style_recommendations"][0]
        
        return f"""Based on comprehensive analysis, I recommend **{top_style[0].replace('_', ' ').title()}** (Score: {top_style[1]}/10) because:

1. **Optimal Concept Fit**: Best alignment with game concept and target audience
2. **Technical Compatibility**: Matches platform and complexity requirements
3. **Market Positioning**: Strong market appeal and competitive differentiation
4. **Production Readiness**: Established workflows and AI model availability

Next step: Generate visual samples to validate this recommendation with stakeholders."""
    
    # MCP instruction creators
    def _create_art_style_mcp_instructions(self, approaches: Dict[str, Any]) -> List[str]:
        """Create MCP instructions for art style validation."""
        
        instructions = []
        
        for approach_key, approach_data in approaches["approaches"].items():
            style = approach_data["style"]
            sample_prompt = style.sample_prompts[0]
            
            instructions.append(f"# {style.name} Sample Generation")
            instructions.append(f"mcp__ScenarioMCP__scenario_simple_generate")
            instructions.append(f"  prompt: '{sample_prompt}'")
            instructions.append(f"  model_id: 'flux.1-dev'")
            instructions.append(f"  width: 1024")
            instructions.append(f"  height: 1024")
            instructions.append("")
        
        return instructions
    
    def _create_direct_generation_instructions(self, prompts: List[Dict[str, Any]]) -> List[str]:
        """Create direct generation instructions."""
        
        instructions = []
        
        for prompt_data in prompts:
            instructions.append(f"# Generate {prompt_data['element']}")
            instructions.append(f"mcp__ScenarioMCP__scenario_simple_generate")
            instructions.append(f"  prompt: '{prompt_data['prompt']}'")
            instructions.append(f"  model_id: '{prompt_data['settings']['model_id']}'")
            instructions.append(f"  width: {prompt_data['settings']['width']}")
            instructions.append(f"  height: {prompt_data['settings']['height']}")
            instructions.append("")
        
        return instructions
    
    def _create_analysis_mcp_instructions(self, analysis: Dict[str, Any]) -> List[str]:
        """Create MCP instructions for analysis validation."""
        
        top_style_name = analysis["style_recommendations"][0][0]
        style = self.visual_style_database[top_style_name]
        
        return [
            f"# Validate {style.name} Style",
            "mcp__ScenarioMCP__scenario_simple_generate",
            f"  prompt: '{style.sample_prompts[0]}'",
            "  model_id: 'flux.1-dev'",
            "  width: 1024",
            "  height: 1024"
        ]
    
    def _format_error_response(self, error_message: str) -> Dict[str, Any]:
        """Format error response."""
        
        return {
            "agent": self.agent_name,
            "status": "error",
            "error_message": error_message,
            "suggested_action": "Please provide valid parameters or try alternative approach"
        }

# Demo and CLI functionality
def run_demo():
    """Run a demonstration of the Art Direction Agent."""
    
    print("🎨 Enhanced Art Direction Analyst (Agent 2) - Demo")
    print("=" * 60)
    print()
    
    agent = SimplifiedArtDirectionAgent()
    
    # Demo scenarios
    scenarios = [
        {
            "name": "Fantasy RPG",
            "concept": "fantasy RPG with magic system and dragon battles",
            "request": "show me art style options",
            "context": {"target_audience": "young_adults", "platform": "desktop"}
        },
        {
            "name": "Mobile Puzzle",
            "concept": "casual mobile puzzle game with zen atmosphere",
            "request": "create mood board",
            "context": {"target_audience": "general", "platform": "mobile", "selected_style": "minimalist_geometric"}
        }
    ]
    
    for scenario in scenarios:
        print(f"📋 SCENARIO: {scenario['name']}")
        print("-" * 40)
        print(f"Game Concept: {scenario['concept']}")
        print(f"CEO Request: {scenario['request']}")
        print()
        
        response = agent.handle_ceo_request(
            scenario["request"],
            scenario["concept"],
            scenario["context"]
        )
        
        print(f"🎨 Agent Response:")
        print(f"  Task: {response['task']}")
        print(f"  Options Presented: {len(response['ceo_options'])}")
        
        for i, option in enumerate(response["ceo_options"], 1):
            print(f"    {i}. {option['option_name']} {option.get('recommendation_level', '')}")
        
        print(f"  Expert Recommendation: {response['expert_recommendation'][:100]}...")
        print(f"  Next Steps: {response['next_steps']}")
        
        if "scenario_mcp_instructions" in response:
            print(f"  MCP Instructions: {len(response['scenario_mcp_instructions'])} steps provided")
        
        print("\n" + "─" * 60 + "\n")
    
    print("✅ Demo Complete - Enhanced Art Direction Agent showcased")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        run_demo()
    else:
        print("Simplified Art Direction Agent")
        print("Usage: python simplified_art_direction_agent.py demo")
        print()
        print("This enhanced agent provides:")
        print("• Visual style analysis with AI model recommendations")
        print("• Comprehensive mood board planning")
        print("• Scenario MCP integration instructions")
        print("• CEO-focused decision presentation")
        print("• Production workflow optimization")