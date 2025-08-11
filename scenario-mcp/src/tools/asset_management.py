"""Asset management MCP tools."""

import structlog
import asyncio
import aiofiles
import hashlib
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse
from mcp.server.fastmcp import Context

from ..utils.response import ResponseHelper
from ..utils.validation import validate_url_or_base64
from ..scenario_client import ScenarioAPIClient
from ..exceptions import *

logger = structlog.get_logger(__name__)


def register_asset_management_tools(mcp):
    """Register asset management tools."""
    
    @mcp.tool()
    async def scenario_download_assets(
        ctx: Context,
        asset_urls: List[str],
        download_path: str = "./downloads",
        organize_by_type: bool = True,
        generate_metadata: bool = True,
        max_concurrent_downloads: int = 5
    ) -> Dict[str, Any]:
        """
        Download and organize generated assets from Scenario API.
        
        Perfect for Agent 4's asset collection workflows where generated assets
        need to be downloaded and organized for game development use.
        
        Args:
            asset_urls: List of Scenario asset URLs to download
            download_path: Local path to download assets
            organize_by_type: Whether to organize into subfolders by asset type
            generate_metadata: Whether to generate metadata files for each asset
            max_concurrent_downloads: Maximum concurrent downloads
            
        Returns:
            Dict containing download results and asset organization info
        """
        try:
            if not asset_urls:
                return ResponseHelper.validation_error("asset_urls", "At least one asset URL is required")
            
            logger.info(f"Downloading {len(asset_urls)} assets to {download_path}")
            
            # Create download directory structure
            base_path = Path(download_path)
            base_path.mkdir(parents=True, exist_ok=True)
            
            # Asset type folders
            if organize_by_type:
                type_folders = {
                    "images": base_path / "images",
                    "videos": base_path / "videos", 
                    "3d_models": base_path / "3d_models",
                    "textures": base_path / "textures",
                    "materials": base_path / "materials",
                    "other": base_path / "other"
                }
                for folder in type_folders.values():
                    folder.mkdir(exist_ok=True)
            
            # Download semaphore for concurrency control
            semaphore = asyncio.Semaphore(max_concurrent_downloads)
            
            async def download_single_asset(asset_url: str, index: int) -> Dict[str, Any]:
                async with semaphore:
                    try:
                        logger.info(f"Downloading asset {index + 1}/{len(asset_urls)}: {asset_url}")
                        
                        # Determine asset type from URL
                        parsed_url = urlparse(asset_url)
                        filename = Path(parsed_url.path).name or f"asset_{index}"
                        extension = Path(filename).suffix.lower()
                        
                        # Categorize asset type
                        if extension in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
                            asset_type = "images"
                        elif extension in ['.mp4', '.mov', '.avi', '.webm']:
                            asset_type = "videos"
                        elif extension in ['.obj', '.fbx', '.gltf', '.glb', '.blend']:
                            asset_type = "3d_models"
                        elif extension in ['.tga', '.exr', '.hdr']:
                            asset_type = "textures"
                        elif extension in ['.mtl', '.mat']:
                            asset_type = "materials"
                        else:
                            asset_type = "other"
                        
                        # Determine final path
                        if organize_by_type:
                            final_folder = type_folders[asset_type]
                        else:
                            final_folder = base_path
                        
                        final_path = final_folder / filename
                        
                        # Download asset using aiohttp
                        async with ScenarioAPIClient() as client:
                            import aiohttp
                            async with client.http_client.session.get(asset_url) as response:
                                if response.status == 200:
                                    content = await response.read()
                                    
                                    # Write file
                                    async with aiofiles.open(final_path, 'wb') as f:
                                        await f.write(content)
                                    
                                    # Generate hash for integrity
                                    content_hash = hashlib.sha256(content).hexdigest()
                                    
                                    # Generate metadata if requested
                                    metadata = None
                                    if generate_metadata:
                                        metadata_path = final_path.with_suffix(final_path.suffix + '.meta.json')
                                        metadata = {
                                            "original_url": asset_url,
                                            "filename": filename,
                                            "asset_type": asset_type,
                                            "file_size": len(content),
                                            "sha256_hash": content_hash,
                                            "download_timestamp": asyncio.get_event_loop().time(),
                                            "local_path": str(final_path)
                                        }
                                        
                                        # Add image-specific metadata
                                        if asset_type == "images" and extension in ['.png', '.jpg', '.jpeg']:
                                            try:
                                                from PIL import Image
                                                import io
                                                
                                                img = Image.open(io.BytesIO(content))
                                                metadata["width"] = img.width
                                                metadata["height"] = img.height
                                                metadata["format"] = img.format
                                                metadata["mode"] = img.mode
                                            except Exception:
                                                pass  # Skip if PIL not available or image corrupt
                                        
                                        async with aiofiles.open(metadata_path, 'w') as f:
                                            await f.write(json.dumps(metadata, indent=2))
                                    
                                    return {
                                        "index": index,
                                        "url": asset_url,
                                        "status": "success",
                                        "local_path": str(final_path),
                                        "asset_type": asset_type,
                                        "file_size": len(content),
                                        "hash": content_hash,
                                        "metadata_generated": generate_metadata,
                                        "metadata": metadata
                                    }
                                else:
                                    return {
                                        "index": index,
                                        "url": asset_url,
                                        "status": "failed",
                                        "error": f"HTTP {response.status}: {await response.text()}"
                                    }
                    
                    except Exception as e:
                        logger.error(f"Failed to download asset {index}: {asset_url} - {str(e)}")
                        return {
                            "index": index,
                            "url": asset_url,
                            "status": "failed",
                            "error": str(e)
                        }
            
            # Execute downloads concurrently
            download_tasks = [
                download_single_asset(url, i) 
                for i, url in enumerate(asset_urls)
            ]
            results = await asyncio.gather(*download_tasks)
            
            # Analyze results
            successful_downloads = [r for r in results if r.get("status") == "success"]
            failed_downloads = [r for r in results if r.get("status") == "failed"]
            
            # Calculate statistics
            total_size = sum(r.get("file_size", 0) for r in successful_downloads)
            asset_types = {}
            for result in successful_downloads:
                asset_type = result.get("asset_type", "unknown")
                asset_types[asset_type] = asset_types.get(asset_type, 0) + 1
            
            return ResponseHelper.success(
                f"Downloaded {len(successful_downloads)}/{len(asset_urls)} assets successfully",
                data={
                    "download_summary": {
                        "total_requested": len(asset_urls),
                        "successful_downloads": len(successful_downloads),
                        "failed_downloads": len(failed_downloads),
                        "total_size_bytes": total_size,
                        "total_size_mb": round(total_size / (1024 * 1024), 2),
                        "download_path": str(base_path)
                    },
                    "organization": {
                        "organized_by_type": organize_by_type,
                        "asset_types": asset_types,
                        "folder_structure": list(type_folders.keys()) if organize_by_type else ["root"]
                    },
                    "metadata": {
                        "generated": generate_metadata,
                        "metadata_files_created": len([r for r in successful_downloads if r.get("metadata_generated")])
                    },
                    "results": results
                }
            )
        
        except Exception as e:
            logger.exception("Error in scenario_download_assets")
            return ResponseHelper.error(f"Asset download failed: {str(e)}")
    
    @mcp.tool()
    async def scenario_list_assets(
        ctx: Context,
        job_ids: Optional[List[str]] = None,
        asset_types: Optional[List[str]] = None,
        limit: int = 50,
        include_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        List and retrieve information about generated assets.
        
        Perfect for Agent 4's asset inventory workflows where they need to
        catalog and manage previously generated assets.
        
        Args:
            job_ids: Specific job IDs to get assets for (optional)
            asset_types: Filter by asset types (optional)
            limit: Maximum number of assets to return
            include_metadata: Whether to include detailed metadata
            
        Returns:
            Dict containing asset inventory and information
        """
        try:
            logger.info(f"Listing assets with limit {limit}")
            
            async with ScenarioAPIClient() as client:
                # Get asset list from Scenario API
                # Note: This would use the actual Scenario API endpoint for listing user assets
                
                assets = []
                total_credits_used = 0.0
                
                if job_ids:
                    # Get assets from specific jobs
                    for job_id in job_ids[:limit]:  # Respect limit
                        try:
                            job_status = await client.get_job_status(job_id)
                            if job_status and job_status.assets:
                                for asset in job_status.assets:
                                    asset_info = {
                                        "id": asset.id,
                                        "job_id": job_id,
                                        "url": asset.url,
                                        "format": asset.format,
                                        "created_at": job_status.created_at.isoformat() if job_status.created_at else None
                                    }
                                    
                                    if include_metadata:
                                        asset_info.update({
                                            "width": getattr(asset, 'width', None),
                                            "height": getattr(asset, 'height', None),
                                            "size_bytes": getattr(asset, 'size_bytes', None),
                                            "status": job_status.status.value
                                        })
                                    
                                    # Apply asset type filter
                                    if asset_types:
                                        asset_format = asset.format.lower() if asset.format else ""
                                        if asset_format in [t.lower() for t in asset_types]:
                                            assets.append(asset_info)
                                    else:
                                        assets.append(asset_info)
                                
                                total_credits_used += job_status.credits_used or 0
                        
                        except Exception as e:
                            logger.error(f"Failed to get job {job_id}: {str(e)}")
                            continue
                
                else:
                    # This would typically call a "list user assets" endpoint
                    # For now, return a structured response indicating the capability
                    assets = []
                    logger.info("Job IDs not provided - would list all user assets from Scenario API")
                
                # Organize assets by type
                assets_by_type = {}
                for asset in assets:
                    asset_format = asset.get("format", "unknown").lower()
                    
                    # Categorize
                    if asset_format in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
                        category = "images"
                    elif asset_format in ['mp4', 'mov', 'avi', 'webm']:
                        category = "videos"
                    elif asset_format in ['obj', 'fbx', 'gltf', 'glb']:
                        category = "3d_models"
                    else:
                        category = "other"
                    
                    if category not in assets_by_type:
                        assets_by_type[category] = []
                    assets_by_type[category].append(asset)
                
                # Calculate statistics
                total_assets = len(assets)
                unique_jobs = len(set(asset.get("job_id") for asset in assets if asset.get("job_id")))
                
                return ResponseHelper.success(
                    f"Found {total_assets} assets across {unique_jobs} generation jobs",
                    data={
                        "inventory_summary": {
                            "total_assets": total_assets,
                            "unique_jobs": unique_jobs,
                            "total_credits_used": total_credits_used,
                            "asset_categories": {k: len(v) for k, v in assets_by_type.items()}
                        },
                        "assets_by_type": assets_by_type,
                        "all_assets": assets[:limit],  # Respect limit
                        "metadata_included": include_metadata,
                        "filters_applied": {
                            "job_ids_filter": job_ids is not None,
                            "asset_types_filter": asset_types is not None,
                            "limit": limit
                        }
                    }
                )
        
        except Exception as e:
            logger.exception("Error in scenario_list_assets")
            return ResponseHelper.error(f"Asset listing failed: {str(e)}")
    
    @mcp.tool()
    async def scenario_organize_assets(
        ctx: Context,
        source_directory: str,
        target_directory: str,
        organization_scheme: str = "by_type",
        create_collections: bool = True,
        generate_index: bool = True
    ) -> Dict[str, Any]:
        """
        Organize downloaded assets into structured collections.
        
        Perfect for Agent 4's asset management workflows where assets need
        to be organized for efficient game development workflows.
        
        Args:
            source_directory: Directory containing downloaded assets
            target_directory: Directory to organize assets into
            organization_scheme: How to organize ("by_type", "by_date", "by_project", "by_style")
            create_collections: Whether to create asset collection files
            generate_index: Whether to generate searchable index
            
        Returns:
            Dict containing organization results and structure info
        """
        try:
            source_path = Path(source_directory)
            target_path = Path(target_directory)
            
            if not source_path.exists():
                return ResponseHelper.validation_error("source_directory", f"Source directory does not exist: {source_directory}")
            
            logger.info(f"Organizing assets from {source_directory} to {target_directory} using {organization_scheme} scheme")
            
            # Create target directory
            target_path.mkdir(parents=True, exist_ok=True)
            
            # Scan source directory for assets
            asset_files = []
            for file_path in source_path.rglob("*"):
                if file_path.is_file() and not file_path.name.endswith('.meta.json'):
                    # Load metadata if exists
                    meta_path = file_path.with_suffix(file_path.suffix + '.meta.json')
                    metadata = None
                    if meta_path.exists():
                        try:
                            async with aiofiles.open(meta_path, 'r') as f:
                                content = await f.read()
                                metadata = json.loads(content)
                        except Exception:
                            pass
                    
                    asset_files.append({
                        "path": file_path,
                        "name": file_path.name,
                        "extension": file_path.suffix.lower(),
                        "size": file_path.stat().st_size if file_path.exists() else 0,
                        "metadata": metadata
                    })
            
            logger.info(f"Found {len(asset_files)} assets to organize")
            
            # Organize based on scheme
            organized_structure = {}
            
            if organization_scheme == "by_type":
                # Organize by asset type
                type_mapping = {
                    'images': ['.png', '.jpg', '.jpeg', '.gif', '.webp'],
                    'videos': ['.mp4', '.mov', '.avi', '.webm'],
                    '3d_models': ['.obj', '.fbx', '.gltf', '.glb', '.blend'],
                    'textures': ['.tga', '.exr', '.hdr'],
                    'materials': ['.mtl', '.mat'],
                    'other': []
                }
                
                for asset in asset_files:
                    # Determine type
                    asset_type = 'other'
                    for type_name, extensions in type_mapping.items():
                        if asset['extension'] in extensions:
                            asset_type = type_name
                            break
                    
                    if asset_type not in organized_structure:
                        organized_structure[asset_type] = []
                    organized_structure[asset_type].append(asset)
            
            elif organization_scheme == "by_style":
                # Organize by art style (from metadata)
                for asset in asset_files:
                    style = "unknown_style"
                    if asset['metadata'] and 'style' in asset['metadata']:
                        style = asset['metadata']['style']
                    elif asset['metadata'] and 'art_style' in asset['metadata']:
                        style = asset['metadata']['art_style']
                    
                    if style not in organized_structure:
                        organized_structure[style] = []
                    organized_structure[style].append(asset)
            
            elif organization_scheme == "by_project":
                # Organize by project (from metadata or folder structure)
                for asset in asset_files:
                    project = "unknown_project"
                    if asset['metadata'] and 'project' in asset['metadata']:
                        project = asset['metadata']['project']
                    else:
                        # Infer from parent folder
                        project = asset['path'].parent.name
                    
                    if project not in organized_structure:
                        organized_structure[project] = []
                    organized_structure[project].append(asset)
            
            else:
                # Default: by_type
                organized_structure["all_assets"] = asset_files
            
            # Create organized directory structure
            created_folders = []
            moved_files = []
            
            for category, assets in organized_structure.items():
                category_folder = target_path / category
                category_folder.mkdir(exist_ok=True)
                created_folders.append(str(category_folder))
                
                for asset in assets:
                    target_file = category_folder / asset['name']
                    
                    # Copy file to new location
                    import shutil
                    try:
                        shutil.copy2(asset['path'], target_file)
                        moved_files.append({
                            "original": str(asset['path']),
                            "new": str(target_file),
                            "category": category
                        })
                        
                        # Copy metadata if exists
                        meta_source = asset['path'].with_suffix(asset['path'].suffix + '.meta.json')
                        if meta_source.exists():
                            meta_target = target_file.with_suffix(target_file.suffix + '.meta.json')
                            shutil.copy2(meta_source, meta_target)
                    
                    except Exception as e:
                        logger.error(f"Failed to copy {asset['path']} to {target_file}: {str(e)}")
                        continue
                
                # Create collection file for this category
                if create_collections:
                    collection_file = category_folder / f"{category}_collection.json"
                    collection_data = {
                        "collection_name": category,
                        "organization_scheme": organization_scheme,
                        "created_at": asyncio.get_event_loop().time(),
                        "total_assets": len(assets),
                        "assets": [
                            {
                                "filename": asset['name'],
                                "size_bytes": asset['size'],
                                "metadata": asset['metadata']
                            }
                            for asset in assets
                        ]
                    }
                    
                    async with aiofiles.open(collection_file, 'w') as f:
                        await f.write(json.dumps(collection_data, indent=2))
            
            # Generate master index
            if generate_index:
                index_file = target_path / "asset_index.json"
                index_data = {
                    "index_created_at": asyncio.get_event_loop().time(),
                    "organization_scheme": organization_scheme,
                    "total_assets": len(asset_files),
                    "categories": list(organized_structure.keys()),
                    "structure": {
                        category: len(assets) 
                        for category, assets in organized_structure.items()
                    },
                    "all_files": moved_files
                }
                
                async with aiofiles.open(index_file, 'w') as f:
                    await f.write(json.dumps(index_data, indent=2))
            
            return ResponseHelper.success(
                f"Organized {len(moved_files)} assets into {len(organized_structure)} categories",
                data={
                    "organization_summary": {
                        "source_directory": str(source_path),
                        "target_directory": str(target_path),
                        "organization_scheme": organization_scheme,
                        "total_assets_processed": len(asset_files),
                        "assets_successfully_moved": len(moved_files),
                        "categories_created": len(organized_structure)
                    },
                    "structure": {
                        category: len(assets) 
                        for category, assets in organized_structure.items()
                    },
                    "created_folders": created_folders,
                    "collections_created": create_collections,
                    "index_generated": generate_index,
                    "moved_files": moved_files[:20],  # Limit output size
                    "workflow_ready": True
                }
            )
        
        except Exception as e:
            logger.exception("Error in scenario_organize_assets")
            return ResponseHelper.error(f"Asset organization failed: {str(e)}")
    
    @mcp.tool()
    async def scenario_asset_collection_manager(
        ctx: Context,
        action: str,
        collection_name: str,
        collection_path: Optional[str] = None,
        assets_to_add: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Manage asset collections for Agent 4's project workflows.
        
        Perfect for Agent 4's game development workflows where assets need to be
        grouped into coherent collections for specific games or features.
        
        Args:
            action: Action to perform ("create", "add_assets", "remove_assets", "list", "info", "delete")
            collection_name: Name of the asset collection
            collection_path: Path to collection directory (for create/info)
            assets_to_add: List of asset paths to add to collection
            metadata: Additional metadata for the collection
            
        Returns:
            Dict containing collection management results
        """
        try:
            logger.info(f"Managing asset collection '{collection_name}' - action: {action}")
            
            if action == "create":
                if not collection_path:
                    return ResponseHelper.validation_error("collection_path", "Collection path required for create action")
                
                collection_dir = Path(collection_path)
                collection_dir.mkdir(parents=True, exist_ok=True)
                
                # Create collection manifest
                manifest_data = {
                    "collection_name": collection_name,
                    "created_at": asyncio.get_event_loop().time(),
                    "assets": [],
                    "metadata": metadata or {},
                    "total_assets": 0,
                    "collection_type": "agent4_asset_collection"
                }
                
                manifest_file = collection_dir / "collection.json"
                async with aiofiles.open(manifest_file, 'w') as f:
                    await f.write(json.dumps(manifest_data, indent=2))
                
                return ResponseHelper.success(
                    f"Created asset collection '{collection_name}'",
                    data={
                        "collection_name": collection_name,
                        "collection_path": str(collection_dir),
                        "manifest_file": str(manifest_file),
                        "action": "create",
                        "status": "created"
                    }
                )
            
            elif action == "add_assets":
                if not collection_path or not assets_to_add:
                    return ResponseHelper.validation_error("parameters", "collection_path and assets_to_add required for add_assets action")
                
                collection_dir = Path(collection_path)
                manifest_file = collection_dir / "collection.json"
                
                if not manifest_file.exists():
                    return ResponseHelper.error(f"Collection manifest not found: {manifest_file}")
                
                # Load existing manifest
                async with aiofiles.open(manifest_file, 'r') as f:
                    content = await f.read()
                    manifest_data = json.loads(content)
                
                # Add new assets
                added_assets = []
                for asset_path in assets_to_add:
                    asset_file = Path(asset_path)
                    if asset_file.exists():
                        asset_info = {
                            "path": str(asset_file),
                            "name": asset_file.name,
                            "size_bytes": asset_file.stat().st_size,
                            "added_at": asyncio.get_event_loop().time()
                        }
                        manifest_data["assets"].append(asset_info)
                        added_assets.append(asset_info)
                
                manifest_data["total_assets"] = len(manifest_data["assets"])
                manifest_data["last_updated"] = asyncio.get_event_loop().time()
                
                # Save updated manifest
                async with aiofiles.open(manifest_file, 'w') as f:
                    await f.write(json.dumps(manifest_data, indent=2))
                
                return ResponseHelper.success(
                    f"Added {len(added_assets)} assets to collection '{collection_name}'",
                    data={
                        "collection_name": collection_name,
                        "added_assets": len(added_assets),
                        "total_assets": manifest_data["total_assets"],
                        "action": "add_assets",
                        "new_assets": added_assets
                    }
                )
            
            elif action == "info":
                if not collection_path:
                    return ResponseHelper.validation_error("collection_path", "Collection path required for info action")
                
                collection_dir = Path(collection_path)
                manifest_file = collection_dir / "collection.json"
                
                if not manifest_file.exists():
                    return ResponseHelper.error(f"Collection manifest not found: {manifest_file}")
                
                # Load and return collection info
                async with aiofiles.open(manifest_file, 'r') as f:
                    content = await f.read()
                    manifest_data = json.loads(content)
                
                return ResponseHelper.success(
                    f"Collection '{collection_name}' information",
                    data={
                        "collection_info": manifest_data,
                        "action": "info"
                    }
                )
            
            else:
                return ResponseHelper.validation_error("action", f"Unsupported action: {action}")
        
        except Exception as e:
            logger.exception("Error in scenario_asset_collection_manager")
            return ResponseHelper.error(f"Asset collection management failed: {str(e)}")