#!/usr/bin/env python3
"""
Art Direction Analyst Agent (Agent 2) - Visual AI Game Studio
Enhanced with Scenario AI for visual communication and model curation
"""

import asyncio
import json
import os
import sys
from typing import Dict, List, Any, Optional
from enhanced_art_direction_analyst import EnhancedArtDirectionAnalyst

class ArtDirectionAgent:
    """
    Art Direction Analyst Agent - Specialized in visual style development
    and AI-powered asset generation planning with Scenario AI integration.
    """
    
    def __init__(self):
        self.agent_name = "Art-Direction-Analyst"
        self.agent_id = "agent_2"
        self.specialization = "Visual Style Development & AI Asset Generation"
        self.analyst = EnhancedArtDirectionAnalyst()
        
    async def handle_ceo_request(self, request: str, game_concept: str = "", 
                               context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Handle CEO requests for art direction with visual communication.
        Presents options to CEO before executing any work.
        """
        
        # Detect request type and route to appropriate method
        request_lower = request.lower()
        
        if any(keyword in request_lower for keyword in ["art style", "visual", "look", "feel", "colors", "aesthetic"]):
            return await self._handle_art_style_request(game_concept, context or {})
        
        elif any(keyword in request_lower for keyword in ["mood board", "concept art", "samples", "examples"]):
            return await self._handle_mood_board_request(game_concept, context or {})
        
        elif any(keyword in request_lower for keyword in ["model", "scenario", "ai generation", "compare models"]):
            return await self._handle_model_selection_request(game_concept, context or {})
        
        elif any(keyword in request_lower for keyword in ["blend", "combine", "merge models"]):
            return await self._handle_model_blending_request(game_concept, context or {})
        
        else:
            # General art direction analysis
            return await self._handle_general_analysis(game_concept, context or {})
    
    async def _handle_art_style_request(self, game_concept: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle requests for art style direction with visual samples."""
        
        # Analyze the game concept first
        analysis = await self.analyst.analyze_game_concept(
            game_concept, 
            target_audience=context.get("target_audience", "general"),
            platform=context.get("platform", "desktop"),
            complexity_level=context.get("complexity", "medium")
        )
        
        # Present 3 art direction approaches with generated samples
        approaches = await self.analyst.present_art_direction_approaches(game_concept, **context)
        
        return self._format_ceo_response(
            task="Art Style Direction",
            analysis={
                "game_concept": game_concept,
                "emotional_target": analysis["emotional_response_target"],
                "technical_constraints": analysis["technical_constraints"],
                "cultural_considerations": analysis["cultural_considerations"]
            },
            options=self._format_art_style_options(approaches["approaches"]),
            recommendation=self._create_art_style_recommendation(approaches),
            next_steps="CEO selects preferred approach → Generate comprehensive mood board → Create style guide"
        )
    
    async def _handle_mood_board_request(self, game_concept: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle requests for mood board generation with AI samples."""
        
        selected_style = context.get("selected_style")
        
        if not selected_style:
            # Present style options first
            return await self._handle_art_style_request(game_concept, context)
        
        # Generate comprehensive mood board
        mood_board = await self.analyst.generate_comprehensive_mood_board(game_concept, selected_style)
        
        if "error" in mood_board:
            return self._format_error_response(mood_board["error"])
        
        return self._format_ceo_response(
            task="Mood Board Generation",
            analysis={
                "game_concept": game_concept,
                "selected_style": selected_style,
                "style_details": mood_board["style_details"].__dict__
            },
            options=self._format_mood_board_options(mood_board),
            recommendation=self._create_mood_board_recommendation(mood_board),
            next_steps="CEO reviews generated samples → Approve style consistency → Begin asset production"
        )
    
    async def _handle_model_selection_request(self, game_concept: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle requests for Scenario AI model selection and curation."""
        
        # If style is specified, find models for that style
        if context.get("style"):
            style_name = context["style"]
            if style_name in self.analyst.visual_style_database:
                style = self.analyst.visual_style_database[style_name]
                model_recommendations = await self.analyst._find_best_models_for_style(style)
                
                return self._format_ceo_response(
                    task="Scenario AI Model Selection",
                    analysis={
                        "target_style": style_name,
                        "total_models_evaluated": len(model_recommendations)
                    },
                    options=self._format_model_selection_options(model_recommendations),
                    recommendation=self._create_model_selection_recommendation(model_recommendations),
                    next_steps="CEO selects primary and secondary models → Test with sample prompts → Begin asset generation"
                )
        
        # Otherwise, present model comparison for different styles
        comparison_styles = ["pixel_perfect", "hand_painted_fantasy", "minimalist_geometric"]
        comparison_prompts = ["game character", "environment background"]
        
        comparison = await self.analyst.create_visual_style_comparison(comparison_styles, comparison_prompts)
        
        return self._format_ceo_response(
            task="Model Performance Comparison",
            analysis={
                "styles_compared": comparison_styles,
                "test_prompts": comparison_prompts
            },
            options=self._format_model_comparison_options(comparison),
            recommendation=self._create_model_comparison_recommendation(comparison),
            next_steps="CEO selects best performing models → Refine with specific style → Generate sample assets"
        )
    
    async def _handle_model_blending_request(self, game_concept: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle requests for model blending strategies."""
        
        target_models = context.get("models", ["flux.1-dev", "stable-diffusion-xl-base-1.0"])
        
        blend_strategy = await self.analyst.create_model_blend_strategy(target_models, game_concept)
        
        return self._format_ceo_response(
            task="Model Blending Strategy",
            analysis={
                "target_models": target_models,
                "compatibility_analysis": blend_strategy["compatibility_matrix"]
            },
            options=self._format_blend_strategy_options(blend_strategy),
            recommendation=self._create_blend_strategy_recommendation(blend_strategy),
            next_steps="CEO approves blend ratios → Test blend workflow → Implement in production"
        )
    
    async def _handle_general_analysis(self, game_concept: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general art direction analysis requests."""
        
        analysis = await self.analyst.analyze_game_concept(game_concept, **context)
        
        return self._format_ceo_response(
            task="Art Direction Analysis",
            analysis={
                "game_concept": game_concept,
                "style_scores": analysis["style_recommendations"],
                "emotional_target": analysis["emotional_response_target"],
                "constraints": analysis["technical_constraints"]
            },
            options=self._format_general_analysis_options(analysis),
            recommendation=self._create_general_analysis_recommendation(analysis),
            next_steps="CEO selects analysis focus → Deep dive into chosen area → Generate visual samples"
        )
    
    def _format_ceo_response(self, task: str, analysis: Dict[str, Any], 
                           options: List[Dict[str, Any]], recommendation: str, 
                           next_steps: str) -> Dict[str, Any]:
        """Format response for CEO decision-making."""
        
        return {
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
                "scenario_models": approach_data["model_recommendations"][:2] if approach_data["model_recommendations"] else [],
                "sample_generation_job": approach_data["generation_job"],
                "suitability_score": f"{approach_data['suitability_score']}/10",
                "pros": style.pros,
                "cons": style.cons,
                "time_estimate": self._estimate_production_time(style),
                "recommendation_level": self._calculate_recommendation_level(approach_data['suitability_score'])
            }
            
            options.append(option)
        
        return options
    
    def _format_mood_board_options(self, mood_board: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format mood board options for CEO presentation."""
        
        elements = mood_board["mood_board_elements"]
        
        options = [
            {
                "option_name": "Option A: Full Mood Board Production",
                "description": f"Generate complete mood board with {len(elements)} visual elements",
                "elements_included": list(elements.keys()),
                "generation_jobs": [elem["generation_result"] for elem in elements.values()],
                "models_used": list(set(elem["model_used"] for elem in elements.values())),
                "time_estimate": f"{len(elements) * 15} minutes for full generation",
                "recommendation_level": "⭐⭐⭐"
            },
            {
                "option_name": "Option B: Core Elements Only",
                "description": "Generate essential mood board elements (character, environment, UI)",
                "elements_included": ["main character concept", "environment/background", "UI element design"],
                "time_estimate": "45 minutes for core elements",
                "recommendation_level": "⭐⭐"
            },
            {
                "option_name": "Option C: Style Test Samples",
                "description": "Generate quick style validation samples before full production",
                "elements_included": ["main character concept", "color palette demonstration"],
                "time_estimate": "20 minutes for style tests",
                "recommendation_level": "⭐"
            }
        ]
        
        return options
    
    def _format_model_selection_options(self, recommendations: List[Any]) -> List[Dict[str, Any]]:
        """Format model selection options for CEO presentation."""
        
        if not recommendations:
            return [{"option_name": "No suitable models found", "description": "Fallback to general-purpose models"}]
        
        options = []
        
        for i, rec in enumerate(recommendations[:3]):
            option = {
                "option_name": f"Option {chr(65+i)}: {rec.model_name}",
                "description": f"Suitability score: {rec.suitability_score:.1f}/10",
                "model_id": rec.model_id,
                "model_name": rec.model_name,
                "strengths": rec.strengths,
                "limitations": rec.limitations,
                "optimal_settings": rec.optimal_settings,
                "sample_prompt": rec.sample_prompt,
                "recommendation_level": "⭐⭐⭐" if rec.suitability_score >= 8 else "⭐⭐" if rec.suitability_score >= 6 else "⭐"
            }
            options.append(option)
        
        return options
    
    def _format_model_comparison_options(self, comparison: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format model comparison options for CEO presentation."""
        
        options = [
            {
                "option_name": "Option A: Best Overall Performance",
                "description": "Select models that performed best across all test prompts",
                "analysis": comparison.get("analysis", {}),
                "recommendation_level": "⭐⭐⭐"
            },
            {
                "option_name": "Option B: Specialized Performance",
                "description": "Select different models optimized for specific asset types",
                "analysis": "Use different models for characters vs environments",
                "recommendation_level": "⭐⭐"
            },
            {
                "option_name": "Option C: Single Model Consistency",
                "description": "Use one primary model for all assets to ensure maximum consistency",
                "analysis": "Sacrifice some quality for visual cohesion",
                "recommendation_level": "⭐"
            }
        ]
        
        return options
    
    def _format_blend_strategy_options(self, blend_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format model blending strategy options for CEO presentation."""
        
        optimal_blends = blend_strategy.get("recommended_blends", [])
        
        options = []
        
        for i, blend in enumerate(optimal_blends[:3]):
            option = {
                "option_name": f"Option {chr(65+i)}: {blend['recommended_ratio']} Blend",
                "description": f"Blend {blend['primary_model']} with {blend['secondary_model']}",
                "primary_model": blend["primary_model"],
                "secondary_model": blend["secondary_model"],
                "ratio": blend["recommended_ratio"],
                "compatibility_score": f"{blend['compatibility_score']:.1f}/10",
                "use_case": blend["use_case"],
                "recommendation_level": "⭐⭐⭐" if blend["compatibility_score"] >= 8 else "⭐⭐"
            }
            options.append(option)
        
        return options
    
    def _format_general_analysis_options(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format general analysis options for CEO presentation."""
        
        top_styles = analysis["style_recommendations"][:3]
        
        options = []
        
        for i, (style_name, score) in enumerate(top_styles):
            option = {
                "option_name": f"Option {chr(65+i)}: Focus on {style_name.replace('_', ' ').title()}",
                "description": f"Deep dive into {style_name} style development (Score: {score})",
                "suitability_score": f"{score}/10",
                "next_action": f"Generate visual samples for {style_name}",
                "recommendation_level": "⭐⭐⭐" if score >= 8 else "⭐⭐" if score >= 6 else "⭐"
            }
            options.append(option)
        
        return options
    
    def _create_art_style_recommendation(self, approaches: Dict[str, Any]) -> str:
        """Create expert recommendation for art style selection."""
        
        # Find the highest scored approach
        best_approach = max(approaches["approaches"].items(), 
                          key=lambda x: x[1]["suitability_score"])
        
        best_style = best_approach[1]["style"]
        
        return f"""I recommend **{best_style.name}** for the following reasons:
        
1. **Highest Suitability**: Scored {best_approach[1]['suitability_score']}/10 for this game concept
2. **Technical Fit**: {self._get_technical_justification(best_style)}
3. **Market Appeal**: {self._get_market_justification(best_style)}
4. **Production Efficiency**: {self._get_production_justification(best_style)}

This style will provide the optimal balance of visual impact, technical feasibility, and market appeal for your game concept."""
    
    def _create_mood_board_recommendation(self, mood_board: Dict[str, Any]) -> str:
        """Create expert recommendation for mood board approach."""
        
        return f"""I recommend generating the **Full Mood Board** (Option A) because:

1. **Complete Visual Language**: All {len(mood_board['mood_board_elements'])} elements ensure comprehensive style coverage
2. **Consistency Validation**: Multiple elements help identify and resolve style inconsistencies early
3. **Production Planning**: Complete mood board enables accurate asset pipeline planning
4. **Stakeholder Alignment**: Comprehensive visuals reduce miscommunication and revision cycles

The additional generation time ({len(mood_board['mood_board_elements']) * 15} minutes) is a worthwhile investment for project success."""
    
    def _create_model_selection_recommendation(self, recommendations: List[Any]) -> str:
        """Create expert recommendation for model selection."""
        
        if not recommendations:
            return "I recommend using flux.1-dev as a reliable fallback model with manual style guidance."
        
        best_model = recommendations[0]
        
        return f"""I recommend **{best_model.model_name}** (Score: {best_model.suitability_score:.1f}/10) because:

1. **Style Alignment**: {best_model.strengths[0] if best_model.strengths else 'Best match for target style'}
2. **Quality Assurance**: {best_model.strengths[1] if len(best_model.strengths) > 1 else 'Consistent output quality'}
3. **Technical Capability**: {best_model.strengths[2] if len(best_model.strengths) > 2 else 'Advanced features support'}

Combine with {recommendations[1].model_name if len(recommendations) > 1 else 'flux.1-dev'} as secondary model for variety and backup options."""
    
    def _create_model_comparison_recommendation(self, comparison: Dict[str, Any]) -> str:
        """Create expert recommendation for model comparison results."""
        
        return f"""Based on the comparison across {len(comparison['styles_compared'])} styles and {len(comparison['prompts_tested'])} test prompts:

I recommend **Option A: Best Overall Performance** because:

1. **Consistency**: Models that perform well across multiple styles reduce production risk
2. **Efficiency**: Single workflow reduces complexity and training overhead  
3. **Quality**: Best performers ensure highest visual standards throughout production
4. **Scalability**: Proven performance across scenarios supports future expansion

Use specialized models only for specific challenging assets that require unique capabilities."""
    
    def _create_blend_strategy_recommendation(self, blend_strategy: Dict[str, Any]) -> str:
        """Create expert recommendation for model blending strategy."""
        
        optimal_blends = blend_strategy.get("recommended_blends", [])
        
        if not optimal_blends:
            return "I recommend using a single primary model to maintain consistency, as no high-compatibility blends were found."
        
        best_blend = optimal_blends[0]
        
        return f"""I recommend the **{best_blend['recommended_ratio']} Blend** (Option A) because:

1. **High Compatibility**: {best_blend['compatibility_score']:.1f}/10 compatibility score ensures smooth blending
2. **Optimal Balance**: {best_blend['recommended_ratio']} ratio provides primary style dominance with enhancement
3. **Proven Workflow**: {best_blend['use_case']}
4. **Risk Mitigation**: High compatibility reduces generation failures and inconsistencies

Start with this blend for core assets, then adjust ratios based on specific asset requirements."""
    
    def _create_general_analysis_recommendation(self, analysis: Dict[str, Any]) -> str:
        """Create expert recommendation for general analysis."""
        
        top_style = analysis["style_recommendations"][0]
        
        return f"""Based on the comprehensive analysis, I recommend focusing on **{top_style[0].replace('_', ' ').title()}** (Score: {top_style[1]}/10) because:

1. **Best Concept Fit**: Highest alignment with game concept and target audience
2. **Technical Feasibility**: Matches platform and complexity requirements  
3. **Market Position**: Aligns with current market trends and player expectations
4. **Production Readiness**: Established workflow and model availability

Next step: Generate visual samples to validate this recommendation with stakeholders."""
    
    def _estimate_production_time(self, style) -> str:
        """Estimate production time for a visual style."""
        
        time_map = {
            "pixel_perfect": "Fast (2-3 days for full asset set)",
            "minimalist_geometric": "Fast (2-3 days for full asset set)", 
            "cartoon_vibrant": "Medium (4-5 days for full asset set)",
            "hand_painted_fantasy": "Slow (6-8 days for full asset set)",
            "dark_atmospheric": "Medium (4-6 days for full asset set)"
        }
        
        return time_map.get(style.name.replace(" ", "_").lower(), "Medium (4-5 days)")
    
    def _calculate_recommendation_level(self, score: float) -> str:
        """Calculate recommendation level based on suitability score."""
        
        if score >= 8:
            return "⭐⭐⭐"
        elif score >= 6:
            return "⭐⭐"
        else:
            return "⭐"
    
    def _get_technical_justification(self, style) -> str:
        """Get technical justification for style recommendation."""
        
        justifications = {
            "Pixel Perfect Retro": "Excellent performance optimization and mobile compatibility",
            "Hand-Painted Fantasy": "High visual impact with manageable technical complexity",
            "Minimalist Geometric": "Outstanding performance across all platforms",
            "Dark Atmospheric Horror": "Efficient rendering with dramatic visual impact",
            "Cartoon Vibrant": "Balanced performance with broad platform support"
        }
        
        return justifications.get(style.name, "Good balance of quality and performance")
    
    def _get_market_justification(self, style) -> str:
        """Get market justification for style recommendation."""
        
        justifications = {
            "Pixel Perfect Retro": "Strong nostalgic appeal with proven market success",
            "Hand-Painted Fantasy": "Premium positioning with high perceived value",
            "Minimalist Geometric": "Universal appeal across demographics and cultures",
            "Dark Atmospheric Horror": "Strong niche appeal with dedicated audience",
            "Cartoon Vibrant": "Broad market appeal across age groups"
        }
        
        return justifications.get(style.name, "Solid market positioning")
    
    def _get_production_justification(self, style) -> str:
        """Get production justification for style recommendation."""
        
        justifications = {
            "Pixel Perfect Retro": "Established workflows and tooling availability",
            "Hand-Painted Fantasy": "AI model availability reduces manual art requirements", 
            "Minimalist Geometric": "Rapid iteration and automated generation possible",
            "Dark Atmospheric Horror": "Focused aesthetic reduces decision complexity",
            "Cartoon Vibrant": "Animation-friendly with efficient asset pipeline"
        }
        
        return justifications.get(style.name, "Efficient production workflow")
    
    def _format_error_response(self, error_message: str) -> Dict[str, Any]:
        """Format error response for CEO communication."""
        
        return {
            "agent": self.agent_name,
            "status": "error",
            "error_message": error_message,
            "suggested_action": "Please provide valid parameters or check system configuration",
            "need_ceo_guidance": True
        }

# CLI Interface
async def main():
    """CLI interface for testing the Art Direction Agent."""
    if len(sys.argv) < 3:
        print("Art Direction Agent - Usage:")
        print("  python art_direction_agent.py 'CEO request here' 'game concept here'")
        print("  Example: python art_direction_agent.py 'show me art styles' 'fantasy adventure game'")
        return
    
    request = sys.argv[1]
    game_concept = sys.argv[2]
    context = {"target_audience": "general", "platform": "desktop"}
    
    agent = ArtDirectionAgent()
    result = await agent.handle_ceo_request(request, game_concept, context)
    
    print(json.dumps(result, indent=2, default=str))

if __name__ == "__main__":
    asyncio.run(main())