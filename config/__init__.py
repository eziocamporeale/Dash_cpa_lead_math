"""
Config package per Dashboard Unificata
"""

from .unified_config import (
    UnifiedConfig,
    get_config,
    get_supabase_config,
    get_ai_config,
    get_auth_config,
    get_app_config,
    get_security_config
)

__all__ = [
    'UnifiedConfig',
    'get_config',
    'get_supabase_config',
    'get_ai_config',
    'get_auth_config',
    'get_app_config',
    'get_security_config'
]
