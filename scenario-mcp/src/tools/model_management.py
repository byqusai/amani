"""Model management MCP tools."""

def register_model_tools(mcp):
    """Register model management tools."""
    
    @mcp.tool()
    async def scenario_list_models(ctx, category: str = None, **kwargs):
        """List available Scenario models."""
        pass
    
    @mcp.tool()
    async def scenario_train_model(ctx, model_name: str, training_images: list, **kwargs):
        """Train custom Scenario model."""
        pass