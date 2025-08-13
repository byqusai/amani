#!/usr/bin/env python3
"""
Enhanced Scenario AI Client with Guaranteed Visual Sample Generation
Fixes all critical issues preventing visual sample generation and download
"""

import asyncio
import aiohttp
import base64
import json
import os
import sys
import time
import requests
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
from dotenv import load_dotenv

class EnhancedScenarioClient:
    """Enhanced Scenario AI client that GUARANTEES visual sample generation."""
    
    def __init__(self, debug: bool = True):
        # Load environment variables
        scenario_dir = Path(__file__).parent.parent
        env_path = scenario_dir / ".env"
        load_dotenv(env_path)
        
        self.api_key = os.getenv("SCENARIO_API_KEY")
        self.api_secret = os.getenv("SCENARIO_API_SECRET") 
        self.api_base_url = os.getenv("SCENARIO_API_BASE_URL", "https://api.cloud.scenario.com/v1")
        self.debug = debug
        
        if not self.api_key or not self.api_secret:
            raise ValueError("❌ Scenario API credentials not found in environment variables.")
        
        self.auth_header = base64.b64encode(f"{self.api_key}:{self.api_secret}".encode()).decode()
        self.session_stats = {"generations_started": 0, "generations_completed": 0, "downloads_successful": 0}
    
    def log(self, message: str, level: str = "INFO"):
        """Enhanced logging with timestamps."""
        if self.debug:
            timestamp = time.strftime("%H:%M:%S")
            print(f"[{timestamp}] {level}: {message}")
    
    async def test_connection_with_diagnostics(self) -> Dict[str, Any]:
        """Comprehensive connection test with detailed diagnostics."""
        self.log("🔌 Testing Scenario AI connection...")
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Basic {self.auth_header}",
                    "Content-Type": "application/json"
                }
                
                # Test models endpoint
                async with session.get(f"{self.api_base_url}/models", headers=headers, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        models = data.get("models", [])
                        
                        self.log(f"✅ Connection successful! Found {len(models)} models")
                        
                        # Log available models for debugging
                        for i, model in enumerate(models[:5]):  # Show first 5 models
                            model_id = model.get("id", "unknown")
                            model_name = model.get("name", "Unknown")
                            self.log(f"  Model {i+1}: {model_id} ({model_name})")
                        
                        return {
                            "success": True,
                            "message": f"✅ Connection successful! {len(models)} models available",
                            "models": models,
                            "recommended_model": models[0]["id"] if models else "flux.1-dev"
                        }
                    else:
                        error_text = await response.text()
                        self.log(f"❌ Connection failed: HTTP {response.status} - {error_text}", "ERROR")
                        return {
                            "success": False,
                            "message": f"❌ Connection failed: HTTP {response.status}",
                            "error": error_text
                        }
                        
        except Exception as e:
            self.log(f"❌ Connection error: {str(e)}", "ERROR")
            return {
                "success": False,
                "message": f"❌ Connection error: {str(e)}",
                "error": str(e)
            }
    
    async def check_public_models(self) -> Dict[str, Any]:
        """Check all available public models."""
        self.log("🌐 Checking public models...")
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"accept": "application/json"}
                
                async with session.get(f"{self.api_base_url}/models/public", headers=headers, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        models = data.get("models", [])
                        self.log(f"✅ Found {len(models)} public models")
                        return {
                            "success": True,
                            "message": f"✅ Found {len(models)} public models",
                            "models": models
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "message": f"❌ Public models check failed: HTTP {response.status}",
                            "error": error_text
                        }
        except Exception as e:
            self.log(f"❌ Public models error: {str(e)}", "ERROR")
            return {
                "success": False,
                "message": f"❌ Public models error: {str(e)}",
                "error": str(e)
            }
    
    async def verify_specific_model(self, model_id: str) -> Dict[str, Any]:
        """Verify if a specific model exists and get its details."""
        self.log(f"🔍 Verifying model: {model_id}")
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"accept": "application/json"}
                
                async with session.get(f"{self.api_base_url}/models/public/{model_id}", headers=headers, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        model = data.get("model", {})
                        capabilities = model.get("capabilities", [])
                        
                        self.log(f"✅ Model {model_id} found with capabilities: {capabilities}")
                        return {
                            "success": True,
                            "message": f"✅ Model {model_id} is available",
                            "model": model,
                            "capabilities": capabilities,
                            "available": True
                        }
                    elif response.status == 404:
                        self.log(f"❌ Model {model_id} not found", "ERROR")
                        return {
                            "success": False,
                            "message": f"❌ Model {model_id} not found",
                            "available": False,
                            "error": "Model not found"
                        }
                    elif response.status == 403:
                        self.log(f"❌ No permission to access model {model_id}", "ERROR")
                        return {
                            "success": False,
                            "message": f"❌ No permission to access model {model_id}",
                            "available": False,
                            "error": "Permission denied"
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "message": f"❌ Model verification failed: HTTP {response.status}",
                            "available": False,
                            "error": error_text
                        }
        except Exception as e:
            self.log(f"❌ Model verification error: {str(e)}", "ERROR")
            return {
                "success": False,
                "message": f"❌ Model verification error: {str(e)}",
                "available": False,
                "error": str(e)
            }
    
    async def verify_models_batch(self, model_ids: List[str]) -> Dict[str, Any]:
        """Verify multiple models and return availability status."""
        self.log(f"🔍 Verifying {len(model_ids)} models...")
        
        results = {}
        available_models = []
        unavailable_models = []
        
        for model_id in model_ids:
            result = await self.verify_specific_model(model_id)
            results[model_id] = result
            
            if result["available"]:
                available_models.append(model_id)
            else:
                unavailable_models.append(model_id)
        
        return {
            "success": True,
            "message": f"✅ Verified {len(model_ids)} models: {len(available_models)} available, {len(unavailable_models)} unavailable",
            "available_models": available_models,
            "unavailable_models": unavailable_models,
            "detailed_results": results
        }

    async def discover_models_with_filtering(self, style_tags: List[str] = None, limit: int = 50) -> Dict[str, Any]:
        """Discover available models with filtering capabilities."""
        self.log("🔍 Discovering available models...")
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Basic {self.auth_header}",
                    "Content-Type": "application/json"
                }
                
                params = {"limit": limit}
                async with session.get(f"{self.api_base_url}/models", headers=headers, params=params, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        models = data.get("models", [])
                        
                        # Filter models by style tags if provided
                        if style_tags:
                            filtered_models = []
                            for model in models:
                                model_name = model.get("name", "").lower()
                                model_desc = model.get("description", "").lower()
                                
                                for tag in style_tags:
                                    if tag.lower() in model_name or tag.lower() in model_desc:
                                        filtered_models.append(model)
                                        break
                            models = filtered_models
                        
                        self.log(f"✅ Discovered {len(models)} models")
                        
                        # Categorize models
                        categorized = {
                            "realistic": [],
                            "stylized": [],
                            "artistic": [],
                            "general": []
                        }
                        
                        for model in models:
                            name_lower = model.get("name", "").lower()
                            if any(term in name_lower for term in ["photo", "realistic", "real"]):
                                categorized["realistic"].append(model)
                            elif any(term in name_lower for term in ["cartoon", "anime", "stylized"]):
                                categorized["stylized"].append(model)
                            elif any(term in name_lower for term in ["art", "paint", "draw"]):
                                categorized["artistic"].append(model)
                            else:
                                categorized["general"].append(model)
                        
                        return {
                            "success": True,
                            "message": f"✅ Discovered {len(models)} models",
                            "models": models,
                            "categorized": categorized,
                            "total_count": len(models)
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "message": f"❌ Model discovery failed: HTTP {response.status}",
                            "error": error_text
                        }
                        
        except Exception as e:
            self.log(f"❌ Model discovery error: {str(e)}", "ERROR")
            return {
                "success": False,
                "message": f"❌ Model discovery error: {str(e)}",
                "error": str(e)
            }
    
    async def generate_and_download_with_validation(
        self,
        prompt: str,
        model_id: str = None,
        width: int = 512,
        height: int = 512,
        num_samples: int = 1,
        num_inference_steps: int = 30,
        guidance: float = 7.0,
        download_dir: str = None,
        verify_model: bool = True
    ) -> Dict[str, Any]:
        """Generate image with GUARANTEED download and validation."""
        
        # CRITICAL: Verify model availability BEFORE attempting generation
        if model_id and verify_model:
            self.log(f"🔍 Verifying model availability: {model_id}")
            model_verification = await self.verify_specific_model(model_id)
            
            if not model_verification["available"]:
                return {
                    "success": False,
                    "message": f"❌ CRITICAL: Model {model_id} is not available. {model_verification['message']}",
                    "error": "Model verification failed",
                    "verification_result": model_verification
                }
            else:
                self.log(f"✅ Model {model_id} verified and available")
        
        # Auto-select model if not provided
        if not model_id:
            models_result = await self.test_connection_with_diagnostics()
            if models_result["success"] and models_result.get("models"):
                # Find the first trained model
                trained_models = [m for m in models_result["models"] if m.get("status") == "trained"]
                if trained_models:
                    model_id = trained_models[0]["id"]
                    self.log(f"🎯 Auto-selected trained model: {model_id}")
                else:
                    model_id = "flux.1-dev"
                    self.log(f"⚠️ No trained models found, using default: {model_id}")
            else:
                model_id = "flux.1-dev"
                self.log(f"⚠️ Fallback to default model: {model_id}")
        
        self.log(f"🎨 Starting generation: '{prompt[:50]}...' using {model_id}")
        
        try:
            # Step 1: Start generation
            generation_result = await self._start_generation(
                prompt, model_id, width, height, num_samples, num_inference_steps, guidance
            )
            
            if not generation_result["success"]:
                return generation_result
            
            job_id = generation_result["job_id"]
            self.session_stats["generations_started"] += 1
            self.log(f"✅ Generation started: Job {job_id}")
            
            # Step 2: Wait for completion with progress updates
            completion_result = await self._wait_for_completion_with_progress(job_id, max_wait=300)
            
            if not completion_result["success"]:
                return completion_result
            
            images = completion_result["images"]
            self.session_stats["generations_completed"] += 1
            self.log(f"✅ Generation completed: {len(images)} image(s) ready")
            
            # Step 3: Download and validate images with GUARANTEED verification
            if download_dir:
                download_results = await self._download_and_validate_images(images, download_dir, prompt)
                
                # CRITICAL: Verify all downloads were successful
                successful_downloads = [d for d in download_results if d["success"]]
                failed_downloads = [d for d in download_results if not d["success"]]
                
                if len(successful_downloads) == 0:
                    return {
                        "success": False,
                        "message": f"❌ CRITICAL: All downloads failed! No images were saved.",
                        "job_id": job_id,
                        "images": images,
                        "downloads": download_results,
                        "error": "All downloads failed"
                    }
                elif len(failed_downloads) > 0:
                    self.log(f"⚠️ Warning: {len(failed_downloads)}/{len(images)} downloads failed", "WARNING")
                
                # Verify all downloaded files actually exist and have content
                verified_paths = []
                for result in successful_downloads:
                    local_path = Path(result["local_path"])
                    if local_path.exists() and local_path.stat().st_size > 1000:
                        verified_paths.append(str(local_path))
                    else:
                        self.log(f"❌ Downloaded file missing or empty: {local_path}", "ERROR")
                
                if len(verified_paths) == 0:
                    return {
                        "success": False,
                        "message": f"❌ CRITICAL: No valid downloaded files found! All files missing or empty.",
                        "job_id": job_id,
                        "images": images,
                        "downloads": download_results,
                        "error": "Downloaded files verification failed"
                    }
                
                return {
                    "success": True,
                    "message": f"🎨 Generation and download completed successfully! {len(verified_paths)} files verified.",
                    "job_id": job_id,
                    "images": images,
                    "downloads": download_results,
                    "local_paths": verified_paths,
                    "verified_file_count": len(verified_paths),
                    "stats": self.session_stats
                }
            else:
                return {
                    "success": True,
                    "message": f"🎨 Generation completed successfully!",
                    "job_id": job_id,
                    "images": images,
                    "stats": self.session_stats
                }
                
        except Exception as e:
            self.log(f"❌ Generation error: {str(e)}", "ERROR")
            return {
                "success": False,
                "message": f"❌ Generation failed: {str(e)}",
                "error": str(e)
            }
    
    async def _start_generation(
        self, prompt: str, model_id: str, width: int, height: int, 
        num_samples: int, num_inference_steps: int, guidance: float
    ) -> Dict[str, Any]:
        """Start image generation via Scenario AI API."""
        
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
            
            # Use correct generation endpoint
            async with session.post(
                f"{self.api_base_url}/generate/txt2img",
                json=payload,
                headers=headers,
                timeout=30
            ) as response:
                response_text = await response.text()
                
                if response.status == 200 or response.status == 201:
                    try:
                        data = json.loads(response_text)
                        job_id = data.get("job", {}).get("jobId") or data.get("job", {}).get("id") or data.get("id")
                        
                        if job_id:
                            return {"success": True, "job_id": job_id, "data": data}
                        else:
                            self.log(f"❌ No job ID in response: {response_text}", "ERROR")
                            return {"success": False, "message": "No job ID returned", "response": response_text}
                            
                    except json.JSONDecodeError as e:
                        self.log(f"❌ JSON decode error: {e}, Response: {response_text}", "ERROR")
                        return {"success": False, "message": f"JSON decode error: {e}", "response": response_text}
                else:
                    self.log(f"❌ API error: HTTP {response.status} - {response_text}", "ERROR")
                    return {"success": False, "message": f"HTTP {response.status}", "response": response_text}
    
    async def _wait_for_completion_with_progress(self, job_id: str, max_wait: int = 300) -> Dict[str, Any]:
        """Wait for generation completion with detailed progress updates."""
        
        start_time = time.time()
        last_status = ""
        
        self.log(f"⏳ Waiting for job {job_id} to complete...")
        
        while (time.time() - start_time) < max_wait:
            try:
                status_result = await self._check_job_status(job_id)
                
                if not status_result["success"]:
                    self.log(f"❌ Status check failed: {status_result['message']}", "ERROR")
                    await asyncio.sleep(5)
                    continue
                
                status = status_result["status"]
                progress = status_result.get("progress", 0)
                
                # Log progress updates
                if status != last_status:
                    self.log(f"🔄 Job {job_id}: {status} (Progress: {progress}%)")
                    last_status = status
                
                if status in ["succeeded", "success"]:
                    images = status_result.get("images", [])
                    self.log(f"✅ Job {job_id} completed successfully! Generated {len(images)} image(s)")
                    return {"success": True, "images": images, "job_id": job_id}
                    
                elif status == "failed":
                    error_msg = status_result.get("error", "Unknown error")
                    self.log(f"❌ Job {job_id} failed: {error_msg}", "ERROR")
                    return {"success": False, "message": f"Generation failed: {error_msg}"}
                    
                elif status in ["queued", "running", "processing"]:
                    await asyncio.sleep(5)  # Check every 5 seconds
                    
                else:
                    self.log(f"🤔 Unknown status '{status}', continuing to wait...")
                    await asyncio.sleep(3)
                    
            except Exception as e:
                self.log(f"❌ Error checking status: {str(e)}", "ERROR")
                await asyncio.sleep(5)
        
        return {"success": False, "message": f"Timeout after {max_wait} seconds"}
    
    async def _check_job_status(self, job_id: str) -> Dict[str, Any]:
        """Check job status via Scenario AI API."""
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Basic {self.auth_header}",
                    "Content-Type": "application/json"
                }
                
                async with session.get(f"{self.api_base_url}/jobs/{job_id}", headers=headers, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        job = data.get("job", {})
                        
                        # Debug logging to understand response structure
                        if self.debug:
                            self.log(f"🔍 Job metadata: {json.dumps(job.get('metadata', {}), indent=2)[:800]}...")
                        
                        # Extract images/assets from job metadata - FIXED URL FORMAT
                        asset_ids = job.get("metadata", {}).get("assetIds", [])
                        images = []
                        
                        # Get signed URLs for asset IDs using API
                        for asset_id in asset_ids:
                            # Get signed URL from assets API
                            signed_url = await self._get_signed_asset_url(asset_id)
                            images.append({
                                "id": asset_id,
                                "url": signed_url
                            })
                        
                        return {
                            "success": True,
                            "status": job.get("status", "unknown"),
                            "progress": 100 if job.get("status") == "success" else 0,
                            "images": images,
                            "error": job.get("errorMessage"),
                            "data": data
                        }
                    else:
                        error_text = await response.text()
                        return {"success": False, "message": f"HTTP {response.status}: {error_text}"}
                        
        except Exception as e:
            return {"success": False, "message": f"Status check error: {str(e)}"}
    
    async def _get_signed_asset_url(self, asset_id: str) -> str:
        """Get signed download URL for an asset."""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Basic {self.auth_header}",
                    "Content-Type": "application/json"
                }
                
                async with session.get(f"{self.api_base_url}/assets/{asset_id}", headers=headers, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        asset = data.get("asset", {})
                        return asset.get("url", f"https://cdn.cloud.scenario.com/{asset_id}")
                    else:
                        # Fallback to direct CDN URL if API fails
                        return f"https://cdn.cloud.scenario.com/{asset_id}"
        except Exception as e:
            self.log(f"⚠️ Failed to get signed URL for {asset_id}: {str(e)}", "WARNING")
            return f"https://cdn.cloud.scenario.com/{asset_id}"
    
    async def generate_multi_resolution_unity_asset(
        self,
        prompt: str,
        model_id: str,
        asset_type: str,
        resolutions: List[Dict] = None,
        unity_optimized: bool = True
    ) -> Dict[str, Any]:
        """Generate Unity-optimized assets in multiple resolutions."""

        if resolutions is None:
            resolutions = [
                {"name": "mobile", "width": 256, "height": 256, "suffix": "_256"},
                {"name": "standard", "width": 512, "height": 512, "suffix": "_512"},
                {"name": "hd", "width": 1024, "height": 1024, "suffix": "_1024"},
                {"name": "ultra", "width": 2048, "height": 2048, "suffix": "_2048"}
            ]

        # Unity-specific prompt enhancement
        if unity_optimized:
            unity_modifiers = {
                "character": ", Unity 2D sprite, transparent PNG, clean alpha channel, pixel-perfect edges, sprite atlas ready",
                "environment": ", Unity tileable texture, seamless edges, collision-friendly geometry, mobile optimized",
                "ui": ", Unity UI element, 9-slice scaling ready, retina display compatible, clean vector-style edges",
                "background": ", Unity parallax background, seamless tiling, depth-layer ready, WebGL optimized",
                "animation": ", Unity sprite animation, consistent pivot point, frame sequence ready, timeline compatible"
            }

            prompt += unity_modifiers.get(asset_type, ", Unity game asset, optimized for 2D rendering")

        all_generated_assets = []
        generation_report = {
            "success": True,
            "total_resolutions": len(resolutions),
            "generated_assets": {},
            "failed_resolutions": [],
            "unity_metadata": {}
        }

        for resolution in resolutions:
            self.log(f"🎮 Generating {resolution['name']} resolution ({resolution['width']}x{resolution['height']})...")

            try:
                result = await self.generate_and_download_with_validation(
                    prompt=prompt,
                    model_id=model_id,
                    width=resolution["width"],
                    height=resolution["height"],
                    num_samples=1,
                    download_dir=f"/Users/qusaiabushanap/dev/amani/Assets/Generated/unity_multi_res/{asset_type}/{resolution['name']}",
                    verify_model=False  # Already verified at higher level
                )

                if result["success"]:
                    # Generate Unity import metadata for each resolution
                    unity_metadata = self._generate_unity_import_metadata(
                        resolution, asset_type, result["local_paths"][0]
                    )

                    generation_report["generated_assets"][resolution["name"]] = {
                        "resolution": f"{resolution['width']}x{resolution['height']}",
                        "file_path": result["local_paths"][0],
                        "file_size": Path(result["local_paths"][0]).stat().st_size,
                        "unity_metadata": unity_metadata,
                        "recommended_use": self._get_unity_use_case(resolution["name"])
                    }

                    all_generated_assets.extend(result["local_paths"])

                else:
                    generation_report["failed_resolutions"].append({
                        "resolution": resolution["name"],
                        "error": result["message"]
                    })

            except Exception as e:
                self.log(f"❌ Failed to generate {resolution['name']}: {str(e)}", "ERROR")
                generation_report["failed_resolutions"].append({
                    "resolution": resolution["name"],
                    "error": str(e)
                })

        generation_report["success"] = len(generation_report["generated_assets"]) > 0
        generation_report["total_generated"] = len(all_generated_assets)

        return generation_report

    def _generate_unity_import_metadata(self, resolution: Dict, asset_type: str, file_path: str) -> Dict:
        """Generate Unity-specific import metadata."""
        import uuid

        base_metadata = {
            "guid": str(uuid.uuid4()).replace("-", ""),
            "folderAsset": "yes" if asset_type == "folder" else "no",
            "DefaultImporter": {
                "externalObjects": {},
                "userData": "",
                "assetBundleName": "",
                "assetBundleVariant": ""
            }
        }

        # Asset-type specific metadata
        if asset_type in ["character", "environment", "ui", "background"]:
            base_metadata["TextureImporter"] = {
                "internalIDToNameTable": [],
                "externalObjects": {},
                "serializedVersion": 12,
                "mipmaps": {
                    "mipMapMode": 0,
                    "enableMipMap": 0,
                    "sRGBTexture": 1,
                    "linearTexture": 0,
                    "fadeOut": 0,
                    "borderMipMap": 0,
                    "mipMapsPreserveCoverage": 0,
                    "alphaTestReferenceValue": 0.5,
                    "mipMapFadeDistanceStart": 1,
                    "mipMapFadeDistanceEnd": 3
                },
                "bumpmap": {
                    "convertToNormalMap": 0,
                    "externalNormalMap": 0,
                    "heightScale": 0.25,
                    "normalMapFilter": 0
                },
                "isReadable": 0,
                "streamingMipmaps": 0,
                "streamingMipmapsPriority": 0,
                "vTOnly": 0,
                "ignoreMasterTextureLimit": 0,
                "grayScaleToAlpha": 0,
                "generateCubemap": 6,
                "cubemapConvolution": 0,
                "seamlessCubemap": 0,
                "textureFormat": 1,
                "maxTextureSize": resolution["width"],
                "textureSettings": {
                    "serializedVersion": 2,
                    "filterMode": 0 if asset_type == "ui" else 1,  # Point for UI, Bilinear for game objects
                    "aniso": -1,
                    "mipBias": -100,
                    "wrapU": 1,
                    "wrapV": 1,
                    "wrapW": 1
                },
                "nPOTScale": 0,
                "lightmap": 0,
                "compressionQuality": 50,
                "spriteMode": 1,
                "spriteExtrude": 1,
                "spriteMeshType": 1,
                "alignment": 0,
                "spritePivot": {"x": 0.5, "y": 0.5},
                "spritePixelsToUnits": 100,
                "spriteBorder": {"x": 0, "y": 0, "z": 0, "w": 0},
                "spriteGenerateFallbackPhysicsShape": 1,
                "alphaUsage": 1,
                "alphaIsTransparency": 1,
                "spriteTessellationDetail": -1,
                "textureType": 8,  # Sprite (2D and UI)
                "textureShape": 1,
                "singleChannelComponent": 0,
                "flipbookRows": 1,
                "flipbookColumns": 1,
                "maxTextureSizeSet": 0,
                "compressionQualitySet": 0,
                "textureFormatSet": 0,
                "ignorePngGamma": 0,
                "applyGammaDecoding": 0
            }

        return base_metadata

    def _get_unity_use_case(self, resolution_name: str) -> str:
        """Get recommended Unity use case for resolution."""
        use_cases = {
            "mobile": "Low-end mobile devices, UI icons, small sprites",
            "standard": "Standard mobile/desktop, main game sprites, UI elements",
            "hd": "High-DPI displays, detailed backgrounds, cinematic sprites",
            "ultra": "4K displays, marketing materials, scalable assets"
        }
        return use_cases.get(resolution_name, "General purpose")

    async def generate_unity_sprite_sheet(
        self,
        base_prompt: str,
        model_id: str,
        animation_frames: List[str],
        sheet_layout: Dict = None
    ) -> Dict[str, Any]:
        """Generate Unity-ready sprite animation sheets."""

        if sheet_layout is None:
            sheet_layout = {
                "columns": 4,
                "rows": 2,
                "frame_width": 128,
                "frame_height": 128,
                "spacing": 2,
                "padding": 4
            }

        generated_frames = []

        # Generate individual animation frames
        for i, frame_description in enumerate(animation_frames):
            frame_prompt = f"{base_prompt}, {frame_description}, animation frame {i+1}, consistent character design, transparent background, Unity sprite animation ready"

            frame_result = await self.generate_and_download_with_validation(
                prompt=frame_prompt,
                model_id=model_id,
                width=sheet_layout["frame_width"],
                height=sheet_layout["frame_height"],
                num_samples=1,
                download_dir=f"/Users/qusaiabushanap/dev/amani/Assets/Generated/animation_frames/temp"
            )

            if frame_result["success"]:
                generated_frames.append(frame_result["local_paths"][0])

        # Combine frames into sprite sheet using PIL
        sprite_sheet_path = await self._create_sprite_sheet(
            generated_frames, sheet_layout, base_prompt
        )

        # Generate Unity Animator Controller metadata
        animator_metadata = self._generate_unity_animator_metadata(
            len(animation_frames), sheet_layout
        )

        return {
            "success": len(generated_frames) > 0,
            "sprite_sheet_path": sprite_sheet_path,
            "individual_frames": generated_frames,
            "animation_metadata": animator_metadata,
            "frame_count": len(generated_frames),
            "sheet_layout": sheet_layout
        }

    async def _create_sprite_sheet(self, frame_paths: List[str], layout: Dict, name: str) -> str:
        """Combine individual frames into a sprite sheet."""
        try:
            from PIL import Image
        except ImportError:
            self.log("❌ PIL not available for sprite sheet creation", "ERROR")
            return None

        # Calculate sprite sheet dimensions
        sheet_width = layout["columns"] * layout["frame_width"] + (layout["columns"] - 1) * layout["spacing"] + 2 * layout["padding"]
        sheet_height = layout["rows"] * layout["frame_height"] + (layout["rows"] - 1) * layout["spacing"] + 2 * layout["padding"]

        # Create sprite sheet image
        sprite_sheet = Image.new("RGBA", (sheet_width, sheet_height), (0, 0, 0, 0))

        for i, frame_path in enumerate(frame_paths):
            if i >= layout["columns"] * layout["rows"]:
                break

            # Calculate position in grid
            col = i % layout["columns"]
            row = i // layout["columns"]

            # Calculate pixel position
            x = layout["padding"] + col * (layout["frame_width"] + layout["spacing"])
            y = layout["padding"] + row * (layout["frame_height"] + layout["spacing"])

            # Load and paste frame
            frame = Image.open(frame_path)
            frame = frame.resize((layout["frame_width"], layout["frame_height"]), Image.Resampling.LANCZOS)
            sprite_sheet.paste(frame, (x, y), frame if frame.mode == "RGBA" else None)

        # Save sprite sheet
        sheet_path = f"/Users/qusaiabushanap/dev/amani/Assets/Generated/sprite_sheets/{name}_sheet.png"
        Path(sheet_path).parent.mkdir(parents=True, exist_ok=True)
        sprite_sheet.save(sheet_path)

        return sheet_path

    def _generate_unity_animator_metadata(self, frame_count: int, layout: Dict) -> Dict:
        """Generate Unity Animator Controller metadata."""
        return {
            "AnimatorController": {
                "serializedVersion": 5,
                "m_AnimatorParameters": [],
                "m_AnimatorLayers": [{
                    "serializedVersion": 5,
                    "m_Name": "Base Layer",
                    "m_StateMachine": {
                        "m_States": [{
                            "serializedVersion": 1,
                            "m_State": {
                                "m_Name": "Animation",
                                "m_Speed": 1,
                                "m_Motion": {
                                    "frameCount": frame_count,
                                    "frameRate": 12,
                                    "wrapMode": 2  # Loop
                                }
                            }
                        }]
                    }
                }]
            },
            "sprite_sheet_config": {
                "spritePackingMode": 1,  # Rectangle
                "spritePackingRotation": 0,
                "userDefinedSlices": [
                    {
                        "serializedVersion": 2,
                        "rect": {
                            "serializedVersion": 2,
                            "x": layout["padding"] + (i % layout["columns"]) * (layout["frame_width"] + layout["spacing"]),
                            "y": layout["padding"] + (i // layout["columns"]) * (layout["frame_height"] + layout["spacing"]),
                            "width": layout["frame_width"],
                            "height": layout["frame_height"]
                        },
                        "alignment": 0,
                        "pivot": {"x": 0.5, "y": 0.5},
                        "border": {"x": 0, "y": 0, "z": 0, "w": 0},
                        "name": f"frame_{i:02d}"
                    }
                    for i in range(frame_count)
                ]
            }
        }

    async def _download_and_validate_images(self, images: List[Dict], download_dir: str, prompt: str) -> List[Dict]:
        """Download images and validate they exist and are valid."""
        
        download_results = []
        download_path = Path(download_dir)
        download_path.mkdir(parents=True, exist_ok=True)
        
        for i, image in enumerate(images):
            try:
                image_url = image.get("url")
                if not image_url:
                    download_results.append({
                        "success": False,
                        "error": "No URL provided",
                        "index": i
                    })
                    continue
                
                # Create local filename
                safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_prompt = safe_prompt.replace(' ', '_')
                filename = f"{safe_prompt}_{i+1}_{int(time.time())}.png"
                local_path = download_path / filename
                
                self.log(f"📥 Downloading image {i+1}/{len(images)}: {filename}")
                
                # Download with requests (more reliable for file downloads)
                response = requests.get(image_url, stream=True, timeout=30)
                if response.status_code == 200:
                    with open(local_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    # Validate file was created and has content
                    if local_path.exists() and local_path.stat().st_size > 1000:  # At least 1KB
                        self.session_stats["downloads_successful"] += 1
                        self.log(f"✅ Downloaded and validated: {local_path}")
                        download_results.append({
                            "success": True,
                            "local_path": str(local_path),
                            "url": image_url,
                            "file_size": local_path.stat().st_size,
                            "index": i
                        })
                    else:
                        download_results.append({
                            "success": False,
                            "error": "File validation failed",
                            "local_path": str(local_path),
                            "index": i
                        })
                else:
                    download_results.append({
                        "success": False,
                        "error": f"HTTP {response.status_code}",
                        "url": image_url,
                        "index": i
                    })
                    
            except Exception as e:
                self.log(f"❌ Download error for image {i}: {str(e)}", "ERROR")
                download_results.append({
                    "success": False,
                    "error": str(e),
                    "index": i
                })
        
        successful_downloads = [r for r in download_results if r["success"]]
        self.log(f"📊 Download summary: {len(successful_downloads)}/{len(images)} successful")
        
        return download_results

# CLI Interface for testing
async def main():
    """CLI for testing the enhanced client."""
    if len(sys.argv) < 2:
        print("🎨 Enhanced Scenario AI Client")
        print("\nUsage:")
        print("  python enhanced_scenario_client.py test                    # Test connection")
        print("  python enhanced_scenario_client.py models                 # Discover account models")
        print("  python enhanced_scenario_client.py public                 # Check public models")
        print("  python enhanced_scenario_client.py verify <model_id>...   # Verify specific model IDs")
        print("  python enhanced_scenario_client.py generate [prompt]      # Generate and download sample")
        return
    
    command = sys.argv[1]
    client = EnhancedScenarioClient(debug=True)
    
    if command == "test":
        result = await client.test_connection_with_diagnostics()
        print(json.dumps(result, indent=2))
        
    elif command == "models":
        result = await client.discover_models_with_filtering(["realistic", "stylized"])
        print(f"\n🎯 DISCOVERED MODELS:")
        for category, models in result.get("categorized", {}).items():
            print(f"\n{category.upper()}: {len(models)} models")
            for model in models[:3]:  # Show first 3 in each category
                print(f"  - {model.get('id')} ({model.get('name', 'Unknown')})")
                
    elif command == "public":
        result = await client.check_public_models()
        print(json.dumps(result, indent=2))
        
    elif command == "verify":
        if len(sys.argv) < 3:
            print("❌ Usage: python enhanced_scenario_client.py verify <model_id1> <model_id2> ...")
            return
        
        model_ids = sys.argv[2:]
        result = await client.verify_models_batch(model_ids)
        print(json.dumps(result, indent=2))
        
    elif command == "generate":
        prompt = sys.argv[2] if len(sys.argv) > 2 else "majestic falcon, game character, detailed feathers, transparent background"
        download_dir = "/Users/qusaiabushanap/dev/amani/Assets/Generated/ArtDirection/test_samples"
        
        print(f"🎨 Generating: '{prompt}'")
        result = await client.generate_and_download_with_validation(
            prompt=prompt,
            download_dir=download_dir,
            width=512,
            height=512
        )
        
        print(json.dumps({
            "success": result["success"],
            "message": result["message"],
            "local_paths": result.get("local_paths", []),
            "stats": result.get("stats", {})
        }, indent=2))
        
    else:
        print("❌ Invalid command. Use 'test', 'models', or 'generate'")

if __name__ == "__main__":
    asyncio.run(main())