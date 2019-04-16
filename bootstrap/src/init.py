"""Initialization for the bootstrap server"""
import inspect
import logging

import kin
from kin.utils import create_channels
from sanic import Sanic

import log
from config import config

VERSION = '0.0.1'

# Setup logging
log.init_logging()
logger = logging.getLogger('bootstrap')
logger.setLevel(config.LOG_LEVEL)

# Setup app-related stuff
app = Sanic(__name__)

# Setup kin-related stuff
@app.listener('before_server_start')
async def setup_kin(app, loop):
    kin_env = kin.Environment('CUSTOM', config.HORIZON_ENDPOINT, config.NETWORK_PASSPHRASE)
    app.kin_client = kin.KinClient(kin_env)

    app.minimum_fee = await app.kin_client.get_minimum_fee()

    # Setup channels, skip if we are running in unittests
    if config.CHANNEL_COUNT > 0 and 'pytest_fixture_setup' not in [a.function for a in inspect.stack()]:
        logger.info(f'Setting up {config.CHANNEL_COUNT} channels')
        channels = await create_channels(config.SEED,
                                         kin_env,
                                         config.CHANNEL_COUNT,
                                         config.CHANNEL_STARTING_BALANCE,
                                         config.CHANNEL_SALT)
    else:
        channels = None
    app.kin_account = app.kin_client.kin_account(config.SEED,
                                                 channel_secret_keys=channels,
                                                 app_id=config.APP_ID)


# Modify this so that we dont print the full seed to the log
printable_config = config.json(indent=2)
logger.info(f'Starting with the following config:\n'
            f'{printable_config.replace(config.SEED, config.SEED[:6] + "*" * 48)}')

