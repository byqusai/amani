#!/usr/bin/env python3
"""
Generate Saudi Falcon (Saqr Al-Sahra) art direction samples
Simplified approach to create visual samples quickly
"""

import asyncio
import json
import os
import time
from pathlib import Path
from core.enhanced_scenario_client import EnhancedScenarioClient

async def generate_saqr_samples():
    """Generate visual samples for all 3 art approaches."""
    
    # Initialize client
    client = EnhancedScenarioClient(debug=True)
    
    # Create base directory
    base_dir = "/Users/qusaiabushanap/dev/amani/Assets/Generated/ArtDirection/saqr_al_sahra_samples"
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    
    # Get available models
    print("🔍 Getting available models...")
    connection_result = await client.test_connection_with_diagnostics()
    if not connection_result["success"]:
        print(f"❌ Connection failed: {connection_result['message']}")
        return
        
    available_models = connection_result["models"]
    model_id = available_models[0]["id"]  # Use first available model
    print(f"✅ Using model: {model_id}")
    
    # Define the 3 art approaches with specific assets
    approaches = {
        "approach_a_heritage_realism": {
            "name": "Saudi Heritage Realism",
            "assets": {
                "falcon_character": "realistic Saudi peregrine falcon with falconry bells, detailed feathers, authentic bird anatomy, desert lighting",
                "desert_environment": "authentic Arabian desert landscape, sand dunes, golden hour lighting, realistic desert atmosphere", 
                "ui_element": "traditional Arabic calligraphy style game UI button, elegant gold and brown colors, cultural motifs",
                "rock_obstacle": "sandstone rock formation, natural desert geology, realistic textures, weathered stone"
            }
        },
        "approach_b_stylized_arabian": {
            "name": "Stylized Arabian Adventure", 
            "assets": {
                "falcon_character": "cartoon style Saudi falcon, friendly appearance, vibrant colors, stylized falconry bells, appealing game character",
                "desert_environment": "colorful Arabian desert scene, stylized sand dunes, warm sunset colors, adventure game atmosphere",
                "ui_element": "colorful Arabic-inspired game button, playful design, warm desert colors, accessible styling",
                "rock_obstacle": "stylized desert rocks, smooth cartoon appearance, warm earth tones, friendly game obstacle"
            }
        },
        "approach_c_modern_minimalist": {
            "name": "Modern Saudi Minimalist",
            "assets": {
                "falcon_character": "minimalist falcon silhouette, clean geometric shapes, modern design, sophisticated simplicity",
                "desert_environment": "minimalist desert landscape, clean geometric dunes, modern color palette, elegant simplicity", 
                "ui_element": "modern minimalist UI button, Islamic geometric patterns, clean contemporary design, gold accent",
                "rock_obstacle": "geometric rock formation, minimalist style, clean shapes, modern design aesthetic"
            }
        }
    }
    
    # Generate samples for each approach
    all_results = {}
    
    for approach_key, approach_data in approaches.items():
        print(f"\n🎨 Generating samples for: {approach_data['name']}")
        approach_dir = f"{base_dir}/{approach_key}"
        Path(approach_dir).mkdir(parents=True, exist_ok=True)
        
        approach_results = {"name": approach_data["name"], "samples": {}}
        
        # Generate each asset type
        for asset_key, prompt in approach_data["assets"].items():
            print(f"  📝 Generating {asset_key}...")
            
            try:
                result = await client.generate_and_download_with_validation(
                    prompt=prompt + ", transparent background, game asset, high quality",
                    model_id=model_id,
                    width=512, height=512,
                    num_inference_steps=20,
                    guidance=7.0,
                    download_dir=approach_dir
                )
                
                if result["success"] and result.get("local_paths"):
                    file_path = result["local_paths"][0]
                    # Rename with descriptive name
                    new_path = f"{approach_dir}/{asset_key}.png"
                    if os.path.exists(file_path) and file_path != new_path:
                        os.rename(file_path, new_path)
                        file_path = new_path
                    
                    approach_results["samples"][asset_key] = {
                        "file_path": file_path,
                        "prompt": prompt,
                        "success": True
                    }
                    print(f"  ✅ Generated: {file_path}")
                else:
                    print(f"  ❌ Failed to generate {asset_key}: {result.get('message', 'Unknown error')}")
                    approach_results["samples"][asset_key] = {
                        "success": False,
                        "error": result.get("message", "Generation failed")
                    }
                
                # Small delay between generations
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"  ❌ Exception generating {asset_key}: {str(e)}")
                approach_results["samples"][asset_key] = {
                    "success": False,
                    "error": str(e)
                }
        
        all_results[approach_key] = approach_results
    
    # Save results summary
    results_file = f"{base_dir}/generation_results.json"
    with open(results_file, "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n📊 Results saved to: {results_file}")
    
    # Count successful generations
    total_generated = 0
    for approach in all_results.values():
        for sample in approach["samples"].values():
            if sample.get("success"):
                total_generated += 1
    
    print(f"\n🎉 SUMMARY: Generated {total_generated}/12 visual samples successfully!")
    
    # List all generated files
    print("\n📁 Generated Files:")
    for approach_key, approach_data in all_results.items():
        print(f"\n  {approach_data['name']}:")
        for asset_key, sample in approach_data["samples"].items():
            if sample.get("success"):
                print(f"    ✅ {asset_key}: {sample['file_path']}")
            else:
                print(f"    ❌ {asset_key}: {sample.get('error', 'Failed')}")
    
    return all_results

if __name__ == "__main__":
    print("🚀 Starting Saqr Al-Sahra Art Direction Sample Generation...")
    print("=" * 60)
    
    try:
        results = asyncio.run(generate_saqr_samples())
        print("\n✅ Art direction sample generation completed!")
    except Exception as e:
        print(f"\n❌ Generation failed with error: {str(e)}")
        import traceback
        traceback.print_exc()