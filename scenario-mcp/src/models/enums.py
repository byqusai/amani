"""Enums and constants for Scenario API."""

from enum import Enum
from typing import List


class SchedulerType(str, Enum):
    """Available scheduler types for generation."""
    EULER_ANCESTRAL_DISCRETE = "EulerAncestralDiscrete"
    EULER_DISCRETE = "EulerDiscrete"
    DDIM = "DDIM"
    DDPM = "DDPM"
    HEUN_DISCRETE = "HeunDiscrete"
    DPM_SOLVER_MULTISTEP = "DPMSolverMultistep"


class ControlNetType(str, Enum):
    """ControlNet control types."""
    POSE = "pose"
    DEPTH = "depth"
    CANNY = "canny"
    OPENPOSE = "openpose"
    SCRIBBLE = "scribble"
    NORMAL = "normal"
    LINEART = "lineart"


class ModelCategory(str, Enum):
    """Model categories."""
    PUBLIC = "public"
    PRIVATE = "private"
    COMMUNITY = "community"
    CUSTOM = "custom"


class AssetOrganization(str, Enum):
    """Asset organization methods."""
    DATE = "date"
    MODEL = "model"
    PROMPT_HASH = "prompt_hash"
    CUSTOM = "custom"


class GenerationStatus(str, Enum):
    """Generation job statuses."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ModelType(str, Enum):
    """3D model types."""
    MESH = "mesh"
    TEXTURE = "texture"
    MATERIAL = "material"
    FULL_SCENE = "full_scene"


# Common model IDs
POPULAR_MODELS = {
    "flux.1-dev": "Flux.1 Dev - High quality general purpose",
    "flux.1-schnell": "Flux.1 Schnell - Fast generation",
    "sdxl-1.0": "Stable Diffusion XL 1.0",
    "sd-v1.5": "Stable Diffusion v1.5",
    "midjourney-v5": "Midjourney v5 style",
}

# Default image dimensions
STANDARD_DIMENSIONS = [
    (512, 512),    # Square SD 1.5
    (768, 768),    # Square HD
    (1024, 1024),  # Square XL
    (512, 768),    # Portrait SD
    (768, 512),    # Landscape SD
    (1024, 768),   # Landscape XL
    (768, 1024),   # Portrait XL
]

# Supported file formats
SUPPORTED_IMAGE_FORMATS = ["png", "jpg", "jpeg", "webp"]
SUPPORTED_VIDEO_FORMATS = ["mp4", "gif", "webm"]
SUPPORTED_3D_FORMATS = ["obj", "fbx", "gltf", "glb"]