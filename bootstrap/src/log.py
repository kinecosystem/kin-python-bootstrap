import logging
from uuid import uuid4
from contextvars import ContextVar

req_id: ContextVar[str] = ContextVar('req_id', default=None)


def req_id_generator() -> str:
    """Generate a unique 8 characters long string to be used as a request id"""
    return str(uuid4())[:8]


def request_id_filter(record):
    """Inject request id into the logs"""
    record.req_id = req_id.get()
    return record


def init_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | request_id=%(req_id)s | %(message)s'))
    handler.addFilter(request_id_filter)
    logging.root.addHandler(handler)

    # Suppress warnings from the kin-sdk
    kin_logger = logging.getLogger('kin')
    kin_logger.setLevel('ERROR')
