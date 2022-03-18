from brownie import accounts, config, network, MockV3Aggregator, FundMe
from web3 import Web3
from scripts.helpful_script import get_account, get_price_feed_address, is_local_env


def main():
    fund()
    withdraw()


def fund():
    fundme_contract = FundMe[-1]
    funder = accounts[1]
    fundme_contract_owner = get_account()
    print("Funding Contract :", fundme_contract, " From Funder :", funder)
    minFee = fundme_contract.getEntranceFee()
    usdPrice = fundme_contract.getPrice() / 10 ** 18
    print(
        "Minimum Funding fees is set to :",
        minFee,
        " and ETH/USD price is currently set to:",
        usdPrice,
    )
    print("Submiting Funding transaction with value :", minFee)
    transaction = fundme_contract.fund({"from": funder, "value": minFee})
    wait = transaction.wait(1)
    print(
        "Funding Transaction completed, transaction reference:",
        transaction.txid,
    )


def withdraw():
    fundme_contract = FundMe[-1]
    contract_owner = get_account()
    print(
        "Withdrawing available fund : ",
        fundme_contract.balance(),
        "to Contract Owner: ",
        contract_owner,
    )

    transaction = fundme_contract.withdraw({"from": contract_owner})
    wait = transaction.wait(1)

    print(
        "Withdraw balance transaction completed, transaction reference:",
        transaction.txid,
    )
