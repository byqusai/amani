"""MCP tools for Scenario API integration."""

from .text_to_image import register_text_to_image_tools
from .image_to_image import register_image_to_image_tools
from .controlnet import register_controlnet_tools
from .video_generation import register_video_tools
from .threed_generation import register_3d_tools
from .model_management import register_model_tools
from .asset_management import register_asset_tools
from .batch_operations import register_batch_tools


def register_all_tools(mcp):
    """Register all Scenario MCP tools."""
    register_text_to_image_tools(mcp)
    register_image_to_image_tools(mcp)
    register_controlnet_tools(mcp)
    register_video_tools(mcp)
    register_3d_tools(mcp)
    register_model_tools(mcp)
    register_asset_tools(mcp)
    register_batch_tools(mcp)