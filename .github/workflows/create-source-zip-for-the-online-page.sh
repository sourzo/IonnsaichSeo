#!/bin/bash

# Creates a source zip, by downloading from GitHub releases, to upload to the website.
#
# This is required for two reasons:
# 1. CORS prevents the IS Online webpage downloading from GitHub releases.
# 2. The zip from GitHub releases puts everything in a common parent
#    directory, for example IonnsaichSeo-2.0.2/. This would
#    complicate path handling on the IS Online webpage.
#
# Parameters:
# $SOURCE_URL: URL to the source zip of a Release on GitHub,
#   e.g. https://github.com/sourzo/IonnsaichSeo/archive/refs/tags/v2.0.2.zip

set -eu -o pipefail # Strict error handling
set -x # Echo executed commands, for debugging failure

pushd website/

mkdir tmp
pushd tmp/

wget --quiet "$SOURCE_URL" -O source.zip

# Unzip, then rezip, but this time without the parent directory.
7z x source.zip
PARENT_DIR="$(find . -mindepth 1 -maxdepth 1 -type d | head -n1)"
shopt -s dotglob
mv "$PARENT_DIR"/* ./
rmdir "$PARENT_DIR"
rm source.zip
7z a source.zip *

mv source.zip ../IonnsaichSeo-source.zip
popd
rm -r tmp/

popd
