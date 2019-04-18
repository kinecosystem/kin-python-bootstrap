import json

import kin
import pytest
import asynctest

import sys
sys.path.append("..")

from src.init import init_app, VERSION
from src import errors
from src.config import Settings

app = init_app(Settings())
# Remove the setup_kin_with_network listener, we dont want to make calls to the blockchain in tests
del app.listeners['before_server_start'][1]
app.minimum_fee = 100


@pytest.fixture
def test_cli(loop, test_client):
    return loop.run_until_complete(test_client(app))


# Balance

async def test_balance(test_cli):
    # Mock response
    app.kin_client.get_account_balance = asynctest.CoroutineMock(return_value=50)

    balance_resp = await \
        (await test_cli.get('/balance/GAKYRLGVYIJSLDEWN6MJNYRMF7HYOHGHBDV4XO5SNLJWXFCR4SC5Z5K5')).json()

    assert balance_resp['balance'] == 50


async def test_balance_not_found(test_cli):
    address = 'GAKYRLGVYIJSLDEWN6MJNYRMF7HYOHGHBDV4XO5SNLJWXFCR4SC5Z5K5'
    # Mock response
    app.kin_client.get_account_balance = asynctest.CoroutineMock(side_effect=kin.KinErrors.AccountNotFoundError)

    balance_resp = await (await test_cli.get(f'/balance/{address}')).json()

    assert balance_resp == errors.AccountNotFoundError(address).to_dict()

# Payment info


async def test_tx_info(test_cli):
    # Mock response
    tx_response = json.loads("""{
  "memo": "1-xnXb-33a7c05eda014bfd",
  "_links": {
    "self": {
      "href": "https://horizon-testnet.kininfrastructure.com/transactions/c3cd7a2e90c6714bb32df16810a1f486bc2d267163db3e3aadccc42554d8102c"
    },
    "account": {
      "href": "https://horizon-testnet.kininfrastructure.com/accounts/GDAIEO6OIKIR3UYS6O547MANCV3DHDJKY5FC3QRW26FQFV76PNLY5Y2Q"
    },
    "ledger": {
      "href": "https://horizon-testnet.kininfrastructure.com/ledgers/2024812"
    },
    "operations": {
      "href": "https://horizon-testnet.kininfrastructure.com/transactions/c3cd7a2e90c6714bb32df16810a1f486bc2d267163db3e3aadccc42554d8102c/operations{?cursor,limit,order}",
      "templated": true
    },
    "effects": {
      "href": "https://horizon-testnet.kininfrastructure.com/transactions/c3cd7a2e90c6714bb32df16810a1f486bc2d267163db3e3aadccc42554d8102c/effects{?cursor,limit,order}",
      "templated": true
    },
    "precedes": {
      "href": "https://horizon-testnet.kininfrastructure.com/transactions?order=asc&cursor=8696501320552448"
    },
    "succeeds": {
      "href": "https://horizon-testnet.kininfrastructure.com/transactions?order=desc&cursor=8696501320552448"
    }
  },
  "id": "c3cd7a2e90c6714bb32df16810a1f486bc2d267163db3e3aadccc42554d8102c",
  "paging_token": "8696501320552448",
  "hash": "c3cd7a2e90c6714bb32df16810a1f486bc2d267163db3e3aadccc42554d8102c",
  "ledger": 2024812,
  "created_at": "2019-04-15T12:06:05Z",
  "source_account": "GDAIEO6OIKIR3UYS6O547MANCV3DHDJKY5FC3QRW26FQFV76PNLY5Y2Q",
  "source_account_sequence": "8324750426243094",
  "fee_paid": 0,
  "operation_count": 1,
  "envelope_xdr": "AAAAAMCCO85CkR3TEvO7z7ANFXYzjSrHSi3CNteLAtf+e1eOAAAAAAAdk1EAAAAWAAAAAAAAAAEAAAAXMS14blhiLTMzYTdjMDVlZGEwMTRiZmQAAAAAAQAAAAAAAAABAAAAACONb55spkRqxsTFui4DSZKeEe/aHzwtn4WbYjxEMDRIAAAAAAAAAAAAD0JAAAAAAAAAAAL+e1eOAAAAQIv/Y9ttK1lR9RmAdOqq46TyixnbX+PEz4nbyRmEilDsSHmNSJhPVYs6C7GUmrAbA432Lgy5lrLK1BYd8ZRKVA5EMDRIAAAAQJrU/psrdXSdQUnFtUngDTqBGSDHuAt0zrREA5BaJmKCyd2c5lWYKgbidsCsp65U9dBr6iMGN4XW7WDN6CqCbAE=",
  "result_xdr": "AAAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAA=",
  "result_meta_xdr": "AAAAAAAAAAEAAAAEAAAAAwAe5WkAAAAAAAAAACONb55spkRqxsTFui4DSZKeEe/aHzwtn4WbYjxEMDRIAAAAAHLSiAAADtBaAAAAWQAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAQAe5WwAAAAAAAAAACONb55spkRqxsTFui4DSZKeEe/aHzwtn4WbYjxEMDRIAAAAAHLhykAADtBaAAAAWQAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAwAe5WwAAAAAAAAAAMCCO85CkR3TEvO7z7ANFXYzjSrHSi3CNteLAtf+e1eOAAAAAAAtxsAAHZNRAAAAFgAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAQAe5WwAAAAAAAAAAMCCO85CkR3TEvO7z7ANFXYzjSrHSi3CNteLAtf+e1eOAAAAAAAehIAAHZNRAAAAFgAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAA",
  "fee_meta_xdr": "AAAAAgAAAAMAHuVpAAAAAAAAAADAgjvOQpEd0xLzu8+wDRV2M40qx0otwjbXiwLX/ntXjgAAAAAALcbAAB2TUQAAABUAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAEAHuVsAAAAAAAAAADAgjvOQpEd0xLzu8+wDRV2M40qx0otwjbXiwLX/ntXjgAAAAAALcbAAB2TUQAAABYAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAA==",
  "memo_type": "text",
  "signatures": [
    "i/9j220rWVH1GYB06qrjpPKLGdtf48TPidvJGYSKUOxIeY1ImE9VizoLsZSasBsDjfYuDLmWssrUFh3xlEpUDg==",
    "mtT+myt1dJ1BScW1SeANOoEZIMe4C3TOtEQDkFomYoLJ3ZzmVZgqBuJ2wKynrlT10GvqIwY3hdbtYM3oKoJsAQ=="
  ]
}""")
    app.kin_client.horizon.transaction = asynctest.CoroutineMock(return_value=tx_response)

    tx_info_resp = await \
        (await test_cli.get('/payment/2c61e62017ff8a0b281c009dff71f8e466447bf31910b49a8ad79a50ab3de872')).json()

    assert tx_info_resp['source'] == 'GDAIEO6OIKIR3UYS6O547MANCV3DHDJKY5FC3QRW26FQFV76PNLY5Y2Q'
    assert tx_info_resp['destination'] == 'GARY2346NSTEI2WGYTC3ULQDJGJJ4EPP3IPTYLM7QWNWEPCEGA2EQJK5'
    assert tx_info_resp['amount'] == 10
    assert tx_info_resp['memo'] == '1-xnXb-33a7c05eda014bfd'
    assert tx_info_resp['timestamp'] == 1555329965


async def test_tx_info_invalid(test_cli):
    # Mock response
    tx_response = json.loads("""{
  "memo": "1-anon-Hey boot",
  "_links": {
    "self": {
      "href": "http://horizon-testnet.kininfrastructure.com/transactions/2c61e62017ff8a0b281c009dff71f8e466447bf31910b49a8ad79a50ab3de872"
    },
    "account": {
      "href": "http://horizon-testnet.kininfrastructure.com/accounts/GDZUR2UCHC2HZHUHJRX64CD5GVNJSR6DD6E3S6PREQ5QEDFNKNXEMGW7"
    },
    "ledger": {
      "href": "http://horizon-testnet.kininfrastructure.com/ledgers/2022231"
    },
    "operations": {
      "href": "http://horizon-testnet.kininfrastructure.com/transactions/2c61e62017ff8a0b281c009dff71f8e466447bf31910b49a8ad79a50ab3de872/operations{?cursor,limit,order}",
      "templated": true
    },
    "effects": {
      "href": "http://horizon-testnet.kininfrastructure.com/transactions/2c61e62017ff8a0b281c009dff71f8e466447bf31910b49a8ad79a50ab3de872/effects{?cursor,limit,order}",
      "templated": true
    },
    "precedes": {
      "href": "http://horizon-testnet.kininfrastructure.com/transactions?order=asc\u0026cursor=8685416009961472"
    },
    "succeeds": {
      "href": "http://horizon-testnet.kininfrastructure.com/transactions?order=desc\u0026cursor=8685416009961472"
    }
  },
  "id": "2c61e62017ff8a0b281c009dff71f8e466447bf31910b49a8ad79a50ab3de872",
  "paging_token": "8685416009961472",
  "hash": "2c61e62017ff8a0b281c009dff71f8e466447bf31910b49a8ad79a50ab3de872",
  "ledger": 2022231,
  "created_at": "2019-04-15T08:31:00Z",
  "source_account": "GDZUR2UCHC2HZHUHJRX64CD5GVNJSR6DD6E3S6PREQ5QEDFNKNXEMGW7",
  "source_account_sequence": "8326288024535042",
  "fee_paid": 100,
  "operation_count": 1,
  "envelope_xdr": "AAAAAPNI6oI4tHyeh0xv7gh9NVqZR8Mfibl58SQ7AgytU25GAAAAZAAdlLcAAAACAAAAAAAAAAEAAAAPMS1hbm9uLUhleSBib290AAAAAAEAAAABAAAAAOf8qChUSQbnaopBqBS7ULaAEAoAEOOhEhsEjDG23RThAAAAAAAAAADWV1VpBDJyNg+e2/w9pKb3KMamTKrxROgf3QhaGrZ1cgAAAAAAAAAAAAAAAAAAAAKtU25GAAAAQDvvAfovoaaXC7bnL7U5+6XiiOzAIpDnf9xyJ4tfGItbjsJT06uJIw2OJp6tHHi+XrEX8CASjlLcNfIe8HGvYw623RThAAAAQF7zWBrCqHFyY56oUT6dyAfUlZshcMr1oHd4L6YNdBtlzsERgXEWGaI5FN9hUStVsbb5pJSZCWgftG7UXH5FeQY=",
  "result_xdr": "AAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAA=",
  "result_meta_xdr": "AAAAAAAAAAEAAAADAAAAAAAe21cAAAAAAAAAANZXVWkEMnI2D57b/D2kpvcoxqZMqvFE6B/dCFoatnVyAAAAAAAAAAAAHttXAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAwAe2jgAAAAAAAAAAOf8qChUSQbnaopBqBS7ULaAEAoAEOOhEhsEjDG23RThAAAAC695caAAAIMqAAABOgAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAQAe21cAAAAAAAAAAOf8qChUSQbnaopBqBS7ULaAEAoAEOOhEhsEjDG23RThAAAAC695caAAAIMqAAABOgAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAA",
  "fee_meta_xdr": "AAAAAgAAAAMAHpcBAAAAAAAAAADzSOqCOLR8nodMb+4IfTVamUfDH4m5efEkOwIMrVNuRgAAAAAAAAAAAB2UtwAAAAEAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAEAHttXAAAAAAAAAADzSOqCOLR8nodMb+4IfTVamUfDH4m5efEkOwIMrVNuRgAAAAAAAAAAAB2UtwAAAAIAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAA==",
  "memo_type": "text",
  "signatures": [
    "O+8B+i+hppcLtucvtTn7peKI7MAikOd/3HIni18Yi1uOwlPTq4kjDY4mnq0ceL5esRfwIBKOUtw18h7wca9jDg==",
    "XvNYGsKocXJjnqhRPp3IB9SVmyFwyvWgd3gvpg10G2XOwRGBcRYZojkU32FRK1WxtvmklJkJaB+0btRcfkV5Bg=="
  ]
}""")
    app.kin_client.horizon.transaction = asynctest.CoroutineMock(return_value=tx_response)

    tx_info_resp = await \
        (await test_cli.get('/payment/2c61e62017ff8a0b281c009dff71f8e466447bf31910b49a8ad79a50ab3de872')).json()

    assert tx_info_resp == errors.InvalidTransactionError().to_dict()


async def test_tx_info_not_found(test_cli):
    # Mock response
    app.kin_client.get_transaction_data = asynctest.CoroutineMock(side_effect=kin.KinErrors.ResourceNotFoundError)

    tx_info_resp = await \
        (await test_cli.get('/payment/2c61e62017ff8a0b281c009dff71f8e466447bf31910b49a8ad79a50ab3de872')).json()

    assert tx_info_resp == errors.TransactionNotFoundError\
        ('2c61e62017ff8a0b281c009dff71f8e466447bf31910b49a8ad79a50ab3de872').to_dict()


# Status

async def test_status(test_cli):
    # Mock response
    status = {'client':
                  {'sdk_version': '2.4.0',
                   'environment': 'PROD',
                   'horizon':
                       {'uri': 'https://horizon.kinfederation.com',
                        'online': True,
                        'error': None},
                   'transport':
                       {'pool_size': 100,
                        'num_retries': 3,
                        'request_timeout': 11,
                        'backoff_factor': 0.5
                        }
                   },
              'account':
                  {'app_id': 'DevX',
                   'public_address': 'GBUZFMZXZ6S2Y6HP5IIMTCESJJYJW32GFPN7XAVMRNE2OYQTM3Y7XYXL',
                   'balance': 2999186.699,
                   'channels':
                       {'total_channels': 1,
                        'free_channels': 1,
                        'non_free_channels': 0
                        }
                   }
              }

    app.kin_account.get_status = asynctest.CoroutineMock(return_value=status)
    status_response = await (await test_cli.get('/status')).json()

    assert status_response['service_version'] == VERSION
    assert status_response['horizon'] == status['client']['horizon']['uri']
    assert status_response['app_id'] == status['account']['app_id']
    assert status_response['public_address'] == status['account']['public_address']
    assert status_response['balance'] == status['account']['balance']
    assert status_response['channels']['total_channels'] == status['account']['channels']['total_channels']


# Pay

async def test_pay(test_cli):
    # Mock response
    app.kin_account.send_kin = asynctest.CoroutineMock(
        return_value='2c61e62017ff8a0b281c009dff71f8e466447bf31910b49a8ad79a50ab3de872')

    payment_resp = await \
        (await test_cli.post('/pay', json={
            'destination': 'GBV2MSCOAVLGB45KUENY77EFWWDCXPBWZIJJMRI75GPR3AUTB5UWUCO6',
            'amount': 15,
            'memo': 'ggwp'
        })).json()

    assert payment_resp['tx_id'] == '2c61e62017ff8a0b281c009dff71f8e466447bf31910b49a8ad79a50ab3de872'


async def test_pay_underfunded(test_cli):
    # Mock response
    app.kin_account.send_kin = asynctest.CoroutineMock(
        side_effect=kin.KinErrors.LowBalanceError)

    payment_resp = await \
        (await test_cli.post('/pay', json={
            'destination': 'GBV2MSCOAVLGB45KUENY77EFWWDCXPBWZIJJMRI75GPR3AUTB5UWUCO6',
            'amount': 15,
            'memo': 'ggwp'
        })).json()

    assert payment_resp == errors.LowBalanceError().to_dict()


async def test_pay_not_exist(test_cli):
    # Mock response
    app.kin_account.send_kin = asynctest.CoroutineMock(
        side_effect=kin.KinErrors.AccountNotFoundError)

    payment_resp = await \
        (await test_cli.post('/pay', json={
            'destination': 'GBV2MSCOAVLGB45KUENY77EFWWDCXPBWZIJJMRI75GPR3AUTB5UWUCO6',
            'amount': 15,
            'memo': 'ggwp'
        })).json()

    assert payment_resp == errors.\
        DestinationDoesNotExistError('GBV2MSCOAVLGB45KUENY77EFWWDCXPBWZIJJMRI75GPR3AUTB5UWUCO6').to_dict()

# Create


async def test_create(test_cli):
    # Mock response
    app.kin_account.create_account = asynctest.CoroutineMock(
        return_value='2c61e62017ff8a0b281c009dff71f8e466447bf31910b49a8ad79a50ab3de872')

    creation_resp = await \
        (await test_cli.post('/create', json={
            'destination': 'GBV2MSCOAVLGB45KUENY77EFWWDCXPBWZIJJMRI75GPR3AUTB5UWUCO6',
            'starting_balance': 15,
            'memo': 'ggwp'
        })).json()

    assert creation_resp['tx_id'] == '2c61e62017ff8a0b281c009dff71f8e466447bf31910b49a8ad79a50ab3de872'


async def test_create_underfunded(test_cli):
    # Mock response
    app.kin_account.create_account = asynctest.CoroutineMock(
        side_effect=kin.KinErrors.LowBalanceError)

    creation_resp = await \
        (await test_cli.post('/create', json={
            'destination': 'GBV2MSCOAVLGB45KUENY77EFWWDCXPBWZIJJMRI75GPR3AUTB5UWUCO6',
            'starting_balance': 15,
            'memo': 'ggwp'
        })).json()

    assert creation_resp == errors.LowBalanceError().to_dict()


async def test_create_already_exists(test_cli):
    # Mock response
    app.kin_account.create_account = asynctest.CoroutineMock(
        side_effect=kin.KinErrors.AccountExistsError)

    creation_resp = await \
        (await test_cli.post('/create', json={
            'destination': 'GBV2MSCOAVLGB45KUENY77EFWWDCXPBWZIJJMRI75GPR3AUTB5UWUCO6',
            'starting_balance': 15,
            'memo': 'ggwp'
        })).json()

    assert creation_resp == errors.\
        DestinationExistsError('GBV2MSCOAVLGB45KUENY77EFWWDCXPBWZIJJMRI75GPR3AUTB5UWUCO6').to_dict()


async def test_whitelist(test_cli):

    envelope = "AAAAAJalymXISxn6Cx+rKsuItEyoR+IoeCiUaSGy5yckSdAIAA" \
               "AAZAAfJbkAAAABAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
               "AQAAAAAAAAABAAAAAJalymXISxn6Cx+rKsuItEyoR+IoeCiUaS" \
               "Gy5yckSdAIAAAAAAAAAAAABhqAAAAAAAAAAAEkSdAIAAAAQDlw" \
               "LjXrjpa/FmtpxrnrRrYbRBtVkpqgaHgy9R0gG/PpLtcuces9LL" \
               "B3B8WmhqS47AlFMPg80WSD2Rv+QbJNHwg="

    creation_resp = await \
        (await test_cli.post('/whitelist', json={
            'envelope': envelope,
            'network_id': kin.config.HORIZON_PASSPHRASE_TEST
        })).json()

    assert creation_resp['tx_envelope'] == "AAAAAJalymXISxn6Cx+rKsuItEyoR+IoeCiUaSGy5yck" \
                                           "SdAIAAAAZAAfJbkAAAABAAAAAQAAAAAAAAAAAAAAAAAA" \
                                           "AAAAAAAAAAAAAQAAAAAAAAABAAAAAJalymXISxn6Cx+r" \
                                           "KsuItEyoR+IoeCiUaSGy5yckSdAIAAAAAAAAAAAABhqA" \
                                           "AAAAAAAAAAIkSdAIAAAAQDlwLjXrjpa/FmtpxrnrRrYb" \
                                           "RBtVkpqgaHgy9R0gG/PpLtcuces9LLB3B8WmhqS47AlF" \
                                           "MPg80WSD2Rv+QbJNHwi23RThAAAAQICXI9dNj/rnP1JV" \
                                           "jDYMSopUaxM/nUIYx36BmaeYuNIhTEfol6dF5G7ufWRE" \
                                           "1OX3mWbcAt/cxCoUz6vBUCbl9QA="


async def test_whitelist_cant_decode(test_cli):

    envelope = "blablabla"

    creation_resp = await \
        (await test_cli.post('/whitelist', json={
            'envelope': envelope,
            'network_id': kin.config.HORIZON_PASSPHRASE_TEST
        })).json()

    assert creation_resp == errors.CantDecodeTransactionError().to_dict()


async def test_whitelist_wrong_network(test_cli):

    envelope = "AAAAAJalymXISxn6Cx+rKsuItEyoR+IoeCiUaSGy5yckSdAIAA" \
               "AAZAAfJbkAAAABAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
               "AQAAAAAAAAABAAAAAJalymXISxn6Cx+rKsuItEyoR+IoeCiUaS" \
               "Gy5yckSdAIAAAAAAAAAAAABhqAAAAAAAAAAAEkSdAIAAAAQDlw" \
               "LjXrjpa/FmtpxrnrRrYbRBtVkpqgaHgy9R0gG/PpLtcuces9LL" \
               "B3B8WmhqS47AlFMPg80WSD2Rv+QbJNHwg="

    creation_resp = await \
        (await test_cli.post('/whitelist', json={
            'envelope': envelope,
            'network_id': 'incorrect'
        })).json()

    assert creation_resp == errors.InvalidParamError(f'The network id sent in the request doesn\'t '
                                                     f'match the network the server is configured with').to_dict()