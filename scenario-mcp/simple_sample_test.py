#!/usr/bin/env python3
"""
Simple test to generate one sample and verify the system works
"""

import asyncio
import sys
from pathlib import Path

sys.path.append('.')
from core.enhanced_scenario_client import EnhancedScenarioClient

async def test_generation():
    client = EnhancedScenarioClient(debug=True)
    
    # Test connection first
    connection_result = await client.test_connection_with_diagnostics()
    if not connection_result["success"]:
        print(f"❌ Connection failed: {connection_result['message']}")
        return
        
    print(f"✅ Connected! Using model: {connection_result['recommended_model']}")
    
    # Create test directory
    test_dir = Path("/Users/qusaiabushanap/dev/amani/Assets/Generated/ArtDirection/test_samples")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate one test sample
    prompt = "Saudi Arabian falcon bird, game character, side view, transparent background"
    model_id = connection_result["recommended_model"]
    
    print(f"🎨 Generating test sample...")
    print(f"Prompt: {prompt}")
    print(f"Model: {model_id}")
    
    try:
        result = await client.generate_and_download_with_validation(
            prompt=prompt,
            model_id=model_id,
            download_dir=str(test_dir),
            width=512,
            height=512,
            num_samples=1
        )
        
        if result["success"]:
            print(f"✅ SUCCESS! Generated: {result.get('local_paths', ['No paths'])}")
            return result
        else:
            print(f"❌ FAILED: {result.get('message', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return None

if __name__ == "__main__":
    result = asyncio.run(test_generation())