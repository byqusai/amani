#!/usr/bin/env python3
"""Basic test for Scenario MCP Server imports."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from config import config
    print("✅ Config imported successfully")
    print(f"   API Base URL: {config.scenario_api_base_url}")
    print(f"   API Key configured: {'Yes' if config.scenario_api_key else 'No'}")
    
    print("\n✅ Scenario MCP Server basic configuration is working!")
    print("🚀 Ready to start the MCP server")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)