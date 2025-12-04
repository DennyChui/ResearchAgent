"""
Configuration module for ResearchAgent

This module handles loading and managing environment variables
from .env file and system environment.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


def load_env():
    """Load environment variables from .env file."""
    # Get the project root directory (where .env file should be)
    project_root = Path(__file__).parent.parent
    env_file = project_root / '.env'
    
    # Load .env file if it exists
    if env_file.exists():
        load_dotenv(env_file)
        print(f"✅ Environment variables loaded from {env_file}")
    else:
        print("⚠️  .env file not found. Using system environment variables only.")
        print(f"💡 Create .env file from .env.example template at: {env_file}")


def get_api_key(key_name: str, default: Optional[str] = None) -> str:
    """
    Get API key from environment variables.
    
    Args:
        key_name: Name of the environment variable
        default: Default value if not found
        
    Returns:
        API key value
        
    Raises:
        ValueError: If the key is required and not found
    """
    value = os.getenv(key_name, default)
    if not value:
        raise ValueError(f"❌ Required environment variable '{key_name}' is not set")
    return value


def get_sandbox_endpoints() -> list:
    """
    Get sandbox endpoints from environment variables.
    
    Returns:
        List of sandbox endpoint URLs
    """
    endpoints_str = os.getenv('SANDBOX_FUSION_ENDPOINT', 'http://localhost:8081')
    # Split by comma and strip whitespace
    endpoints = [endpoint.strip() for endpoint in endpoints_str.split(',') if endpoint.strip()]
    
    if not endpoints:
        raise ValueError("❌ No valid sandbox endpoints configured")
    
    return endpoints


def validate_required_keys():
    """Validate that all required API keys are present."""
    required_keys = ['LLM_API_KEY', 'SERPER_KEY_ID', 'JINA_API_KEY']
    # LLM_MODEL and LLM_MODEL_SERVER are optional with defaults
    missing_keys = []
    
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        error_msg = "❌ Missing required environment variables:\n"
        for key in missing_keys:
            error_msg += f"   - {key}\n"
        error_msg += "\n💡 Please set these variables in your .env file or system environment."
        raise ValueError(error_msg)
    
    print("✅ All required API keys are configured")


# Auto-load environment variables when module is imported
load_env()
