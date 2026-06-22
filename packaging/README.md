# Standalone packaging

Builds self-contained `pybritive` installers that **bundle their own Python
interpreter**, so the target machine needs nothing pre-installed (no
`pip install`, no Python). This mirrors how the **AWS CLI v2** is distributed:
a [PyInstaller](https://pyinstaller.org) *onedir* bundle wrapped in a native
installer per operating system.

The PyPI package (`pip install pybritive`) is unchanged and still published —
these installers are an additional distribution channel for users who don't
have (or don't want) Python.

## What gets built

A single onedir bundle (`dist/pybritive/`) containing one embedded interpreter
plus three launcher executables — matching the three console scripts in
`pyproject.toml`:

| Executable | Invoked by |
| --- | --- |
| `pybritive` | the user, interactively |
| `pybritive-aws-cred-process` | AWS SDKs, on every credential refresh |
| `pybritive-kube-exec` | `kubectl`, on every command |

### Why onedir (not onefile)

`--onefile` unpacks the entire bundle to a temp directory **on every launch**.
Because `pybritive-kube-exec` and `pybritive-aws-cred-process` run on every
`kubectl` / AWS credential refresh, that overhead is unacceptable. onedir keeps
cold start at ~0.25s. AWS CLI v2 makes the same choice for the same reason.

## Layout

```
packaging/
  pybritive.spec              # PyInstaller spec (3 launchers, one shared bundle via MERGE)
  requirements-build.txt      # pyinstaller + bundled optional deps (boto3, beautifulsoup4)
  entrypoints/                # one shim per executable (named to avoid shadowing the package)
  linux/install               # zip-and-go installer script (copies bundle, symlinks onto PATH)
  macos/build-pkg.sh          # builds a signed/notarized .pkg
  macos/scripts/postinstall   # symlinks commands into /usr/local/bin
  windows/pybritive.wxs       # WiX v4 source for the MSI (auto-harvests bundle, adds to PATH)
  windows/build-msi.ps1       # builds + signs the MSI
```

## Build locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install . -r packaging/requirements-build.txt
pyinstaller packaging/pybritive.spec --noconfirm
./dist/pybritive/pybritive --version          # smoke test
```

Then package for the current OS:

```bash
# Linux  -> dist/pybritive-<ver>-linux-x86_64.zip  (contains ./install)
# (the release workflow assembles the zip; locally just run dist/pybritive/* directly)

# macOS  -> dist/pybritive-<ver>-macos-<arch>.pkg
bash packaging/macos/build-pkg.sh <version>

# Windows (PowerShell, requires `dotnet tool install --global wix`)
.\packaging\windows\build-msi.ps1 -Version <version>
```

PyInstaller **cannot cross-compile** — each OS/arch must be built on its own
machine. CI (`.github/workflows/release-binaries.yml`) does this with a runner
matrix and attaches every artifact to the GitHub Release.

## Code signing

Unsigned binaries trigger SmartScreen (Windows) and Gatekeeper (macOS) warnings.
Signing is **opt-in** via env vars / secrets, so local builds work unsigned:

| Platform | Secrets / env | Effect |
| --- | --- | --- |
| macOS | `MACOS_SIGN_IDENTITY`, `MACOS_INSTALLER_IDENTITY`, `AC_NOTARY_PROFILE` | codesign + productsign + notarize/staple |
| Windows | `WIN_PFX_BASE64`, `WIN_PFX_PASSWORD` | Authenticode sign the exes + MSI |

## Distribution channels (optional follow-ups)

Once installers are attached to releases, publishing to package managers is a
small additional step: `winget` / Scoop / Chocolatey (Windows), a Homebrew tap
(macOS), and the `install` script over `curl` (Linux).
