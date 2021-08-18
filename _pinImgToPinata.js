const process = require("process");
const fs = require('fs');
const pinataSDK = require('@pinata/sdk');
const PINATA_API_KEY = '00951809b073d0a55e9a';
const PINATA_SECRET_API_KEY = '3b1089f9a77e2f6cee967aeab3bcda8c9427e519b118f07bbf274ae00993983f';
const pinata = pinataSDK(PINATA_API_KEY, PINATA_SECRET_API_KEY);

var imgPath = process.argv[2]
const readableStreamForFile = fs.createReadStream(imgPath);
const options = {};

pinata.pinFileToIPFS(readableStreamForFile, options).then((result) => {
    console.log(result["IpfsHash"])
}).catch((err) => {
    console.log(err)
});
