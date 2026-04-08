# register the completion scripts since they are not required to be registered anywhere else
import os
from typing import Optional

from . import bash_gte_42, powershell_completion  # noqa: F401


def get_tenant_for_api_completion() -> Optional[str]:
    """Resolve the tenant for API completion from environment or config."""
    tenant = os.getenv('BRITIVE_TENANT')
    if not tenant:
        from pybritive.helpers.config import ConfigManager  # noqa: PLC0415

        config = ConfigManager(None)
        config.load()
        if config.default_tenant and config.default_tenant in config.tenants:
            tenant = config.tenants[config.default_tenant].get('name')
    if not tenant:
        return None
    if not tenant.endswith('.britive-app.com'):
        tenant = f'{tenant.strip()}.britive-app.com'
    return tenant
