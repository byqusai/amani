#!/usr/bin/env python3
"""Test Scenario API connection and authentication."""

import sys
import os
import asyncio
import aiohttp

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_scenario_api():
    """Test the Scenario API connection."""
    try:
        from config import config
        print("✅ Config loaded successfully")
        print(f"   API Key: {config.scenario_api_key[:20]}...")
        print(f"   API Secret: {config.scenario_api_secret[:10]}...")
        print(f"   Base URL: {config.scenario_api_base_url}")
        
        # Test API authentication
        import base64
        credentials = f"{config.scenario_api_key}:{config.scenario_api_secret}"
        auth_header = base64.b64encode(credentials.encode()).decode()
        
        print("\n🔍 Testing API connection...")
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/json"
            }
            
            # Test with a simple API endpoint (like getting user info or models)
            test_url = f"{config.scenario_api_base_url}/models"
            
            try:
                async with session.get(test_url, headers=headers, timeout=10) as response:
                    print(f"   Status: {response.status}")
                    
                    if response.status == 200:
                        data = await response.json()
                        print("✅ API connection successful!")
                        print(f"   Response type: {type(data)}")
                        if isinstance(data, dict):
                            print(f"   Keys: {list(data.keys())[:5]}...")
                        elif isinstance(data, list):
                            print(f"   Items count: {len(data)}")
                        return True
                    elif response.status == 401:
                        print("❌ Authentication failed - check your API credentials")
                        print("   Make sure your API key and secret are correct")
                        return False
                    elif response.status == 403:
                        print("❌ Forbidden - your API key may not have sufficient permissions")
                        return False
                    else:
                        text = await response.text()
                        print(f"❌ API request failed: {response.status}")
                        print(f"   Response: {text[:200]}...")
                        return False
                        
            except asyncio.TimeoutError:
                print("❌ API request timed out - check your internet connection")
                return False
            except aiohttp.ClientError as e:
                print(f"❌ Network error: {e}")
                return False
    
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function."""
    print("🧪 Testing Scenario API Connection...")
    print("=" * 50)
    
    success = await test_scenario_api()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Scenario API test PASSED!")
        print("✅ Your MCP server is ready for Claude Code integration")
    else:
        print("⚠️  Scenario API test FAILED!")
        print("   Please check your API credentials in .env file")
        print("   Visit https://docs.scenario.com to verify your API setup")

if __name__ == "__main__":
    asyncio.run(main())