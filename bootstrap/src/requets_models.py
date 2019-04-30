"""Contains all models for the bootstrap server's requests"""
import json

from kin.config import MEMO_CAP
from kin.blockchain.utils import is_valid_address, is_valid_transaction_hash
from pydantic import BaseModel, Extra, validator
from pydantic import ValidationError

from . import errors

from typing import Optional


class BaseRequest(BaseModel):
    """
    Abstract base request class that all request objects inherit from

    pydantic already validates the types (int/float/str), and we add custom validators to all parameters as well
    """

    class Config:
        extra = Extra.forbid  # Dont allow extra args

    def __init__(self, **data):
        try:
            super(BaseRequest, self).__init__(**data)
        except ValidationError as e:
            raise errors.translate_validation_error(e)

    @classmethod
    def from_json(cls, json_string):
        try:
            body_dict = json.loads(json_string)
        except json.JSONDecodeError:
            raise errors.InvalidBodyError()
        if not isinstance(body_dict, dict):
            # json.loads might return string in some cases like json.loads('"{}"')
            raise errors.InvalidBodyError()
        return cls(**body_dict)


class PaymentRequest(BaseRequest):

    destination: str
    amount: float
    memo: Optional[str]

    @validator('destination')
    def validate_destination(cls, value):
        if is_valid_address(value):
            return value
        raise errors.InvalidParamError(f"Destination '{value}' is not a valid public address")

    @validator('amount')
    def validate_amount(cls, value):
        if value > 0:
            return value
        raise errors.InvalidParamError('Amount for payment must be bigger than 0')

    @validator('memo')
    def validate_memo(cls, value):
        if value is None or len(value) <= MEMO_CAP:
            return value
        raise errors.InvalidParamError(f"Memo: '{value}' is longer than {MEMO_CAP}")


class CreationRequest(BaseRequest):
    destination: str
    starting_balance: float
    memo: Optional[str]

    @validator('destination')
    def validate_destination(cls, value):
        if is_valid_address(value):
            return value
        raise errors.InvalidParamError(f"Destination '{value}' is not a valid public address")

    @validator('starting_balance')
    def validate_amount(cls, value):
        if value >= 0:
            return value
        raise errors.InvalidParamError('Starting balance for account creation must not be negative')

    @validator('memo')
    def validate_memo(cls, value):
        if value is None or len(value) <= MEMO_CAP:
            return value
        raise errors.InvalidParamError(f"Memo: '{value}' is longer than {MEMO_CAP}")


class WhitelistRequest(BaseRequest):
    envelope: str
    network_id: str


class BalanceRequest(BaseRequest):
    address: str

    @validator('address')
    def validate_address(cls, value):
        if is_valid_address(value):
            return value
        raise errors.InvalidParamError(f"Address '{value}' is not a valid public address")


class TransactionInfoRequest(BaseRequest):
    tx_hash: str

    @validator('tx_hash')
    def validate_tx_hash(cls, value):
        if is_valid_transaction_hash(value):
            return value
        raise errors.InvalidParamError(f"Transaction hash: '{value}' is not a valid transaction hash")

