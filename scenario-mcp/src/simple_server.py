#!/usr/bin/env python3
"""Simplified Scenario MCP Server for testing."""

import asyncio
import sys
import os
import structlog
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Any
from mcp.server.fastmcp import FastMCP, Context

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import basic config
from config import config

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.dev.ConsoleRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Server lifecycle management."""
    logger.info("🎨 Scenario MCP Server starting up...")
    logger.info(f"   API Base URL: {config.scenario_api_base_url}")
    logger.info(f"   API Key configured: {'Yes' if config.scenario_api_key else 'No'}")
    
    context = {
        "scenario_client": None,
        "config": config
    }
    
    yield context
    
    logger.info("🎨 Scenario MCP Server shutting down...")

# Create FastMCP server without lifespan for debugging
mcp = FastMCP("ScenarioMCP")

@mcp.tool()
async def hello_world() -> Dict[str, Any]:
    """Simple hello world test."""
    return {
        "success": True,
        "message": "✅ Hello from Scenario MCP!",
        "data": {"server": "working"}
    }

@mcp.tool()
async def scenario_test_connection() -> Dict[str, Any]:
    """Test Scenario API connection."""
    try:
        import aiohttp
        import base64
        
        # Access config directly from the global instance
        from config import config
        credentials = f"{config.scenario_api_key}:{config.scenario_api_secret}"
        auth_header = base64.b64encode(credentials.encode()).decode()
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/json"
            }
            
            async with session.get(f"{config.scenario_api_base_url}/models", headers=headers, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "message": "✅ Scenario API connection successful!",
                        "data": {
                            "status_code": response.status,
                            "models_available": len(data.get("models", [])) if isinstance(data, dict) else "unknown"
                        }
                    }
                else:
                    return {
                        "success": False,
                        "message": f"❌ API connection failed: {response.status}",
                        "data": {"status_code": response.status}
                    }
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error testing connection: {str(e)}",
            "data": {"error": str(e)}
        }

@mcp.tool()
async def scenario_simple_generate(
    ctx: Context,
    prompt: str,
    model_id: str = "flux.1-dev",
    width: int = 1024,
    height: int = 1024
) -> Dict[str, Any]:
    """Simple text-to-image generation."""
    try:
        import aiohttp
        import base64
        
        # Access config directly from the global instance
        from config import config
        credentials = f"{config.scenario_api_key}:{config.scenario_api_secret}"
        auth_header = base64.b64encode(credentials.encode()).decode()
        
        payload = {
            "prompt": prompt,
            "modelId": model_id,
            "width": width,
            "height": height,
            "numImages": 1
        }
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/json"
            }
            
            async with session.post(
                f"{config.scenario_api_base_url}/generate/txt2img",
                json=payload,
                headers=headers,
                timeout=10
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "message": f"✅ Generation started for: {prompt}",
                        "data": data
                    }
                else:
                    text = await response.text()
                    return {
                        "success": False,
                        "message": f"❌ Generation failed: {response.status}",
                        "data": {"status_code": response.status, "error": text}
                    }
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error during generation: {str(e)}",
            "data": {"error": str(e)}
        }

def main():
    """Run the simplified MCP server."""
    logger.info("🚀 Starting Simplified Scenario MCP Server...")
    mcp.run()

if __name__ == "__main__":
    main()