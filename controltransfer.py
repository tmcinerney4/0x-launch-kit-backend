from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

def issuance_contract(conaddr, privkey, abi):
    w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/6525379c8368414e87dcea85ea89a3c2"))
    w3.middleware_onion.inject(geth_poa_middleware,layer=0)
    address = w3.toChecksumAddress(conaddr)
    con = w3.eth.contract(address=address,abi=abi)
    acct = w3.eth.account.privateKeyToAccount(privkey)
    return con, w3, acct

privkey = '405d2ec220aec8a9f429f6d9fbe0a5f0b0a514175ecc88a9676f2ad7aee0514b'
pubaddr = '0xc3af8595E01Dc6Ed9820A18f7Fee7f10b6E8bCb9'
toaddr = '0xDAb44562b628736554D8a11562c51b103Aa843e0'
fromAddr = '0xbb3c4183f95c4e1a07cb0f6127a43922ebd21784'
conaddr = '0xc3f89e22d785348af45d2edbe5dc8e70ba2f4341'
amount = 1000
with open('./StandaloneERC20.abi', 'r') as fp:
    abi = json.load(fp)
amount *= 10**18
contract, w3, acct = issuance_contract(conaddr, privkey, abi)
toaddr = w3.toChecksumAddress(toaddr)
fromAddr = w3.toChecksumAddress(fromAddr)
nonce = w3.eth.getTransactionCount(w3.toChecksumAddress(pubaddr))
txn = contract.functions.controlTransfer(fromAddr,toaddr,amount).buildTransaction({'from':pubaddr,'gas':5000000,'gasPrice':w3.toWei(1,'gwei'), 'nonce':nonce})
signed_txn = acct.signTransaction(txn)
w3.eth.sendRawTransaction(signed_txn.rawTransaction)

