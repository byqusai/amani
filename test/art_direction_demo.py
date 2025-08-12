#!/usr/bin/env python3
"""
Art Direction Agent Demo - Visual Communication with Scenario AI
Demonstrates the enhanced capabilities of Agent 2 in the AI Game Studio
"""

import asyncio
import json
import sys
from typing import Dict, Any
from art_direction_agent import ArtDirectionAgent

class ArtDirectionDemo:
    """Demonstration of Art Direction Agent capabilities."""
    
    def __init__(self):
        self.agent = ArtDirectionAgent()
        self.demo_scenarios = self._create_demo_scenarios()
    
    def _create_demo_scenarios(self) -> Dict[str, Dict[str, Any]]:
        """Create demonstration scenarios for different use cases."""
        
        return {
            "fantasy_rpg": {
                "game_concept": "fantasy RPG with magic system and dragon battles",
                "target_audience": "young adults",
                "platform": "desktop",
                "complexity": "high",
                "ceo_requests": [
                    "Show me art style options for this fantasy game",
                    "Generate a mood board for the selected style",
                    "Find the best Scenario AI models for fantasy art",
                    "Create a model blending strategy for consistent art"
                ]
            },
            
            "mobile_puzzle": {
                "game_concept": "casual mobile puzzle game with zen atmosphere",
                "target_audience": "general",
                "platform": "mobile", 
                "complexity": "low",
                "ceo_requests": [
                    "What art styles work best for mobile puzzle games?",
                    "Show me minimalist design options",
                    "Generate samples for zen-style backgrounds"
                ]
            },
            
            "horror_adventure": {
                "game_concept": "psychological horror adventure with dark mysteries",
                "target_audience": "mature",
                "platform": "desktop",
                "complexity": "medium",
                "ceo_requests": [
                    "Create dark atmospheric art direction",
                    "Show me horror-themed visual samples",
                    "Find models that excel at creepy atmospheres"
                ]
            },
            
            "retro_platformer": {
                "game_concept": "retro-style platformer inspired by 16-bit classics",
                "target_audience": "nostalgic gamers",
                "platform": "web",
                "complexity": "medium",
                "ceo_requests": [
                    "Show me pixel art style options",
                    "Compare retro vs modern pixel art approaches",
                    "Generate pixel art character samples"
                ]
            }
        }
    
    async def run_full_demo(self) -> None:
        """Run a comprehensive demonstration of all agent capabilities."""
        
        print("🎨 Art Direction Agent (Agent 2) - Enhanced Demo")
        print("=" * 60)
        print("Visual Communication with Scenario AI Integration")
        print()
        
        # Test each scenario
        for scenario_name, scenario_data in self.demo_scenarios.items():
            print(f"\n📋 SCENARIO: {scenario_name.replace('_', ' ').title()}")
            print("-" * 40)
            print(f"Game Concept: {scenario_data['game_concept']}")
            print(f"Target Audience: {scenario_data['target_audience']}")
            print(f"Platform: {scenario_data['platform']}")
            print()
            
            # Process each CEO request for this scenario
            for i, request in enumerate(scenario_data["ceo_requests"], 1):
                print(f"\n💼 CEO Request {i}: {request}")
                print("🎨 Art Direction Agent Response:")
                
                try:
                    context = {
                        "target_audience": scenario_data["target_audience"],
                        "platform": scenario_data["platform"],
                        "complexity": scenario_data["complexity"]
                    }
                    
                    response = await self.agent.handle_ceo_request(
                        request, 
                        scenario_data["game_concept"], 
                        context
                    )
                    
                    self._display_agent_response(response)
                    
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                
                print("\n" + "─" * 50)
        
        print(f"\n✅ Demo Complete - {self.agent.agent_name} showcased all capabilities")
    
    async def run_specific_demo(self, scenario_name: str, request_index: int = 0) -> None:
        """Run a specific demonstration scenario."""
        
        if scenario_name not in self.demo_scenarios:
            print(f"❌ Scenario '{scenario_name}' not found")
            print(f"Available scenarios: {list(self.demo_scenarios.keys())}")
            return
        
        scenario = self.demo_scenarios[scenario_name]
        
        if request_index >= len(scenario["ceo_requests"]):
            print(f"❌ Request index {request_index} out of range")
            print(f"Available requests: 0-{len(scenario['ceo_requests'])-1}")
            return
        
        request = scenario["ceo_requests"][request_index]
        
        print(f"🎨 Art Direction Agent Demo - {scenario_name}")
        print("=" * 50)
        print(f"Game Concept: {scenario['game_concept']}")
        print(f"CEO Request: {request}")
        print()
        
        try:
            context = {
                "target_audience": scenario["target_audience"],
                "platform": scenario["platform"],
                "complexity": scenario["complexity"]
            }
            
            response = await self.agent.handle_ceo_request(
                request,
                scenario["game_concept"],
                context
            )
            
            self._display_detailed_response(response)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    def _display_agent_response(self, response: Dict[str, Any]) -> None:
        """Display agent response in a formatted way."""
        
        print(f"📊 Task: {response.get('task', 'Unknown')}")
        print(f"🎯 Status: {response.get('status', 'Unknown')}")
        
        # Show analysis
        if "analysis" in response:
            print("\n📈 Analysis:")
            for key, value in response["analysis"].items():
                if isinstance(value, (list, dict)):
                    print(f"  • {key}: {len(value) if isinstance(value, list) else 'Complex data'}")
                else:
                    print(f"  • {key}: {value}")
        
        # Show options count
        if "ceo_options" in response:
            options_count = len(response["ceo_options"])
            print(f"\n💡 CEO Options Presented: {options_count}")
            
            for i, option in enumerate(response["ceo_options"], 1):
                option_name = option.get("option_name", f"Option {i}")
                recommendation = option.get("recommendation_level", "⭐")
                print(f"  {i}. {option_name} {recommendation}")
        
        # Show recommendation
        if "expert_recommendation" in response:
            rec_preview = response["expert_recommendation"][:100] + "..." if len(response["expert_recommendation"]) > 100 else response["expert_recommendation"]
            print(f"\n🎯 Expert Recommendation: {rec_preview}")
        
        # Show next steps
        if "next_steps" in response:
            print(f"\n➡️  Next Steps: {response['next_steps']}")
    
    def _display_detailed_response(self, response: Dict[str, Any]) -> None:
        """Display detailed agent response for specific demos."""
        
        print("🎨 Art Direction Agent Response")
        print("=" * 40)
        
        # Agent info
        print(f"Agent: {response.get('agent', 'Unknown')}")
        print(f"Specialization: {response.get('specialization', 'Unknown')}")
        print(f"Task: {response.get('task', 'Unknown')}")
        print(f"Status: {response.get('status', 'Unknown')}")
        print()
        
        # Detailed analysis
        if "analysis" in response:
            print("📊 Analysis:")
            self._print_dict_formatted(response["analysis"], indent=2)
            print()
        
        # CEO Options
        if "ceo_options" in response:
            print("💡 CEO Decision Options:")
            for i, option in enumerate(response["ceo_options"], 1):
                print(f"\n  Option {i}: {option.get('option_name', f'Option {i}')}")
                print(f"    Description: {option.get('description', 'No description')}")
                
                if "recommendation_level" in option:
                    print(f"    Recommendation: {option['recommendation_level']}")
                
                if "time_estimate" in option:
                    print(f"    Time Estimate: {option['time_estimate']}")
                
                # Show key details
                key_fields = ["model_id", "suitability_score", "compatibility_score", "elements_included"]
                for field in key_fields:
                    if field in option:
                        print(f"    {field.replace('_', ' ').title()}: {option[field]}")
        
        # Expert recommendation
        if "expert_recommendation" in response:
            print(f"\n🎯 Expert Recommendation:")
            print(self._format_multiline_text(response["expert_recommendation"], indent=2))
        
        # Next steps
        if "next_steps" in response:
            print(f"\n➡️  Next Steps:")
            print(f"  {response['next_steps']}")
        
        print(f"\n✅ Agent awaiting CEO decision...")
    
    def _print_dict_formatted(self, data: Dict[str, Any], indent: int = 0) -> None:
        """Print dictionary data in a formatted way."""
        
        spaces = " " * indent
        
        for key, value in data.items():
            if isinstance(value, dict):
                print(f"{spaces}{key}:")
                self._print_dict_formatted(value, indent + 2)
            elif isinstance(value, list):
                if len(value) <= 3:
                    print(f"{spaces}{key}: {value}")
                else:
                    print(f"{spaces}{key}: [{len(value)} items] {value[:2]}...")
            else:
                if isinstance(value, str) and len(value) > 80:
                    print(f"{spaces}{key}: {value[:80]}...")
                else:
                    print(f"{spaces}{key}: {value}")
    
    def _format_multiline_text(self, text: str, indent: int = 0) -> str:
        """Format multiline text with proper indentation."""
        
        spaces = " " * indent
        lines = text.split('\n')
        return '\n'.join([spaces + line.strip() for line in lines])
    
    def display_agent_capabilities(self) -> None:
        """Display comprehensive overview of agent capabilities."""
        
        print("🎨 Art Direction Agent (Agent 2) - Enhanced Capabilities")
        print("=" * 60)
        print()
        
        print("🔍 Core Specializations:")
        print("  • Visual style analysis and mood board creation")
        print("  • Scenario AI model selection and optimization")
        print("  • Art asset planning and organization")
        print("  • Color theory and visual consistency")
        print("  • Performance optimization for game art")
        print()
        
        print("🤖 AI Integration Features:")
        print("  • Real-time Scenario AI model browsing and curation")
        print("  • Visual model comparison with generated samples")
        print("  • Model blending strategies for style consistency")
        print("  • Automated mood board generation")
        print("  • Visual communication instead of text descriptions")
        print()
        
        print("💼 CEO Interaction Protocol:")
        print("  • Presents 2-3 visual options for every decision")
        print("  • Generates actual AI samples for style validation")
        print("  • Provides expert recommendations with justification")
        print("  • Waits for CEO approval before proceeding")
        print("  • Maintains visual consistency throughout project")
        print()
        
        print("🎯 Key Workflows:")
        print("  1. Game Concept → Art Style Analysis → Visual Options")
        print("  2. Style Selection → Scenario Model Curation → Sample Generation")
        print("  3. Model Selection → Mood Board Creation → Production Guidelines")
        print("  4. Asset Planning → Consistency Checklist → Quality Assurance")
        print()
        
        print("🔧 Technical Capabilities:")
        print("  • Scenario AI API integration for real-time generation")
        print("  • Model compatibility analysis and recommendation")
        print("  • Visual style database with production guidelines")
        print("  • Automated asset categorization and workflow planning")
        print("  • Performance optimization recommendations")
        print()
        
        print("Available Demo Scenarios:")
        for scenario_name, scenario_data in self.demo_scenarios.items():
            print(f"  • {scenario_name}: {scenario_data['game_concept']}")

# CLI Interface
async def main():
    """CLI interface for Art Direction Agent demonstrations."""
    
    demo = ArtDirectionDemo()
    
    if len(sys.argv) < 2:
        print("Art Direction Agent Demo - Usage:")
        print("  python art_direction_demo.py capabilities")
        print("  python art_direction_demo.py full")
        print("  python art_direction_demo.py [scenario_name] [request_index]")
        print()
        print("Available scenarios:")
        for scenario in demo.demo_scenarios.keys():
            print(f"  • {scenario}")
        return
    
    command = sys.argv[1]
    
    if command == "capabilities":
        demo.display_agent_capabilities()
    
    elif command == "full":
        await demo.run_full_demo()
    
    elif command in demo.demo_scenarios:
        request_index = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        await demo.run_specific_demo(command, request_index)
    
    else:
        print(f"❌ Unknown command or scenario: {command}")
        print("Use 'capabilities', 'full', or a valid scenario name")

if __name__ == "__main__":
    asyncio.run(main())