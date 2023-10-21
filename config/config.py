"""Configs for the project."""

import os

HEALTHZ_PREFIX = os.environ.get('HEALTHZ_PREFIX', '/healthz')

APP_PORT = int(os.environ.get('APP_PORT', 24501))

JAEGER_HOST = os.environ.get('JAEGER_HOST', 'localhost')

SHORT_URL_LENGTH = int(os.environ.get('SHORT_URL_LENGTH', 8))

POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')

POSTGRES_DB_USER = os.environ.get('POSTGRES_DB_USER', 'gran_url')
POSTGRES_DB_PASS = os.environ.get('POSTGRES_DB_PASS', 'gran_url_pass')
POSTGRES_DB_NAME = os.environ.get('POSTGRES_DB_NAME', 'gran_url_db')
