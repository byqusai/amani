#!/usr/bin/env python3
"""Check job status for Saudi Falcon asset generation"""

import os
import base64
import requests
import json
import time
from pathlib import Path

# Load environment
scenario_dir = Path(__file__).parent.parent / "scenario-mcp"
env_file = scenario_dir / ".env"

if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

API_KEY = os.getenv("SCENARIO_API_KEY")
API_SECRET = os.getenv("SCENARIO_API_SECRET")
BASE_URL = "https://api.cloud.scenario.com/v1"

auth_header = base64.b64encode(f"{API_KEY}:{API_SECRET}".encode()).decode()
headers = {
    "Authorization": f"Basic {auth_header}",
    "Content-Type": "application/json"
}

def check_recent_jobs():
    """Check status of recent generation jobs."""
    print("🔍 Checking recent job statuses...")
    
    try:
        response = requests.get(f"{BASE_URL}/jobs", headers=headers, timeout=30)
        
        if response.status_code == 200:
            jobs_data = response.json()
            jobs = jobs_data.get("jobs", [])
            
            print(f"📊 Found {len(jobs)} recent jobs")
            
            for job in jobs[:5]:
                job_id = job.get("jobId")
                status = job.get("status")
                created = job.get("createdAt", "")
                
                print(f"\n🔸 Job: {job_id}")
                print(f"   Status: {status}")
                print(f"   Created: {created}")
                
                if status in ["completed", "success"]:
                    print(f"   ✅ Job completed! Checking assets...")
                    
                    job_detail_response = requests.get(f"{BASE_URL}/jobs/{job_id}", headers=headers)
                    if job_detail_response.status_code == 200:
                        job_detail = job_detail_response.json()
                        print(f"   📋 Job Detail Structure: {json.dumps(job_detail, indent=2)[:500]}...")
                        
                        # Try different possible asset locations
                        assets = (job_detail.get("job", {}).get("assets", []) or 
                                 job_detail.get("assets", []) or
                                 job_detail.get("inference", {}).get("images", []))
                        
                        if assets:
                            print(f"   🖼️  Found {len(assets)} assets:")
                            for i, asset in enumerate(assets):
                                asset_url = asset.get("url")
                                if asset_url:
                                    print(f"      Asset {i+1}: {asset_url}")
                                    
                                    output_dir = Path("/Users/qusaiabushanap/dev/amani/Assets/Generated/ArtDirection/Model_A_k9vXd76ZEJtJBRM8DaEwYkQN")
                                    output_dir.mkdir(parents=True, exist_ok=True)
                                    
                                    try:
                                        asset_response = requests.get(asset_url, timeout=60)
                                        if asset_response.status_code == 200:
                                            file_path = output_dir / f"saudi_falcon_asset_{job_id}_{i+1}.png"
                                            with open(file_path, 'wb') as f:
                                                f.write(asset_response.content)
                                            
                                            if file_path.exists() and file_path.stat().st_size > 0:
                                                print(f"      ✅ Downloaded: {file_path}")
                                                return str(file_path)
                                            else:
                                                print(f"      ❌ Download failed or empty file")
                                        else:
                                            print(f"      ❌ Asset download failed: HTTP {asset_response.status_code}")
                                    except Exception as e:
                                        print(f"      ❌ Download error: {str(e)}")
                        else:
                            print(f"   ❌ No assets found in completed job")
                elif status == "failed":
                    error = job.get("error", "Unknown error")
                    print(f"   ❌ Job failed: {error}")
                elif status in ["queued", "processing"]:
                    print(f"   ⏳ Job still in progress...")
        else:
            print(f"❌ Failed to get jobs list: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking jobs: {str(e)}")
    
    return None

if __name__ == "__main__":
    result = check_recent_jobs()
    if result:
        print(f"\n🏁 SUCCESS: Downloaded Saudi Falcon asset to {result}")
    else:
        print(f"\n⏳ No completed assets found yet. Jobs may still be processing.")