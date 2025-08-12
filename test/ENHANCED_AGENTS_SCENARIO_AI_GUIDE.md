# Enhanced Agents with Scenario AI Integration

## 🎯 Overview

This guide covers the enhanced Agent 2 (Art Direction) and Agent 4 (Asset Generator) with full Scenario AI integration, enabling visual communication, model selection, model blending, and comprehensive asset generation workflows.

## 🗂️ File Organization

All Scenario AI files are now properly organized in `/dev/amani/scenario-mcp/`:

```
dev/amani/scenario-mcp/
├── scenario_ai_direct.py          # Core Direct API Integration
├── generate_with_scenario.py      # Agent-friendly CLI wrapper
├── .env                          # API credentials
├── src/                          # MCP server components
└── ...                           # Other MCP files
```

## 🎨 Enhanced Agent 2: Art Direction Analyst

### Key Capabilities

1. **Visual Style Analysis & Recommendation**
   - Analyzes game concepts for optimal art direction
   - Provides 3 visual approaches with generated samples
   - Scores styles based on target audience, platform, and complexity

2. **Scenario AI Model Curation**
   - Automatically finds best models for each art style
   - Categorizes models by capability (flux_lora, backgrounds, characters, etc.)
   - Provides model recommendations with suitability scores

3. **Visual Communication**
   - Generates mood boards with multiple visual elements
   - Creates side-by-side style comparisons
   - Produces comprehensive visual samples instead of text descriptions

4. **Model Blending & Comparison**
   - Tests model compatibility for blending
   - Generates with multiple models for comparison
   - Recommends optimal model combinations

### Usage Examples

#### Basic Art Direction Analysis
```bash
cd /Users/qusaiabushanab/dev/amani/test
python enhanced_art_direction_analyst.py analyze "fantasy adventure game with magical creatures"
```

#### Visual Style Approaches (CEO Decision Points)
```bash
python enhanced_art_direction_analyst.py approaches "cyberpunk puzzle game for mobile"
```

#### Style Comparison with Visuals
```bash
python enhanced_art_direction_analyst.py compare "pixel_perfect,hand_painted_fantasy" "character,environment"
```

#### Comprehensive Mood Board Generation
```bash
python enhanced_art_direction_analyst.py moodboard "medieval fantasy RPG" "hand_painted_fantasy"
```

#### Model Blending Strategy
```bash
python enhanced_art_direction_analyst.py blend "fantasy-art-v3,painterly-style,magical-environments" "fantasy game characters"
```

### Integration with CEO Workflow

**Agent 2 CEO Decision Process:**
1. **Present 3 Visual Approaches** → CEO selects preferred style
2. **Show Model Recommendations** → CEO approves model selection
3. **Generate Sample Visuals** → CEO reviews quality and consistency
4. **Create Production Guidelines** → CEO approves workflow and standards

## 🎮 Enhanced Agent 4: Asset Generator

### Key Capabilities

1. **Comprehensive Asset Categories**
   - Characters & NPCs (player, enemies, creatures)
   - Environments & Backgrounds (landscapes, interiors)
   - UI & Interface Elements (buttons, icons, panels)
   - Items & Equipment (weapons, armor, consumables)
   - Effects & Particles (spells, impacts, auras)
   - Tiles & Props (level building, decorations)

2. **Intelligent Asset Planning**
   - Analyzes GDD content for asset requirements
   - Creates comprehensive generation plans with timelines
   - Optimizes model assignments per category
   - Provides batch scheduling and priority management

3. **Advanced Generation Features**
   - Batch processing with dependency management
   - Quality consistency checking across assets
   - Automatic variation generation
   - Performance optimization recommendations

4. **Production Management**
   - Progress tracking and reporting
   - Quality checkpoints and validation
   - Mobile optimization planning
   - File format and compression recommendations

### Usage Examples

#### Asset Requirements Analysis
```bash
cd /Users/qusaiabushanab/dev/amani/test
python enhanced_asset_generator_agent.py analyze "GDD content with character descriptions and environment details" fantasy
```

#### Comprehensive Asset Plan Creation
```bash
python enhanced_asset_generator_agent.py plan requirements.json
```

#### Batch Generation Execution
```bash
python enhanced_asset_generator_agent.py generate_batch batch_001.json fantasy
```

#### Quality & Consistency Check
```bash
python enhanced_asset_generator_agent.py quality_check generated_assets.json
```

#### Asset Variations Generation
```bash
python enhanced_asset_generator_agent.py variations "fantasy warrior character" 4 color
```

#### Optimization Report
```bash
python enhanced_asset_generator_agent.py optimize final_assets.json
```

### Integration with CEO Workflow

**Agent 4 CEO Decision Process:**
1. **Asset Analysis** → CEO approves identified requirements
2. **Generation Plan** → CEO reviews timeline and priorities
3. **Batch Execution** → CEO monitors progress and quality
4. **Quality Review** → CEO approves assets or requests modifications
5. **Optimization** → CEO approves performance optimization plan

## 🔧 Core Scenario AI Integration

### Direct API Access Commands

All agents use the organized Scenario AI Direct API located in `scenario-mcp/`:

```bash
# Test connection
uv run --directory /Users/qusaiabushanab/dev/amani/scenario-mcp python scenario_ai_direct.py test

# Generate images 
uv run --directory /Users/qusaiabushanab/dev/amani/scenario-mcp python generate_with_scenario.py "your prompt"

# Get available models
uv run --directory /Users/qusaiabushanab/dev/amani/scenario-mcp python scenario_ai_direct.py models
```

### Model Categories & Recommendations

The system automatically categorizes Scenario models:

- **flux_lora**: Advanced Flux-based models with LoRA fine-tuning
- **backgrounds**: Environment and landscape specialists  
- **characters**: Character design and creature models
- **general**: All-purpose models (flux.1-dev, stable-diffusion, etc.)
- **specialized**: Specific use-case models

### Enhanced Features

1. **Model Compatibility Scoring**: Rates model suitability (0-10) for specific tasks
2. **Multi-Model Generation**: Generates with multiple models for comparison
3. **Model Blending Strategies**: Recommends optimal model combinations
4. **Quality Consistency Tracking**: Maintains visual consistency across batches

## 🎯 Agent Enhancement Benefits

### For Agent 2 (Art Direction):

✅ **Visual Communication**: Shows instead of just describing art styles
✅ **Model Expertise**: Automatically selects best models for each style
✅ **CEO Decision Support**: Provides clear visual options for selection
✅ **Production Ready**: Creates complete style guides and workflows

### For Agent 4 (Asset Generator):

✅ **Comprehensive Planning**: Analyzes entire project for asset needs
✅ **Intelligent Scheduling**: Optimizes generation order and dependencies
✅ **Quality Management**: Ensures consistency across all assets
✅ **Production Optimization**: Handles file formats, compression, mobile optimization

## 🚀 Quick Start Workflow

### 1. Game Concept → Art Direction
```bash
# Agent 2: Analyze concept and present visual approaches
python enhanced_art_direction_analyst.py approaches "your game concept"
# → CEO selects preferred approach
```

### 2. Art Style → Asset Planning  
```bash
# Agent 4: Analyze asset requirements
python enhanced_asset_generator_agent.py analyze "GDD content" selected_style
# → CEO approves asset plan
```

### 3. Planned Assets → Generation
```bash
# Agent 4: Execute generation plan
python enhanced_asset_generator_agent.py generate_batch batch_data.json
# → CEO reviews quality and progress
```

### 4. Generated Assets → Quality Review
```bash
# Agent 4: Perform quality check
python enhanced_asset_generator_agent.py quality_check assets.json
# → CEO approves or requests revisions
```

## 🎨 Advanced Features

### Visual Style Database
Agent 2 includes 5 comprehensive visual styles:
- **Pixel Perfect Retro**: 16-bit inspired with modern polish
- **Hand-Painted Fantasy**: Rich, painterly with magical atmosphere  
- **Minimalist Geometric**: Clean shapes with bold colors
- **Dark Atmospheric**: Moody themes with dramatic lighting
- **Cartoon Vibrant**: Bright, cheerful with exaggerated features

### Asset Category System
Agent 4 manages 6 major categories with 100+ specific asset types:
- **Characters**: 13 types (player variants, NPCs, enemies, creatures)
- **Environments**: 16 types (outdoor, indoor, sky variations)
- **UI Elements**: 16 types (buttons, icons, panels, bars)
- **Items**: 16 types (weapons, armor, consumables, treasures)
- **Effects**: 16 types (spells, particles, impacts, auras)
- **Tiles/Props**: 16 types (level tiles, environmental objects)

### Model Integration Features
- **Smart Model Selection**: Automatically chooses optimal models per task
- **Compatibility Matrix**: Calculates model blending compatibility
- **Quality Optimization**: Adjusts settings per model and style combination
- **Batch Processing**: Handles large-scale generation with dependencies

## 🔍 Troubleshooting

### If Scenario AI Connection Fails:
1. Verify credentials in `scenario-mcp/.env`
2. Test connection: `python scenario_ai_direct.py test`
3. Check API status and quotas

### If Agents Can't Find scenario_ai_direct:
1. Ensure files are in `scenario-mcp/` directory
2. Verify Python path includes the correct directory
3. Check import statements in agent files

### If Generation Quality Is Poor:
1. Review model recommendations from Agent 2
2. Adjust prompt templates in Agent 4
3. Use quality consistency checker
4. Consider regenerating with different models

## 📊 Success Metrics

- **Agent 2**: Provides 3 visual approaches with generated samples in <5 minutes
- **Agent 4**: Plans and executes 50+ assets with 90%+ success rate
- **CEO Workflow**: Clear decision points with visual evidence at each step
- **Quality**: Maintains visual consistency across all generated assets
- **Efficiency**: Reduces art direction and asset creation time by 80%

## 🎯 Next Steps

1. **Test Enhanced Agents**: Run sample workflows with your game concept
2. **Customize Styles**: Add project-specific visual styles to Agent 2 database
3. **Extend Categories**: Add custom asset categories to Agent 4
4. **Integration**: Connect agents with your existing game development pipeline
5. **Optimization**: Use performance recommendations for production deployment

The enhanced agents now provide CEO-level decision support with visual evidence, comprehensive asset planning, and production-ready workflows powered by Scenario AI's advanced models.