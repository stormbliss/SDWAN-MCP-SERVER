#!/usr/bin/env python3
"""
Configuration file for SD-WAN MCP Server
"""
import os
from typing import Optional

class SDWANConfig:
    """Configuration class for SD-WAN settings"""
    
    def __init__(self):
        # SD-WAN network settings
        self.base_url: str = os.getenv("SDWAN_BASE_URL", "https://192.168.10.130:8443")
        self.auth_endpoint: str = "/j_security_check"
        
        # Authentication settings
        self.username: str = os.getenv("SDWAN_USERNAME", "admin")
        self.password: str = os.getenv("SDWAN_PASSWORD", "1")
        
        # Session settings
        self.session_timeout: int = int(os.getenv("SESSION_TIMEOUT", "3600"))  # 1 hour
        self.auto_reconnect: bool = os.getenv("AUTO_RECONNECT", "true").lower() == "true"
        
        # SSL settings
        self.verify_ssl: bool = os.getenv("VERIFY_SSL", "false").lower() == "true"
        
        # Logging settings
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.log_auth_details: bool = os.getenv("LOG_AUTH_DETAILS", "false").lower() == "true"
    
    @property
    def auth_url(self) -> str:
        """Get full authentication URL"""
        return f"{self.base_url}{self.auth_endpoint}"
    
    def update_credentials(self, username: Optional[str] = None, password: Optional[str] = None):
        """Update authentication credentials"""
        if username:
            self.username = username
        if password:
            self.password = password
    
    def __repr__(self):
        return f"SDWANConfig(base_url='{self.base_url}', username='{self.username}', verify_ssl={self.verify_ssl})"

# Global configuration instance
config = SDWANConfig()
