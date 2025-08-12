#!/usr/bin/env python3
"""
Direct Scenario AI Integration for Claude Code Agents
Bypasses MCP Context issues and provides direct API access
"""

import asyncio
import aiohttp
import base64
import json
import os
import sys
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

class ScenarioAI:
    """Direct Scenario AI API client for Claude Code agents."""
    
    def __init__(self):
        # Load environment variables from scenario-mcp directory
        scenario_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scenario-mcp")
        env_path = os.path.join(scenario_dir, ".env")
        load_dotenv(env_path)
        
        self.api_key = os.getenv("SCENARIO_API_KEY")
        self.api_secret = os.getenv("SCENARIO_API_SECRET") 
        self.api_base_url = os.getenv("SCENARIO_API_BASE_URL", "https://api.cloud.scenario.com/v1")
        
        if not self.api_key or not self.api_secret:
            raise ValueError("❌ Scenario API credentials not found. Check .env file in scenario-mcp directory.")
        
        self.auth_header = base64.b64encode(f"{self.api_key}:{self.api_secret}".encode()).decode()
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test API connection and return status."""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Basic {self.auth_header}",
                    "Content-Type": "application/json"
                }
                
                async with session.get(f"{self.api_base_url}/models", headers=headers, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        models_count = len(data.get("models", [])) if isinstance(data, dict) else "unknown"
                        
                        return {
                            "success": True,
                            "message": f"✅ Scenario AI connection successful! Found {models_count} models",
                            "data": {
                                "status_code": response.status,
                                "models_available": models_count,
                                "api_base": self.api_base_url,
                                "credentials_valid": True
                            }
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "message": f"❌ Connection failed: HTTP {response.status}",
                            "data": {"status_code": response.status, "error": error_text}
                        }
                        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Connection error: {str(e)}",
                "data": {"error": str(e), "error_type": type(e).__name__}
            }
    
    async def generate_image(
        self,
        prompt: str,
        model_id: str = "flux.1-dev",
        width: int = 1024,
        height: int = 1024,
        num_samples: int = 1,
        num_inference_steps: int = 28,
        guidance: float = 3.5
    ) -> Dict[str, Any]:
        """Generate images using Scenario AI."""
        try:
            payload = {
                "prompt": prompt,
                "modelId": model_id,
                "width": width,
                "height": height,
                "numImages": num_samples,
                "numInferenceSteps": num_inference_steps,
                "guidance": guidance
            }
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Basic {self.auth_header}",
                    "Content-Type": "application/json"
                }
                
                async with session.post(
                    f"{self.api_base_url}/generate/txt2img",
                    json=payload,
                    headers=headers,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        job_id = data.get("inference", {}).get("id", "unknown")
                        
                        return {
                            "success": True,
                            "message": f"🎨 Image generation started successfully!",
                            "data": {
                                "job_id": job_id,
                                "status": "started",
                                "prompt": prompt,
                                "model_id": model_id,
                                "dimensions": f"{width}x{height}",
                                "samples": num_samples,
                                "inference_steps": num_inference_steps,
                                "guidance": guidance,
                                "full_response": data
                            }
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "message": f"❌ Generation failed: HTTP {response.status}",
                            "data": {"status_code": response.status, "error": error_text}
                        }
                        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Generation error: {str(e)}",
                "data": {"error": str(e), "error_type": type(e).__name__}
            }
    
    async def get_models(self, limit: int = 50, filter_type: Optional[str] = None) -> Dict[str, Any]:
        """Get available models from Scenario AI with filtering."""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Basic {self.auth_header}",
                    "Content-Type": "application/json"
                }
                
                async with session.get(f"{self.api_base_url}/models", headers=headers, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        models = data.get("models", [])
                        
                        # Filter by type if specified
                        if filter_type:
                            models = [m for m in models if m.get("type", "").lower() == filter_type.lower()]
                        
                        # Categorize models by type and capability
                        categorized_models = {
                            "flux_lora": [],
                            "backgrounds": [],
                            "characters": [],
                            "general": [],
                            "specialized": []
                        }
                        
                        # Format and categorize models
                        for model in models[:limit]:
                            formatted_model = {
                                "id": model.get("id", ""),
                                "name": model.get("name", ""),
                                "description": model.get("description", "")[:150] + "..." if len(model.get("description", "")) > 150 else model.get("description", ""),
                                "category": model.get("category", ""),
                                "type": model.get("type", ""),
                                "is_public": model.get("isPublic", False),
                                "supports_3d": model.get("supports3D", False),
                                "supports_video": model.get("supportsVideo", False),
                                "supports_controlnet": model.get("supportsControlNet", False),
                                "tags": model.get("tags", []),
                                "training_steps": model.get("trainingSteps", 0),
                                "training_images": model.get("trainingImages", 0),
                                "learning_rate": model.get("learningRate", ""),
                                "batch_size": model.get("batchSize", 1)
                            }
                            
                            # Categorize by content
                            model_name_lower = formatted_model["name"].lower()
                            tags_str = " ".join(formatted_model["tags"]).lower()
                            
                            if "flux" in model_name_lower and "lora" in model_name_lower:
                                categorized_models["flux_lora"].append(formatted_model)
                            elif any(word in model_name_lower or word in tags_str for word in ["background", "environment", "landscape", "scene"]):
                                categorized_models["backgrounds"].append(formatted_model)
                            elif any(word in model_name_lower or word in tags_str for word in ["character", "person", "portrait", "figure"]):
                                categorized_models["characters"].append(formatted_model)
                            elif any(word in model_name_lower for word in ["flux", "stable", "dall", "midjourney"]):
                                categorized_models["general"].append(formatted_model)
                            else:
                                categorized_models["specialized"].append(formatted_model)
                        
                        return {
                            "success": True,
                            "message": f"📋 Retrieved {len(models)} models (showing {sum(len(cat) for cat in categorized_models.values())} categorized)",
                            "data": {
                                "total_models": len(models),
                                "categorized_models": categorized_models,
                                "recommended_for_game_dev": [
                                    "flux.1-dev",
                                    "stable-diffusion-xl-base-1.0",
                                    "midjourney-v6-1"
                                ],
                                "recommended_for_backgrounds": [m["id"] for m in categorized_models["backgrounds"][:3]],
                                "recommended_for_characters": [m["id"] for m in categorized_models["characters"][:3]]
                            }
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "message": f"❌ Failed to get models: HTTP {response.status}",
                            "data": {"status_code": response.status, "error": error_text}
                        }
                        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error getting models: {str(e)}",
                "data": {"error": str(e)}
            }
    
    async def get_model_details(self, model_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific model."""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Basic {self.auth_header}",
                    "Content-Type": "application/json"
                }
                
                async with session.get(f"{self.api_base_url}/models/{model_id}", headers=headers, timeout=10) as response:
                    if response.status == 200:
                        model_data = await response.json()
                        
                        return {
                            "success": True,
                            "message": f"📋 Model details for {model_id}",
                            "data": {
                                "model": {
                                    "id": model_data.get("id", ""),
                                    "name": model_data.get("name", ""),
                                    "description": model_data.get("description", ""),
                                    "type": model_data.get("type", ""),
                                    "category": model_data.get("category", ""),
                                    "tags": model_data.get("tags", []),
                                    "is_public": model_data.get("isPublic", False),
                                    "created_by": model_data.get("createdBy", ""),
                                    "training_details": {
                                        "steps": model_data.get("trainingSteps", 0),
                                        "images": model_data.get("trainingImages", 0),
                                        "learning_rate": model_data.get("learningRate", ""),
                                        "batch_size": model_data.get("batchSize", 1)
                                    },
                                    "capabilities": {
                                        "supports_3d": model_data.get("supports3D", False),
                                        "supports_video": model_data.get("supportsVideo", False),
                                        "supports_controlnet": model_data.get("supportsControlNet", False)
                                    },
                                    "recommended_settings": model_data.get("recommendedSettings", {})
                                }
                            }
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "message": f"❌ Failed to get model details: HTTP {response.status}",
                            "data": {"status_code": response.status, "error": error_text}
                        }
                        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error getting model details: {str(e)}",
                "data": {"error": str(e)}
            }
    
    async def generate_with_multiple_models(
        self,
        prompt: str,
        model_ids: List[str],
        shared_settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate images using multiple models for comparison."""
        if not model_ids:
            return {
                "success": False,
                "message": "❌ At least one model ID is required",
                "data": {}
            }
        
        default_settings = {
            "width": 1024,
            "height": 1024,
            "num_samples": 1,
            "num_inference_steps": 28,
            "guidance": 3.5
        }
        
        if shared_settings:
            default_settings.update(shared_settings)
        
        results = []
        total_cost = 0
        
        for i, model_id in enumerate(model_ids):
            try:
                result = await self.generate_image(
                    prompt=prompt,
                    model_id=model_id,
                    **default_settings
                )
                
                if result["success"]:
                    model_result = {
                        "model_index": i,
                        "model_id": model_id,
                        "job_id": result["data"]["job_id"],
                        "status": result["data"]["status"],
                        "cost": result["data"].get("full_response", {}).get("creativeUnitsCost", 0)
                    }
                    total_cost += model_result["cost"]
                    results.append(model_result)
                else:
                    results.append({
                        "model_index": i,
                        "model_id": model_id,
                        "error": result["message"],
                        "status": "failed"
                    })
                    
            except Exception as e:
                results.append({
                    "model_index": i,
                    "model_id": model_id,
                    "error": str(e),
                    "status": "failed"
                })
        
        successful_generations = len([r for r in results if r.get("status") != "failed"])
        
        return {
            "success": True,
            "message": f"🎨 Generated with {successful_generations}/{len(model_ids)} models",
            "data": {
                "prompt": prompt,
                "models_used": model_ids,
                "successful_generations": successful_generations,
                "total_models": len(model_ids),
                "total_estimated_cost": total_cost,
                "shared_settings": default_settings,
                "results": results
            }
        }

# Convenience functions for direct use
async def test_scenario_connection():
    """Quick function to test Scenario AI connection."""
    scenario = ScenarioAI()
    return await scenario.test_connection()

async def generate_scenario_image(prompt: str, model_id: str = "flux.1-dev", width: int = 1024, height: int = 1024):
    """Quick function to generate an image."""
    scenario = ScenarioAI()
    return await scenario.generate_image(prompt, model_id, width, height)

async def get_scenario_models(limit: int = 10):
    """Quick function to get available models.""" 
    scenario = ScenarioAI()
    return await scenario.get_models(limit)

# CLI interface for testing
async def main():
    """CLI interface for testing Scenario AI integration."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scenario_ai_direct.py test")
        print("  python scenario_ai_direct.py generate 'your prompt here'")
        print("  python scenario_ai_direct.py models")
        return
    
    command = sys.argv[1]
    scenario = ScenarioAI()
    
    if command == "test":
        result = await scenario.test_connection()
        print(json.dumps(result, indent=2))
    
    elif command == "generate" and len(sys.argv) > 2:
        prompt = sys.argv[2]
        result = await scenario.generate_image(prompt)
        print(json.dumps(result, indent=2))
    
    elif command == "models":
        result = await scenario.get_models()
        print(json.dumps(result, indent=2))
    
    else:
        print("Invalid command or missing arguments")

if __name__ == "__main__":
    asyncio.run(main())