import pytest

import sys
sys.path.append("..")

from src import errors, requets_models


def test_from_json():
    normal = requets_models.BalanceRequest(address='GCLKLSTFZBFRT6QLD6VSVS4IWRGKQR7CFB4CRFDJEGZOOJZEJHIARI4G')
    from_json = requets_models.BalanceRequest.from_json('{"address":"GCLKLSTFZBFRT6QLD6VSVS4IWRGKQR7CFB4CRFDJEGZOOJZEJHIARI4G"}')
    assert normal == from_json


def test_from_json_fail():

    with pytest.raises(errors.InvalidBodyError):
        requets_models.BalanceRequest.from_json('basdas')

    with pytest.raises(errors.InvalidBodyError):
        requets_models.BalanceRequest.from_json('"{}"')


def test_extra_args():
    with pytest.raises(errors.ExtraParamError):
        requets_models.BalanceRequest(address='GCLKLSTFZBFRT6QLD6VSVS4IWRGKQR7CFB4CRFDJEGZOOJZEJHIARI4G',
                                      some_arg=5)


def test_missing_args():
    with pytest.raises(errors.MissingParamError):
        requets_models.BalanceRequest()


def test_invalid_types():
    with pytest.raises(errors.InvalidParamError):
        requets_models.WhitelistRequest(envelope=None, network_id=None)


def test_payment_request():

    # Check nothing is raised
    requets_models.PaymentRequest(destination='GCLKLSTFZBFRT6QLD6VSVS4IWRGKQR7CFB4CRFDJEGZOOJZEJHIARI4G',
                                  amount=10,
                                  memo=None)

    requets_models.PaymentRequest(destination='GCLKLSTFZBFRT6QLD6VSVS4IWRGKQR7CFB4CRFDJEGZOOJZEJHIARI4G',
                                  amount=10,
                                  memo='Hello')

    # Check validations
    with pytest.raises(errors.InvalidParamError):
        requets_models.PaymentRequest(destination='blabla',
                                      amount=10,
                                      memo='Hello')

    with pytest.raises(errors.InvalidParamError):
        requets_models.PaymentRequest(destination='GCLKLSTFZBFRT6QLD6VSVS4IWRGKQR7CFB4CRFDJEGZOOJZEJHIARI4G',
                                      amount=0,
                                      memo='Hello')

    with pytest.raises(errors.InvalidParamError):
        requets_models.PaymentRequest(destination='GCLKLSTFZBFRT6QLD6VSVS4IWRGKQR7CFB4CRFDJEGZOOJZEJHIARI4G',
                                      amount=10,
                                      memo='a' * 50)


def test_creation_request():
    # Check nothing is raised
    requets_models.CreationRequest(destination='GCLKLSTFZBFRT6QLD6VSVS4IWRGKQR7CFB4CRFDJEGZOOJZEJHIARI4G',
                                   starting_balance=10,
                                   memo=None)

    requets_models.CreationRequest(destination='GCLKLSTFZBFRT6QLD6VSVS4IWRGKQR7CFB4CRFDJEGZOOJZEJHIARI4G',
                                   starting_balance=10,
                                   memo='Hello')

    # Check validations
    with pytest.raises(errors.InvalidParamError):
        requets_models.CreationRequest(destination='blabla',
                                       starting_balance=10,
                                       memo='Hello')

    with pytest.raises(errors.InvalidParamError):
        requets_models.CreationRequest(destination='GCLKLSTFZBFRT6QLD6VSVS4IWRGKQR7CFB4CRFDJEGZOOJZEJHIARI4G',
                                       starting_balance=-5,
                                       memo='Hello')

    with pytest.raises(errors.InvalidParamError):
        requets_models.CreationRequest(destination='GCLKLSTFZBFRT6QLD6VSVS4IWRGKQR7CFB4CRFDJEGZOOJZEJHIARI4G',
                                       starting_balance=10,
                                       memo='a' * 50)


def test_balance_request():
    # Check nothing is raised
    requets_models.BalanceRequest(address='GCLKLSTFZBFRT6QLD6VSVS4IWRGKQR7CFB4CRFDJEGZOOJZEJHIARI4G')

    # Check validations
    with pytest.raises(errors.InvalidParamError):
        requets_models.BalanceRequest(address='qwewq')


def test_transaction_info_request():
    # Check nothing is raised
    requets_models.TransactionInfoRequest(tx_hash='e9d42295b0dbb30b9b83b70b7b49fd3e09dc9986f46'
                                                  '27dcbbbca490063eb2d56')

    # Check validations
    with pytest.raises(errors.InvalidParamError):
        requets_models.TransactionInfoRequest(tx_hash='abcdefg')