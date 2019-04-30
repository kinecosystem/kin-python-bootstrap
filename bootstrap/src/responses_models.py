"""Contains all models for the bootstrap server's responses"""
from dataclasses import dataclass, asdict

from typing import Optional

@dataclass
class BaseResponse:
    """Abstract base response class that all response objects inherit from"""

    def to_response_dict(self):
        """Use dataclasses.asdict to get a dictionary (which sanic will use for a json response)"""
        return asdict(self)


@dataclass
class TransactionResponse(BaseResponse):
    tx_id: str


@dataclass
class BalanceResponse(BaseResponse):
    balance: float


@dataclass
class PaymentInfoResponse(BaseResponse):
    source: str
    destination: str
    amount: float
    memo: Optional[str]
    timestamp: float


@dataclass
class WhitelistResponse(BaseResponse):
    tx_envelope: str


@dataclass
class StatusResponse(BaseResponse):

    @dataclass
    class ChannelsInfo:
        free_channels: int
        non_free_channels: int
        total_channels: int

    service_version: str
    horizon: str
    app_id: str
    public_address: str
    balance: float
    channels: ChannelsInfo
