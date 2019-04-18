"""Initialization for the bootstrap server"""
import logging

from sanic import Sanic

from .log import init_logging
from .config import Settings
from .routes import init_routes
from .middlewares import init_middlewares

VERSION = '1.0.0'


def init_app(config: Settings) -> Sanic:
    # Setup logging
    init_logging()
    logger = logging.getLogger('bootstrap')
    logger.setLevel(config.LOG_LEVEL)

    app = Sanic(__name__)

    init_routes(app, VERSION)
    init_middlewares(app, config)

    # Modify this so that we dont print the full seed to the log
    printable_config = config.json(indent=2)
    logger.info(f'Starting with the following config:\n'
                f'{printable_config.replace(config.SEED, config.SEED[:6] + "*" * 48)}')

    return app
