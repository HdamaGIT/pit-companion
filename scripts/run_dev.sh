#!/usr/bin/env bash
set -e

# From repo root, run:
#   ./scripts/run_dev.sh

cd "$(dirname "$0")/.."
source .venv/bin/activate
streamlit run pit_companion/ui/streamlit_app.py
