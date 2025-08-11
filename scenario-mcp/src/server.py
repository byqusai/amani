"""Main Scenario MCP Server with FastMCP."""

import asyncio
import structlog
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Any
import signal
import sys

from mcp.server.fastmcp import FastMCP, Context

from .config import config
from .utils.auth import AuthenticationManager
from .scenario_client import ScenarioAPIClient
from .tools import register_all_tools
from .exceptions import ScenarioMCPError

# Configure logging
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.ConsoleRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Handle server startup and shutdown."""
    logger.info("🎨 Scenario MCP Server starting up...")
    
    # Initialize components
    auth_manager = None
    scenario_client = None
    
    try:
        # Validate configuration
        config.validate()
        logger.info("✅ Configuration validated")
        
        # Initialize authentication
        auth_manager = AuthenticationManager(config)
        await auth_manager.validate_credentials()
        logger.info("✅ Scenario API credentials validated")
        
        # Initialize Scenario client
        scenario_client = ScenarioAPIClient()
        await scenario_client.initialize()
        logger.info("✅ Scenario API client initialized")
        
        # Store in context for tools to access
        context = {
            "auth_manager": auth_manager,
            "scenario_client": scenario_client,
            "config": config
        }
        
        logger.info("🚀 Scenario MCP Server ready! Available capabilities:")
        logger.info("   • Text-to-Image Generation (2D)")
        logger.info("   • Image-to-Image Generation")
        logger.info("   • ControlNet (Pose, Depth, Canny)")
        logger.info("   • 3D Model Generation")
        logger.info("   • Video Generation")
        logger.info("   • Batch Processing")
        logger.info("   • Model Management")
        logger.info("   • Asset Organization")
        logger.info("   • Cost Estimation")
        
        yield context
        
    except Exception as e:
        logger.error(f"❌ Failed to start Scenario MCP Server: {str(e)}")
        raise
    
    finally:
        # Cleanup resources
        logger.info("🧹 Cleaning up Scenario MCP Server...")
        
        if scenario_client:
            try:
                await scenario_client.close()
                logger.info("✅ Scenario API client closed")
            except Exception as e:
                logger.error(f"Error closing Scenario client: {str(e)}")
        
        if auth_manager:
            try:
                await auth_manager.close()
                logger.info("✅ Authentication manager closed")
            except Exception as e:
                logger.error(f"Error closing auth manager: {str(e)}")
        
        logger.info("👋 Scenario MCP Server shut down")


# Initialize MCP server
mcp = FastMCP(
    "scenario-mcp-server",
    description="Scenario.gg AI Asset Generation via Model Context Protocol - Perfect for Agent 4 workflows",
    lifespan=server_lifespan
)

# Register all tools
register_all_tools(mcp)


@mcp.middleware()
async def request_logging_middleware(request, call_next):
    """Log all requests for debugging and monitoring."""
    tool_name = request.get("method", "unknown_tool")
    
    # Extract prompt from params for better logging
    params = request.get("params", {})
    prompt_preview = ""
    if "prompt" in params:
        prompt = params["prompt"]
        prompt_preview = f" - '{prompt[:50]}...'" if len(prompt) > 50 else f" - '{prompt}'"
    
    logger.info(f"🔧 Tool called: {tool_name}{prompt_preview}")
    
    try:
        response = await call_next(request)
        
        # Log success/failure
        if isinstance(response, dict) and response.get("success"):
            logger.info(f"✅ Tool completed: {tool_name}")
        else:
            logger.warning(f"⚠️ Tool had issues: {tool_name}")
        
        return response
    
    except Exception as e:
        logger.error(f"❌ Tool failed: {tool_name} - {str(e)}")
        raise


def handle_shutdown(signum, frame):
    """Handle graceful shutdown."""
    logger.info(f"🛑 Received shutdown signal {signum}")
    sys.exit(0)


if __name__ == "__main__":
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    
    logger.info("🎨 Starting Scenario MCP Server...")
    logger.info("   Author: Qusai Saleem (hi@qusai.org)")
    logger.info("   Purpose: AI-Powered Asset Generation for Game Development")
    logger.info("   Integration: Perfect for AI Game Studio Agent 4")
    
    try:
        # Run the MCP server
        mcp.run()
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server failed: {str(e)}")
        sys.exit(1)