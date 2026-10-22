from pybritive.helpers.config import ConfigManager


def tenant_completer(ctx, param, incomplete):
    try:
        config = ConfigManager(None)
        config.load()
        tenants = list(config.tenants.keys())
    except Exception:
        tenants = []

    return [t for t in tenants if incomplete.lower() in t.lower()]
