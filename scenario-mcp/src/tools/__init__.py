"""MCP tools for Scenario API integration."""

from tools.text_to_image import register_text_to_image_tools
from tools.image_to_image import register_image_to_image_tools
from tools.controlnet import register_controlnet_tools
from tools.video_generation import register_video_tools
from tools.threed_generation import register_3d_tools
from tools.model_management import register_model_tools
from tools.asset_management import register_asset_management_tools
from tools.batch_operations import register_batch_tools


def register_all_tools(mcp):
    """Register all Scenario MCP tools."""
    register_text_to_image_tools(mcp)
    register_image_to_image_tools(mcp)
    register_controlnet_tools(mcp)
    register_video_tools(mcp)
    register_3d_tools(mcp)
    register_model_tools(mcp)
    register_asset_management_tools(mcp)
    register_batch_tools(mcp)