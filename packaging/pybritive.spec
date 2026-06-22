# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for the standalone pybritive distribution.

Mirrors the AWS CLI v2 packaging model: a self-contained *onedir* bundle that
embeds its own Python interpreter, so the target machine never needs Python
installed. The three console scripts declared in pyproject.toml become three
launcher executables that share a single copy of the interpreter and libraries
(via PyInstaller's MERGE), keeping the bundle one-interpreter-sized.

Build (from the repo root, with pybritive + build deps installed):

    pyinstaller packaging/pybritive.spec --noconfirm

Output: dist/pybritive/  ->  contains `pybritive`, `pybritive-aws-cred-process`,
`pybritive-kube-exec` plus the shared `_internal/` runtime.

onedir (not onefile) is deliberate: pybritive-kube-exec and
pybritive-aws-cred-process are invoked on every kubectl / AWS credential
refresh, and onefile would re-unpack the whole bundle to a temp dir on each
launch. AWS CLI v2 makes the same choice for the same reason.
"""

import os

from PyInstaller.building.api import COLLECT, EXE, MERGE, PYZ
from PyInstaller.building.build_main import Analysis
from PyInstaller.utils.hooks import collect_submodules, copy_metadata

# SPECPATH is injected by PyInstaller and points at this spec's directory.
ENTRY_DIR = os.path.join(SPECPATH, 'entrypoints')

# --- shared data / hidden imports --------------------------------------------
# importlib.metadata.version('pybritive') is used by the --version output and by
# the kube-exec / aws-cred-process helpers; version('click') is read by the api
# command completer. Frozen apps don't ship dist-info unless we copy it in.
datas = []
datas += copy_metadata('pybritive')
datas += copy_metadata('click')

# The britive SDK is imported lazily/dynamically in places, so pull in every
# submodule. boto3 (AWS console / cred process) and bs4 (OpenShift OIDC) are
# imported inside function bodies and would otherwise be missed.
hiddenimports = []
hiddenimports += collect_submodules('britive')
hiddenimports += ['boto3', 'botocore', 'bs4']

block_cipher = None


def make_analysis(script_name):
    return Analysis(
        [os.path.join(ENTRY_DIR, script_name)],
        pathex=[],
        binaries=[],
        datas=datas,
        hiddenimports=hiddenimports,
        hookspath=[],
        hooksconfig={},
        runtime_hooks=[],
        excludes=['tkinter', 'pytest', 'mkdocs'],
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        cipher=block_cipher,
        noarchive=False,
    )


# Script filenames must NOT match an importable package name: a script named
# pybritive.py would shadow the real `pybritive` package and break
# `from pybritive... import`. The executable names are set on EXE() below.
a_main = make_analysis('run_pybritive.py')
a_aws = make_analysis('run_aws_cred_process.py')
a_kube = make_analysis('run_kube_exec.py')

# MERGE dedups everything shared across the three executables so the embedded
# interpreter + dependencies are bundled exactly once. The first tuple is the
# "primary" bundle the others reference.
MERGE(
    (a_main, 'pybritive', 'pybritive'),
    (a_aws, 'pybritive_aws_cred_process', 'pybritive-aws-cred-process'),
    (a_kube, 'pybritive_kube_exec', 'pybritive-kube-exec'),
)

pyz_main = PYZ(a_main.pure, a_main.zipped_data, cipher=block_cipher)
pyz_aws = PYZ(a_aws.pure, a_aws.zipped_data, cipher=block_cipher)
pyz_kube = PYZ(a_kube.pure, a_kube.zipped_data, cipher=block_cipher)


def make_exe(pyz, analysis, name):
    return EXE(
        pyz,
        analysis.scripts,
        [],
        exclude_binaries=True,
        name=name,
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        console=True,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    )


exe_main = make_exe(pyz_main, a_main, 'pybritive')
exe_aws = make_exe(pyz_aws, a_aws, 'pybritive-aws-cred-process')
exe_kube = make_exe(pyz_kube, a_kube, 'pybritive-kube-exec')

coll = COLLECT(
    exe_main,
    a_main.binaries,
    a_main.datas,
    exe_aws,
    a_aws.binaries,
    a_aws.datas,
    exe_kube,
    a_kube.binaries,
    a_kube.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='pybritive',
)
