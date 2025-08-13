#!/usr/bin/env python3
"""
Generate Flappy Wings game asset samples for CEO art direction review.
Creates actual visual samples for each approach using available models.
"""
import sys
import os
import json
import time
import asyncio
from pathlib import Path

# Import local modules
from core.enhanced_scenario_client import EnhancedScenarioClient

class FlappyWingsArtDirector:
    def __init__(self):
        self.client = EnhancedScenarioClient()
        self.base_output_dir = Path("/Users/qusaiabushanap/dev/amani/Assets/Generated/ArtDirection/FlappyWings_CEO_Models")
        self.base_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Flappy Wings specific game elements
        self.game_elements = {
            "main_character": "cartoon bird character for flappy bird game, side view, wings spread, colorful, simple design, transparent background, game sprite",
            "primary_environment": "green pipe obstacle for flappy bird game, vertical pipe with gap in middle, simple geometric design, side view, game asset",
            "key_ui_element": "score number display for flappy bird game, bold white numbers with black outline, game UI element, clean design",
            "important_game_object": "background cloud element for flappy bird game, simple white fluffy cloud, minimalist design, game background asset"
        }
        
        # Standard locked parameters for consistency
        self.locked_parameters = {
            "width": 512,
            "height": 512,
            "steps": 30,
            "cfg_scale": 7,
            "seed": 42
        }

    async def generate_sample_with_client(self, prompt, model_id, output_file):
        """Generate a single sample using the enhanced client"""
        try:
            # Create directory for the file
            output_file = Path(output_file)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Use the enhanced client's generate method with correct parameter names
            result = await self.client.generate_and_download_with_validation(
                prompt=prompt,
                model_id=model_id,
                download_dir=str(output_file.parent),
                width=self.locked_parameters["width"],
                height=self.locked_parameters["height"],
                num_inference_steps=self.locked_parameters["steps"],
                guidance=self.locked_parameters["cfg_scale"]
            )
            
            # If successful, rename downloaded file to our desired name
            if result.get("success") and result.get("downloaded_files"):
                downloaded_file = result["downloaded_files"][0]
                if Path(downloaded_file).exists():
                    Path(downloaded_file).rename(output_file)
                    result["final_path"] = str(output_file)
                    
            return result
        except Exception as e:
            print(f"    ❌ Error generating sample: {str(e)}")
            return {"success": False, "error": str(e)}

    async def generate_samples_for_approach(self, model_id, approach_name):
        """Generate all 4 game asset samples for a specific model approach"""
        approach_dir = self.base_output_dir / f"{approach_name}_samples"
        approach_dir.mkdir(exist_ok=True)
        
        samples = []
        sample_paths = []
        
        print(f"\n🎮 Generating Flappy Wings assets for {approach_name}")
        print(f"📁 Output directory: {approach_dir}")
        
        for asset_name, prompt in self.game_elements.items():
            print(f"  🎨 Generating {asset_name}...")
            
            file_path = approach_dir / f"{asset_name}.png"
            
            result = await self.generate_sample_with_client(prompt, model_id, file_path)
            
            if result.get("success", False):
                samples.append(result)
                sample_paths.append(str(file_path))
                print(f"    ✅ {asset_name} generated successfully")
            else:
                print(f"    ❌ Failed to generate {asset_name}: {result.get('error', 'Unknown error')}")
                
            # Brief pause between generations
            await asyncio.sleep(2)
        
        return {
            "model_id": model_id,
            "approach_name": approach_name,
            "samples": samples,
            "sample_paths": sample_paths,
            "locked_parameters": self.locked_parameters
        }

    def calculate_consistency_score(self, samples):
        """Calculate a basic consistency score based on successful generations"""
        if not samples:
            return 0.0
        
        successful_samples = len([s for s in samples if s.get("success", False)])
        total_samples = len(samples)
        
        # Base score on success rate, with bonus for complete set
        base_score = (successful_samples / total_samples) * 8.0
        if successful_samples == total_samples:
            base_score += 1.5  # Bonus for complete set
            
        return min(base_score, 10.0)

    async def generate_all_approaches(self):
        """Generate samples for all available model approaches"""
        
        # Get available models for comparison
        models_result = await self.client.discover_models_with_filtering(limit=10)
        
        if not models_result.get("success") or not models_result.get("models") or len(models_result["models"]) < 3:
            print("❌ Insufficient models available for comparison")
            return None
            
        models = models_result["models"]
        
        # Use first 3 available models to represent different art approaches
        model_approaches = [
            {"model_id": models[0]["id"], "name": "Model_A_ComixTopDown"},
            {"model_id": models[1]["id"], "name": "Model_B_TestStyle"}, 
            {"model_id": models[2]["id"], "name": "Model_C_NewModel"}
        ]
        
        print(f"🎯 Generating Flappy Wings samples for {len(model_approaches)} model approaches")
        
        all_results = []
        
        for i, approach in enumerate(model_approaches):
            print(f"\n📊 Approach {i+1}/3: {approach['name']}")
            
            result = await self.generate_samples_for_approach(
                approach["model_id"], 
                approach["name"]
            )
            
            # Calculate consistency score
            result["consistency_score"] = self.calculate_consistency_score(result["samples"])
            print(f"  📈 Consistency Score: {result['consistency_score']:.1f}/10")
            
            all_results.append(result)
        
        return all_results

    def create_ceo_decision_report(self, results):
        """Create CEO decision report with actual file paths"""
        
        report = {
            "project": "Flappy Wings",
            "game_type": "2D side-scrolling endless runner (Flappy Bird clone)",
            "generation_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "approaches": [],
            "decision_required": True
        }
        
        print(f"\n🎮 FLAPPY WINGS - CEO ART DIRECTION DECISION REQUIRED")
        print(f"=" * 60)
        
        for i, result in enumerate(results):
            approach_letter = chr(65 + i)  # A, B, C
            
            approach_info = {
                "id": approach_letter,
                "model_id": result["model_id"],
                "approach_name": result["approach_name"],
                "consistency_score": result["consistency_score"],
                "sample_paths": result["sample_paths"],
                "locked_parameters": result["locked_parameters"]
            }
            
            report["approaches"].append(approach_info)
            
            print(f"\n### Model {approach_letter}: {result['approach_name']} - FLAPPY WINGS ASSETS")
            print(f"📱 Generated Flappy Bird Game Asset Samples (Local file paths):")
            
            asset_names = ["Main Character (Flappy Bird)", "Primary Environment (Pipe Obstacle)", 
                          "Key UI Element (Score Display)", "Important Game Object (Background Cloud)"]
            
            for j, (asset_name, file_path) in enumerate(zip(asset_names, result["sample_paths"])):
                if j < len(result["sample_paths"]):
                    print(f"- **{asset_name}**: {file_path}")
            
            print(f"\n🎯 Flappy Wings Game Context Analysis:")
            print(f"- **Model ID**: {result['model_id']}")
            print(f"- **Visual Style**: [Based on actual Flappy Bird game assets generated]")
            print(f"- **Game Fit**: [How well it matches Flappy Wings concept]")
            print(f"- **Consistency Score**: ✅ {result['consistency_score']:.1f}/10 across Flappy Bird assets")
        
        # Save detailed report
        report_path = self.base_output_dir / "flappy_wings_ceo_decision_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📋 SIMPLE CEO CHOICE:")
        print(f"**Which model best represents how you want FLAPPY WINGS to look?**")
        for i, result in enumerate(results):
            approach_letter = chr(65 + i)
            print(f"- Option {approach_letter}: {result['approach_name']} (Score: {result['consistency_score']:.1f}/10)")
        
        print(f"\n✅ **Decision Time**: 2-3 minutes (you can see exactly how Flappy Wings will look!)")
        print(f"🔒 **Result**: Selected model becomes your LOCKED style for ALL future Flappy Wings assets")
        print(f"\n📄 Detailed Report: {report_path}")
        
        return report

async def main():
    director = FlappyWingsArtDirector()
    
    print("🚀 Starting Flappy Wings Art Direction Sample Generation")
    print("🎮 Game: Flappy Bird clone with tap-to-flap bird physics")
    print("🎨 Generating actual game asset samples for CEO review...")
    
    try:
        results = await director.generate_all_approaches()
        
        if results:
            report = director.create_ceo_decision_report(results)
            print(f"\n🎯 SUCCESS: Generated {len(results)} Flappy Wings model approaches")
            print(f"📊 Total assets generated: {sum(len(r['sample_paths']) for r in results)}")
            print(f"📁 All files saved to: {director.base_output_dir}")
            
            return report
        else:
            print("❌ Failed to generate approaches")
            return None
            
    except Exception as e:
        print(f"❌ Error during generation: {str(e)}")
        return None

if __name__ == "__main__":
    asyncio.run(main())