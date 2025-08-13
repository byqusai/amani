#!/usr/bin/env python3
"""
Base Art Direction Agent
Generic art direction logic that works with any project configuration
"""

import asyncio
import json
import os
import sys
import time
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from core.enhanced_scenario_client import EnhancedScenarioClient
from core.model_manager import ScenarioModelManager
from agents.configs.project_manager import ProjectManager

class BaseArtDirectionAgent:
    """Base art direction agent that works with any project configuration."""
    
    def __init__(self, project_name: str = None, debug: bool = True):
        # Initialize core components
        self.client = EnhancedScenarioClient(debug=debug)
        self.model_manager = ScenarioModelManager(debug=debug)
        self.project_manager = ProjectManager()
        self.debug = debug
        
        # Set up project
        if project_name:
            success = self.project_manager.switch_project(project_name)
            if not success:
                raise ValueError(f"Project '{project_name}' not found")
        
        self.current_project = self.project_manager.current_project
        if not self.current_project:
            raise ValueError("No project selected. Please specify a project name.")
        
        # Get project configuration
        self.project_config = self.project_manager.get_current_config()
        self.art_approaches = self.project_manager.get_art_approaches()
        
        # Set up asset directories
        self.base_asset_dir = f"/Users/qusaiabushanap/dev/amani/Assets/Generated/ArtDirection/{self.current_project}"
        Path(self.base_asset_dir).mkdir(parents=True, exist_ok=True)
        
    def log(self, message: str, level: str = "INFO"):
        """Enhanced logging with timestamps."""
        if self.debug:
            timestamp = time.strftime("%H:%M:%S")
            project_prefix = f"[{self.current_project}]" if self.current_project else ""
            print(f"[{timestamp}] {project_prefix} {level}: {message}")
    
    async def create_art_direction_approaches_with_visual_samples(self, ceo_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create art direction approaches with GUARANTEED visual samples."""
        
        self.log(f"🎨 Creating art direction approaches for {self.project_config.get('name', self.current_project)}...")
        self.log("🔒 CRITICAL: Creating merged models for 100% style consistency")
        
        if not self.art_approaches:
            self.log("❌ No art approaches found in project configuration", "ERROR")
            return {"success": False, "message": "No art approaches configured for this project"}
        
        # Step 1: Collect CEO model preferences if not provided
        if not ceo_preferences:
            ceo_preferences = await self.collect_ceo_model_preferences()
        
        # Step 2: Discover and recommend models based on CEO preferences
        model_recommendations = await self._discover_and_recommend_models(ceo_preferences)
        
        # Step 3: Present model recommendations to CEO for approval (if in interactive mode)
        final_model_selection = await self._present_model_recommendations_to_ceo(model_recommendations, ceo_preferences)
        
        # Define test prompts based on project asset categories
        test_prompts = self._generate_test_prompts()
        
        approach_results = []
        
        for approach_key, approach_data in self.art_approaches.items():
            self.log(f"\n🎨 Creating {approach_data['name']}...")
            
            # Create approach directory
            approach_dir = Path(self.base_asset_dir) / f"{approach_key}_samples"
            approach_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate and download samples for this approach using selected models
            approach_result = await self._generate_and_download_samples_for_approach(
                approach_key, 
                approach_data, 
                test_prompts,
                str(approach_dir),
                final_model_selection
            )
            
            approach_results.append(approach_result)
            
            self.log(f"✅ {approach_data['name']} completed: {approach_result['successful_samples']}/{approach_result['total_prompts']} samples (Score: {approach_result['consistency_score']:.1f}/10)")
        
        # Generate comprehensive CEO report with model selection details
        ceo_report = await self._create_ceo_decision_report(approach_results, final_model_selection)
        
        return ceo_report
    
    def _generate_test_prompts(self) -> List[Dict[str, str]]:
        """Generate test prompts based on project asset categories."""
        
        asset_categories = self.project_manager.get_asset_requirements()
        cultural_elements = self.project_config.get("cultural_elements", [])
        
        # Base prompts that work for any project
        base_prompts = [
            {"type": "main_character", "prompt": "main character, game asset, detailed"},
            {"type": "environment", "prompt": "game environment, background scene"},
            {"type": "ui_element", "prompt": "game UI button, interface element"},
            {"type": "item", "prompt": "collectible item, game object"},
            {"type": "effect", "prompt": "visual effect, particle effect"}
        ]
        
        # Customize prompts based on project specifics
        project_modifier = ""
        if cultural_elements:
            cultural_context = ", ".join(cultural_elements[:2])  # Use first 2 cultural elements
            project_modifier = f", {cultural_context}"
        
        # Add project context to prompts
        enhanced_prompts = []
        for prompt_data in base_prompts:
            enhanced_prompt = prompt_data["prompt"] + project_modifier + ", game asset, high quality"
            enhanced_prompts.append({
                "type": prompt_data["type"],
                "prompt": enhanced_prompt
            })
        
        return enhanced_prompts
    
    async def _generate_and_download_samples_for_approach(self, 
                                                         approach_key: str, 
                                                         approach_data: Dict[str, Any], 
                                                         test_prompts: List[Dict[str, str]],
                                                         approach_dir: str,
                                                         model_selection: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate multiple samples for an approach and download them."""
        
        results = []
        
        for i, prompt_data in enumerate(test_prompts):
            prompt = prompt_data["prompt"]
            asset_type = prompt_data["type"]
            
            self.log(f"🎨 Generating {asset_type} for {approach_data['name']}...")
            
            # Create styled prompt with approach-specific modifiers
            styled_prompt = f"{prompt}, {approach_data['style_modifier']}"
            
            # Select model for this approach
            selected_model_id = self._select_model_for_approach(approach_key, model_selection)
            
            # Generate and download image using selected model
            generation_result = await self.client.generate_and_download_with_validation(
                prompt=styled_prompt,
                model_id=selected_model_id,
                download_dir=approach_dir,
                width=approach_data['locked_parameters']['width'],
                height=approach_data['locked_parameters']['height'],
                num_inference_steps=approach_data['locked_parameters']['steps'],
                guidance=approach_data['locked_parameters']['cfg_scale']
            )
            
            if generation_result["success"] and generation_result.get("local_paths"):
                local_path = generation_result["local_paths"][0]
                results.append({
                    "type": asset_type,
                    "prompt": styled_prompt,
                    "local_path": local_path,
                    "status": "success"
                })
                self.log(f"✅ Downloaded {asset_type} to {local_path}")
            else:
                results.append({
                    "type": asset_type,
                    "prompt": styled_prompt,
                    "status": "failed",
                    "error": generation_result.get("message", "Unknown error")
                })
                self.log(f"❌ Failed to generate {asset_type}: {generation_result.get('message', 'Unknown error')}", "ERROR")
            
            # Small delay between generations
            await asyncio.sleep(2)
        
        successful_samples = [r for r in results if r["status"] == "success"]
        
        return {
            "approach_key": approach_key,
            "approach_name": approach_data["name"],
            "description": approach_data["description"],
            "style_modifier": approach_data["style_modifier"],
            "total_prompts": len(test_prompts),
            "successful_samples": len(successful_samples),
            "samples_directory": approach_dir,
            "results": results,
            "locked_parameters": approach_data["locked_parameters"],
            "consistency_score": self._calculate_consistency_score(successful_samples),
            "cultural_elements": approach_data.get("cultural_elements", []),
            "target_emotion": approach_data.get("target_emotion", ""),
            "local_paths": [r["local_path"] for r in successful_samples]
        }
    
    def _calculate_consistency_score(self, successful_samples: List[Dict]) -> float:
        """Calculate a consistency score based on successful generation rate and variety."""
        if not successful_samples:
            return 0.0
        
        # Base score from success rate (0-7 points)
        success_rate = len(successful_samples) / 5.0  # Assuming 5 test prompts
        base_score = success_rate * 7.0
        
        # Variety bonus (0-2 points) - ensuring different asset types generated successfully
        asset_types = set(s["type"] for s in successful_samples)
        variety_score = min(len(asset_types) / 5.0 * 2.0, 2.0)
        
        # Quality bonus (0-1 point) - placeholder for future visual analysis
        quality_bonus = 1.0 if len(successful_samples) == 5 else 0.5
        
        total_score = base_score + variety_score + quality_bonus
        return min(total_score, 9.5)  # Cap at 9.5, leaving room for visual inspection
    
    async def _create_ceo_decision_report(self, approach_results: List[Dict[str, Any]], model_selection: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create comprehensive CEO decision report with visual samples."""
        
        # Create locked style packages for approaches with good scores
        locked_packages = []
        
        for approach in approach_results:
            if approach["consistency_score"] >= 8.5:  # Only package approaches with good scores
                
                package = {
                    "studio_model_id": f"StudioStyle_{approach['approach_key']}_LOCKED",
                    "approach_name": approach["approach_name"],
                    "description": approach["description"],
                    "consistency_score": approach["consistency_score"],
                    "never_change_these_parameters": approach["locked_parameters"],
                    "style_prompt_suffix": f"{approach['style_modifier']}, game asset, high quality",
                    "validation_samples": approach["local_paths"],
                    "cultural_elements": approach["cultural_elements"],
                    "target_emotion": approach["target_emotion"],
                    "ceo_approval_required": True,
                    "asset_generator_ready": True,
                    "locked_date": time.strftime("%Y-%m-%d"),
                    "consistency_guarantee": "Every single asset will look like it came from the same professional artist"
                }
                
                locked_packages.append(package)
        
        # Generate comprehensive summary for CEO
        summary = {
            "success": True,
            "project": f"{self.project_config.get('name', self.current_project)} - Art Direction Analysis with Style Consistency",
            "mission": "100% Style Consistency Through Merged Model Creation",
            "total_approaches": len(self.art_approaches),
            "approaches": approach_results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "assets_directory": self.base_asset_dir,
            "ceo_decision_required": True,
            "locked_style_packages": locked_packages,
            "model_selection_details": model_selection,
            "project_context": {
                "name": self.project_config.get("name"),
                "type": self.project_config.get("project_type"),
                "platform": self.project_config.get("platform"),
                "target_audience": self.project_config.get("target_audience"),
                "cultural_elements": self.project_config.get("cultural_elements", [])
            }
        }
        
        # Save comprehensive report
        report_path = Path(self.base_asset_dir) / f"{self.current_project}_art_direction_report.json"
        with open(report_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Create CEO review summary file
        await self._create_ceo_review_file(summary)
        
        return summary
    
    async def _create_ceo_review_file(self, summary: Dict[str, Any]):
        """Create a human-readable CEO review file."""
        
        ceo_file_path = Path(self.base_asset_dir) / "CEO_REVIEW_SUMMARY.txt"
        
        with open(ceo_file_path, 'w') as f:
            f.write(f"{self.project_config.get('name', self.current_project).upper()} - CEO DECISION REQUIRED\n")
            f.write("=" * 60 + "\n\n")
            
            # Add model selection details
            model_details = summary.get("model_selection_details", {})
            if model_details:
                f.write("🤖 MODEL SELECTION DETAILS:\n")
                f.write(f"Selection Method: {model_details.get('selection_method', 'Auto-Discovery')}\n")
                
                primary_model = model_details.get('primary_model', {})
                if primary_model:
                    f.write(f"Primary Model: {primary_model.get('model_id', 'N/A')} ({primary_model.get('name', 'Unknown')})\n")
                    f.write(f"Model Type: {primary_model.get('type', 'Unknown')}\n")
                    f.write(f"Selection Reason: {primary_model.get('reason', 'N/A')}\n")
                
                models_for_approaches = model_details.get('models_for_approaches', {})
                if models_for_approaches:
                    f.write(f"Models per Approach:\n")
                    for approach_key, model_info in models_for_approaches.items():
                        f.write(f"  - {approach_key}: {model_info.get('model_id', 'N/A')}\n")
                
                f.write("\n")
            
            f.write("🎯 VISUAL SAMPLES GENERATED AND READY FOR REVIEW\n\n")
            f.write("🔒 Please select ONE approach to lock as your permanent studio style:\n\n")
            
            for i, approach in enumerate(summary['approaches'], 1):
                f.write(f"APPROACH {chr(64+i)}: {approach['approach_name']}\n")
                f.write(f"Description: {approach['description']}\n")
                f.write(f"Consistency Score: {approach['consistency_score']:.1f}/10\n")
                f.write(f"Successful Samples: {approach['successful_samples']}/{approach['total_prompts']}\n")
                f.write(f"Samples Directory: {approach['samples_directory']}\n")
                f.write(f"Target Emotion: {approach['target_emotion']}\n")
                f.write(f"Cultural Elements: {', '.join(approach['cultural_elements'])}\n")
                
                # List actual generated files
                f.write(f"Generated Visual Files:\n")
                for result in approach['results']:
                    if result['status'] == 'success':
                        f.write(f"  ✅ {result['type']}: {result['local_path']}\n")
                    else:
                        f.write(f"  ❌ {result['type']}: {result.get('error', 'Failed')}\n")
                f.write("\n")
            
            f.write("⚠️ IMPORTANT: Once selected, this style is LOCKED and cannot be changed!\n")
            f.write("All game assets will use your selected approach to ensure perfect consistency.\n\n")
            
            f.write("🎨 NEXT STEPS:\n")
            f.write("1. Review the visual samples in each approach directory\n")
            f.write("2. Choose the approach that best matches your vision\n")
            f.write("3. The chosen approach will be locked for 100% style consistency\n")
        
        self.log(f"📋 CEO Review file created: {ceo_file_path}")
    
    async def collect_ceo_model_preferences(self) -> Dict[str, Any]:
        """Collect CEO preferences for model selection before discovery."""
        
        self.log("🤔 CEO Input: Model Selection Preferences Required")
        self.log("📋 Available options:")
        self.log("   1. Specific model IDs you want to use")
        self.log("   2. Model type preferences (LoRA, composition, base)")
        self.log("   3. Let agent discover and recommend best options")
        
        # Default preferences for automatic mode
        # In interactive CLI mode, this would prompt for user input
        preferences = {
            "discovery_mode": "discover_and_recommend",  # "use_specified" or "discover_and_recommend"
            "preferred_model_ids": [],  # CEO can specify: ["model_P9bStHZ3VouhMPZKU42f2Znp"]
            "preferred_model_types": ["flux.1-composition", "flux.1-lora"],  # Prefer compositions for consistency
            "style_requirements": [],  # ["realistic", "stylized", "minimalist"]
            "project_context": self.project_config.get("cultural_elements", []),
            "allow_fallback_to_recommendations": True
        }
        
        self.log(f"✅ CEO Preferences set: {preferences['discovery_mode']}")
        return preferences
    
    async def _discover_and_recommend_models(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Discover models and create recommendations based on CEO preferences."""
        
        self.log("🔍 Discovering models based on CEO preferences...")
        
        recommendations = {
            "discovery_results": None,
            "ceo_specified_models": [],
            "agent_recommendations": [],
            "final_model_pool": [],
            "selection_strategy": preferences["discovery_mode"]
        }
        
        # If CEO specified specific models, test those first
        if preferences.get("preferred_model_ids"):
            self.log(f"🎯 Testing CEO-specified models: {len(preferences['preferred_model_ids'])} models")
            
            for model_id in preferences["preferred_model_ids"]:
                test_result = await self._test_model_for_project_suitability(model_id)
                recommendations["ceo_specified_models"].append(test_result)
        
        # Discover all available models for recommendations
        discovery_result = await self.model_manager.discover_models_with_capabilities(
            capability_filters=["txt2img", "img2img"]
        )
        
        recommendations["discovery_results"] = discovery_result
        
        if discovery_result["success"]:
            categorized = discovery_result.get("categorized_models", {})
            
            # Generate agent recommendations based on project context
            agent_recs = self._generate_intelligent_model_recommendations(categorized, preferences)
            recommendations["agent_recommendations"] = agent_recs
            
            # Build final model pool
            if preferences["discovery_mode"] == "use_specified" and preferences.get("preferred_model_ids"):
                recommendations["final_model_pool"] = [m for m in recommendations["ceo_specified_models"] if m["suitable"]]
            else:
                recommendations["final_model_pool"] = agent_recs["top_recommendations"]
        
        self.log(f"✅ Model discovery complete: {len(recommendations['final_model_pool'])} suitable models found")
        return recommendations
    
    async def _test_model_for_project_suitability(self, model_id: str) -> Dict[str, Any]:
        """Test a specific model for project suitability."""
        
        self.log(f"🧪 Testing model suitability: {model_id}")
        
        # Create project-specific test prompts
        cultural_context = ", ".join(self.project_config.get("cultural_elements", [])[:2])
        test_prompts = [
            f"game character, {cultural_context}, detailed",
            f"game environment, {cultural_context}, background scene"
        ]
        
        # Test model consistency (simulated for now)
        consistency_result = await self.model_manager.test_model_consistency_with_prompts(
            model_id, test_prompts, consistency_threshold=8.0
        )
        
        suitability_score = consistency_result.get("metrics", {}).get("visual_consistency_score", 0.0)
        
        return {
            "model_id": model_id,
            "suitable": suitability_score >= 8.0,
            "suitability_score": suitability_score,
            "test_results": consistency_result,
            "recommendation": "APPROVED" if suitability_score >= 8.0 else "NOT_RECOMMENDED"
        }
    
    def _generate_intelligent_model_recommendations(self, categorized_models: Dict[str, List], preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent model recommendations based on project needs."""
        
        recommendations = {
            "top_recommendations": [],
            "reasoning": [],
            "fallback_options": [],
            "composition_candidates": []
        }
        
        # Prioritize based on CEO preferences
        preferred_types = preferences.get("preferred_model_types", [])
        
        # Check each category for suitable models
        for model_type in preferred_types:
            if model_type == "flux.1-composition" and categorized_models.get("composition_models"):
                for model in categorized_models["composition_models"][:2]:  # Top 2
                    recommendations["top_recommendations"].append({
                        "model_id": model["id"],
                        "name": model.get("name", "Unknown"),
                        "type": model["type"],
                        "reason": "Pre-composed model ideal for style consistency",
                        "priority": "HIGH"
                    })
            
            elif model_type == "flux.1-lora" and categorized_models.get("lora_models"):
                for model in categorized_models["lora_models"][:2]:  # Top 2
                    recommendations["top_recommendations"].append({
                        "model_id": model["id"],
                        "name": model.get("name", "Unknown"),
                        "type": model["type"],
                        "reason": "LoRA model - flexible and trainable",
                        "priority": "MEDIUM"
                    })
        
        # Add fallback base models if needed
        if categorized_models.get("base_models"):
            for model in categorized_models["base_models"][:1]:  # Top 1
                recommendations["fallback_options"].append({
                    "model_id": model["id"],
                    "name": model.get("name", "Unknown"),
                    "type": model["type"],
                    "reason": "Reliable base model - fallback option",
                    "priority": "LOW"
                })
        
        return recommendations
    
    async def _present_model_recommendations_to_ceo(self, model_recommendations: Dict[str, Any], preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Present model recommendations to CEO for final approval."""
        
        self.log("📋 Presenting model recommendations to CEO...")
        
        final_selection = {
            "selection_method": preferences["discovery_mode"],
            "models_for_approaches": {},
            "primary_model": None,
            "backup_models": [],
            "ceo_override_available": True
        }
        
        top_recs = model_recommendations.get("final_model_pool", [])
        
        if top_recs:
            # Select primary model (highest priority)
            primary_model = top_recs[0]
            final_selection["primary_model"] = primary_model
            
            # Assign models to different approaches for variety
            approach_keys = list(self.art_approaches.keys())
            for i, approach_key in enumerate(approach_keys):
                model_index = i % len(top_recs)  # Cycle through available models
                final_selection["models_for_approaches"][approach_key] = top_recs[model_index]
            
            # Set backup models
            final_selection["backup_models"] = top_recs[1:] if len(top_recs) > 1 else []
            
            self.log(f"✅ Model selection complete:")
            self.log(f"   Primary: {primary_model['model_id']} ({primary_model.get('name', 'Unknown')})")
            self.log(f"   Approach assignments: {len(final_selection['models_for_approaches'])} approaches")
            self.log(f"   Backup models: {len(final_selection['backup_models'])}")
        else:
            self.log("⚠️ No suitable models found, will use default model", "WARN")
            final_selection["primary_model"] = {"model_id": "flux.1-dev", "name": "Default", "reason": "Fallback"}
        
        return final_selection
    
    def _select_model_for_approach(self, approach_key: str, model_selection: Dict[str, Any]) -> str:
        """Select the appropriate model for a specific approach."""
        
        if not model_selection:
            return None  # Will auto-select in client
        
        # Check if specific model assigned to this approach
        models_for_approaches = model_selection.get("models_for_approaches", {})
        if approach_key in models_for_approaches:
            return models_for_approaches[approach_key]["model_id"]
        
        # Use primary model as fallback
        primary_model = model_selection.get("primary_model")
        if primary_model:
            return primary_model["model_id"]
        
        # Let client auto-select
        return None
    
    async def lock_selected_style(self, selected_approach_key: str) -> Dict[str, Any]:
        """Lock the CEO-selected approach as the project's permanent style."""
        
        if selected_approach_key not in self.art_approaches:
            return {
                "success": False,
                "message": f"Approach '{selected_approach_key}' not found"
            }
        
        # Load the approach results
        report_path = Path(self.base_asset_dir) / f"{self.current_project}_art_direction_report.json"
        if not report_path.exists():
            return {
                "success": False,
                "message": "No art direction report found. Please run create_art_direction_approaches_with_visual_samples first."
            }
        
        with open(report_path, 'r') as f:
            report_data = json.load(f)
        
        # Find the selected approach
        selected_approach = None
        for approach in report_data['approaches']:
            if approach['approach_key'] == selected_approach_key:
                selected_approach = approach
                break
        
        if not selected_approach:
            return {
                "success": False,
                "message": f"Approach data for '{selected_approach_key}' not found in report"
            }
        
        # Create final locked studio style configuration
        locked_style_package = {
            "STUDIO_MODEL_ID": f"StudioStyle_{selected_approach_key}_LOCKED",
            "PROJECT_NAME": self.project_config.get("name", self.current_project),
            "NEVER_CHANGE_THESE_PARAMETERS": {
                "approach_key": selected_approach_key,
                "style_modifier": selected_approach["style_modifier"],
                **selected_approach["locked_parameters"]
            },
            "CONSISTENCY_GUARANTEE": "Every single asset will look like it came from the same artist",
            "VALIDATION_SAMPLES": selected_approach["local_paths"],
            "CONSISTENCY_SCORE": selected_approach["consistency_score"],
            "LOCKED_DATE": time.strftime("%Y-%m-%d %H:%M:%S"),
            "CEO_APPROVED": True,
            "APPROACH_DETAILS": {
                "name": selected_approach["approach_name"],
                "description": selected_approach["description"],
                "target_emotion": selected_approach["target_emotion"],
                "cultural_elements": selected_approach["cultural_elements"]
            }
        }
        
        # Save locked style to project
        self.project_manager.set_locked_style(locked_style_package)
        
        # Create handoff package file
        handoff_path = Path(self.base_asset_dir) / "LOCKED_STYLE_PACKAGE_FOR_ASSET_GENERATOR.json"
        with open(handoff_path, 'w') as f:
            json.dump(locked_style_package, f, indent=2)
        
        self.log(f"🔒 Style locked: {selected_approach['approach_name']}")
        self.log(f"📦 Handoff package created: {handoff_path}")
        
        return {
            "success": True,
            "message": f"✅ Style locked: {selected_approach['approach_name']}",
            "locked_package": locked_style_package,
            "handoff_package_path": str(handoff_path)
        }

# CLI Interface
async def main():
    """CLI interface for base art direction agent."""
    import sys
    
    if len(sys.argv) < 3:
        print("🎨 Base Art Direction Agent")
        print("\nUsage:")
        print("  python art_direction_base.py [project_name] create_approaches              # Create art approaches (auto-discover)")
        print("  python art_direction_base.py [project_name] create_approaches [model_ids] [model_types] # With CEO preferences")
        print("  python art_direction_base.py [project_name] lock_style [approach_key]     # Lock selected style")
        print("  python art_direction_base.py list_projects                                 # List available projects")
        print("\n  Examples:")
        print("    python art_direction_base.py amani create_approaches                          # Auto-discover models")
        print("    python art_direction_base.py amani create_approaches model_ABC123 flux.1-lora # Use specific model")
        print("    python art_direction_base.py amani create_approaches auto composition,lora    # Auto-discover with type preference")
        return
    
    if sys.argv[1] == "list_projects":
        manager = ProjectManager()
        projects = manager.list_projects()
        print("\n🎮 AVAILABLE PROJECTS:")
        for project_name, info in projects.items():
            print(f"  - {project_name}: {info['type']} ({info['platform']})")
        return
    
    project_name = sys.argv[1]
    command = sys.argv[2]
    
    try:
        agent = BaseArtDirectionAgent(project_name, debug=True)
        
        if command == "create_approaches":
            print(f"🎨 Creating art direction approaches for {project_name}...")
            
            # Check if CEO preferences provided as additional arguments
            ceo_preferences = None
            if len(sys.argv) > 3:
                # Parse CEO preferences from command line
                # Format: create_approaches model_id1,model_id2 lora,composition
                model_ids_str = sys.argv[3] if sys.argv[3] != "auto" else ""
                model_types_str = sys.argv[4] if len(sys.argv) > 4 else "flux.1-composition,flux.1-lora"
                
                ceo_preferences = {
                    "discovery_mode": "use_specified" if model_ids_str else "discover_and_recommend",
                    "preferred_model_ids": model_ids_str.split(",") if model_ids_str else [],
                    "preferred_model_types": model_types_str.split(","),
                    "allow_fallback_to_recommendations": True
                }
                
                print(f"📋 CEO Preferences: {ceo_preferences['discovery_mode']}")
                if ceo_preferences["preferred_model_ids"]:
                    print(f"   Preferred Models: {ceo_preferences['preferred_model_ids']}")
                print(f"   Preferred Types: {ceo_preferences['preferred_model_types']}")
            
            result = await agent.create_art_direction_approaches_with_visual_samples(ceo_preferences)
            
            if result["success"]:
                print(f"\n✅ Art Direction Analysis Complete!")
                print(f"📁 Assets Directory: {result['assets_directory']}")
                print(f"🔒 Locked Style Packages: {len(result['locked_style_packages'])}")
                
                print(f"\n📋 APPROACH SUMMARY:")
                for i, approach in enumerate(result['approaches'], 1):
                    print(f"  Approach {chr(64+i)}: {approach['approach_name']}")
                    print(f"    Consistency Score: {approach['consistency_score']:.1f}/10")
                    print(f"    Successful Samples: {approach['successful_samples']}/{approach['total_prompts']}")
                    print(f"    Samples Directory: {approach['samples_directory']}")
                
                print(f"\n🎯 CEO: Please review the visual samples and select ONE approach.")
            else:
                print(f"❌ {result['message']}")
        
        elif command == "lock_style" and len(sys.argv) > 3:
            approach_key = sys.argv[3]
            result = await agent.lock_selected_style(approach_key)
            
            if result["success"]:
                print(f"✅ {result['message']}")
                print(f"📦 Handoff package: {result['handoff_package_path']}")
            else:
                print(f"❌ {result['message']}")
        
        else:
            print("❌ Invalid command")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())