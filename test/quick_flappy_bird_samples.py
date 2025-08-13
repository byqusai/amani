#!/usr/bin/env python3
"""
Quick Flappy Bird sample generation for CEO art direction review.
Uses simplified approach with direct API calls.
"""
import asyncio
import sys
import os
import json
import time
from pathlib import Path

# Add scenario-mcp to path
sys.path.append('/Users/qusaiabushanap/dev/amani/scenario-mcp')

from core.enhanced_scenario_client import EnhancedScenarioClient

async def quick_flappy_bird_test():
    """Quick test to generate Flappy Bird samples"""
    
    print("🚀 Quick Flappy Bird Art Direction Test")
    
    # Initialize client
    client = EnhancedScenarioClient()
    
    # Test connection first
    print("🔌 Testing connection...")
    connection_test = await client.test_connection_with_diagnostics()
    
    if not connection_test.get("success"):
        print("❌ Connection failed")
        return
    
    print(f"✅ Connection successful! Found {len(connection_test.get('models', []))} models")
    
    # Get available models
    models = connection_test.get("models", [])
    if not models:
        print("❌ No models available")
        return
    
    # Create output directory
    output_dir = Path("/Users/qusaiabushanap/dev/amani/Assets/Generated/ArtDirection/FlappyWings_Quick_Test")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Test generation with first available model
    model = models[0]
    model_id = model["id"]
    model_name = model.get("name", "Unknown")
    
    print(f"🎨 Testing generation with model: {model_name} ({model_id})")
    
    # Simple Flappy Bird prompt
    prompt = "cartoon bird character for flappy bird game, side view, wings spread, colorful, simple design, game sprite"
    
    try:
        print("🎮 Generating Flappy Bird character...")
        
        result = await client.generate_and_download_with_validation(
            prompt=prompt,
            model_id=model_id,
            download_dir=str(output_dir),
            width=512,
            height=512,
            num_inference_steps=20,  # Faster for testing
            guidance=7.0
        )
        
        if result.get("success"):
            print(f"✅ Generation successful!")
            
            if result.get("downloaded_files"):
                downloaded_files = result["downloaded_files"]
                print(f"📁 Downloaded {len(downloaded_files)} files:")
                for file_path in downloaded_files:
                    print(f"   {file_path}")
                
                # Create simple CEO report
                report = {
                    "project": "Flappy Wings - Quick Test",
                    "model_used": {"id": model_id, "name": model_name},
                    "prompt": prompt,
                    "generated_files": downloaded_files,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "success": True
                }
                
                report_path = output_dir / "quick_test_report.json"
                with open(report_path, 'w') as f:
                    json.dump(report, f, indent=2)
                
                print(f"\n🎯 QUICK TEST RESULTS:")
                print(f"Model: {model_name}")
                print(f"Generated Files: {len(downloaded_files)}")
                print(f"Output Directory: {output_dir}")
                print(f"Report: {report_path}")
                
                return True
            else:
                print("❌ No files downloaded")
        else:
            print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error during generation: {str(e)}")
    
    return False

if __name__ == "__main__":
    success = asyncio.run(quick_flappy_bird_test())
    if success:
        print("\n✅ Quick test completed successfully!")
    else:
        print("\n❌ Quick test failed")