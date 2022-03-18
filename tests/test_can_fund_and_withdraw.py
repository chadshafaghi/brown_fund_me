from tokenize import triple_quoted
from brownie import Contract, accounts, web3, exceptions
import brownie
import pytest
from scripts.fund_and_deploy import withdraw
from scripts.helpful_script import get_account, get_price_feed_address, is_local_env
from scripts.deploy import deploy_fund_me
from web3 import Web3


def test_can_fund_and_withdraw():
    # prepare the data
    account = get_account()
    initial_balance_account = account.balance()
    fund_me = deploy_fund_me()
    deploy_fees = fund_me.tx.gas_used * fund_me.tx.gas_price
    entrance_fee = fund_me.getEntranceFee() + 1
    initial_balance_contract = fund_me.balance()

    # execute the operation fund()
    transaction_fund = fund_me.fund({"from": account, "value": entrance_fee})

    transaction_fund.wait(1)
    fund_transaction_fees = transaction_fund.gas_used * transaction_fund.gas_price

    print(
        "Balance of the contract before the fund_me contract:", initial_balance_contract
    )
    print("Balance of the contract after the fund_me contract:", fund_me.balance())

    # assert the operation fund()
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    assert fund_me.balance() == initial_balance_contract + entrance_fee

    expected_account_balance = (
        initial_balance_account - deploy_fees - entrance_fee - fund_transaction_fees
    )

    assert account.balance() == expected_account_balance

    # execute the operation withdraw()
    transaction_withdraw = fund_me.withdraw({"from": account})
    transaction_withdraw.wait(1)

    # assert the operation  withdraw()
    assert fund_me.balance() == initial_balance_contract
    assert account.balance() == (
        initial_balance_account
        - (fund_me.tx.gas_used * transaction_fund.gas_price)
        - (transaction_fund.gas_used * transaction_fund.gas_price)
        - (transaction_withdraw.gas_used * transaction_withdraw.gas_price)
    )


def test_only_owner_can_withdraw():
    if not is_local_env():
        pytest.skip("this is only for local testing")

    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # bad_actor = get_account()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
