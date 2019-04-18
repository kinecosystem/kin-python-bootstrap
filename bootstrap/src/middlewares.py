"""Contains middlewares and error handlers"""

import time
import logging
from contextvars import ContextVar

import kin
from kin.utils import create_channels, get_hd_channels
from sanic import Sanic
from sanic.exceptions import SanicException

from . import errors
from .helpers import json_response, prettify_exc
from .log import req_id, req_id_generator

req_start_time: ContextVar[int] = ContextVar('req_start_time', default=None)

logger = logging.getLogger('bootstrap')


def init_middlewares(app: Sanic, config):

    @app.middleware('request')
    async def before_request(request):
        """Set context variables for this request"""
        req_start_time.set(time.time())
        req_id.set(req_id_generator())
        logger.info(f'Got request {request.method} {request.path},\n'
                    f'body: {request.body.decode()}')

    @app.middleware('response')
    async def before_response(request, response):
        """Log response time"""
        try:
            response_time = time.time() - req_start_time.get()
        except:
            # Shouldn't really happen, but lets not return 500 cause of this
            logger.error("Cannot determine response time for request")
        else:
            logger.info(f'Finished handling request after: {response_time} seconds')

        logger.info(f'Response: body: {response.body.decode()}\n'
                    f'status: {response.status}')

    @app.listener('before_server_start')
    async def setup_kin(app, loop):

        # Setup kin client
        kin_env = kin.Environment('CUSTOM', config.HORIZON_ENDPOINT, config.NETWORK_PASSPHRASE)
        app.kin_client = kin.KinClient(kin_env)

        # Create channels
        if config.CHANNEL_COUNT > 0:
            logger.info(f'Setting up {config.CHANNEL_COUNT} channels')
            channels = get_hd_channels(config.SEED, config.CHANNEL_SALT, config.CHANNEL_COUNT)
        else:
            channels = None

        app.kin_account = app.kin_client.kin_account(config.SEED,
                                                     channel_secret_keys=channels,
                                                     app_id=config.APP_ID)

    @app.listener('before_server_start')
    async def setup_kin_with_network(app, loop):
        """This method is separate from "setup_kin" cause it makes network calls that we want to mock"""
        app.minimum_fee = await app.kin_client.get_minimum_fee()

        # Create channels
        if config.CHANNEL_COUNT > 0:
            await create_channels(config.SEED,
                                  app.kin_client.environment,
                                  config.CHANNEL_COUNT,
                                  config.CHANNEL_STARTING_BALANCE,
                                  config.CHANNEL_SALT)

    @app.middleware('after_server_stop')
    async def close_kin_client(app, loop):
        """Close the kin client"""
        await app.kin_client.close()

    @app.exception(errors.BootstrapError)
    def bootstrap_error_handle(request, exception: errors.BootstrapError):
        # If it is one of our custom errors, log it
        logger.error(exception.error)
        return json_response(exception.to_dict(), exception.http_code)

    @app.exception(SanicException)
    def http_error_handler(request, exception: SanicException):
        logger.error(f'Http exception: {repr(exception)}')
        return json_response({'code': exception.status_code, 'message': str(exception)},
                             exception.status_code)

    @app.exception(Exception)
    def internal_error_handler(request, exception: Exception):
        # Log the exception and return an internal server error
        logger.error(f'Unexpected exception:\n'
                     f'{prettify_exc(exception)}')
        return json_response(errors.InternalError().to_dict(), errors.InternalError.code)
