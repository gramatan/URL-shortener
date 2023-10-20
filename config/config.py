"""Configs for the project."""

import os

HEALTHZ_PREFIX = os.environ.get('HEALTHZ_PREFIX', '/healthz')

APP_PORT = int(os.environ.get('APP_PORT', 24501))

JAEGER_HOST = os.environ.get('JAEGER_HOST', 'localhost')

URL_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
SHORT_URL_LENGTH = int(os.environ.get('SHORT_URL_LENGTH', 6))
