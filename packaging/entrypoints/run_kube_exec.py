"""Frozen entry point for the `pybritive-kube-exec` helper.

Invoked by kubectl via the kubeconfig `exec` credential plugin, so it runs on
every kubectl command. This is the most startup-sensitive path, which is why
the binaries are built in PyInstaller onedir mode (no per-launch unpack).
"""

from pybritive.helpers.k8s_exec import main

if __name__ == '__main__':
    main()
