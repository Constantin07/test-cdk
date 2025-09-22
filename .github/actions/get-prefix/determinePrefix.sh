#!/usr/bin/env bash

set -e

# Get the branch name, stripping out refs/heads/
BRANCH_NAME=$(echo "$1" | sed 's/refs\/heads\///')

# Compute stack name from branch
# 1) replace non [a-z0-9-] (including /) with -
# 2) trim leading/trailing -
# 3) collapse multiple -
# 4) max 128 chars
BRANCH_NAME="$(echo "$BRANCH_NAME" \
  | sed -E 's/[^a-z0-9-]+/-/g; s/^-+//; s/-+$//; s/-{2,}/-/g' \
  | cut -c1-127)"

echo "Branch name: $BRANCH_NAME"

# For main branch - no prefix
if [[ "$BRANCH" == "main" ]]; then
  PREFIX=""
else
  PREFIX="$BRANCH_NAME-"
fi

echo "Prefix: $PREFIX"

# Set the output for CDK stack prefix
echo "prefix=$PREFIX" >> "$GITHUB_OUTPUT"
