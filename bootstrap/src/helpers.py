import traceback
from functools import wraps

from sanic import response
from .requets_models import BaseRequest


def json_response(resp: dict, http_code: int) -> response.HTTPResponse:
    """Easier way to get a json response"""
    # escape_forward_slashes: https://github.com/huge-success/sanic/issues/1019
    return response.json(resp, status=http_code,
                         escape_forward_slashes=False)


def get_model(model: BaseRequest):
    """Init the expected request model before passing it to the route"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = args[0]
            return func(model.from_json(request.body.decode()))

        return wrapper
    return decorator


def prettify_exc(exception: Exception) -> str:
    return ''.join(traceback.format_exception(None, exception, exception.__traceback__))
