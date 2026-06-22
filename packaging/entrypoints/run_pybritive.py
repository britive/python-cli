"""Frozen entry point for the main `pybritive` CLI.

PyInstaller builds one executable per script in packaging/entrypoints/. Each
shim simply forwards to the console-script callable declared in pyproject.toml
so the frozen binaries stay in lock-step with the pip install.
"""

from pybritive.cli_interface import safe_cli

if __name__ == '__main__':
    safe_cli()
