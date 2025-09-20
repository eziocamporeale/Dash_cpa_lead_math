"""
Database package per Dashboard Unificata
"""

from .unified_database_manager import (
    UnifiedDatabaseManager,
    get_database_manager,
    test_all_connections
)

__all__ = [
    'UnifiedDatabaseManager',
    'get_database_manager',
    'test_all_connections'
]
