import os

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from app import create_app
from config import ProductionConfig

SENTRY_DSN = os.getenv('SENTRY_DSN')

if SENTRY_DSN is not None:
    sentry_sdk.init(dsn=SENTRY_DSN,
                    integrations=[
                        FlaskIntegration(),
                    ],
                    traces_sample_rate=1.0)

app = create_app(ProductionConfig)
