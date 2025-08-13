#!/usr/bin/env python3
"""
Verified Art Direction Agent - GUARANTEED Model Verification & Download
This agent ensures model availability BEFORE generation and GUARANTEES file downloads
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from core.enhanced_scenario_client import EnhancedScenarioClient

class VerifiedArtDirectionAgent:
    """Art Direction Agent with GUARANTEED model verification and downloads."""
    
    def __init__(self, project_name: str = "FlappyWings"):
        self.project_name = project_name
        self.client = EnhancedScenarioClient(debug=True)
        self.base_download_dir = Path("/Users/qusaiabushanap/dev/amani/Assets/Generated/ArtDirection")
        
        # Create project-specific directory
        self.project_dir = self.base_download_dir / f"{project_name}_VerifiedModels"
        self.project_dir.mkdir(parents=True, exist_ok=True)
        
        self.log(f"🎨 Initialized Verified Art Direction Agent for {project_name}")
        
    def log(self, message: str):
        """Log with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] ART-DIRECTION: {message}")
    
    async def verify_and_generate_art_approaches(self, model_ids: List[str], game_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify all models FIRST, then generate art approaches with GUARANTEED downloads.
        This prevents the model availability issue permanently.
        """
        self.log(f"🔍 Starting VERIFIED art direction workflow...")
        
        # STEP 1: CRITICAL - Verify ALL models before any generation
        self.log(f"🔍 Verifying {len(model_ids)} CEO-provided models...")
        model_verification = await self.client.verify_models_batch(model_ids)
        
        if not model_verification["success"]:
            return {
                "success": False,
                "message": "❌ CRITICAL: Model verification failed",
                "error": model_verification.get("message", "Unknown verification error")
            }
        
        available_models = model_verification["available_models"]
        unavailable_models = model_verification["unavailable_models"]
        
        self.log(f"✅ Model verification complete: {len(available_models)} available, {len(unavailable_models)} unavailable")
        
        if len(unavailable_models) > 0:
            self.log(f"❌ CRITICAL: These models are NOT available: {unavailable_models}")
            return {
                "success": False,
                "message": f"❌ CRITICAL: {len(unavailable_models)} models are not available: {unavailable_models}",
                "available_models": available_models,
                "unavailable_models": unavailable_models,
                "error": "Model availability check failed"
            }
        
        if len(available_models) == 0:
            return {
                "success": False,
                "message": "❌ CRITICAL: No models are available for generation",
                "error": "No available models"
            }
        
        self.log(f"🎯 All {len(available_models)} models verified and available!")
        
        # STEP 2: Generate assets with each VERIFIED model
        generation_results = {}
        all_generated_files = []
        
        for i, model_id in enumerate(available_models):
            self.log(f"🎨 Generating assets with model {i+1}/{len(available_models)}: {model_id}")
            
            model_result = await self._generate_assets_for_model(
                model_id, 
                game_context,
                approach_name=f"approach_{chr(65+i)}"  # A, B, C, etc.
            )
            
            generation_results[model_id] = model_result
            
            if model_result["success"]:
                all_generated_files.extend(model_result.get("local_paths", []))
                self.log(f"✅ Model {model_id}: {len(model_result.get('local_paths', []))} files generated")
            else:
                self.log(f"❌ Model {model_id} generation failed: {model_result.get('message', 'Unknown error')}")
        
        # STEP 3: GUARANTEE - Verify all files actually exist
        verified_files = []
        for file_path in all_generated_files:
            path_obj = Path(file_path)
            if path_obj.exists() and path_obj.stat().st_size > 1000:
                verified_files.append(file_path)
            else:
                self.log(f"❌ File missing or empty: {file_path}")
        
        # STEP 4: Create comprehensive CEO report
        ceo_report = await self._create_ceo_decision_report(
            available_models, 
            generation_results, 
            verified_files,
            game_context
        )
        
        success = len(verified_files) > 0
        
        return {
            "success": success,
            "message": f"✅ Art Direction Complete! {len(verified_files)} verified files ready for CEO review" if success else "❌ No valid files generated",
            "verified_models": available_models,
            "unavailable_models": unavailable_models,
            "total_files_generated": len(verified_files),
            "verified_file_paths": verified_files,
            "generation_results": generation_results,
            "ceo_report_path": ceo_report["report_path"] if success else None,
            "model_verification_details": model_verification["detailed_results"]
        }
    
    async def _generate_assets_for_model(self, model_id: str, game_context: Dict[str, Any], approach_name: str) -> Dict[str, Any]:
        """Generate all game assets for a specific verified model."""
        
        # Create approach-specific directory
        approach_dir = self.project_dir / f"{approach_name}_{model_id}_samples"
        approach_dir.mkdir(parents=True, exist_ok=True)
        
        # Define game-specific assets to generate
        assets_to_generate = [
            {
                "name": "main_character",
                "prompt": f"{game_context['main_character_prompt']}, transparent background, game sprite",
                "filename": "main_character.png"
            },
            {
                "name": "primary_environment", 
                "prompt": f"{game_context['environment_prompt']}, game background, clean design",
                "filename": "primary_environment.png"
            },
            {
                "name": "key_ui_element",
                "prompt": f"{game_context['ui_prompt']}, game UI element, clear design",
                "filename": "key_ui_element.png"
            },
            {
                "name": "important_game_object",
                "prompt": f"{game_context['object_prompt']}, game asset, transparent background",
                "filename": "important_game_object.png"
            }
        ]
        
        generated_files = []
        
        for asset in assets_to_generate:
            self.log(f"   🖼️ Generating {asset['name']}...")
            
            # Generate with VERIFIED model (verify_model=False since we already verified)
            result = await self.client.generate_and_download_with_validation(
                prompt=asset["prompt"],
                model_id=model_id,
                width=512,
                height=512,
                num_samples=1,
                download_dir=str(approach_dir),
                verify_model=False  # Skip re-verification since we already verified
            )
            
            if result["success"] and result.get("local_paths"):
                # Rename file to expected name
                downloaded_file = Path(result["local_paths"][0])
                target_file = approach_dir / asset["filename"]
                
                if downloaded_file.exists():
                    downloaded_file.rename(target_file)
                    generated_files.append(str(target_file))
                    self.log(f"   ✅ {asset['name']} saved: {target_file}")
                else:
                    self.log(f"   ❌ {asset['name']} download failed: file not found")
            else:
                self.log(f"   ❌ {asset['name']} generation failed: {result.get('message', 'Unknown error')}")
        
        return {
            "success": len(generated_files) > 0,
            "message": f"Generated {len(generated_files)}/{len(assets_to_generate)} assets",
            "local_paths": generated_files,
            "approach_directory": str(approach_dir),
            "model_id": model_id,
            "approach_name": approach_name
        }
    
    async def _create_ceo_decision_report(self, models: List[str], results: Dict, files: List[str], context: Dict) -> Dict[str, Any]:
        """Create comprehensive CEO decision report with file paths."""
        
        report_path = self.project_dir / "CEO_FLAPPY_BIRD_ART_DECISION_REPORT.md"
        
        report_content = f"""# 🎮 {self.project_name} - CEO Art Direction Decision Report

## 📋 **EXECUTIVE SUMMARY**
- **Project**: {self.project_name}
- **Models Verified**: {len(models)} models confirmed available
- **Assets Generated**: {len(files)} files successfully created
- **Generation Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🎨 **VISUAL SAMPLES READY FOR REVIEW**

"""
        
        approach_letters = ['A', 'B', 'C']
        for i, model_id in enumerate(models):
            if model_id in results:
                result = results[model_id]
                letter = approach_letters[i] if i < len(approach_letters) else str(i+1)
                
                report_content += f"""### **Approach {letter}: {model_id}**
**Directory**: `{result.get('approach_directory', 'N/A')}`
**Files Generated**: {len(result.get('local_paths', []))}

**Asset Files:**
"""
                
                for file_path in result.get('local_paths', []):
                    filename = Path(file_path).name
                    report_content += f"- **{filename}**: `{file_path}`\n"
                
                report_content += "\n"
        
        report_content += f"""
## 🎯 **CEO DECISION REQUIRED**

**Please review the visual samples above and select your preferred approach:**

- [ ] **Approach A**: {models[0] if len(models) > 0 else 'N/A'}
- [ ] **Approach B**: {models[1] if len(models) > 1 else 'N/A'}  
- [ ] **Approach C**: {models[2] if len(models) > 2 else 'N/A'}

## 📁 **All Generated Files**
{len(files)} total files verified and ready:

"""
        
        for file_path in files:
            report_content += f"- `{file_path}`\n"
        
        report_content += f"""
## 🔒 **NEXT STEPS**
1. **Review Visual Samples**: Open the file paths above to view your {self.project_name} assets
2. **Make CEO Decision**: Select Approach A, B, or C based on visual preference  
3. **Style Locking**: Selected model parameters will be locked for consistency
4. **Asset Generation**: All future assets will use your selected model

**{self.project_name} game will have 100% visual consistency using your selected model!** 🎮✨
"""
        
        # Write report to file
        with open(report_path, 'w') as f:
            f.write(report_content)
        
        return {
            "success": True,
            "report_path": str(report_path),
            "message": f"CEO report created: {report_path}"
        }

async def main():
    """CLI interface for verified art direction agent."""
    if len(sys.argv) < 4:
        print("🎨 Verified Art Direction Agent")
        print("\nUsage:")
        print("  python verified_art_direction_agent.py <project_name> <model_id1> <model_id2> [model_id3]")
        print("\nExample:")
        print("  python verified_art_direction_agent.py FlappyBird model_123 model_456 model_789")
        return
    
    project_name = sys.argv[1]
    model_ids = sys.argv[2:]
    
    # Define Flappy Bird game context
    game_context = {
        "main_character_prompt": "cute cartoon bird character, side view, yellow bird with small wings, flappy bird style",
        "environment_prompt": "green pipe obstacle, vertical pipe, simple geometric, game environment",
        "ui_prompt": "score number display, game UI, clean simple design",
        "object_prompt": "fluffy white cloud, sky background element, cartoon style"
    }
    
    agent = VerifiedArtDirectionAgent(project_name)
    result = await agent.verify_and_generate_art_approaches(model_ids, game_context)
    
    print(json.dumps({
        "success": result["success"],
        "message": result["message"],
        "total_files": result.get("total_files_generated", 0),
        "ceo_report": result.get("ceo_report_path"),
        "verified_files": len(result.get("verified_file_paths", []))
    }, indent=2))

if __name__ == "__main__":
    asyncio.run(main())