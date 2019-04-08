"""Contains all models for the bootstrap server"""
import json
from dataclasses import dataclass, asdict

from kin.config import MEMO_CAP
from kin.blockchain.utils import is_valid_address
from pydantic import (BaseModel, ValidationError, 
                      Extra, validator, 
                      ExtraError, MissingError)

from . import errors

from typing import Union


def translate_validation_error(val_error: ValidationError) -> Exception:
    """
    Method to translate validation errors to 1 of 3:
      1. Any BootstrapError
      2. ExtraParams
      3. MissingParams
    """
    first_error = val_error.raw_errors[0].exc  # We want to return the first error found
    faulty_arg = val_error.raw_errors[0].loc[0]  # The argument that caused the error
    if isinstance(first_error, errors.BootstrapError):
        return first_error
    if isinstance(first_error, ExtraError):
        return errors.ExtraParamError(faulty_arg)
    if isinstance(first_error, MissingError):
        return errors.MissingParamError(faulty_arg)
    
    return val_error  # If we can't translate the error, raise it like that.


class BaseRequest(BaseModel):
    """Abstract base request class that all request objects inherit from"""

    class Config:
        extra = Extra.forbid  # Dont allow extra args

    @classmethod
    def from_json(cls, json_string):
        try:
            body_dict = json.loads(json_string)
        except json.JSONDecodeError:
            raise errors.InvalidBodyError()
        try:
            return cls(**body_dict)
        except ValidationError as e:
            raise translate_validation_error(e)


@dataclass
class BaseResponse:
    """Abstract base response class that all response objects inherit from"""

    def to_response_dict(self):
        """Use dataclasses.asdict to get a dictionary (which sanic will use for a json response) """
        return asdict(self)


class PaymentRequest(BaseRequest):

    destination: str
    amount: float
    memo: Union[str, None]

    @validator('destination')
    def validate_destination(cls, value):
        if is_valid_address(value):
            return value
        raise errors.InvalidParamError(f'Destination "{value}" is not a valid public address')

    @validator('amount')
    def validate_amount(cls, value):
        if value > 0:
            return value
        raise errors.InvalidParamError('Amount for payment must be bigger than 0')

    @validator('memo')
    def validate_memo(cls, value):
        if value is None or len(value) <= MEMO_CAP:
            return value
        raise errors.InvalidParamError(f'Memo: {value} is longer than {MEMO_CAP}')




