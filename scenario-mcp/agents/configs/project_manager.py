#!/usr/bin/env python3
"""
Multi-Project Configuration Manager
Handles switching between different game projects with isolated configurations
"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

class ProjectType(Enum):
    """Supported project types."""
    MOBILE_GAME = "mobile_game"
    WEB_GAME = "web_game"
    UNITY_GAME = "unity_game"
    PROTOTYPE = "prototype"

class ArtStyle(Enum):
    """Supported art styles."""
    REALISTIC = "realistic"
    STYLIZED = "stylized"
    MINIMALIST = "minimalist"
    PIXEL_ART = "pixel_art"
    CARTOON = "cartoon"

@dataclass
class ProjectConfig:
    """Project configuration structure."""
    name: str
    project_type: ProjectType
    target_audience: str
    platform: str
    art_approaches: Dict[str, Any]
    asset_categories: List[str]
    cultural_elements: List[str] = None
    technical_constraints: Dict[str, Any] = None
    locked_style: Dict[str, Any] = None

class ProjectManager:
    """Manages multiple project configurations and switching."""
    
    def __init__(self, configs_dir: str = None):
        self.configs_dir = Path(configs_dir) if configs_dir else Path(__file__).parent / "projects"
        self.configs_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_project = None
        self.available_projects = {}
        self.load_available_projects()
        
        # Initialize default projects if none exist
        if not self.available_projects:
            self._create_default_projects()
    
    def load_available_projects(self):
        """Load all available project configurations."""
        self.available_projects = {}
        
        for config_file in self.configs_dir.glob("*.json"):
            try:
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
                    project_name = config_file.stem
                    self.available_projects[project_name] = config_data
            except Exception as e:
                print(f"⚠️ Error loading project config {config_file}: {e}")
    
    def switch_project(self, project_name: str) -> bool:
        """Switch to a different project configuration."""
        if project_name not in self.available_projects:
            print(f"❌ Project '{project_name}' not found")
            return False
        
        self.current_project = project_name
        print(f"✅ Switched to project: {project_name}")
        return True
    
    def get_current_config(self) -> Dict[str, Any]:
        """Get the current project configuration."""
        if not self.current_project:
            print("⚠️ No project selected")
            return {}
        
        return self.available_projects.get(self.current_project, {})
    
    def create_new_project(self, 
                          name: str, 
                          project_type: str,
                          target_audience: str,
                          platform: str,
                          template: str = "default") -> bool:
        """Create a new project from template."""
        
        # Load template
        template_path = self.configs_dir / f"{template}.json"
        if template_path.exists():
            with open(template_path, 'r') as f:
                template_config = json.load(f)
        else:
            template_config = self._get_default_template()
        
        # Customize template
        project_config = template_config.copy()
        project_config.update({
            "name": name,
            "project_type": project_type,
            "target_audience": target_audience,
            "platform": platform,
            "created_at": __import__('time').strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Save new project
        project_file = self.configs_dir / f"{name.lower().replace(' ', '_')}.json"
        with open(project_file, 'w') as f:
            json.dump(project_config, f, indent=2)
        
        # Reload projects
        self.load_available_projects()
        
        print(f"✅ Created new project: {name}")
        return True
    
    def get_art_approaches(self, project_name: str = None) -> Dict[str, Any]:
        """Get art direction approaches for a project."""
        project_name = project_name or self.current_project
        if not project_name:
            return {}
        
        config = self.available_projects.get(project_name, {})
        return config.get("art_approaches", {})
    
    def get_asset_requirements(self, project_name: str = None) -> List[str]:
        """Get asset requirements for a project."""
        project_name = project_name or self.current_project
        if not project_name:
            return []
        
        config = self.available_projects.get(project_name, {})
        return config.get("asset_categories", [])
    
    def set_locked_style(self, style_package: Dict[str, Any], project_name: str = None):
        """Lock a style for a project."""
        project_name = project_name or self.current_project
        if not project_name:
            print("⚠️ No project selected")
            return
        
        # Update in memory
        if project_name in self.available_projects:
            self.available_projects[project_name]["locked_style"] = style_package
        
        # Save to file
        project_file = self.configs_dir / f"{project_name}.json"
        if project_file.exists():
            with open(project_file, 'w') as f:
                json.dump(self.available_projects[project_name], f, indent=2)
        
        print(f"🔒 Style locked for project: {project_name}")
    
    def get_locked_style(self, project_name: str = None) -> Dict[str, Any]:
        """Get locked style for a project."""
        project_name = project_name or self.current_project
        if not project_name:
            return {}
        
        config = self.available_projects.get(project_name, {})
        return config.get("locked_style", {})
    
    def list_projects(self) -> Dict[str, Any]:
        """List all available projects with summary info."""
        projects_summary = {}
        
        for project_name, config in self.available_projects.items():
            projects_summary[project_name] = {
                "type": config.get("project_type", "unknown"),
                "platform": config.get("platform", "unknown"),
                "audience": config.get("target_audience", "unknown"),
                "has_locked_style": bool(config.get("locked_style")),
                "art_approaches_count": len(config.get("art_approaches", {})),
                "asset_categories_count": len(config.get("asset_categories", []))
            }
        
        return projects_summary
    
    def _create_default_projects(self):
        """Create default project configurations."""
        
        # Amani project configuration
        amani_config = {
            "name": "Amani",
            "project_type": "unity_game",
            "target_audience": "children_8_14",
            "platform": "unity_webgl",
            "description": "Educational game focusing on children's skills development",
            "art_approaches": {
                "approach_a_child_friendly": {
                    "name": "Child-Friendly Colorful",
                    "description": "Bright, colorful, approachable art style perfect for children",
                    "style_modifier": "colorful cartoon style, child-friendly, bright vibrant colors, friendly characters, educational game aesthetic",
                    "target_emotion": "Joy, curiosity, learning enthusiasm",
                    "cultural_elements": ["Educational", "Child development", "Learning games"],
                    "technical_focus": "Bright colors with educational clarity",
                    "locked_parameters": {
                        "steps": 30,
                        "cfg_scale": 7,
                        "seed_base": 42,
                        "width": 512,
                        "height": 512
                    }
                },
                "approach_b_educational_modern": {
                    "name": "Educational Modern",
                    "description": "Modern educational aesthetic with clean design principles",
                    "style_modifier": "modern educational design, clean interface, learning-focused, contemporary children's media style",
                    "target_emotion": "Focus, engagement, modern learning",
                    "cultural_elements": ["Modern education", "Digital learning", "Contemporary design"],
                    "technical_focus": "Clean modern aesthetics for learning",
                    "locked_parameters": {
                        "steps": 30,
                        "cfg_scale": 7,
                        "seed_base": 42,
                        "width": 512,
                        "height": 512
                    }
                },
                "approach_c_playful_minimalist": {
                    "name": "Playful Minimalist",
                    "description": "Simple, clean design with playful elements for focus",
                    "style_modifier": "minimalist children's design, simple shapes, playful colors, clean educational interface",
                    "target_emotion": "Calm focus, playful learning, clarity",
                    "cultural_elements": ["Minimalist education", "Focus-friendly", "Simple learning"],
                    "technical_focus": "Minimalist with playful educational elements",
                    "locked_parameters": {
                        "steps": 30,
                        "cfg_scale": 7,
                        "seed_base": 42,
                        "width": 512,
                        "height": 512
                    }
                }
            },
            "asset_categories": [
                "Educational Characters",
                "Learning UI Elements",
                "Skill Development Items",
                "Educational Environments",
                "Progress Indicators",
                "Interactive Elements"
            ],
            "cultural_elements": ["Child development", "Educational gaming", "Learning psychology"],
            "technical_constraints": {
                "platform": "Unity WebGL",
                "performance": "optimized_for_web",
                "accessibility": "child_friendly_ui",
                "color_requirements": "high_contrast_for_learning"
            }
        }
        
        # Riyadh Sky Guardian project configuration
        riyadh_config = {
            "name": "Riyadh Sky Guardian",
            "project_type": "unity_game",
            "target_audience": "general_audience",
            "platform": "unity_webgl",
            "description": "Cultural action game featuring Saudi Arabian themes and landmarks",
            "art_approaches": {
                "approach_a_heritage_realism": {
                    "name": "Heritage Realism",
                    "description": "Photorealistic falcon with authentic Saudi architectural accuracy",
                    "style_modifier": "photorealistic, ultra-detailed, architectural photography style, traditional falconry, cultural authenticity, National Geographic quality",
                    "target_emotion": "Pride, authenticity, cultural reverence",
                    "cultural_elements": ["Traditional falconry", "Authentic architecture", "Desert landscapes", "Cultural patterns"],
                    "technical_focus": "Photorealism with cultural accuracy",
                    "locked_parameters": {
                        "steps": 30,
                        "cfg_scale": 7,
                        "seed_base": 42,
                        "width": 512,
                        "height": 512
                    }
                },
                "approach_b_cultural_stylized": {
                    "name": "Cultural Stylized",
                    "description": "Artistic interpretation with traditional Saudi patterns and vibrant colors",
                    "style_modifier": "stylized illustration, islamic geometric patterns, traditional Saudi art style, vibrant desert colors, ornamental design, cultural motifs",
                    "target_emotion": "Cultural pride, artistic beauty, heritage celebration",
                    "cultural_elements": ["Islamic geometry", "Traditional patterns", "Desert colors", "Cultural ornaments"],
                    "technical_focus": "Stylized art with cultural authenticity",
                    "locked_parameters": {
                        "steps": 30,
                        "cfg_scale": 7,
                        "seed_base": 42,
                        "width": 512,
                        "height": 512
                    }
                },
                "approach_c_modern_minimalist": {
                    "name": "Modern Minimalist",
                    "description": "Clean, contemporary aesthetic with subtle Saudi cultural accents",
                    "style_modifier": "minimalist design, clean geometric shapes, flat colors, contemporary art style, modern Saudi Vision 2030 aesthetic, subtle cultural elements",
                    "target_emotion": "Modern sophistication, clean elegance, future vision",
                    "cultural_elements": ["Vision 2030 aesthetics", "Modern architecture", "Geometric subtlety", "Contemporary Saudi"],
                    "technical_focus": "Minimalist with cultural subtlety",
                    "locked_parameters": {
                        "steps": 30,
                        "cfg_scale": 7,
                        "seed_base": 42,
                        "width": 512,
                        "height": 512
                    }
                }
            },
            "asset_categories": [
                "Saudi Falcon Character",
                "Riyadh Landmarks",
                "Cultural UI Elements",
                "Desert Environments",
                "Traditional Patterns",
                "Modern Saudi Architecture"
            ],
            "cultural_elements": ["Saudi Arabian heritage", "Falconry tradition", "Islamic art patterns", "Vision 2030"],
            "technical_constraints": {
                "platform": "Unity WebGL",
                "cultural_accuracy": "high_priority",
                "authenticity": "required",
                "modern_integration": "vision_2030_aligned"
            }
        }
        
        # Default template for new projects
        default_template = {
            "name": "New Project",
            "project_type": "unity_game",
            "target_audience": "general_audience",
            "platform": "unity_webgl",
            "description": "A new game project",
            "art_approaches": {
                "approach_a_realistic": {
                    "name": "Realistic Style",
                    "description": "Photorealistic art style with detailed textures",
                    "style_modifier": "photorealistic, detailed, high quality, professional game art",
                    "target_emotion": "Immersion, realism, engagement",
                    "cultural_elements": [],
                    "technical_focus": "Photorealism",
                    "locked_parameters": {
                        "steps": 30,
                        "cfg_scale": 7,
                        "seed_base": 42,
                        "width": 512,
                        "height": 512
                    }
                },
                "approach_b_stylized": {
                    "name": "Stylized Art",
                    "description": "Artistic, stylized approach with creative interpretation",
                    "style_modifier": "stylized art, creative illustration, artistic interpretation, vibrant colors",
                    "target_emotion": "Creativity, artistic beauty, style",
                    "cultural_elements": [],
                    "technical_focus": "Artistic stylization",
                    "locked_parameters": {
                        "steps": 30,
                        "cfg_scale": 7,
                        "seed_base": 42,
                        "width": 512,
                        "height": 512
                    }
                },
                "approach_c_minimalist": {
                    "name": "Minimalist Design",
                    "description": "Clean, simple design with focus on clarity",
                    "style_modifier": "minimalist design, clean shapes, simple colors, geometric art",
                    "target_emotion": "Clarity, focus, simplicity",
                    "cultural_elements": [],
                    "technical_focus": "Minimalism",
                    "locked_parameters": {
                        "steps": 30,
                        "cfg_scale": 7,
                        "seed_base": 42,
                        "width": 512,
                        "height": 512
                    }
                }
            },
            "asset_categories": [
                "Characters",
                "Environments",
                "UI Elements",
                "Items",
                "Effects",
                "Props"
            ],
            "cultural_elements": [],
            "technical_constraints": {
                "platform": "Unity WebGL",
                "performance": "optimized",
                "style": "consistent"
            }
        }
        
        # Save default projects
        projects = {
            "amani": amani_config,
            "riyadh_sky_guardian": riyadh_config,
            "template": default_template
        }
        
        for project_name, config in projects.items():
            project_file = self.configs_dir / f"{project_name}.json"
            with open(project_file, 'w') as f:
                json.dump(config, f, indent=2)
        
        # Reload projects
        self.load_available_projects()
        print("✅ Created default project configurations")
    
    def _get_default_template(self) -> Dict[str, Any]:
        """Get default template structure."""
        return {
            "name": "New Project",
            "project_type": "unity_game",
            "target_audience": "general_audience", 
            "platform": "unity_webgl",
            "art_approaches": {},
            "asset_categories": ["Characters", "Environments", "UI", "Items"],
            "cultural_elements": [],
            "technical_constraints": {}
        }

# CLI Interface
def main():
    """CLI for project management."""
    import sys
    
    if len(sys.argv) < 2:
        print("🎯 Multi-Project Configuration Manager")
        print("\nUsage:")
        print("  python project_manager.py list                     # List all projects")
        print("  python project_manager.py switch [project_name]    # Switch project")
        print("  python project_manager.py create [name] [type]     # Create new project")
        print("  python project_manager.py info [project_name]      # Get project info")
        return
    
    command = sys.argv[1]
    manager = ProjectManager()
    
    if command == "list":
        projects = manager.list_projects()
        print(f"\n🎮 AVAILABLE PROJECTS:")
        print(f"Current project: {manager.current_project or 'None'}")
        
        for project_name, info in projects.items():
            status = "🔒 LOCKED" if info["has_locked_style"] else "🔓 Open"
            print(f"\n  📁 {project_name} ({info['type']}) {status}")
            print(f"     Platform: {info['platform']}")
            print(f"     Audience: {info['audience']}")
            print(f"     Art Approaches: {info['art_approaches_count']}")
            print(f"     Asset Categories: {info['asset_categories_count']}")
    
    elif command == "switch" and len(sys.argv) > 2:
        project_name = sys.argv[2]
        success = manager.switch_project(project_name)
        if success:
            config = manager.get_current_config()
            print(f"✅ Switched to: {config.get('name', project_name)}")
            print(f"   Type: {config.get('project_type', 'unknown')}")
            print(f"   Platform: {config.get('platform', 'unknown')}")
    
    elif command == "create" and len(sys.argv) > 3:
        name = sys.argv[2]
        project_type = sys.argv[3] if len(sys.argv) > 3 else "unity_game"
        manager.create_new_project(name, project_type, "general_audience", "unity_webgl")
    
    elif command == "info" and len(sys.argv) > 2:
        project_name = sys.argv[2]
        if project_name in manager.available_projects:
            config = manager.available_projects[project_name]
            print(f"\n🎮 PROJECT INFO: {config['name']}")
            print(f"Type: {config.get('project_type', 'unknown')}")
            print(f"Platform: {config.get('platform', 'unknown')}")
            print(f"Target Audience: {config.get('target_audience', 'unknown')}")
            
            art_approaches = config.get('art_approaches', {})
            print(f"\n🎨 ART APPROACHES ({len(art_approaches)}):")
            for approach_key, approach in art_approaches.items():
                print(f"  - {approach.get('name', approach_key)}")
                print(f"    {approach.get('description', 'No description')}")
            
            locked_style = config.get('locked_style')
            if locked_style:
                print(f"\n🔒 LOCKED STYLE:")
                print(f"  Model: {locked_style.get('model_id', 'Unknown')}")
                print(f"  Score: {locked_style.get('consistency_score', 'Unknown')}")
        else:
            print(f"❌ Project '{project_name}' not found")
    
    else:
        print("❌ Invalid command or missing parameters")

if __name__ == "__main__":
    main()