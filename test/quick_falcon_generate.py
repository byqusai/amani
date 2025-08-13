#!/usr/bin/env python3
"""Quick Saudi Falcon asset generation with timeout handling"""

import sys
import os
import asyncio
import json
from pathlib import Path

# Add the scenario-mcp directory to Python path
scenario_dir = Path(__file__).parent.parent / "scenario-mcp"
sys.path.insert(0, str(scenario_dir))

from core.enhanced_scenario_client import EnhancedScenarioClient

async def quick_generate():
    client = EnhancedScenarioClient(debug=True)
    
    # Test single asset generation
    print("🎮 Testing single Saudi Falcon asset generation...")
    
    result = await client.generate_and_download_with_validation(
        prompt="Saudi peregrine falcon with traditional falconry bells, detailed feathers, transparent background, game asset",
        model_id="model_k9vXd76ZEJtJBRM8DaEwYkQN",
        width=512,
        height=512,
        num_inference_steps=30,
        guidance=7.0,
        download_dir="/Users/qusaiabushanap/dev/amani/Assets/Generated/ArtDirection/Model_A_k9vXd76ZEJtJBRM8DaEwYkQN"
    )
    
    print(f"Result: {result}")
    
    if result.get('success'):
        print(f"✅ Generated: {result.get('local_file_path')}")
        return result.get('local_file_path')
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
        return None

if __name__ == "__main__":
    asyncio.run(quick_generate())