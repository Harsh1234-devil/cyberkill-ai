"""Configuration settings for Cyberkill.ai using Pydantic."""

from typing import List
from pydantic import BaseModel, Field

class ScopeConfig(BaseModel):
    allowed_domains: List[str] = Field(default_factory=lambda: ["localhost", "127.0.0.1", "*.local", "*.lab"])
    allowed_cidrs: List[str] = Field(default_factory=lambda: ["127.0.0.1/32", "10.0.0.0/8", "192.168.0.0/16", "172.16.0.0/12"])
    disallowed_domains: List[str] = Field(
        default_factory=lambda: [
            "*.gov",
            "*.mil",
            "*.edu",
            "*.gov.in",
            "*.nic.in",
            "google.com",
            "microsoft.com",
            "amazon.com",
            "apple.com"
        ]
    )
    strict_enforcement: bool = True

class CyberkillSettings(BaseModel):
    app_name: str = "Cyberkill.ai"
    version: str = "1.0.0"
    author: str = "Harsh Vardhan"
    server_host: str = "0.0.0.0"
    server_port: int = 8888
    debug: bool = False
    max_concurrent_processes: int = 16
    default_timeout_seconds: int = 300
    cache_ttl_seconds: int = 3600
    cache_max_items: int = 1000
    log_level: str = "INFO"
    scope: ScopeConfig = Field(default_factory=ScopeConfig)

settings = CyberkillSettings()
