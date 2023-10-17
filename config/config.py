"""Configs for the project."""

import os

HEALTHZ_PREFIX = os.environ.get('HEALTHZ_PREFIX', '/healthz')

APP_PORT = int(os.environ.get('APP_PORT', 24501))
