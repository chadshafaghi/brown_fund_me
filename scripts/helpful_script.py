from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3


DECIMAL = 8
STARTING_PRICE = 200000000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
MAINNET_FORK = ["mainnet-fork", "mainnet-fork-dev"]


def is_local_env():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return True
    else:
        return False


def get_account():
    print(network.show_active())
    if is_local_env() or network.show_active() in MAINNET_FORK:
        return accounts[0]
    else:
        return accounts.add(config["wallet"]["from_key"])


def get_price_feed_address():
    if not is_local_env():
        print("Environment is not Local .... Getting network V3Aggregator instance")
        return config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        print("Environment is Local .... a Mocked V3Aggregator is required ")
        if len(MockV3Aggregator) <= 0:
            mock_v3aggregator = deploy_mock_v3aggregator()
        else:
            mock_v3aggregator = MockV3Aggregator[-1].address
            print(
                "An existing V3Aggregator contract has been identified at address:",
                MockV3Aggregator[-1].address,
            )
        return mock_v3aggregator


def deploy_mock_v3aggregator():
    print("Creating mock for PriceFeed V3Aggregator Contract")
    mock_v3aggregator = MockV3Aggregator.deploy(
        DECIMAL, STARTING_PRICE, {"from": get_account()}
    )
    print(
        "A New PriceFeed V3Aggregator mock contract created at address:",
        mock_v3aggregator,
    )
    return mock_v3aggregator
