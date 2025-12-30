#!/usr/bin/env bash
set -euo pipefail
echo "$1" > seal.txt
ots stamp seal.txt
echo "Stamped: seal.txt.ots"
