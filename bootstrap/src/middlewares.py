"""Contains middlewares and error handlers"""

import time
import logging
from contextvars import ContextVar

from sanic.exceptions import SanicException
from pydantic import ValidationError

import errors
from helpers import json_response
from log import req_id, req_id_generator

req_start_time: ContextVar[int] = ContextVar('req_start_time', default=None)

logger = logging.getLogger('bootstrap')


async def before_request(request):
    """Set context variables for this request"""
    req_start_time.set(time.time())
    req_id.set(req_id_generator())
    logger.info(f'Got request {request.method} {request.path},\n'
                f'body: {request.body.decode()}')


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


async def close_kin_client(app, loop):
    """Close the kin client"""
    await app.kin_client.close()


def bootstrap_error_handle(request, exception: errors.BootstrapError):
    # If it is one of our custom errors, log it
    logger.error(exception.error)
    return json_response(exception.to_dict(), exception.http_code)


def validation_error_handler(request, exception: ValidationError):
    # Translate and raise return bootstrap error
    return bootstrap_error_handle(request, errors.translate_validation_error(exception))


def http_error_handler(request, exception: SanicException):
    logger.error(f'Http exception: {repr(exception)}')
    return json_response({'code': exception.status_code, 'message': str(exception)},
                         exception.status_code)


def internal_error_handler(request, exception: Exception):
    # Log the exception and return an internal server error
    logger.error(f'Unexpected exception: {str(exception)}')
    return json_response(errors.InternalError().to_dict(), errors.InternalError.code)
