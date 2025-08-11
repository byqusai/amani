"""File management utilities."""

import os
import json
import hashlib
import aiofiles
import aiohttp
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import structlog

from ..models.enums import AssetOrganization
from ..exceptions import AssetError

logger = structlog.get_logger(__name__)


class FileManager:
    """Manages file operations for assets and metadata."""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    async def download_asset(self, url: str, filename: str, 
                           subfolder: Optional[str] = None) -> Tuple[str, int]:
        """Download asset from URL to local file."""
        try:
            if subfolder:
                download_path = self.base_path / subfolder
            else:
                download_path = self.base_path
            
            download_path.mkdir(parents=True, exist_ok=True)
            file_path = download_path / filename
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    
                    file_size = 0
                    async with aiofiles.open(file_path, 'wb') as file:
                        async for chunk in response.content.iter_chunked(8192):
                            await file.write(chunk)
                            file_size += len(chunk)
                    
                    logger.info(f"Downloaded asset: {file_path} ({file_size} bytes)")
                    return str(file_path), file_size
        
        except Exception as e:
            logger.error(f"Failed to download asset from {url}: {str(e)}")
            raise AssetError(f"Download failed: {str(e)}")
    
    def organize_path(self, asset_info: Dict[str, Any], 
                     organization: AssetOrganization) -> str:
        """Generate organized subfolder path for asset."""
        if organization == AssetOrganization.DATE:
            now = datetime.now()
            return now.strftime("%Y/%m/%d")
        
        elif organization == AssetOrganization.MODEL:
            model_id = asset_info.get('model_id', 'unknown')
            return f"models/{model_id}"
        
        elif organization == AssetOrganization.PROMPT_HASH:
            prompt = asset_info.get('prompt', '')
            prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
            return f"prompts/{prompt_hash}"
        
        else:  # CUSTOM or fallback
            return asset_info.get('custom_path', 'generated')
    
    def generate_filename(self, asset_id: str, prompt: str, 
                         extension: str = "png", index: int = 0) -> str:
        """Generate descriptive filename for asset."""
        # Clean prompt for filename
        clean_prompt = self._sanitize_filename(prompt)
        
        # Truncate if too long
        if len(clean_prompt) > 50:
            clean_prompt = clean_prompt[:50] + "..."
        
        if index > 0:
            return f"{clean_prompt}_{asset_id}_{index}.{extension}"
        else:
            return f"{clean_prompt}_{asset_id}.{extension}"
    
    def _sanitize_filename(self, text: str) -> str:
        """Sanitize text for use in filename."""
        import re
        # Remove or replace problematic characters
        sanitized = re.sub(r'[^\w\s-]', '', text)
        sanitized = re.sub(r'[-\s]+', '_', sanitized)
        return sanitized.strip('_').lower()
    
    async def save_metadata(self, asset_id: str, metadata: Dict[str, Any], 
                          subfolder: Optional[str] = None) -> str:
        """Save asset metadata as JSON file."""
        try:
            if subfolder:
                metadata_path = self.base_path / subfolder
            else:
                metadata_path = self.base_path
            
            metadata_path.mkdir(parents=True, exist_ok=True)
            filename = f"{asset_id}_metadata.json"
            file_path = metadata_path / filename
            
            # Add timestamp if not present
            if 'saved_at' not in metadata:
                metadata['saved_at'] = datetime.now().isoformat()
            
            async with aiofiles.open(file_path, 'w') as file:
                await file.write(json.dumps(metadata, indent=2))
            
            logger.debug(f"Saved metadata: {file_path}")
            return str(file_path)
        
        except Exception as e:
            logger.error(f"Failed to save metadata for {asset_id}: {str(e)}")
            raise AssetError(f"Metadata save failed: {str(e)}")
    
    async def load_metadata(self, asset_id: str, 
                          subfolder: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Load asset metadata from JSON file."""
        try:
            if subfolder:
                metadata_path = self.base_path / subfolder
            else:
                metadata_path = self.base_path
            
            filename = f"{asset_id}_metadata.json"
            file_path = metadata_path / filename
            
            if not file_path.exists():
                return None
            
            async with aiofiles.open(file_path, 'r') as file:
                content = await file.read()
                return json.loads(content)
        
        except Exception as e:
            logger.error(f"Failed to load metadata for {asset_id}: {str(e)}")
            return None
    
    def get_organization_structure(self) -> Dict[str, List[str]]:
        """Get current file organization structure."""
        structure = {}
        
        try:
            for root, dirs, files in os.walk(self.base_path):
                rel_path = os.path.relpath(root, self.base_path)
                if rel_path == '.':
                    rel_path = 'root'
                
                # Filter out metadata files for cleaner structure
                asset_files = [f for f in files if not f.endswith('_metadata.json')]
                
                if asset_files:
                    structure[rel_path] = asset_files
        
        except Exception as e:
            logger.error(f"Failed to get organization structure: {str(e)}")
        
        return structure
    
    async def cleanup_orphaned_files(self) -> Dict[str, int]:
        """Clean up orphaned files (assets without metadata or vice versa)."""
        try:
            orphaned_assets = []
            orphaned_metadata = []
            
            for root, dirs, files in os.walk(self.base_path):
                asset_files = [f for f in files if not f.endswith('_metadata.json')]
                metadata_files = [f for f in files if f.endswith('_metadata.json')]
                
                # Extract asset IDs
                asset_ids = set()
                for asset_file in asset_files:
                    # Try to extract asset ID from filename
                    parts = asset_file.rsplit('_', 1)
                    if len(parts) > 1:
                        asset_id = parts[1].split('.')[0]
                        asset_ids.add(asset_id)
                
                metadata_ids = set()
                for metadata_file in metadata_files:
                    asset_id = metadata_file.replace('_metadata.json', '')
                    metadata_ids.add(asset_id)
                
                # Find orphans
                orphaned_assets.extend([
                    os.path.join(root, f) for f in asset_files 
                    if not any(aid in f for aid in metadata_ids)
                ])
                
                orphaned_metadata.extend([
                    os.path.join(root, f) for f in metadata_files
                    if f.replace('_metadata.json', '') not in asset_ids
                ])
            
            # Cleanup (optional - could return list for user decision)
            cleanup_stats = {
                'orphaned_assets_found': len(orphaned_assets),
                'orphaned_metadata_found': len(orphaned_metadata),
                'orphaned_assets_removed': 0,
                'orphaned_metadata_removed': 0
            }
            
            logger.info(f"Found {len(orphaned_assets)} orphaned assets and {len(orphaned_metadata)} orphaned metadata files")
            
            return cleanup_stats
        
        except Exception as e:
            logger.error(f"Failed to cleanup orphaned files: {str(e)}")
            return {'error': str(e)}