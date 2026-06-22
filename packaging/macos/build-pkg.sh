#!/bin/bash
# Build a macOS .pkg installer from the PyInstaller onedir bundle.
#
# Expects the bundle at dist/pybritive (produced by `pyinstaller
# packaging/pybritive.spec`). Produces dist/pybritive-<version>-macos-<arch>.pkg.
#
# Signing + notarization are applied only when the relevant env vars are set,
# so the script runs unsigned locally and signed in CI:
#   MACOS_SIGN_IDENTITY    Developer ID Application identity (codesign)
#   MACOS_INSTALLER_IDENTITY  Developer ID Installer identity (productsign)
#   AC_NOTARY_PROFILE      `xcrun notarytool` keychain profile name
set -euo pipefail

VERSION="${1:?usage: build-pkg.sh <version>}"
ARCH="$(uname -m)"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BUNDLE="$ROOT/dist/pybritive"
PKGROOT="$(mktemp -d)/root"
INSTALL_DIR="/usr/local/pybritive"
IDENT="com.britive.pybritive"
OUT="$ROOT/dist/pybritive-${VERSION}-macos-${ARCH}.pkg"

[ -x "$BUNDLE/pybritive" ] || { echo "bundle missing at $BUNDLE; run pyinstaller first" >&2; exit 1; }

# Stage the payload at its final on-disk location.
mkdir -p "$PKGROOT$INSTALL_DIR"
cp -R "$BUNDLE/." "$PKGROOT$INSTALL_DIR/"

# Optionally codesign the embedded executables (deep) before packaging.
if [ -n "${MACOS_SIGN_IDENTITY:-}" ]; then
    echo "codesigning bundle with: $MACOS_SIGN_IDENTITY"
    codesign --force --deep --options runtime --timestamp \
        --sign "$MACOS_SIGN_IDENTITY" \
        "$PKGROOT$INSTALL_DIR/pybritive" \
        "$PKGROOT$INSTALL_DIR/pybritive-aws-cred-process" \
        "$PKGROOT$INSTALL_DIR/pybritive-kube-exec"
fi

COMPONENT="$(mktemp -d)/pybritive-component.pkg"
pkgbuild \
    --root "$PKGROOT" \
    --identifier "$IDENT" \
    --version "$VERSION" \
    --scripts "$ROOT/packaging/macos/scripts" \
    --install-location "/" \
    "$COMPONENT"

DISTRIB="$(mktemp -d)/distribution.xml"
cat > "$DISTRIB" <<XML
<?xml version="1.0" encoding="utf-8"?>
<installer-gui-script minSpecVersion="1">
    <title>PyBritive CLI</title>
    <pkg-ref id="$IDENT"/>
    <options customize="never" require-scripts="false" hostArchitectures="$ARCH"/>
    <choices-outline><line choice="default"><line choice="$IDENT"/></line></choices-outline>
    <choice id="default"/>
    <choice id="$IDENT" visible="false"><pkg-ref id="$IDENT"/></choice>
    <pkg-ref id="$IDENT" version="$VERSION" onConclusion="none">pybritive-component.pkg</pkg-ref>
</installer-gui-script>
XML

PRODUCT="$OUT"
productbuild --distribution "$DISTRIB" --package-path "$(dirname "$COMPONENT")" "$PRODUCT"

# Sign the product archive if an installer identity is available.
if [ -n "${MACOS_INSTALLER_IDENTITY:-}" ]; then
    echo "productsigning installer with: $MACOS_INSTALLER_IDENTITY"
    productsign --sign "$MACOS_INSTALLER_IDENTITY" "$PRODUCT" "$PRODUCT.signed"
    mv "$PRODUCT.signed" "$PRODUCT"
fi

# Notarize + staple when a notarytool profile is configured.
if [ -n "${AC_NOTARY_PROFILE:-}" ]; then
    echo "notarizing $PRODUCT"
    xcrun notarytool submit "$PRODUCT" --keychain-profile "$AC_NOTARY_PROFILE" --wait
    xcrun stapler staple "$PRODUCT"
fi

echo "built: $PRODUCT"
