#!/usr/bin/env python3
"""Direct API test for Scenario.gg with Saudi Falcon assets"""

import os
import sys
import base64
import requests
import json
import time
from pathlib import Path

# Load environment variables from scenario-mcp
scenario_dir = Path(__file__).parent.parent / "scenario-mcp"
env_file = scenario_dir / ".env"

if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

# API Configuration
API_KEY = os.getenv("SCENARIO_API_KEY")
API_SECRET = os.getenv("SCENARIO_API_SECRET")
BASE_URL = "https://api.cloud.scenario.com/v1"

if not API_KEY or not API_SECRET:
    print("❌ API credentials not found in .env file")
    sys.exit(1)

# Create authorization header
auth_header = base64.b64encode(f"{API_KEY}:{API_SECRET}".encode()).decode()
headers = {
    "Authorization": f"Basic {auth_header}",
    "Content-Type": "application/json"
}

def test_single_generation():
    """Test single image generation directly through API."""
    
    # Generation payload
    payload = {
        "prompt": "Saudi peregrine falcon with traditional falconry bells, detailed feathers, transparent background, game asset",
        "modelId": "model_k9vXd76ZEJtJBRM8DaEwYkQN",
        "width": 512,
        "height": 512,
        "numSamples": 1,
        "numInferenceSteps": 30,
        "guidance": 7.0
    }
    
    print("🎮 SAUDI FALCON FLAPPY BIRD - Direct API Test")
    print(f"📱 Model ID: {payload['modelId']}")
    print(f"🔒 Parameters: {payload}")
    print("=" * 60)
    
    try:
        # Start generation
        print("🎨 Starting generation request...")
        response = requests.post(
            f"{BASE_URL}/generate/txt2img",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📋 API Response: {json.dumps(result, indent=2)}")
            
            job_id = result.get("job", {}).get("jobId")
            if not job_id:
                # Try alternative response structure
                job_id = result.get("id") or result.get("jobId")
            
            if job_id:
                print(f"✅ Job started: {job_id}")
                
                # Poll for completion
                max_attempts = 30
                for attempt in range(max_attempts):
                    print(f"⏳ Checking status... ({attempt + 1}/{max_attempts})")
                    
                    status_response = requests.get(
                        f"{BASE_URL}/jobs/{job_id}",
                        headers=headers,
                        timeout=30
                    )
                    
                    if status_response.status_code == 200:
                        job_data = status_response.json()
                        status = job_data.get("job", {}).get("status")
                        
                        print(f"📊 Status: {status}")
                        
                        if status == "completed":
                            assets = job_data.get("job", {}).get("assets", [])
                            if assets:
                                asset_url = assets[0].get("url")
                                if asset_url:
                                    print(f"✅ Generation completed!")
                                    print(f"🖼️ Asset URL: {asset_url}")
                                    
                                    # Download the asset
                                    output_dir = Path("/Users/qusaiabushanap/dev/amani/Assets/Generated/ArtDirection/Model_A_k9vXd76ZEJtJBRM8DaEwYkQN")
                                    output_dir.mkdir(parents=True, exist_ok=True)
                                    
                                    asset_response = requests.get(asset_url, timeout=60)
                                    if asset_response.status_code == 200:
                                        file_path = output_dir / "main_character_falcon_test.png"
                                        with open(file_path, 'wb') as f:
                                            f.write(asset_response.content)
                                        
                                        print(f"📱 Downloaded: {file_path}")
                                        
                                        if file_path.exists() and file_path.stat().st_size > 0:
                                            print("✅ SUCCESS: Saudi Falcon asset generated and downloaded!")
                                            return str(file_path)
                                        else:
                                            print("❌ Downloaded file is empty or corrupted")
                                    else:
                                        print(f"❌ Failed to download asset: HTTP {asset_response.status_code}")
                                else:
                                    print("❌ No asset URL found in completed job")
                            else:
                                print("❌ No assets found in completed job")
                            break
                        elif status == "failed":
                            error = job_data.get("job", {}).get("error", "Unknown error")
                            print(f"❌ Generation failed: {error}")
                            break
                        else:
                            time.sleep(10)  # Wait before next check
                    else:
                        print(f"❌ Status check failed: HTTP {status_response.status_code}")
                        break
                
                if attempt == max_attempts - 1:
                    print("⏱️ Timeout waiting for generation to complete")
                    
            else:
                print("❌ No job ID returned from generation request")
        else:
            print(f"❌ Generation request failed: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception during generation: {str(e)}")
        return None

if __name__ == "__main__":
    result = test_single_generation()
    if result:
        print(f"\n🏁 FINAL RESULT: {result}")
    else:
        print("\n❌ Generation failed")