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
.\packaging\windows\build-msi.ps1 -Version <version>            # x64 (default)
.\packaging\windows\build-msi.ps1 -Version <version> -Arch arm64 # on a win-arm64 host
```

PyInstaller **cannot cross-compile** — each OS/arch must be built on its own
machine. CI (`.github/workflows/release-binaries.yml`) does this with a runner
matrix covering linux x86_64/arm64, macOS x86_64/arm64, and Windows x64/arm64,
and attaches every artifact to the GitHub Release. (arm64 Linux/Windows runners
are free on public repos; native-dependency wheels such as `cryptography` must
exist for win-arm64.)

## Code signing

Unsigned binaries trigger SmartScreen (Windows) and Gatekeeper (macOS) warnings.
Signing is **opt-in** via env vars / secrets, so local builds work unsigned:

| Platform | Secrets | Effect |
| --- | --- | --- |
| macOS | `MACOS_CERT_P12_BASE64`, `MACOS_CERT_P12_PASSWORD` | Developer ID certs imported into a throwaway CI keychain |
| macOS | `MACOS_SIGN_IDENTITY`, `MACOS_INSTALLER_IDENTITY` | codesign the bundle + productsign the .pkg |
| macOS | `APPLE_ID`, `APPLE_TEAM_ID`, `APPLE_APP_SPECIFIC_PASSWORD` | notarize + staple via `notarytool` |
| Windows | `WIN_PFX_BASE64`, `WIN_PFX_PASSWORD` | Authenticode sign the exes + MSI |

Locally, `build-pkg.sh` reads `MACOS_SIGN_IDENTITY` / `MACOS_INSTALLER_IDENTITY` /
`AC_NOTARY_PROFILE` from the environment and uses whatever keychain/notary
profile you already have; in CI those are derived from the secrets above.

## Homebrew tap

`.github/workflows/release-homebrew.yml` keeps the
[britive/homebrew-pybritive](https://github.com/britive/homebrew-pybritive) tap
in sync automatically. On every **stable** (non-prerelease) GitHub release it
waits for the new sdist to appear on PyPI, then runs
`brew bump-formula-pr --write-only`, which rewrites the formula's `url`/`sha256`
and regenerates the Python `resource` blocks from the new dependency set. The
updated formula is test-installed (`brew install --build-from-source` +
`brew test`) before being pushed to the tap. Pre-releases are skipped;
`workflow_dispatch` accepts an explicit version for manual re-runs.

Note the tap installs from PyPI (a virtualenv build), not from the standalone
bundles above — it still requires nothing from the user but does compile
`cryptography` from source (hence the formula's build-time `rust` dependency).

Requires the `HOMEBREW_TAP_TOKEN` secret: a token with write (contents) access
to `britive/homebrew-pybritive`.

## Distribution channels (optional follow-ups)

With installers attached to releases and the Homebrew tap automated, the
remaining candidates are: `winget` / Scoop / Chocolatey (Windows) and hosting
the Linux `install` script + zip behind `curl https://... | sh` on
downloads.britive.com.
