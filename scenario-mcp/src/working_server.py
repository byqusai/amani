#!/usr/bin/env python3
"""Working Scenario MCP Server - Fixed Context Issues"""

import asyncio
import aiohttp
import base64
import structlog
from typing import Dict, Any, Optional
from fastmcp import FastMCP, Context

# Simple, clean server without problematic lifespan
mcp = FastMCP("ScenarioMCP")

# Configure basic logging
logger = structlog.get_logger(__name__)

@mcp.tool()
async def scenario_test_connection() -> Dict[str, Any]:
    """Test Scenario API connection - No Context to avoid issues."""
    try:
        # Import config inside function to avoid initialization issues
        import sys
        import os
        sys.path.insert(0, os.path.dirname(__file__))
        from config import config
        
        credentials = f"{config.scenario_api_key}:{config.scenario_api_secret}"
        auth_header = base64.b64encode(credentials.encode()).decode()
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/json"
            }
            
            async with session.get(f"{config.scenario_api_base_url}/models", headers=headers, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "message": "✅ Scenario API connection successful!",
                        "data": {
                            "status_code": response.status,
                            "models_available": len(data.get("models", [])) if isinstance(data, dict) else "unknown",
                            "api_base": config.scenario_api_base_url
                        }
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "message": f"❌ API connection failed: HTTP {response.status}",
                        "data": {"status_code": response.status, "error": error_text}
                    }
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error testing connection: {str(e)}",
            "data": {"error": str(e), "error_type": type(e).__name__}
        }

@mcp.tool()
async def scenario_simple_generate(
    prompt: str,
    model_id: str = "flux.1-dev",
    width: int = 1024,
    height: int = 1024,
    num_samples: int = 1
) -> Dict[str, Any]:
    """Simple text-to-image generation using Scenario API."""
    try:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(__file__))
        from config import config
        
        credentials = f"{config.scenario_api_key}:{config.scenario_api_secret}"
        auth_header = base64.b64encode(credentials.encode()).decode()
        
        payload = {
            "prompt": prompt,
            "modelId": model_id,
            "width": width,
            "height": height,
            "numImages": num_samples,
            "numInferenceSteps": 28,
            "guidance": 3.5
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
                timeout=30
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "message": f"✅ Generation started successfully!",
                        "data": {
                            "job_id": data.get("inference", {}).get("id"),
                            "status": "started",
                            "prompt": prompt,
                            "model_id": model_id,
                            "dimensions": f"{width}x{height}",
                            "samples": num_samples,
                            "full_response": data
                        }
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "message": f"❌ Generation failed: HTTP {response.status}",
                        "data": {"status_code": response.status, "error": error_text}
                    }
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error during generation: {str(e)}",
            "data": {"error": str(e), "error_type": type(e).__name__}
        }

@mcp.tool()
async def scenario_get_models() -> Dict[str, Any]:
    """Get available Scenario AI models."""
    try:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(__file__))
        from config import config
        
        credentials = f"{config.scenario_api_key}:{config.scenario_api_secret}"
        auth_header = base64.b64encode(credentials.encode()).decode()
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/json"
            }
            
            async with session.get(f"{config.scenario_api_base_url}/models", headers=headers, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    models = data.get("models", [])
                    
                    # Format model data for easy use
                    formatted_models = []
                    for model in models[:10]:  # Limit to first 10 for brevity
                        formatted_models.append({
                            "id": model.get("id", ""),
                            "name": model.get("name", ""),
                            "description": model.get("description", ""),
                            "category": model.get("category", ""),
                            "supports_3d": model.get("supports3D", False),
                            "supports_video": model.get("supportsVideo", False)
                        })
                    
                    return {
                        "success": True,
                        "message": f"✅ Retrieved {len(models)} available models",
                        "data": {
                            "total_models": len(models),
                            "sample_models": formatted_models,
                            "recommended": ["flux.1-dev", "stable-diffusion-xl", "midjourney-v6"]
                        }
                    }
                else:
                    return {
                        "success": False,
                        "message": f"❌ Failed to get models: HTTP {response.status}",
                        "data": {"status_code": response.status}
                    }
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error getting models: {str(e)}",
            "data": {"error": str(e)}
        }

if __name__ == "__main__":
    logger.info("🎨 Starting Working Scenario MCP Server...")
    mcp.run()