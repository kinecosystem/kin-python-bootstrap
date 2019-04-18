"""Contains all of the routes for the server"""
import logging
from datetime import datetime

import kin
from kin import KinErrors
from sanic import Sanic

from . import errors
from . import requets_models
from . import responses_models
from .helpers import json_response, get_model

logger = logging.getLogger('bootstrap')


def init_routes(app: Sanic, version: str):

    # Has no effect, just to help the IDE a bit :)
    app.kin_client: kin.KinClient
    app.kin_account: kin.KinAccount
    app.minimum_fee: int

    @app.route('/balance/<address>', methods=['GET'])
    async def get_balance(request, address: str):
        balance_request = requets_models.BalanceRequest(address=address)
        try:
            balance = await app.kin_client.get_account_balance(balance_request.address)
        except KinErrors.AccountNotFoundError:
            raise errors.AccountNotFoundError(balance_request.address)

        return json_response(responses_models.BalanceResponse(balance).to_response_dict(), 200)

    @app.route('/payment/<tx_hash>', methods=['GET'])
    async def get_tx_info(request, tx_hash: str):
        tx_info_request = requets_models.TransactionInfoRequest(tx_hash=tx_hash)
        try:
            tx = await app.kin_client.get_transaction_data(tx_info_request.tx_hash)
        except KinErrors.ResourceNotFoundError:
            raise errors.TransactionNotFoundError(tx_info_request.tx_hash)
        except KinErrors.CantSimplifyError:
            raise errors.InvalidTransactionError()

        if tx.operation.type != kin.OperationTypes.PAYMENT:
            raise errors.InvalidTransactionError()

        # Convert from '2018-11-12T06:45:40Z' to unix timestamp
        timestamp = datetime.strptime(tx.timestamp, '%Y-%m-%dT%H:%M:%S%z').timestamp()
        info_response = responses_models.PaymentInfoResponse(tx.source,
                                                             tx.operation.destination,
                                                             tx.operation.amount,
                                                             tx.memo,
                                                             timestamp)

        return json_response(info_response.to_response_dict(), 200)

    @app.route('/status', methods=['GET'])
    async def get_status(request):
        status = await app.kin_account.get_status()
        status_response = responses_models.StatusResponse(version,
                                                          status['client']['horizon']['uri'],
                                                          status['account']['app_id'],
                                                          status['account']['public_address'],
                                                          status['account']['balance'],
                                                          status['account']['channels'])

        return json_response(status_response.to_response_dict(), 200)

    @app.route('/pay', methods=['POST'])
    @get_model(model=requets_models.PaymentRequest)
    async def pay(payment_request: requets_models.PaymentRequest):
        try:
            tx_id = await app.kin_account.send_kin(payment_request.destination,
                                                   payment_request.amount,
                                                   app.minimum_fee,
                                                   payment_request.memo)
        except KinErrors.AccountNotFoundError:
            raise errors.DestinationDoesNotExistError(payment_request.destination)
        except KinErrors.LowBalanceError:
            raise errors.LowBalanceError()

        return json_response(responses_models.TransactionResponse(tx_id).to_response_dict(), 200)

    @app.route('/create', methods=['POST'])
    @get_model(model=requets_models.CreationRequest)
    async def create(creation_request: requets_models.CreationRequest):
        try:
            tx_id = await app.kin_account.create_account(creation_request.destination,
                                                         creation_request.starting_balance,
                                                         app.minimum_fee,
                                                         creation_request.memo)
        except KinErrors.LowBalanceError:
            raise errors.LowBalanceError()
        except KinErrors.AccountExistsError:
            raise errors.DestinationExistsError(creation_request.destination)

        return json_response(responses_models.TransactionResponse(tx_id).to_response_dict(), 200)

    @app.route('/whitelist', methods=['POST'])
    @get_model(model=requets_models.WhitelistRequest)
    async def create(whitelist_request: requets_models.WhitelistRequest):
        try:
            whitelisted_tx = app.kin_account.whitelist_transaction(whitelist_request.dict())
        except kin.KinErrors.WrongNetworkError:
            raise errors.InvalidParamError(f'The network id sent in the request doesn\'t '
                                           f'match the network the server is configured with')
        except:
            raise errors.CantDecodeTransactionError()

        return json_response(responses_models.WhitelistResponse(whitelisted_tx).to_response_dict(), 200)