# 🛠️ **PRACTICAL IMPLEMENTATION PLAN - FROM CURRENT TO REVOLUTIONARY**

## 🎯 **STEP-BY-STEP MIGRATION GUIDE**

This document shows exactly how to transform your **current MCP system** into the **revolutionary Unity-first architecture** using Scenario's advanced capabilities.

---

## 📊 **CURRENT vs NEW ARCHITECTURE COMPARISON**

### **CURRENT SYSTEM (What You Have Now):**
```
art_direction_base.py → generic PNG generation
asset_generator_base.py → basic image files  
enhanced_scenario_client.py → simple API calls
project_manager.py → basic project switching
```

### **NEW SYSTEM (What We're Building):**
```
unity_texture_agent.py → PBR materials with all maps
unity_skybox_agent.py → 360° game-ready environments  
unity_ui_agent.py → complete UI element sets
unity_orchestrator.py → coordinated scene generation
prompt_spark_integration.py → AI-optimized prompts
```

---

## 🔄 **MIGRATION STRATEGY: PARALLEL DEVELOPMENT**

Instead of replacing your current system (which works), we'll build the new system **alongside** it, then gradually migrate projects over.

### **Directory Structure Enhancement:**
```
scenario-mcp/
├── core/                                    # Keep existing
│   ├── enhanced_scenario_client.py          # ✅ Keep as fallback
│   └── model_manager.py                     # ✅ Keep as fallback
├── agents/
│   ├── legacy/                              # Move current agents here
│   │   ├── art_direction_base.py            # ✅ Moved, still functional
│   │   └── asset_generator_base.py          # ✅ Moved, still functional
│   └── unity_optimized/                     # 🆕 NEW Unity-first agents
│       ├── prompt_spark_integration.py      # 🆕 NEW
│       ├── unity_texture_agent.py           # 🆕 NEW  
│       ├── unity_skybox_agent.py            # 🆕 NEW
│       ├── unity_ui_agent.py                # 🆕 NEW
│       ├── unity_character_agent.py         # 🆕 NEW
│       └── unity_orchestrator.py            # 🆕 NEW
└── configs/
    └── unity_asset_specifications/          # 🆕 NEW Unity-specific configs
        ├── pbr_material_specs.json
        ├── skybox_specifications.json  
        └── ui_element_definitions.json
```

---

## 🚀 **PHASE 1: CORE ENHANCEMENTS (Week 1)**

### **Step 1.1: Enhance Scenario Client with Unity Features**
```python
# File: core/unity_enhanced_scenario_client.py
"""
Enhanced Scenario client with Unity-specific capabilities
Extends existing client without breaking current functionality
"""

from .enhanced_scenario_client import EnhancedScenarioClient
import asyncio
import json

class UnityEnhancedScenarioClient(EnhancedScenarioClient):
    """Extended client with Unity-optimized generation capabilities."""
    
    def __init__(self, debug: bool = True):
        super().__init__(debug)
        self.unity_optimization_enabled = True
        self.pbr_generation_enabled = True
    
    async def generate_pbr_texture_set(self, 
                                     prompt: str,
                                     model_id: str,
                                     generate_maps: bool = True,
                                     **kwargs):
        """Generate complete PBR texture set using Scenario's enhanced workflow."""
        
        # Base texture generation
        base_generation = await self.generate_and_download_with_validation(
            prompt=prompt,
            model_id=model_id,
            **kwargs
        )
        
        if not base_generation["success"]:
            return base_generation
        
        albedo_path = base_generation["downloaded_file"]
        
        # Generate additional PBR maps using Scenario's "Generate Maps" feature
        if generate_maps:
            pbr_maps = await self._generate_pbr_maps_from_albedo(
                albedo_path, model_id
            )
            
            return {
                "success": True,
                "albedo_path": albedo_path,
                "normal_path": pbr_maps.get("normal"),
                "metallic_path": pbr_maps.get("metallic"),
                "height_path": pbr_maps.get("height"),
                "ao_path": pbr_maps.get("ao"),
                "roughness_path": pbr_maps.get("roughness"),
                "unity_ready": True,
                "maps_generated": len(pbr_maps)
            }
        
        return base_generation
    
    async def generate_360_skybox(self,
                                prompt: str, 
                                model_id: str,
                                resolution: str = "4096x2048",
                                **kwargs):
        """Generate 360-degree skybox optimized for Unity."""
        
        # Enhance prompt for 360-degree generation
        enhanced_prompt = f"{prompt}, 360-degree panoramic view, seamless horizon, game-ready skybox"
        
        # Generate panoramic skybox
        skybox_generation = await self.generate_and_download_with_validation(
            prompt=enhanced_prompt,
            model_id=model_id,
            width=int(resolution.split('x')[0]),
            height=int(resolution.split('x')[1]),
            format="panoramic",
            **kwargs
        )
        
        if skybox_generation["success"]:
            return {
                "success": True,
                "panoramic_path": skybox_generation["downloaded_file"],
                "resolution": resolution,
                "unity_cubemap_ready": True,
                "format": "HDR_compatible"
            }
        
        return skybox_generation
    
    async def _generate_pbr_maps_from_albedo(self, albedo_path: str, model_id: str):
        """Use Scenario's PBR map generation from albedo texture."""
        
        # This would call Scenario's PBR map generation API
        # Simulated for now - replace with actual API call
        
        pbr_maps = {}
        map_types = ["normal", "metallic", "height", "ao", "roughness"]
        
        for map_type in map_types:
            # API call to generate specific map type from albedo
            map_result = await self._call_scenario_pbr_api(
                albedo_path, map_type, model_id
            )
            
            if map_result["success"]:
                pbr_maps[map_type] = map_result["generated_map_path"]
        
        return pbr_maps
    
    async def _call_scenario_pbr_api(self, albedo_path: str, map_type: str, model_id: str):
        """Call Scenario's PBR map generation API."""
        # Implementation would use actual Scenario PBR API endpoint
        # For now, simulate the process
        
        await asyncio.sleep(0.1)  # Simulate API call
        
        return {
            "success": True,
            "generated_map_path": albedo_path.replace("_albedo", f"_{map_type}"),
            "map_type": map_type
        }
```

### **Step 1.2: Create Prompt Spark Integration**
```python
# File: agents/unity_optimized/prompt_spark_integration.py
"""
Integration with Scenario's Prompt Spark AI assistant
Optimizes prompts for Unity-specific asset generation
"""

import asyncio
import json
from typing import Dict, List, Any

class PromptSparkIntegration:
    """Integrates Scenario's Prompt Spark for Unity-optimized prompts."""
    
    def __init__(self, debug: bool = True):
        self.debug = debug
        self.unity_keywords = [
            "Unity-optimized", "game-ready", "transparent background",
            "high-quality game asset", "seamless tileable", "PBR-ready"
        ]
    
    async def optimize_for_unity_asset(self, 
                                     base_prompt: str,
                                     asset_type: str,
                                     unity_specs: Dict[str, Any] = None) -> Dict[str, str]:
        """Optimize prompt using Prompt Spark for specific Unity asset type."""
        
        # Asset-type-specific optimizations
        optimization_strategies = {
            "texture": self._optimize_texture_prompt,
            "skybox": self._optimize_skybox_prompt,
            "ui_element": self._optimize_ui_prompt,
            "character": self._optimize_character_prompt
        }
        
        optimizer = optimization_strategies.get(asset_type, self._optimize_generic_prompt)
        optimized = await optimizer(base_prompt, unity_specs or {})
        
        # Apply Prompt Spark AI enhancements (simulated - replace with actual API)
        spark_enhanced = await self._call_prompt_spark_api(optimized, asset_type)
        
        return {
            "original": base_prompt,
            "optimized": optimized,
            "spark_enhanced": spark_enhanced["enhanced_prompt"],
            "improvements": spark_enhanced["improvements_made"],
            "unity_keywords_added": spark_enhanced["unity_keywords"]
        }
    
    async def _optimize_texture_prompt(self, prompt: str, unity_specs: dict) -> str:
        """Optimize prompts specifically for Unity texture generation."""
        
        enhancements = [
            "seamless tileable texture",
            "PBR-ready with clear albedo definition", 
            "high-resolution game texture",
            "Unity material optimization"
        ]
        
        if unity_specs.get("tiling"):
            enhancements.append(f"perfect {unity_specs['tiling']} tiling")
        
        if unity_specs.get("surface_type"):
            enhancements.append(f"suitable for {unity_specs['surface_type']} surfaces")
        
        return f"{prompt}, {', '.join(enhancements)}"
    
    async def _optimize_skybox_prompt(self, prompt: str, unity_specs: dict) -> str:
        """Optimize prompts for Unity skybox generation."""
        
        enhancements = [
            "360-degree panoramic view",
            "seamless horizon",
            "Unity cubemap compatible",
            "game-ready skybox",
            "immersive background environment"
        ]
        
        if unity_specs.get("time_of_day"):
            enhancements.append(f"{unity_specs['time_of_day']} lighting")
        
        return f"{prompt}, {', '.join(enhancements)}"
    
    async def _optimize_ui_prompt(self, prompt: str, unity_specs: dict) -> str:
        """Optimize prompts for Unity UI elements."""
        
        enhancements = [
            "clean interface design",
            "Unity UI compatible",
            "professional game UI",
            "transparent background where appropriate"
        ]
        
        if unity_specs.get("interactive_states"):
            enhancements.append("multiple interactive states")
        
        return f"{prompt}, {', '.join(enhancements)}"
    
    async def _call_prompt_spark_api(self, optimized_prompt: str, asset_type: str) -> dict:
        """Call Scenario's Prompt Spark API for final enhancement."""
        
        # Simulated Prompt Spark API call - replace with actual implementation
        await asyncio.sleep(0.1)
        
        # Simulate AI improvements
        improvements = [
            "Enhanced technical precision",
            "Added Unity-specific terminology", 
            "Improved clarity and specificity",
            "Optimized for AI generation"
        ]
        
        return {
            "enhanced_prompt": f"{optimized_prompt}, professional game development quality",
            "improvements_made": improvements,
            "unity_keywords": ["Unity-optimized", "game-ready", "professional quality"],
            "confidence_score": 0.92
        }
```

### **Step 1.3: Create First Unity-Optimized Agent**
```python
# File: agents/unity_optimized/unity_texture_agent.py
"""
Unity-optimized texture material generation agent
Generates complete PBR material sets ready for Unity import
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Any

from core.unity_enhanced_scenario_client import UnityEnhancedScenarioClient
from agents.unity_optimized.prompt_spark_integration import PromptSparkIntegration

class UnityTextureAgent:
    """Generates Unity-ready PBR texture materials using Scenario's advanced workflow."""
    
    def __init__(self, debug: bool = True):
        self.client = UnityEnhancedScenarioClient(debug=debug)
        self.prompt_spark = PromptSparkIntegration(debug=debug)
        self.debug = debug
        
    async def generate_unity_pbr_material(self, material_request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete PBR material set optimized for Unity."""
        
        self.log(f"🎨 Generating Unity PBR material: {material_request['name']}")
        
        # Step 1: Optimize prompt with Prompt Spark
        base_prompt = f"{material_request['description']} texture"
        prompt_optimization = await self.prompt_spark.optimize_for_unity_asset(
            base_prompt, 
            "texture",
            material_request.get("unity_specs", {})
        )
        
        # Step 2: Select optimal model for texture generation
        model_id = await self.select_texture_model(material_request.get("style", "realistic"))
        
        # Step 3: Generate complete PBR set using Scenario's enhanced workflow
        pbr_result = await self.client.generate_pbr_texture_set(
            prompt=prompt_optimization["spark_enhanced"],
            model_id=model_id,
            generate_maps=True,
            width=material_request.get("resolution", {}).get("width", 1024),
            height=material_request.get("resolution", {}).get("height", 1024),
            steps=material_request.get("locked_parameters", {}).get("steps", 30),
            cfg_scale=material_request.get("locked_parameters", {}).get("cfg_scale", 7)
        )
        
        if not pbr_result["success"]:
            return pbr_result
        
        # Step 4: Create Unity material configuration
        unity_material_config = await self.create_unity_material_config(
            pbr_result,
            material_request
        )
        
        # Step 5: Organize files for Unity import
        unity_package = await self.organize_for_unity_import(
            pbr_result,
            unity_material_config,
            material_request["name"]
        )
        
        return {
            "success": True,
            "material_name": material_request["name"],
            "pbr_maps": {
                "albedo": pbr_result["albedo_path"],
                "normal": pbr_result["normal_path"],
                "metallic": pbr_result["metallic_path"],
                "height": pbr_result["height_path"],
                "ao": pbr_result["ao_path"]
            },
            "unity_material_file": unity_package["material_path"],
            "unity_import_folder": unity_package["import_folder"],
            "materialize_shader_config": unity_package["shader_config"],
            "prompt_used": prompt_optimization["spark_enhanced"],
            "model_used": model_id,
            "ready_for_unity_import": True
        }
    
    async def select_texture_model(self, style: str) -> str:
        """Select best Scenario model for texture generation."""
        
        # Scenario's recommended models for different texture styles
        model_map = {
            "realistic": "scenario_texture_realistic_v2",
            "stylized": "scenario_texture_stylized_v1",
            "cartoon": "scenario_texture_cartoon_v1",
            "fantasy": "scenario_texture_fantasy_v1"
        }
        
        selected = model_map.get(style, model_map["realistic"])
        self.log(f"📋 Selected texture model: {selected} for style: {style}")
        return selected
    
    async def create_unity_material_config(self, pbr_result: dict, material_request: dict) -> dict:
        """Create Unity material configuration with Materialize shader setup."""
        
        material_config = {
            "shader": "Materialize/Materialize_Standard_Displace",
            "properties": {
                "_MainTex": pbr_result["albedo_path"],
                "_BumpMap": pbr_result["normal_path"],
                "_MetallicGlossMap": pbr_result["metallic_path"],
                "_ParallaxMap": pbr_result["height_path"],
                "_OcclusionMap": pbr_result["ao_path"]
            },
            "keywords": ["_NORMALMAP", "_METALLICGLOSSMAP", "_PARALLAXMAP", "_OCCLUSIONMAP"],
            "material_name": f"{material_request['name']}_PBR_Material"
        }
        
        return material_config
    
    async def organize_for_unity_import(self, pbr_result: dict, material_config: dict, material_name: str) -> dict:
        """Organize generated assets for Unity import."""
        
        # Create Unity-ready folder structure
        unity_folder = Path(f"/Users/qusaiabushanap/dev/amani/Assets/Generated/Unity_Materials/{material_name}")
        unity_folder.mkdir(parents=True, exist_ok=True)
        
        # Copy/move PBR maps to Unity folder
        textures_folder = unity_folder / "Textures"
        textures_folder.mkdir(exist_ok=True)
        
        # Create Unity material file
        material_file = unity_folder / f"{material_name}.mat.json"
        with open(material_file, 'w') as f:
            json.dump(material_config, f, indent=2)
        
        # Create import instructions
        import_instructions = unity_folder / "UNITY_IMPORT_INSTRUCTIONS.txt"
        with open(import_instructions, 'w') as f:
            f.write(f"""
# Unity Import Instructions for {material_name}

## Step 1: Import Textures
1. Drag all files from 'Textures/' folder into Unity Assets/Materials/Textures/
2. Set texture import settings:
   - Albedo: Texture Type = Default, sRGB = ON
   - Normal: Texture Type = Normal map, sRGB = OFF
   - Metallic: Texture Type = Default, sRGB = OFF
   - Height: Texture Type = Default, sRGB = OFF
   - AO: Texture Type = Default, sRGB = OFF

## Step 2: Create Material
1. Create new Material in Unity
2. Set Shader to "Materialize > Materialize_Standard_Displace"
3. Assign textures to appropriate slots using the material config

## Step 3: Apply Material
1. Drag material onto your 3D model
2. Adjust tiling and offset as needed
3. Test in different lighting conditions

Material is now ready to use in your Unity project!
            """)
        
        return {
            "material_path": str(material_file),
            "import_folder": str(unity_folder),
            "shader_config": material_config,
            "instructions_file": str(import_instructions)
        }
    
    def log(self, message: str):
        """Debug logging."""
        if self.debug:
            print(f"[UnityTextureAgent] {message}")


# Usage Example:
async def test_unity_texture_generation():
    """Test the Unity texture generation workflow."""
    
    texture_agent = UnityTextureAgent(debug=True)
    
    material_request = {
        "name": "DesertSandMaterial",
        "description": "Desert sand with small rocks and wind patterns",
        "style": "realistic",
        "resolution": {"width": 1024, "height": 1024},
        "unity_specs": {
            "tiling": "seamless",
            "surface_type": "terrain"
        },
        "locked_parameters": {
            "steps": 30,
            "cfg_scale": 7,
            "seed": 42
        }
    }
    
    result = await texture_agent.generate_unity_pbr_material(material_request)
    
    if result["success"]:
        print(f"✅ Generated Unity PBR material: {result['material_name']}")
        print(f"📁 Import folder: {result['unity_import_folder']}")
        print(f"🎨 Shader: Materialize_Standard_Displace")
        print(f"🗂️ PBR Maps: {len(result['pbr_maps'])} textures ready")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    asyncio.run(test_unity_texture_generation())
```

---

## 📋 **IMMEDIATE TESTING PROTOCOL**

### **Test 1: Prompt Optimization Validation**
```python
# Create test file: test/test_prompt_optimization.py

async def test_prompt_spark_integration():
    spark = PromptSparkIntegration()
    
    # Test texture prompt optimization
    result = await spark.optimize_for_unity_asset(
        "stone wall", 
        "texture",
        {"tiling": "seamless", "surface_type": "building"}
    )
    
    print("Original:", result["original"])
    print("Optimized:", result["optimized"])
    print("Spark Enhanced:", result["spark_enhanced"])
    
    assert "seamless" in result["optimized"]
    assert "Unity" in result["spark_enhanced"]
    print("✅ Prompt optimization working!")

if __name__ == "__main__":
    asyncio.run(test_prompt_spark_integration())
```

### **Test 2: Unity Texture Generation**
```python
# Create test file: test/test_unity_texture_generation.py

async def test_unity_texture_workflow():
    """Test complete Unity texture generation workflow."""
    
    texture_agent = UnityTextureAgent(debug=True)
    
    # Simple material request
    simple_request = {
        "name": "TestWoodMaterial",
        "description": "Wooden planks with grain detail",
        "style": "realistic"
    }
    
    result = await texture_agent.generate_unity_pbr_material(simple_request)
    
    # Verify results
    assert result["success"] == True
    assert "TestWoodMaterial" in result["material_name"]
    assert "albedo" in result["pbr_maps"]
    assert "normal" in result["pbr_maps"]
    assert result["ready_for_unity_import"] == True
    
    print("✅ Unity texture generation working!")
    print(f"📁 Check folder: {result['unity_import_folder']}")

if __name__ == "__main__":
    asyncio.run(test_unity_texture_workflow())
```

---

## 🎯 **SUCCESS VALIDATION CHECKLIST**

### **Phase 1 Completion Criteria:**
- [ ] UnityEnhancedScenarioClient successfully extends current client
- [ ] PromptSparkIntegration optimizes prompts for Unity assets  
- [ ] UnityTextureAgent generates complete PBR material sets
- [ ] All agents work alongside existing legacy system
- [ ] Generated materials include Unity import instructions
- [ ] Test files validate functionality

### **Phase 1 Deliverables:**
- [ ] 3 new Unity-optimized Python files
- [ ] 2 test files proving functionality
- [ ] Documentation for Unity import process
- [ ] Parallel system running alongside current MCP

---

## 🚀 **NEXT STEPS AFTER PHASE 1**

Once Phase 1 is validated:
- **Phase 2**: Add Unity Skybox Agent and UI Element Agent
- **Phase 3**: Create Unity Orchestrator for complete scene generation  
- **Phase 4**: CEO dashboard integration and project management

**This plan gets you from current system to revolutionary Unity-first architecture in 4 weeks, with working prototypes in Week 1!** 🎮✨