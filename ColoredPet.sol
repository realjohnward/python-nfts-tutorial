pragma solidity ^0.6.6;
import "github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v3.4/contracts/token/ERC721/ERC721.sol";

//this contract inherits ERC721
contract ColoredPet is ERC721 {
    uint256 public tokenCounter;
    
    
    //constructor for an ERC721 is a name and symbol
    constructor () public ERC721 ("ColoredPets", "COLOREDPET"){
        tokenCounter = 0;
    }

    //a token url is a ipfs url
    //after we mint the token we are going to return the id of the token
    function createNFT(string memory tokenURI) public returns (uint256) {

    //get number from token counter
        uint256 newNFTTokenId = tokenCounter;

    //safely mint token for the person that called the function
        _safeMint(msg.sender, newNFTTokenId);
    
    //set the token uri of the token id of the uri passed
        _setTokenURI(newNFTTokenId, tokenURI);
    
    //increment the counter
        tokenCounter = tokenCounter + 1;
        
    //return the token id
        return newNFTTokenId;
    }

}