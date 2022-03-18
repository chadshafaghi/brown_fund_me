// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address public owner;
    address[] public funders;
    AggregatorV3Interface public priceFeed;

    uint256 public minimuFundTreshold = 50 * 10**18; //50 USD :

    constructor(address _priceFeed) public {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed);
        // Rinkeby priceFeed Address : 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
    }

    modifier onlyOwner() {
        // only want the contract owner persona
        require(msg.sender == owner, "only the DAO can execute withdraw");
        _;
    }

    modifier minimumFundingTreshold() {
        // only want the contract owner persona
        require(
            getConversionRate(msg.value) >= minimuFundTreshold,
            "you need to send USD 50 at least"
        );
        _;
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 minUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return ((minUSD * precision) / price);
    }

    function fund() public payable minimumFundingTreshold {
        //msg.sender = adress of the sender
        //msg.value = amount sended by the sender
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function withdraw() public payable onlyOwner {
        msg.sender.transfer(address(this).balance);
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000); // this is to covert in wei. Already 8 decimals, adding 10 to have ^18.
        //2,920.81945273
    }

    // sending / returning is in Gwei
    // 1 Gwei >  1000000000 WEI (10^9)
    // 1 Gwei > 0.000000001 Eth  (1/^9)
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountinUSD = ((ethPrice * ethAmount) / 1000000000000000000); // this is to convert to gwei
        return ethAmountinUSD;
    }
}
