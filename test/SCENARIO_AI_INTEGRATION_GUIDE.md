# 🎨 Scenario AI Integration Guide for Claude Code Agents

## ✅ Status: **WORKING** - Direct API Integration Ready

The Scenario AI integration is now **fully functional** and available for all agents in Claude Code! While the MCP server has Context issues, the direct integration bypasses these problems completely.

## 🚀 Quick Start for Agents

### Method 1: Direct Command Usage
```bash
# Generate an image (recommended for agents)
uv run --directory /Users/qusaiabushanap/dev/amani/scenario-mcp python /Users/qusaiabushanap/dev/amani/generate_with_scenario.py "your prompt here"

# Test connection
uv run --directory /Users/qusaiabushanap/dev/amani/scenario-mcp python /Users/qusaiabushanap/dev/amani/test/scenario_ai_direct.py test

# Get available models  
uv run --directory /Users/qusaiabushanap/dev/amani/scenario-mcp python /Users/qusaiabushanap/dev/amani/test/scenario_ai_direct.py models
```

### Method 2: Python Integration
```python
# For agents that need to integrate Scenario AI directly into their code
import sys
sys.path.append('/Users/qusaiabushanap/dev/amani/test')
from scenario_ai_direct import ScenarioAI, test_scenario_connection, generate_scenario_image

# Test connection
result = await test_scenario_connection()

# Generate image
result = await generate_scenario_image("a magical forest", "flux.1-dev", 1024, 1024)
```

## 🛠️ Available Functions

### 1. Test Connection
```bash
uv run --directory /Users/qusaiabushanap/dev/amani/scenario-mcp python /Users/qusaiabushanap/dev/amani/test/scenario_ai_direct.py test
```
**Output**: Connection status, API validation, available models count

### 2. Generate Images
```bash
# Basic generation
uv run --directory /Users/qusaiabushanap/dev/amani/scenario-mcp python /Users/qusaiabushanap/dev/amani/generate_with_scenario.py "cyberpunk cat"

# With custom parameters  
uv run --directory /Users/qusaiabushanap/dev/amani/scenario-mcp python /Users/qusaiabushanap/dev/amani/generate_with_scenario.py "epic fantasy landscape" flux.1-dev 1280 720
```
**Returns**: Job ID, generation status, full API response

### 3. Get Models
```bash
uv run --directory /Users/qusaiabushanap/dev/amani/scenario-mcp python /Users/qusaiabushanap/dev/amani/test/scenario_ai_direct.py models
```
**Output**: List of available models with capabilities

## 📋 Recommended Models for Agents

| Model ID | Best For | Strengths |
|----------|----------|-----------|
| `flux.1-dev` | General images | High quality, fast, versatile |
| `stable-diffusion-xl-base-1.0` | Realistic images | Photorealistic results |
| `midjourney-v6-1` | Artistic images | Creative, artistic style |
| `dall-e-3` | Conceptual art | Abstract concepts |

## 🎯 Usage Examples for Different Agent Types

### For Game Development Agents (Agent 4 - Asset Generator)
```bash
# Character concepts
uv run --directory /Users/qusaiabushanap/dev/amani/scenario-mcp python /Users/qusaiabushanap/dev/amani/generate_with_scenario.py "pixel art knight character, game sprite, transparent background"

# Environment art
uv run --directory /Users/qusaiabushanap/dev/amani/scenario-mcp python /Users/qusaiabushanap/dev/amani/generate_with_scenario.py "medieval castle interior, game background, detailed" flux.1-dev 1920 1080

# UI elements
uv run --directory /Users/qusaiabushanap/dev/amani/scenario-mcp python /Users/qusaiabushanap/dev/amani/generate_with_scenario.py "fantasy game button, glowing magical design, UI element"
```

### For Art Direction Agents (Agent 2)
```bash
# Style exploration
uv run --directory /Users/qusaiabushanap/dev/amani/scenario-mcp python /Users/qusaiabushanap/dev/amani/generate_with_scenario.py "color palette mood board, vibrant fantasy theme"

# Visual references
uv run --directory /Users/qusaiabushanap/dev/amani/scenario-mcp python /Users/qusaiabushanap/dev/amani/generate_with_scenario.py "lighting study, dramatic sunset, reference art"
```

### For Technical Architect Agents (Agent 5)
```bash
# Technical diagrams
uv run --directory /Users/qusaiabushanap/dev/amani/scenario-mcp python /Users/qusaiabushanap/dev/amani/generate_with_scenario.py "software architecture diagram, clean minimalist style"

# Wireframes and mockups
uv run --directory /Users/qusaiabushanap/dev/amani/scenario-mcp python /Users/qusaiabushanap/dev/amani/generate_with_scenario.py "mobile app wireframe, clean UI design"
```

## 🔧 Advanced Configuration

### Custom Generation Parameters
```python
# For fine-tuned control
result = await scenario.generate_image(
    prompt="detailed prompt here",
    model_id="flux.1-dev",
    width=1024,
    height=1024,
    num_samples=1,           # Number of images (1-4)
    num_inference_steps=28,  # Quality vs speed (10-50)
    guidance=3.5            # Prompt adherence (1-10)
)
```

### Batch Generation for Agent Workflows
```python
# For agents that need multiple assets
prompts = [
    "character design 1",
    "character design 2", 
    "environment concept"
]

results = []
for prompt in prompts:
    result = await generate_scenario_image(prompt)
    results.append(result)
```

## 🚨 Error Handling

All functions return structured responses:
```json
{
  "success": true/false,
  "message": "Human-readable status",
  "data": {
    // Detailed response data
  }
}
```

**Common Issues:**
- **Connection Failed**: Check internet connection and API credentials
- **Generation Failed**: Try simpler prompt or different model
- **Rate Limits**: Wait a moment between requests

## 📈 Integration Status

| Component | Status | Notes |
|-----------|---------|-------|
| ✅ Direct API Access | **WORKING** | Full functionality available |
| ✅ Connection Testing | **WORKING** | API validation working |
| ✅ Image Generation | **WORKING** | All models accessible |
| ✅ Model Listing | **WORKING** | Full model catalog |
| ✅ Agent Integration | **READY** | Easy command-line interface |
| ❌ MCP Server | **BLOCKED** | Context object issues (bypass with direct integration) |

## 🎯 Next Steps for Agents

1. **Test the Integration**: Run the test command to verify everything works
2. **Try Image Generation**: Generate a test image with your preferred prompt
3. **Integrate into Workflows**: Use the command-line interface in your agent workflows
4. **Explore Models**: Try different models to find what works best for your use case

## 💡 Pro Tips for Agents

- **Prompt Engineering**: Be specific and descriptive for better results
- **Model Selection**: Use flux.1-dev for general purposes, it's fast and high-quality
- **Dimensions**: Standard 1024x1024 works well, use 1280x720 for landscape formats
- **Batch Processing**: Generate multiple variations by running the command multiple times
- **Error Recovery**: Always check the `success` field in responses before proceeding

---

🚀 **Ready to create amazing AI-generated content with Scenario AI!**