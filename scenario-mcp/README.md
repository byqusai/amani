# 🎨 Scenario MCP Server

**AI Asset Generation via Model Context Protocol**  
*Perfect integration for AI Game Studio Agent 4 workflows*

Created by **Qusai Saleem** (hi@qusai.org)

---

## 🚀 Overview

The Scenario MCP Server provides comprehensive integration with Scenario.gg's AI asset generation API through the Model Context Protocol (MCP). This server enables **Agent 4: Scenario AI Asset Generator** to execute their asset generation expertise programmatically, automating the entire workflow from prompt engineering to organized asset delivery.

### 🎯 Built for Agent 4

This MCP server transforms Agent 4's manual workflows into automated, scalable operations:

- **Before**: Agent 4 manually visits Scenario.gg, crafts prompts, monitors jobs, downloads assets
- **After**: Agent 4 calls MCP tools that execute their complete generation strategies automatically

## ✨ Features

### 🖼️ Generation Capabilities
- **Text-to-Image**: High-quality image generation from text prompts
- **Image-to-Image**: Style transfer and image-guided generation  
- **ControlNet**: Pose, depth, and edge-guided generation
- **3D Models**: 3D asset generation with textures and materials
- **Video**: Short video clip generation from prompts
- **Batch Processing**: Concurrent generation with progress monitoring

### 🏗️ Production Architecture
- **Async/Await**: Full async support for optimal performance
- **Rate Limiting**: Intelligent throttling and retry mechanisms
- **Authentication**: Secure API key management and validation
- **Error Handling**: Comprehensive error types and recovery
- **Input Validation**: Pydantic models for request validation
- **Structured Logging**: Detailed logging for monitoring and debugging

### 🎮 Agent 4 Integration
- **Batch Execution**: Execute Agent 4's complete generation plans
- **Cost Estimation**: Budget planning before generation
- **Asset Organization**: Automated file organization and metadata
- **Quality Monitoring**: Track generation success rates and quality
- **Prompt Variations**: Generate multiple variations efficiently

## 📦 Installation

### Prerequisites
- Python 3.9+
- UV package manager (recommended) or pip
- Scenario.gg API credentials

### Setup

1. **Clone and setup project**:
   ```bash
   git clone <repository>
   cd scenario-mcp
   
   # Using UV (recommended)
   uv sync
   
   # Or using pip
   pip install -e .
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your Scenario API credentials
   ```

3. **Required environment variables**:
   ```bash
   # .env file
   SCENARIO_API_KEY=your_api_key_here
   SCENARIO_API_SECRET=your_api_secret_here
   SCENARIO_API_BASE_URL=https://api.cloud.scenario.com/v1
   
   # Optional settings
   LOG_LEVEL=INFO
   MAX_CONCURRENT_REQUESTS=5
   DEFAULT_DOWNLOAD_PATH=./scenario_assets
   ```

## 🚀 Usage

### Starting the Server

```bash
# Development mode
uv run src/server.py

# Production mode  
python -m src.server
```

### MCP Integration

Add to your MCP configuration (`.mcp.json`):

```json
{
  "mcpServers": {
    "scenario-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/scenario-mcp",
        "src/server.py"
      ]
    }
  }
}
```

## 🔧 Core MCP Tools

### Text-to-Image Generation

```python
# Basic generation
await scenario_text_to_image(
    ctx=context,
    prompt="a majestic dragon in a fantasy landscape",
    model_id="flux.1-dev",
    width=1024,
    height=1024,
    guidance=3.5,
    wait_for_completion=True
)

# Prompt variations (Agent 4's specialty)
await scenario_text_to_image_variations(
    ctx=context,
    base_prompt="fantasy character",
    variations=[
        "+ warrior with sword",
        "+ mage with staff", 
        "+ archer with bow"
    ],
    model_id="flux.1-dev"
)
```

### Batch Processing (Agent 4's Power Tool)

```python
# Execute Agent 4's complete batch strategy
await scenario_agent4_batch_execute(
    ctx=context,
    agent4_batch_plan={
        "engineered_prompts": [
            "detailed fantasy character, warrior class, full body, concept art style",
            "magical staff weapon, glowing crystals, game asset, transparent background",
            "ancient castle environment, isometric view, game tileset"
        ],
        "selected_model": "flux.1-dev",
        "generation_settings": {
            "width": 1024,
            "height": 1024,
            "guidance": 3.5,
            "num_samples": 2
        },
        "organization_config": {
            "max_concurrent": 5,
            "organize_by": "prompt_type"
        }
    }
)
```

### Cost Estimation

```python
# Plan budgets before generation
await scenario_estimate_text_to_image_cost(
    ctx=context,
    prompt="detailed game character art",
    model_id="flux.1-dev",
    num_samples=4,
    width=1024,
    height=1024
)
```

## 🎯 Agent 4 Workflow Integration

### Traditional Agent 4 Process:
```
1. Agent 4 analyzes game requirements
2. Agent 4 creates art direction approach  
3. Agent 4 engineers optimal prompts
4. Agent 4 manually executes on Scenario.gg
5. Agent 4 monitors job progress
6. Agent 4 downloads and organizes assets
7. Agent 4 provides assets to development team
```

### Automated Agent 4 Process:
```python
# Agent 4 now does this programmatically:

# 1. Agent 4's analysis leads to batch plan
agent4_plan = {
    "engineered_prompts": agent4.create_prompt_variations(),
    "selected_model": agent4.choose_optimal_model(),
    "generation_settings": agent4.optimize_settings(),
    "organization_config": agent4.define_organization()
}

# 2. Execute complete workflow
result = await scenario_agent4_batch_execute(ctx, agent4_plan)

# 3. Assets automatically organized and ready
ready_assets = result["data"]["generated_assets"]

# 4. Agent 4 provides structured output to next workflow step
```

## 🏗️ Architecture

### Component Structure
```
ScenarioMCPServer
├── ScenarioAPIClient      # Core API integration
├── AuthenticationManager  # Secure credential handling
├── AsyncThrottler        # Rate limiting and concurrency
├── FileManager          # Asset organization
├── ValidationSystem     # Input validation
└── ResponseHelper       # Standardized responses
```

### Error Handling Hierarchy
```
ScenarioMCPError
├── AuthenticationError
├── ValidationError
├── ScenarioAPIError
├── ConnectionError
├── RateLimitError
├── GenerationError
├── AssetError
└── BatchProcessingError
```

## 🔒 Security

- **Secure Authentication**: API credentials managed through environment variables
- **Input Validation**: All inputs validated with Pydantic models
- **Rate Limiting**: Built-in protection against API overuse
- **Error Handling**: No sensitive information exposed in error messages
- **Connection Security**: HTTPS-only connections to Scenario API

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# Run specific test category
uv run pytest tests/test_tools/test_text_to_image.py

# Run with coverage
uv run pytest --cov=src --cov-report=html
```

## 📊 Monitoring

The server provides comprehensive logging for monitoring:

```bash
# View server logs
tail -f scenario_mcp.log

# Monitor specific operations
grep "batch_generate" scenario_mcp.log

# Track error patterns  
grep "ERROR" scenario_mcp.log | tail -20
```

## 🤝 Integration Examples

### With Unity Game Development

```python
# Agent 4 generates game assets for Unity import
unity_assets = await scenario_agent4_batch_execute(
    ctx=context,
    agent4_batch_plan={
        "engineered_prompts": [
            "player character sprite, 2D side view, pixel art style, 64x64",
            "enemy sprite, flying type, pixel art, transparent background",
            "power-up item, glowing effect, game icon, 32x32"
        ],
        "selected_model": "pixel-art-v2",
        "generation_settings": {
            "width": 512,
            "height": 512,
            "guidance": 7.0
        },
        "organization_config": {
            "organize_by": "asset_type"
        }
    }
)

# Assets ready for Unity import with proper organization
```

### With Web Game Development

```python
# Generate web-optimized assets
web_assets = await scenario_batch_generate(
    ctx=context,
    prompts=[
        "UI button, modern design, web game interface",
        "background pattern, seamless tile, web optimized", 
        "character portrait, web game style, square format"
    ],
    model_id="web-game-ui-v1",
    batch_settings={
        "width": 256,
        "height": 256,
        "format": "webp"  # Web-optimized format
    }
)
```

## 🛠️ Development

### Adding New Tools

1. Create tool file in `src/tools/`
2. Implement MCP tool functions
3. Add registration to `__init__.py`
4. Add tests in `tests/test_tools/`

### Tool Template

```python
def register_my_tools(mcp):
    @mcp.tool()
    async def scenario_my_feature(ctx: Context, **kwargs) -> Dict[str, Any]:
        """Tool description for Agent 4 usage."""
        try:
            # Validate inputs
            # Execute Scenario API operations
            # Return standardized response
            return ResponseHelper.success("Operation completed", data=result)
        except Exception as e:
            return ResponseHelper.error(f"Operation failed: {str(e)}")
```

## 📈 Performance

### Benchmarks
- **Single Generation**: ~10-30 seconds (model dependent)
- **Batch Processing**: 5 concurrent requests optimal
- **Memory Usage**: <100MB during normal operation
- **API Rate Limits**: Automatically handled with exponential backoff

### Optimization Tips
- Use batch processing for multiple generations
- Enable cost estimation for budget planning
- Implement proper error handling and retries
- Monitor rate limits and adjust concurrency

## 🆘 Troubleshooting

### Common Issues

**Authentication Failed**
```bash
# Check API credentials
echo $SCENARIO_API_KEY
echo $SCENARIO_API_SECRET

# Verify credentials are valid
curl -H "Authorization: Basic $(echo -n $SCENARIO_API_KEY:$SCENARIO_API_SECRET | base64)" \
     https://api.cloud.scenario.com/v1/models
```

**Rate Limited**
```bash
# Check rate limiting settings
grep "rate_limit" .env
grep "max_concurrent" .env

# Reduce concurrency if needed
export MAX_CONCURRENT_REQUESTS=3
```

**Generation Failures**
```bash
# Check model availability
uv run -c "
from src.scenario_client import ScenarioAPIClient
import asyncio
async def check():
    async with ScenarioAPIClient() as client:
        models = await client.list_models()
        print([m.id for m in models])
asyncio.run(check())
"
```

## 🚧 Roadmap

### Upcoming Features
- [ ] Advanced ControlNet presets
- [ ] Custom model training automation
- [ ] Asset quality scoring
- [ ] Integration with popular game engines
- [ ] Advanced batch strategies for Agent 4
- [ ] Real-time generation monitoring
- [ ] Asset versioning and management
- [ ] Multi-format export support

### Agent 4 Enhancements
- [ ] Prompt optimization suggestions
- [ ] Style consistency analysis
- [ ] Automated A/B testing for prompts
- [ ] Integration with art pipeline tools
- [ ] Advanced asset organization strategies

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests
4. Update documentation
5. Submit a pull request

## 📞 Support

- **Issues**: Create GitHub issues for bugs and feature requests
- **Email**: hi@qusai.org for direct support
- **Discord**: Join our AI Game Development community

---

**Built with ❤️ for AI-powered game development**  
*Empowering Agent 4 and the future of automated asset generation*