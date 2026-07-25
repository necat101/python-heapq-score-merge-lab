#!/usr/bin/env zsh
set -eu
cd "${0:a:h}"
python3 run_lab.py
echo
python3 -m unittest test_lab -v
