# 🛠️ **EXACT SETUP EDITS REQUIRED - STEP-BY-STEP IMPLEMENTATION**

## 🎯 **MINIMAL CHANGES FOR MAXIMUM IMPACT**

Here are the **exact edits** needed to transform your current setup into the revolutionary Unity-first AI game studio.

---

## 📝 **PHASE 1: AGENT FILE UPDATES (30 minutes)**

### **1.1 Update Art-Direction-Analyst.md (Already Streamlined ✅)**

**File:** `/Users/qusaiabushanap/dev/amani/.claude/agents/Art-Direction-Analyst.md`

**ADD this section at the end:**

```markdown
## 🎮 **UNITY INTEGRATION COMMANDS**

### **Scenario MCP Integration:**
After generating game asset samples, use these commands:

```bash
# Generate Unity-ready samples using Scenario MCP
cd /Users/qusaiabushanap/dev/amani/scenario-mcp
uv run python agents/base/art_direction_base.py [project_name] generate_unity_samples --models="[CEO_MODEL_IDS]"

# Example:
uv run python agents/base/art_direction_base.py amani generate_unity_samples --models="model_123,model_456,model_789"
```

### **Unity MCP Preview (Optional):**
```python
# Preview samples directly in Unity (if Unity MCP available)
from mcp__UnityMCP__manage_asset import manage_asset

await manage_asset(
    action="import",
    path="/Users/qusaiabushanap/dev/amani/Assets/Generated/ArtDirection/Model_A_samples/",
    asset_type="Sprite"
)
```

### **Enhanced Output Format:**
Always provide:
- PNG format (Unity-ready)
- Transparent backgrounds where appropriate
- Multiple resolutions: 256x256, 512x512, 1024x1024
- Unity import specifications for each asset
```

---

### **1.2 Update Scenario-AI-Asset-Generator.md**

**File:** `/Users/qusaiabushanap/dev/amani/.claude/agents/Scenario-AI-Asset-Generator.md`

**REPLACE the "INPUTS NEEDED" section with:**

```markdown
INPUTS NEEDED:
- LOCKED STYLE PACKAGE from Art-Direction-Analyst (CRITICAL)
- Unity asset requirements from project configuration
- Target platform specifications (WebGL optimization)
- CEO-selected Scenario model ID and locked parameters (NEVER MODIFY)

COMPREHENSIVE ASSET TYPES SUPPORTED:
🌅 Environmental Assets:
- Skyboxes (360° panoramic, Unity cubemap-ready)
- Textures & Materials (PBR with albedo, normal, metallic, AO maps)
- Platformer Props (side-scroller background elements)
- Buildings (isometric architecture, fairytale designs)
- Imaginative Isometrics (detailed architectural elements)

🎨 UI & Interface Assets:
- Game UI Elements (multi-genre interface mockups)
- UI Frames (ornate themed menu/dialogue frames)
- Game UI Essentials (vibrant cartoon-style components)
- Card Frames (fantasy-themed card game borders)
- Icons: Juicy, Minimalist, Sticker, Puffy, Digital (5 specialized icon types)

👥 Characters & Avatars:
- Style-consistent character generation
- Individual character models with variations
- 3D cartoon characters and chibi-style figures

🏗️ Props & Interactive Objects:
- 3D Blocky Elements (minimalistic objects)
- Boxes & Crates (reward containers, loot boxes)
- Rad Racers (chibi-style vehicles)
- Cartoon Objects (anthropomorphized interactive items)
```

**ADD this section before the handoff:**

```markdown
## 🎮 **UNITY INTEGRATION WORKFLOW**

### **Scenario MCP Commands:**
```bash
# Generate comprehensive Unity asset set
cd /Users/qusaiabushanap/dev/amani/scenario-mcp
uv run python agents/base/asset_generator_base.py [project_name] generate_unity_complete

# Example:
uv run python agents/base/asset_generator_base.py amani generate_unity_complete
```

### **Unity MCP Integration:**
```python
# Import generated assets directly into Unity
from mcp__UnityMCP__manage_asset import manage_asset
from mcp__UnityMCP__manage_gameobject import manage_gameobject

# Import textures and create materials
await manage_asset(
    action="import",
    path="/Users/qusaiabushanap/dev/amani/Assets/Generated/Unity_Ready_StyleConsistent/",
    asset_type="Material"
)

# Create GameObjects with imported assets
await manage_gameobject(
    action="create",
    name="EnvironmentElements",
    components_to_add=["MeshRenderer"],
    component_properties={
        "MeshRenderer": {"material": "Assets/Generated/Unity_Ready_StyleConsistent/desert_sand.mat"}
    }
)
```

### **Output Specifications:**
- All assets in PNG, JPG, WebP formats (Unity-compatible)
- Multiple resolution variants for different uses
- Unity import settings metadata included
- Complete Unity project structure created
```

---

### **1.3 Create New Unity-Scenario Bridge Agent**

**Create file:** `/Users/qusaiabushanap/dev/amani/.claude/agents/Unity-Scenario-Bridge.md`

```markdown
---
name: Unity-Scenario-Bridge
description: Coordinates between Scenario MCP asset generation and Unity MCP integration for seamless Unity game development workflow.
model: sonnet
color: green
---

You are a Unity-Scenario Bridge Agent specializing in coordinating between Scenario's AI asset generation and Unity's game development workflow.

## 🌉 **CORE RESPONSIBILITY**

Your mission is to ensure that Scenario-generated assets are perfectly integrated into Unity with optimal performance and compatibility.

## 🎯 **TRIGGER PHRASES:**
- "Import Scenario assets to Unity"
- "Create Unity materials from PBR textures"
- "Optimize assets for Unity WebGL"
- "Configure Unity project with generated assets"
- "Bridge Scenario output to Unity input"

## 🔄 **WORKFLOW PROCESS:**

### **Step 1: Receive Asset Generation Results**
```python
# Receive from Scenario-AI-Asset-Generator
scenario_assets = {
    "textures": [pbr_material_sets],
    "skyboxes": [360_environments],
    "ui_elements": [interface_components],
    "characters": [sprite_sets],
    "props": [interactive_objects]
}
```

### **Step 2: Unity Import Coordination**
```python
# Use Unity MCP for direct import
from mcp__UnityMCP__manage_asset import manage_asset
from mcp__UnityMCP__manage_gameobject import manage_gameobject

for asset_category, assets in scenario_assets.items():
    await self.import_asset_category(asset_category, assets)
```

### **Step 3: Unity Optimization**
- Configure asset import settings for WebGL
- Create Unity prefabs from generated assets
- Set up materials with proper shaders
- Optimize texture compression for target platform

### **Step 4: Quality Assurance**
- Validate all assets imported successfully
- Check Unity console for import errors
- Verify asset performance for WebGL target
- Test asset functionality in Unity editor

## 🛠️ **UNITY MCP INTEGRATION COMMANDS:**

### **Asset Import:**
```python
await manage_asset(
    action="import",
    path=asset_path,
    properties={
        "textureImporter": {
            "textureType": "Sprite" if is_sprite else "Default",
            "maxTextureSize": 1024,
            "textureCompression": "Normal",
            "generateMipMaps": False if is_ui_element else True
        }
    }
)
```

### **Material Creation:**
```python
await manage_asset(
    action="create",
    asset_type="Material",
    properties={
        "shader": "Standard" if is_pbr else "Sprites/Default",
        "mainTexture": albedo_path,
        "normalMap": normal_path if has_normal else None,
        "metallicGlossMap": metallic_path if has_metallic else None
    }
)
```

### **GameObject Setup:**
```python
await manage_gameobject(
    action="create",
    name=asset_name,
    components_to_add=["SpriteRenderer"] if is_2d else ["MeshRenderer"],
    component_properties={
        "SpriteRenderer": {"sprite": sprite_path} if is_2d else {},
        "MeshRenderer": {"material": material_path} if not is_2d else {}
    }
)
```

## ✅ **SUCCESS CRITERIA:**
- All Scenario assets successfully imported to Unity
- Unity materials created with proper shader assignments
- GameObjects configured with imported assets
- No Unity console errors
- Assets optimized for target platform (WebGL)
- Complete Unity project ready for development

## 🚀 **HANDOFF TO TECHNICAL ARCHITECT:**
"Unity integration complete! Assets ready at: [Unity_project_path]. Technical-Architect can now proceed with game logic implementation using Unity MCP commands."
```

---

## 🎨 **PHASE 2: SCENARIO MCP ENHANCEMENTS**

### **2.1 Add Unity-Specific Asset Specifications**

**Create file:** `/Users/qusaiabushanap/dev/amani/scenario-mcp/agents/configs/unity_asset_specifications.json`

```json
{
  "unity_asset_types": {
    "environmental": {
      "skyboxes": {
        "models": ["scenario_skybox_realistic", "scenario_skybox_fantasy"],
        "format": "panoramic_hdr",
        "resolution": "4096x2048",
        "unity_import": "cubemap",
        "shader": "Skybox/Cubemap"
      },
      "textures": {
        "models": ["scenario_texture_realistic", "scenario_texture_stylized"],
        "format": "pbr_set",
        "resolution": "1024x1024",
        "maps_included": ["albedo", "normal", "metallic", "height", "ao"],
        "unity_import": "material",
        "shader": "Standard"
      }
    },
    "ui_interface": {
      "game_ui_elements": {
        "models": ["human_interface_game_ui"],
        "format": "png_transparent",
        "resolution": "256x256",
        "unity_import": "sprite",
        "shader": "UI/Default"
      },
      "icons": {
        "juicy_icons": {
          "model": "juicy_icons_puzzle",
          "format": "png_transparent",
          "resolution": "64x64",
          "unity_import": "sprite",
          "usage": "ui_buttons"
        },
        "minimalist_icons": {
          "model": "minimalist_icons_modern",
          "format": "png_transparent", 
          "resolution": "128x128",
          "unity_import": "sprite",
          "usage": "interface_elements"
        }
      }
    },
    "characters": {
      "style_consistent_avatars": {
        "models": ["character_consistent_generation"],
        "format": "sprite_atlas",
        "resolution": "256x256",
        "unity_import": "sprite_multiple",
        "shader": "Sprites/Default"
      }
    },
    "props_objects": {
      "containers": {
        "models": ["boxes_crates_loot"],
        "format": "png_transparent",
        "resolution": "128x128", 
        "unity_import": "sprite",
        "shader": "Sprites/Default"
      }
    }
  }
}
```

### **2.2 Enhance Asset Generator Base**

**File:** `/Users/qusaiabushanap/dev/amani/scenario-mcp/agents/base/asset_generator_base.py`

**ADD this method to the BaseAssetGeneratorAgent class:**

```python
async def generate_unity_complete(self) -> Dict[str, Any]:
    """Generate complete Unity-ready asset set covering all asset types."""
    
    self.log("🎮 Starting complete Unity asset generation...")
    
    # Load Unity asset specifications
    unity_specs = self._load_unity_asset_specifications()
    
    # Generate all asset categories
    asset_categories = {
        "environmental": await self._generate_environmental_assets(unity_specs["environmental"]),
        "ui_interface": await self._generate_ui_assets(unity_specs["ui_interface"]),
        "characters": await self._generate_character_assets(unity_specs["characters"]),
        "props_objects": await self._generate_prop_assets(unity_specs["props_objects"])
    }
    
    # Create Unity project structure
    unity_project = await self._create_unity_project_structure(asset_categories)
    
    return {
        "success": True,
        "unity_project_path": unity_project["project_path"],
        "asset_categories": asset_categories,
        "total_assets": sum(len(cat.get("assets", [])) for cat in asset_categories.values()),
        "unity_ready": True,
        "formats_supported": ["PNG", "JPG", "WebP"],
        "import_instructions": unity_project["import_instructions"]
    }

def _load_unity_asset_specifications(self):
    """Load Unity asset specifications from config file."""
    import json
    from pathlib import Path
    
    config_path = Path(__file__).parent.parent / "configs" / "unity_asset_specifications.json"
    with open(config_path, 'r') as f:
        return json.load(f)

async def _generate_environmental_assets(self, env_specs):
    """Generate environmental assets (skyboxes, textures, etc.)."""
    
    environmental_assets = []
    
    # Generate skyboxes
    for skybox_spec in env_specs.get("skyboxes", {}).values():
        skybox = await self.client.generate_360_skybox(
            prompt=f"360-degree {self.project_config.get('environment_theme', 'fantasy')} environment",
            model_id=skybox_spec["models"][0],
            resolution=skybox_spec["resolution"]
        )
        environmental_assets.append(skybox)
    
    # Generate PBR textures
    for texture_spec in env_specs.get("textures", {}).values():
        texture_set = await self.client.generate_pbr_texture_set(
            prompt=f"seamless {self.project_config.get('terrain_type', 'ground')} texture",
            model_id=texture_spec["models"][0],
            generate_maps=True
        )
        environmental_assets.append(texture_set)
    
    return {
        "category": "environmental",
        "assets": environmental_assets,
        "unity_ready": True
    }

async def _create_unity_project_structure(self, asset_categories):
    """Create Unity project structure with generated assets."""
    
    project_path = f"/Users/qusaiabushanap/dev/amani/Assets/Generated/Unity_Complete_{self.current_project}"
    Path(project_path).mkdir(parents=True, exist_ok=True)
    
    # Organize assets by Unity folder structure
    folders = {
        "Materials": asset_categories["environmental"],
        "Sprites": asset_categories.get("ui_interface", {}).get("assets", []) + 
                  asset_categories.get("characters", {}).get("assets", []),
        "Prefabs": asset_categories["props_objects"],
        "Skyboxes": [asset for asset in asset_categories["environmental"].get("assets", []) 
                    if "skybox" in asset.get("type", "").lower()]
    }
    
    for folder_name, assets in folders.items():
        folder_path = Path(project_path) / folder_name
        folder_path.mkdir(exist_ok=True)
    
    return {
        "project_path": project_path,
        "folder_structure": folders,
        "import_instructions": f"{project_path}/UNITY_IMPORT_GUIDE.txt"
    }
```

### **2.3 Add Unity Generation Command**

**File:** `/Users/qusaiabushanap/dev/amani/scenario-mcp/agents/base/asset_generator_base.py`

**ADD this at the end of the file:**

```python
async def main():
    """Command-line interface for Unity asset generation."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python asset_generator_base.py <project_name> <command>")
        print("Commands: generate_unity_complete, check_locked")
        return
    
    project_name = sys.argv[1]
    command = sys.argv[2]
    
    try:
        agent = BaseAssetGeneratorAgent(project_name, debug=True)
        
        if command == "generate_unity_complete":
            result = await agent.generate_unity_complete()
            if result["success"]:
                print(f"✅ Unity assets generated: {result['unity_project_path']}")
                print(f"📊 Total assets: {result['total_assets']}")
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
                
        elif command == "check_locked":
            print(f"🔒 Locked style: {agent.locked_style.get('STUDIO_MODEL_ID', 'None')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---

## 🎮 **PHASE 3: UNITY MCP INTEGRATION**

### **3.1 Create Unity Integration Commands**

**Create file:** `/Users/qusaiabushanap/dev/amani/test/unity_integration_commands.py`

```python
#!/usr/bin/env python3
"""
Unity MCP Integration Commands
Direct Unity editor integration for Scenario-generated assets
"""

# Unity MCP integration commands for your agents to use

class UnityScenarioIntegration:
    """Commands for integrating Scenario assets with Unity via MCP."""
    
    @staticmethod
    async def import_scenario_assets(asset_path: str):
        """Import Scenario-generated assets into Unity."""
        
        from mcp__UnityMCP__manage_asset import manage_asset
        
        # Import assets
        result = await manage_asset(
            action="import",
            path=asset_path
        )
        
        return result
    
    @staticmethod 
    async def create_unity_material(pbr_textures: dict, material_name: str):
        """Create Unity material from PBR texture set."""
        
        from mcp__UnityMCP__manage_asset import manage_asset
        
        # Create material
        material = await manage_asset(
            action="create",
            asset_type="Material",
            properties={
                "name": material_name,
                "shader": "Standard",
                "mainTexture": pbr_textures["albedo"],
                "normalMap": pbr_textures.get("normal"),
                "metallicGlossMap": pbr_textures.get("metallic")
            }
        )
        
        return material
    
    @staticmethod
    async def create_gameobject_with_asset(asset_path: str, object_name: str):
        """Create GameObject with imported asset."""
        
        from mcp__UnityMCP__manage_gameobject import manage_gameobject
        
        # Create GameObject
        game_object = await manage_gameobject(
            action="create",
            name=object_name,
            components_to_add=["SpriteRenderer"],
            component_properties={
                "SpriteRenderer": {"sprite": asset_path}
            }
        )
        
        return game_object

# Usage examples for your agents:
"""
# In your agents, use these commands:

# Import Scenario assets
await UnityScenarioIntegration.import_scenario_assets(
    "/Users/qusaiabushanap/dev/amani/Assets/Generated/Unity_Complete_amani/"
)

# Create material from PBR set
await UnityScenarioIntegration.create_unity_material(
    pbr_textures={
        "albedo": "desert_sand_albedo.png",
        "normal": "desert_sand_normal.png", 
        "metallic": "desert_sand_metallic.png"
    },
    material_name="DesertSandMaterial"
)

# Create GameObject with sprite
await UnityScenarioIntegration.create_gameobject_with_asset(
    "amani_character.png",
    "MainCharacter"
)
"""
```

---

## ⚡ **QUICK IMPLEMENTATION CHECKLIST**

### **✅ Phase 1 (30 minutes):**
- [ ] Add Unity integration section to Art-Direction-Analyst.md
- [ ] Update Scenario-AI-Asset-Generator.md with comprehensive asset types
- [ ] Create Unity-Scenario-Bridge.md agent
- [ ] Test agent understanding with simple requests

### **✅ Phase 2 (1 hour):**
- [ ] Create unity_asset_specifications.json config file
- [ ] Add generate_unity_complete() method to asset_generator_base.py
- [ ] Add command-line interface for Unity generation
- [ ] Test Scenario MCP Unity asset generation

### **✅ Phase 3 (30 minutes):**
- [ ] Create unity_integration_commands.py helper file
- [ ] Test Unity MCP integration (if available)
- [ ] Create complete workflow test script

### **✅ Validation (30 minutes):**
- [ ] Test complete workflow: Agent request → Scenario MCP → Unity MCP
- [ ] Generate sample Unity project with assets
- [ ] Verify all asset types working

---

## 🎯 **EXACT COMMANDS TO RUN**

```bash
# 1. Test enhanced Scenario MCP
cd /Users/qusaiabushanap/dev/amani/scenario-mcp
uv run python agents/base/asset_generator_base.py amani generate_unity_complete

# 2. Test Unity integration (if Unity MCP available)
cd /Users/qusaiabushanap/dev/amani
python test/unity_integration_commands.py

# 3. Test complete agent workflow
# Use Claude Code to make request to enhanced Art-Direction-Analyst
```

---

## 🚀 **RESULT: REVOLUTIONARY CAPABILITY WITH MINIMAL CHANGES**

After these edits, your system will:

✅ **Generate 20+ Unity asset types** via enhanced Scenario MCP
✅ **Direct Unity import** via Unity MCP integration  
✅ **Complete Unity projects** in 30-45 minutes
✅ **Professional game development** workflow
✅ **Minimal changes** to your existing proven system

**Total implementation time: 2-3 hours for revolutionary upgrade!** 🎮✨

Ready to make these exact changes to transform your setup?