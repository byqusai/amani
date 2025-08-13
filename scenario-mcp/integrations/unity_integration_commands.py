#!/usr/bin/env python3
"""
Unity MCP Integration Commands
Helper functions for Unity MCP integration with Scenario assets
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

class UnityIntegrationCommands:
    """Unity MCP integration helper commands for Scenario assets."""
    
    def __init__(self, debug: bool = True):
        self.debug = debug
    
    def log(self, message: str, level: str = "INFO"):
        """Enhanced logging with timestamps."""
        if self.debug:
            import time
            timestamp = time.strftime("%H:%M:%S")
            print(f"[{timestamp}] Unity-MCP {level}: {message}")
    
    async def import_scenario_assets(self, assets_path: str) -> Dict[str, Any]:
        """Import all Scenario assets into Unity project."""
        
        self.log(f"🎮 Importing Scenario assets from: {assets_path}")
        
        # Check if Unity MCP is available
        try:
            from mcp__UnityMCP__manage_asset import manage_asset
            unity_mcp_available = True
        except ImportError:
            self.log("⚠️ Unity MCP not available - simulating import operations", "WARN")
            unity_mcp_available = False
        
        assets_path = Path(assets_path)
        if not assets_path.exists():
            return {"success": False, "error": f"Assets path does not exist: {assets_path}"}
        
        imported_assets = {
            "sprites": [],
            "materials": [],
            "skyboxes": [],
            "ui_elements": [],
            "prefabs": []
        }
        
        # Import sprites
        sprite_dirs = [assets_path / "Characters", assets_path / "UI", assets_path / "Props"]
        for sprite_dir in sprite_dirs:
            if sprite_dir.exists():
                for sprite_file in sprite_dir.glob("*.png"):
                    if unity_mcp_available:
                        try:
                            result = await manage_asset(
                                action="import",
                                path=str(sprite_file),
                                asset_type="Sprite",
                                properties={
                                    "textureType": "Sprite",
                                    "alphaIsTransparency": True,
                                    "generateMipMaps": False,
                                    "maxTextureSize": 1024,
                                    "spriteMode": "Single",
                                    "pixelsPerUnit": 100
                                }
                            )
                            imported_assets["sprites"].append({
                                "file": str(sprite_file),
                                "unity_result": result,
                                "status": "imported"
                            })
                        except Exception as e:
                            self.log(f"Error importing sprite {sprite_file.name}: {e}", "ERROR")
                    else:
                        imported_assets["sprites"].append({
                            "file": str(sprite_file),
                            "status": "simulated"
                        })
        
        # Import materials
        materials_dir = assets_path / "Materials"
        if materials_dir.exists():
            await self._import_pbr_materials(materials_dir, imported_assets, unity_mcp_available)
        
        # Import skyboxes
        skybox_dir = assets_path / "Skyboxes"
        if skybox_dir.exists():
            await self._import_skyboxes(skybox_dir, imported_assets, unity_mcp_available)
        
        self.log(f"✅ Import complete: {len(imported_assets['sprites'])} sprites, {len(imported_assets['materials'])} materials, {len(imported_assets['skyboxes'])} skyboxes")
        
        return {
            "success": True,
            "imported_assets": imported_assets,
            "total_assets": sum(len(category) for category in imported_assets.values()),
            "unity_mcp_available": unity_mcp_available
        }
    
    async def _import_pbr_materials(self, materials_dir: Path, imported_assets: Dict, unity_available: bool):
        """Import PBR materials with proper Unity setup."""
        
        if unity_available:
            from mcp__UnityMCP__manage_asset import manage_asset
        
        for material_file in materials_dir.glob("*.png"):
            if "albedo" in material_file.name.lower():
                # Create Unity material from PBR textures
                if unity_available:
                    try:
                        # Import texture
                        texture_result = await manage_asset(
                            action="import",
                            path=str(material_file),
                            asset_type="Texture2D",
                            properties={
                                "textureType": "Default",
                                "sRGBTexture": True,
                                "generateMipMaps": True,
                                "maxTextureSize": 1024
                            }
                        )
                        
                        # Create material
                        material_name = material_file.stem.replace("_albedo", "")
                        material_result = await manage_asset(
                            action="create",
                            path=f"Assets/Materials/{material_name}.mat",
                            asset_type="Material",
                            properties={
                                "shader": "Standard",
                                "mainTexture": str(material_file)
                            }
                        )
                        
                        imported_assets["materials"].append({
                            "material_name": material_name,
                            "albedo_texture": str(material_file),
                            "unity_material": material_result,
                            "status": "created"
                        })
                    except Exception as e:
                        self.log(f"Error creating material from {material_file.name}: {e}", "ERROR")
                else:
                    imported_assets["materials"].append({
                        "material_name": material_file.stem.replace("_albedo", ""),
                        "albedo_texture": str(material_file),
                        "status": "simulated"
                    })
    
    async def _import_skyboxes(self, skybox_dir: Path, imported_assets: Dict, unity_available: bool):
        """Import skyboxes as Unity cubemaps."""
        
        if unity_available:
            from mcp__UnityMCP__manage_asset import manage_asset
        
        for skybox_file in skybox_dir.glob("*.png"):
            if unity_available:
                try:
                    # Import as cubemap
                    cubemap_result = await manage_asset(
                        action="import",
                        path=str(skybox_file),
                        asset_type="Cubemap",
                        properties={
                            "textureShape": "Cube",
                            "generateMipMaps": True,
                            "maxTextureSize": 2048,
                            "sRGBTexture": True
                        }
                    )
                    
                    # Create skybox material
                    skybox_material_result = await manage_asset(
                        action="create",
                        path=f"Assets/Materials/{skybox_file.stem}_Skybox.mat",
                        asset_type="Material",
                        properties={
                            "shader": "Skybox/Cubemap",
                            "_Tex": str(skybox_file)
                        }
                    )
                    
                    imported_assets["skyboxes"].append({
                        "skybox_file": str(skybox_file),
                        "cubemap_result": cubemap_result,
                        "material_result": skybox_material_result,
                        "status": "created"
                    })
                except Exception as e:
                    self.log(f"Error importing skybox {skybox_file.name}: {e}", "ERROR")
            else:
                imported_assets["skyboxes"].append({
                    "skybox_file": str(skybox_file),
                    "status": "simulated"
                })
    
    async def create_unity_materials(self, pbr_assets_path: str) -> Dict[str, Any]:
        """Create Unity materials from PBR texture sets."""
        
        self.log(f"🎨 Creating Unity materials from PBR assets: {pbr_assets_path}")
        
        try:
            from mcp__UnityMCP__manage_asset import manage_asset
            unity_mcp_available = True
        except ImportError:
            self.log("⚠️ Unity MCP not available - simulating material creation", "WARN")
            unity_mcp_available = False
        
        pbr_path = Path(pbr_assets_path)
        if not pbr_path.exists():
            return {"success": False, "error": f"PBR assets path does not exist: {pbr_path}"}
        
        created_materials = []
        
        # Find PBR texture sets (albedo, normal, metallic, etc.)
        albedo_textures = list(pbr_path.glob("*albedo*.png"))
        
        for albedo_texture in albedo_textures:
            base_name = albedo_texture.stem.replace("_albedo", "")
            
            # Look for related PBR maps
            normal_map = pbr_path / f"{base_name}_normal.png"
            metallic_map = pbr_path / f"{base_name}_metallic.png"
            height_map = pbr_path / f"{base_name}_height.png"
            ao_map = pbr_path / f"{base_name}_ao.png"
            
            if unity_mcp_available:
                try:
                    # Create Unity material with PBR setup
                    material_properties = {
                        "shader": "Standard",
                        "mainTexture": str(albedo_texture)
                    }
                    
                    if normal_map.exists():
                        material_properties["bumpMap"] = str(normal_map)
                    
                    if metallic_map.exists():
                        material_properties["metallicGlossMap"] = str(metallic_map)
                    
                    if height_map.exists():
                        material_properties["parallaxMap"] = str(height_map)
                    
                    if ao_map.exists():
                        material_properties["occlusionMap"] = str(ao_map)
                    
                    material_result = await manage_asset(
                        action="create",
                        path=f"Assets/Materials/{base_name}_PBR.mat",
                        asset_type="Material",
                        properties=material_properties
                    )
                    
                    created_materials.append({
                        "material_name": f"{base_name}_PBR",
                        "albedo": str(albedo_texture),
                        "normal": str(normal_map) if normal_map.exists() else None,
                        "metallic": str(metallic_map) if metallic_map.exists() else None,
                        "height": str(height_map) if height_map.exists() else None,
                        "ao": str(ao_map) if ao_map.exists() else None,
                        "unity_result": material_result,
                        "status": "created"
                    })
                except Exception as e:
                    self.log(f"Error creating material {base_name}: {e}", "ERROR")
            else:
                created_materials.append({
                    "material_name": f"{base_name}_PBR",
                    "albedo": str(albedo_texture),
                    "status": "simulated"
                })
        
        self.log(f"✅ Created {len(created_materials)} Unity materials")
        
        return {
            "success": True,
            "created_materials": created_materials,
            "total_materials": len(created_materials),
            "unity_mcp_available": unity_mcp_available
        }
    
    async def setup_game_scene(self, project_name: str, assets_directory: str) -> Dict[str, Any]:
        """Setup complete Unity game scene with imported assets."""
        
        self.log(f"🎮 Setting up Unity game scene for project: {project_name}")
        
        try:
            from mcp__UnityMCP__manage_scene import manage_scene
            from mcp__UnityMCP__manage_gameobject import manage_gameobject
            unity_mcp_available = True
        except ImportError:
            self.log("⚠️ Unity MCP not available - simulating scene setup", "WARN")
            unity_mcp_available = False
        
        scene_elements = {
            "scene_created": False,
            "camera_setup": False,
            "lighting_setup": False,
            "gameobjects_created": [],
            "ui_canvas_setup": False
        }
        
        if unity_mcp_available:
            try:
                # Create new scene
                scene_result = await manage_scene(
                    action="create",
                    name=f"{project_name}_GeneratedScene",
                    path="Assets/Scenes/",
                    build_index=0
                )
                scene_elements["scene_created"] = True
                
                # Setup main camera
                camera_result = await manage_gameobject(
                    action="create",
                    name="Main Camera",
                    components_to_add=["Camera", "AudioListener"],
                    component_properties={
                        "Camera": {
                            "clearFlags": "Skybox",
                            "cullingMask": -1,
                            "fieldOfView": 60,
                            "orthographic": False
                        }
                    },
                    position=[0, 1, -10]
                )
                scene_elements["camera_setup"] = True
                
                # Setup UI Canvas
                canvas_result = await manage_gameobject(
                    action="create",
                    name="UI Canvas",
                    components_to_add=["Canvas", "CanvasScaler", "GraphicRaycaster"],
                    component_properties={
                        "Canvas": {"renderMode": "ScreenSpaceOverlay"},
                        "CanvasScaler": {
                            "uiScaleMode": "ScaleWithScreenSize",
                            "referenceResolution": {"x": 1920, "y": 1080}
                        }
                    }
                )
                scene_elements["ui_canvas_setup"] = True
                
                # Create environment objects
                assets_path = Path(assets_directory)
                if (assets_path / "Characters").exists():
                    for char_sprite in (assets_path / "Characters").glob("*.png"):
                        char_name = char_sprite.stem
                        char_result = await manage_gameobject(
                            action="create",
                            name=f"Character_{char_name}",
                            components_to_add=["SpriteRenderer", "Rigidbody2D", "BoxCollider2D"],
                            component_properties={
                                "SpriteRenderer": {"sprite": str(char_sprite)},
                                "Rigidbody2D": {"gravityScale": 1.0},
                                "BoxCollider2D": {"isTrigger": False}
                            },
                            position=[0, 0, 0]
                        )
                        scene_elements["gameobjects_created"].append({
                            "name": f"Character_{char_name}",
                            "type": "Character",
                            "sprite": str(char_sprite)
                        })
                
                # Setup lighting (if skybox available)
                skybox_dir = assets_path / "Skyboxes"
                if skybox_dir.exists():
                    skybox_materials = list(skybox_dir.glob("*.mat"))
                    if skybox_materials:
                        lighting_result = await manage_scene(
                            action="configure_lighting",
                            skybox_material=str(skybox_materials[0]),
                            ambient_lighting="Skybox"
                        )
                        scene_elements["lighting_setup"] = True
                
            except Exception as e:
                self.log(f"Error setting up Unity scene: {e}", "ERROR")
        else:
            # Simulate scene setup
            scene_elements = {
                "scene_created": True,
                "camera_setup": True,
                "lighting_setup": True,
                "gameobjects_created": [{"name": "Simulated_Character", "type": "Character"}],
                "ui_canvas_setup": True
            }
        
        self.log(f"✅ Game scene setup complete for {project_name}")
        
        return {
            "success": True,
            "project_name": project_name,
            "scene_elements": scene_elements,
            "total_gameobjects": len(scene_elements["gameobjects_created"]),
            "unity_mcp_available": unity_mcp_available
        }
    
    async def validate_unity_compatibility(self, assets_directory: str) -> Dict[str, Any]:
        """Validate that all assets are Unity-compatible."""
        
        self.log(f"🔍 Validating Unity compatibility: {assets_directory}")
        
        assets_path = Path(assets_directory)
        if not assets_path.exists():
            return {"success": False, "error": f"Assets directory does not exist: {assets_path}"}
        
        validation_results = {
            "sprites": {"total": 0, "valid": 0, "issues": []},
            "materials": {"total": 0, "valid": 0, "issues": []},
            "skyboxes": {"total": 0, "valid": 0, "issues": []},
            "overall_compatibility": 0.0
        }
        
        # Validate sprites
        sprite_dirs = [assets_path / "Characters", assets_path / "UI", assets_path / "Props"]
        for sprite_dir in sprite_dirs:
            if sprite_dir.exists():
                for sprite_file in sprite_dir.glob("*.png"):
                    validation_results["sprites"]["total"] += 1
                    
                    # Check sprite properties
                    try:
                        from PIL import Image
                        with Image.open(sprite_file) as img:
                            # Check transparency
                            has_alpha = img.mode in ('RGBA', 'LA') or 'transparency' in img.info
                            
                            # Check dimensions (power of 2 is preferred)
                            width, height = img.size
                            is_valid_size = width <= 4096 and height <= 4096
                            
                            if has_alpha and is_valid_size:
                                validation_results["sprites"]["valid"] += 1
                            else:
                                validation_results["sprites"]["issues"].append(
                                    f"{sprite_file.name}: Alpha={has_alpha}, Size={width}x{height}"
                                )
                    except Exception as e:
                        validation_results["sprites"]["issues"].append(
                            f"{sprite_file.name}: Validation error - {e}"
                        )
        
        # Validate materials
        materials_dir = assets_path / "Materials"
        if materials_dir.exists():
            for material_file in materials_dir.glob("*.png"):
                validation_results["materials"]["total"] += 1
                
                # Basic validation for PBR textures
                if any(keyword in material_file.name.lower() for keyword in ["albedo", "diffuse", "color"]):
                    validation_results["materials"]["valid"] += 1
                else:
                    validation_results["materials"]["issues"].append(
                        f"{material_file.name}: Not recognized as standard PBR texture"
                    )
        
        # Validate skyboxes
        skybox_dir = assets_path / "Skyboxes"
        if skybox_dir.exists():
            for skybox_file in skybox_dir.glob("*.png"):
                validation_results["skyboxes"]["total"] += 1
                
                try:
                    from PIL import Image
                    with Image.open(skybox_file) as img:
                        width, height = img.size
                        
                        # Check if it's panoramic format (2:1 ratio)
                        is_panoramic = width / height == 2
                        is_high_res = width >= 1024
                        
                        if is_panoramic and is_high_res:
                            validation_results["skyboxes"]["valid"] += 1
                        else:
                            validation_results["skyboxes"]["issues"].append(
                                f"{skybox_file.name}: Not panoramic format or too low resolution"
                            )
                except Exception as e:
                    validation_results["skyboxes"]["issues"].append(
                        f"{skybox_file.name}: Validation error - {e}"
                    )
        
        # Calculate overall compatibility
        total_assets = sum(cat["total"] for cat in validation_results.values() if isinstance(cat, dict) and "total" in cat)
        valid_assets = sum(cat["valid"] for cat in validation_results.values() if isinstance(cat, dict) and "valid" in cat)
        
        validation_results["overall_compatibility"] = (valid_assets / total_assets * 100) if total_assets > 0 else 0
        
        self.log(f"✅ Unity compatibility: {validation_results['overall_compatibility']:.1f}% ({valid_assets}/{total_assets} assets valid)")
        
        return {
            "success": True,
            "validation_results": validation_results,
            "total_assets": total_assets,
            "valid_assets": valid_assets,
            "compatibility_percentage": validation_results["overall_compatibility"]
        }

# CLI Interface
async def main():
    """CLI interface for Unity integration commands."""
    import sys
    
    if len(sys.argv) < 2:
        print("🎮 Unity MCP Integration Commands")
        print("\nUsage:")
        print("  python unity_integration_commands.py import_scenario_assets [assets_path]")
        print("  python unity_integration_commands.py create_unity_materials [pbr_assets_path]")
        print("  python unity_integration_commands.py setup_game_scene [project_name] [assets_directory]")
        print("  python unity_integration_commands.py validate_compatibility [assets_directory]")
        return
    
    command = sys.argv[1]
    unity_commands = UnityIntegrationCommands(debug=True)
    
    try:
        if command == "import_scenario_assets":
            if len(sys.argv) < 3:
                print("❌ Please provide assets path")
                return
            
            assets_path = sys.argv[2]
            print(f"🎮 Importing Scenario assets from: {assets_path}")
            
            result = await unity_commands.import_scenario_assets(assets_path)
            
            if result["success"]:
                print(f"\n✅ Assets imported successfully!")
                print(f"📊 Total assets: {result['total_assets']}")
                print(f"🎨 Sprites: {len(result['imported_assets']['sprites'])}")
                print(f"🏗️ Materials: {len(result['imported_assets']['materials'])}")
                print(f"🌅 Skyboxes: {len(result['imported_assets']['skyboxes'])}")
                print(f"🔧 Unity MCP Available: {result['unity_mcp_available']}")
            else:
                print(f"❌ Import failed: {result.get('error', 'Unknown error')}")
        
        elif command == "create_unity_materials":
            if len(sys.argv) < 3:
                print("❌ Please provide PBR assets path")
                return
            
            pbr_path = sys.argv[2]
            print(f"🎨 Creating Unity materials from: {pbr_path}")
            
            result = await unity_commands.create_unity_materials(pbr_path)
            
            if result["success"]:
                print(f"\n✅ Materials created successfully!")
                print(f"🏗️ Total materials: {result['total_materials']}")
                print(f"🔧 Unity MCP Available: {result['unity_mcp_available']}")
            else:
                print(f"❌ Material creation failed: {result.get('error', 'Unknown error')}")
        
        elif command == "setup_game_scene":
            if len(sys.argv) < 4:
                print("❌ Please provide project name and assets directory")
                return
            
            project_name = sys.argv[2]
            assets_directory = sys.argv[3]
            print(f"🎮 Setting up Unity scene for: {project_name}")
            
            result = await unity_commands.setup_game_scene(project_name, assets_directory)
            
            if result["success"]:
                print(f"\n✅ Unity scene setup complete!")
                print(f"🎮 Project: {result['project_name']}")
                print(f"🎯 GameObjects created: {result['total_gameobjects']}")
                print(f"🔧 Unity MCP Available: {result['unity_mcp_available']}")
            else:
                print(f"❌ Scene setup failed")
        
        elif command == "validate_compatibility":
            if len(sys.argv) < 3:
                print("❌ Please provide assets directory")
                return
            
            assets_directory = sys.argv[2]
            print(f"🔍 Validating Unity compatibility: {assets_directory}")
            
            result = await unity_commands.validate_unity_compatibility(assets_directory)
            
            if result["success"]:
                print(f"\n✅ Validation complete!")
                print(f"📊 Overall compatibility: {result['compatibility_percentage']:.1f}%")
                print(f"🎯 Valid assets: {result['valid_assets']}/{result['total_assets']}")
                
                validation = result['validation_results']
                print(f"\n📋 Detailed Results:")
                print(f"  🎨 Sprites: {validation['sprites']['valid']}/{validation['sprites']['total']}")
                print(f"  🏗️ Materials: {validation['materials']['valid']}/{validation['materials']['total']}")
                print(f"  🌅 Skyboxes: {validation['skyboxes']['valid']}/{validation['skyboxes']['total']}")
                
                # Show issues if any
                total_issues = sum(len(cat['issues']) for cat in validation.values() if isinstance(cat, dict) and 'issues' in cat)
                if total_issues > 0:
                    print(f"\n⚠️ Found {total_issues} compatibility issues - check logs for details")
            else:
                print(f"❌ Validation failed: {result.get('error', 'Unknown error')}")
        
        else:
            print("❌ Invalid command")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())