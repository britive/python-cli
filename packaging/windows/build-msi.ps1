<#
.SYNOPSIS
    Build (and optionally sign) the pybritive MSI from the PyInstaller bundle.

.DESCRIPTION
    Expects the onedir bundle at dist\pybritive (from
    `pyinstaller packaging\pybritive.spec`). Produces
    dist\pybritive-<Version>-windows-x64.msi.

    Requires the WiX v4 toolset: `dotnet tool install --global wix`.

    Code signing is applied only when a certificate is provided, so the script
    runs unsigned locally and signed in CI. Provide either:
      -PfxPath / -PfxPassword   (sign with a PFX file), or
      -SignThumbprint           (sign with a cert already in the cert store).
.PARAMETER Version
    Product version, e.g. 2.4.0. PEP 440 pre-release suffixes (rc1) are
    stripped to keep MSI versioning happy.
#>
param(
    [Parameter(Mandatory = $true)][string]$Version,
    [ValidateSet("x64", "arm64")][string]$Arch = "x64",
    [string]$BundleDir = "dist\pybritive",
    [string]$PfxPath,
    [string]$PfxPassword,
    [string]$SignThumbprint,
    [string]$TimestampUrl = "http://timestamp.digicert.com"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path (Join-Path $BundleDir "pybritive.exe"))) {
    throw "bundle not found at $BundleDir; run pyinstaller first"
}

# MSI ProductVersion must be numeric (x.y.z); drop any PEP 440 suffix.
$MsiVersion = ($Version -split '[^0-9.]')[0].TrimEnd('.')
$Out = "dist\pybritive-$Version-windows-$Arch.msi"

# Sign the executables inside the bundle before packaging.
function Invoke-Sign($path) {
    if ($PfxPath) {
        & signtool sign /fd SHA256 /tr $TimestampUrl /td SHA256 `
            /f $PfxPath /p $PfxPassword $path
    } elseif ($SignThumbprint) {
        & signtool sign /fd SHA256 /tr $TimestampUrl /td SHA256 `
            /sha1 $SignThumbprint $path
    }
}

if ($PfxPath -or $SignThumbprint) {
    Write-Host "Signing bundled executables..."
    Get-ChildItem -Path $BundleDir -Filter *.exe | ForEach-Object { Invoke-Sign $_.FullName }
}

Write-Host "Building MSI $Out (ProductVersion $MsiVersion, arch $Arch)..."
& wix build packaging\windows\pybritive.wxs `
    -d Version=$MsiVersion `
    -d BundleDir=$BundleDir `
    -arch $Arch `
    -o $Out

if ($PfxPath -or $SignThumbprint) {
    Write-Host "Signing MSI..."
    Invoke-Sign $Out
}

Write-Host "built: $Out"
