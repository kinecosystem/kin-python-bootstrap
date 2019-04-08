"""Contains all models for the bootstrap server's requests"""
import json

from kin import decode_transaction
from kin.config import MEMO_CAP
from kin.blockchain.utils import is_valid_address, is_valid_transaction_hash
from pydantic import (BaseModel, ValidationError, 
                      Extra, validator, 
                      ExtraError, MissingError)

from . import errors

from typing import Optional


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


class PaymentRequest(BaseRequest):

    destination: str
    amount: float
    memo: Optional[str]

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


class CreationRequest(BaseRequest):
    destination: str
    starting_balance: float
    memo: Optional[str]

    @validator('destination')
    def validate_destination(cls, value):
        if is_valid_address(value):
            return value
        raise errors.InvalidParamError(f'Destination "{value}" is not a valid public address')

    @validator('starting_balance')
    def validate_amount(cls, value):
        if value >= 0:
            return value
        raise errors.InvalidParamError('Starting balance for account creation must not be negative')

    @validator('memo')
    def validate_memo(cls, value):
        if value is None or len(value) <= MEMO_CAP:
            return value
        raise errors.InvalidParamError(f'Memo: {value} is longer than {MEMO_CAP}')


class WhitelistRequest(BaseRequest):
    tx_envelope: str

    @validator('tx_envelope')
    def validate_tx_envelope(cls, value):
        try:
            # Try to decode the tx, network id doesn't matter
            decode_transaction(value, '', simple=False)
        except:
            raise errors.InvalidParamError('The service was not able to decode the transaction envelope')
        return value


class BalanceRequest(BaseRequest):
    address: str

    @validator('address')
    def validate_address(cls, value):
        if is_valid_address(value):
            return value
        raise errors.InvalidParamError(f'Address: "{value}" is not a valid public address')


class TransactionInfoRequest(BaseRequest):
    tx_hash: str

    @validator('tx_hash')
    def validate_tx_hash(cls, value):
        if is_valid_transaction_hash(value):
            return value
        raise errors.InvalidParamError(f'Transaction hash: "{value}" is not a valid transaction hash')




