#!/usr/bin/env python3
"""Minimal MCP server test for debugging Context issues."""

from fastmcp import FastMCP, Context
from typing import Dict, Any

# Create minimal server
mcp = FastMCP("TestServer")

@mcp.tool()
async def test_tool(ctx: Context) -> Dict[str, Any]:
    """Test tool to check Context object."""
    try:
        # Test basic context access
        request_id = ctx.request_id
        return {
            "success": True,
            "message": "✅ Context access works!",
            "data": {
                "request_id": request_id,
                "context_type": str(type(ctx))
            }
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Context error: {str(e)}",
            "data": {"error": str(e), "error_type": type(e).__name__}
        }

if __name__ == "__main__":
    mcp.run()