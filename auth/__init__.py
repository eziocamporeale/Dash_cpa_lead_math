"""
Auth package per Dashboard Unificata
"""

from .unified_auth import (
    UnifiedAuthSystem,
    auth_system,
    require_auth,
    get_current_user,
    get_current_project,
    switch_project,
    is_authenticated,
    logout,
    authenticate
)

__all__ = [
    'UnifiedAuthSystem',
    'auth_system',
    'require_auth',
    'get_current_user',
    'get_current_project',
    'switch_project',
    'is_authenticated',
    'logout',
    'authenticate'
]
