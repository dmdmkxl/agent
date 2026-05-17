#!/usr/bin/env bash
set -euo pipefail

uvicorn src.app.api:app --reload

