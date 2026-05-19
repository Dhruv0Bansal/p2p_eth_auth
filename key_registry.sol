// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract KeyRegistry {
    mapping(address => string) public publicKeys;
    event KeyRegistered(address indexed user, string key);

    function register(string calldata key) external {
        publicKeys[msg.sender] = key;
        emit KeyRegistered(msg.sender, key);
    }

    function get(address user) external view returns (string memory) {
        return publicKeys[user];
    }
}