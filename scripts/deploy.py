from brownie import FundMe, accounts, network, config
from scripts.helpful_script import get_account, get_price_feed_address, is_local_env


def deploy_fund_me():
    account = get_account()
    print("Getting a PriceFeed from AggregatorV3 util... ")
    price_fee_address = get_price_feed_address()
    print("Deploying FundMe Contract from...", account)

    if not is_local_env():
        fund_me = FundMe.deploy(
            price_fee_address,
            {"from": account},
            publish_source=config["networks"][network.show_active()].get("verify"),
        )
    else:
        fund_me = FundMe.deploy(price_fee_address, {"from": account})

    print("Contract FundMe has been deployed at address :", fund_me)
    return fund_me


def main():
    deploy_fund_me()
