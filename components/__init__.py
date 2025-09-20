"""
Components package per Dashboard Unificata
"""

from .unified_components import (
    UnifiedForm,
    UnifiedTable,
    UnifiedChart,
    UnifiedMetrics,
    get_form,
    get_table,
    get_chart,
    get_metrics
)

from .login_form import (
    render_login_form,
    render_logout_section,
    render_auth_guard,
    render_user_info
)

__all__ = [
    'UnifiedForm',
    'UnifiedTable',
    'UnifiedChart',
    'UnifiedMetrics',
    'get_form',
    'get_table',
    'get_chart',
    'get_metrics',
    'render_login_form',
    'render_logout_section',
    'render_auth_guard',
    'render_user_info'
]
