"""Configs for the project."""

import os

HEALTHZ_PREFIX = os.environ.get('HEALTHZ_PREFIX', '/healthz')

APP_PORT = int(os.environ.get('APP_PORT', 24501))

JAEGER_HOST = os.environ.get('JAEGER_HOST', 'jaeger-agent.monitoring.svc.cluster.local')
