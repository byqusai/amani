#!/usr/bin/env python3
"""Minimal MCP Server using official MCP SDK - Avoiding FastMCP Context issues"""

import asyncio
import aiohttp
import base64
import logging
from typing import Any, Dict
from mcp.server import Server, Context
from mcp.server.session import ServerSession
from mcp.server.stdio import stdio_server
from mcp.types import ClientCapabilities, ServerCapabilities, TextContent, Tool, CallToolResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server instance
server = Server("ScenarioMCP")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="scenario_test_connection",
            description="Test connection to Scenario API",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="scenario_simple_generate", 
            description="Generate images using Scenario AI",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Text prompt for image generation"},
                    "model_id": {"type": "string", "description": "Model ID to use", "default": "flux.1-dev"},
                    "width": {"type": "integer", "description": "Image width", "default": 1024},
                    "height": {"type": "integer", "description": "Image height", "default": 1024}
                },
                "required": ["prompt"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls."""
    try:
        if name == "scenario_test_connection":
            return await handle_test_connection()
        elif name == "scenario_simple_generate":
            return await handle_simple_generate(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        logger.error(f"Tool {name} failed: {str(e)}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")],
            is_error=True
        )

async def handle_test_connection() -> CallToolResult:
    """Test Scenario API connection."""
    try:
        # Load config
        import os
        from dotenv import load_dotenv
        
        # Load environment from scenario-mcp directory
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        load_dotenv(env_path)
        
        api_key = os.getenv("SCENARIO_API_KEY")
        api_secret = os.getenv("SCENARIO_API_SECRET") 
        api_base_url = os.getenv("SCENARIO_API_BASE_URL", "https://api.cloud.scenario.com/v1")
        
        if not api_key or not api_secret:
            return CallToolResult(
                content=[TextContent(type="text", text="❌ Scenario API credentials not configured")],
                is_error=True
            )
        
        credentials = f"{api_key}:{api_secret}"
        auth_header = base64.b64encode(credentials.encode()).decode()
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/json"
            }
            
            async with session.get(f"{api_base_url}/models", headers=headers, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    models_count = len(data.get("models", [])) if isinstance(data, dict) else "unknown"
                    result_text = f"✅ Scenario API connection successful!\nStatus: {response.status}\nModels available: {models_count}\nAPI Base: {api_base_url}"
                    
                    return CallToolResult(
                        content=[TextContent(type="text", text=result_text)]
                    )
                else:
                    error_text = await response.text()
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"❌ API connection failed: HTTP {response.status}\nError: {error_text}")],
                        is_error=True
                    )
                    
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"❌ Connection test failed: {str(e)}")],
            is_error=True
        )

async def handle_simple_generate(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle image generation."""
    try:
        prompt = arguments.get("prompt", "")
        model_id = arguments.get("model_id", "flux.1-dev")
        width = arguments.get("width", 1024)
        height = arguments.get("height", 1024)
        
        if not prompt:
            return CallToolResult(
                content=[TextContent(type="text", text="❌ Prompt is required for image generation")],
                is_error=True
            )
        
        # Load config
        import os
        from dotenv import load_dotenv
        
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        load_dotenv(env_path)
        
        api_key = os.getenv("SCENARIO_API_KEY")
        api_secret = os.getenv("SCENARIO_API_SECRET")
        api_base_url = os.getenv("SCENARIO_API_BASE_URL", "https://api.cloud.scenario.com/v1")
        
        if not api_key or not api_secret:
            return CallToolResult(
                content=[TextContent(type="text", text="❌ Scenario API credentials not configured")],
                is_error=True
            )
        
        credentials = f"{api_key}:{api_secret}"
        auth_header = base64.b64encode(credentials.encode()).decode()
        
        payload = {
            "prompt": prompt,
            "modelId": model_id,
            "width": width,
            "height": height,
            "numImages": 1,
            "numInferenceSteps": 28,
            "guidance": 3.5
        }
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/json"
            }
            
            async with session.post(
                f"{api_base_url}/generate/txt2img",
                json=payload,
                headers=headers,
                timeout=30
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    job_id = data.get("inference", {}).get("id", "unknown")
                    
                    result_text = f"✅ Image generation started successfully!\nJob ID: {job_id}\nPrompt: {prompt}\nModel: {model_id}\nDimensions: {width}x{height}\nStatus: Generation in progress..."
                    
                    return CallToolResult(
                        content=[TextContent(type="text", text=result_text)]
                    )
                else:
                    error_text = await response.text()
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"❌ Generation failed: HTTP {response.status}\nError: {error_text}")],
                        is_error=True
                    )
                    
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"❌ Generation failed: {str(e)}")],
            is_error=True
        )

async def main():
    """Run the MCP server."""
    logger.info("🎨 Starting Minimal Scenario MCP Server...")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            ServerCapabilities(),
            ClientCapabilities()
        )

if __name__ == "__main__":
    asyncio.run(main())