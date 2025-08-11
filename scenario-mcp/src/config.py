"""Configuration management for Scenario MCP Server."""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class ScenarioMCPConfig:
    """Configuration settings for Scenario MCP Server."""
    
    # Scenario API Configuration
    scenario_api_key: Optional[str] = None
    scenario_api_secret: Optional[str] = None
    scenario_api_base_url: str = "https://api.cloud.scenario.com/v1"
    
    # Server Configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Performance & Rate Limiting
    max_concurrent_requests: int = 5
    request_timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0
    connection_pool_size: int = 10
    
    # Asset Management
    default_download_path: str = "./scenario_assets"
    organize_assets_by: str = "date"  # date, model, prompt_hash, custom
    
    # Cost Management
    enable_cost_estimation: bool = True
    max_credits_per_batch: int = 1000
    
    # Buffer Settings
    buffer_size: int = 16 * 1024 * 1024  # 16MB
    
    def __post_init__(self):
        """Load configuration from environment variables."""
        # API Configuration
        self.scenario_api_key = os.getenv("SCENARIO_API_KEY", self.scenario_api_key)
        self.scenario_api_secret = os.getenv("SCENARIO_API_SECRET", self.scenario_api_secret)
        self.scenario_api_base_url = os.getenv("SCENARIO_API_BASE_URL", self.scenario_api_base_url)
        
        # Server Configuration
        self.log_level = os.getenv("LOG_LEVEL", self.log_level)
        self.log_format = os.getenv("LOG_FORMAT", self.log_format)
        
        # Performance Settings
        self.max_concurrent_requests = int(os.getenv("MAX_CONCURRENT_REQUESTS", self.max_concurrent_requests))
        self.request_timeout = float(os.getenv("REQUEST_TIMEOUT", self.request_timeout))
        self.max_retries = int(os.getenv("MAX_RETRIES", self.max_retries))
        self.retry_delay = float(os.getenv("RETRY_DELAY", self.retry_delay))
        
        # Asset Management
        self.default_download_path = os.getenv("DEFAULT_DOWNLOAD_PATH", self.default_download_path)
        self.organize_assets_by = os.getenv("ORGANIZE_ASSETS_BY", self.organize_assets_by)
        
        # Cost Management
        self.enable_cost_estimation = os.getenv("ENABLE_COST_ESTIMATION", "true").lower() == "true"
        self.max_credits_per_batch = int(os.getenv("MAX_CREDITS_PER_BATCH", self.max_credits_per_batch))
    
    def validate(self) -> bool:
        """Validate required configuration."""
        if not self.scenario_api_key:
            raise ValueError("SCENARIO_API_KEY is required")
        if not self.scenario_api_secret:
            raise ValueError("SCENARIO_API_SECRET is required")
        return True
    
    @property
    def auth_header(self) -> str:
        """Get basic authentication header value."""
        import base64
        if not self.scenario_api_key or not self.scenario_api_secret:
            raise ValueError("API key and secret required for authentication")
        
        credentials = f"{self.scenario_api_key}:{self.scenario_api_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"


# Global configuration instance
config = ScenarioMCPConfig()