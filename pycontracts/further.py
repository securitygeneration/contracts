from pycontracts import contracts
from pycontracts.forward import Forward
from web3 import Web3

class Further(Forward):
    def __init__(self, w3, address):
        super().__init__(address)
        self.w3 = w3

    @staticmethod
    def wrap(w3, address):
        return Further(w3, address)


    @staticmethod
    def deploy(w3, owner, originator):
        def push(bs):
            return (0x60 + len(bs) - 1).to_bytes(1, 'big') + bs

        init = push(Web3.toBytes(hexstr=owner)) + contracts['further']['deploy']

        tx_hash = w3.eth.sendTransaction({
            'from': originator,
            'data': init,
        })
        r = w3.eth.waitForTransactionReceipt(tx_hash)
        return Further.wrap(w3, r.contractAddress)

    @property
    def owner(self):
        bs = self.w3.eth.call({ 'to': self.address })
        return Web3.toChecksumAddress(Web3.toHex(bs[:20]))

    def nonce(self):
        bs = self.w3.eth.call({ 'to': self.address })
        return int.from_bytes(bs[20:20+32], 'big')

    def sign(self, private_key, target, value, data, nonce):
        if hasattr(data, 'buildTransaction'):
            t = data.buildTransaction({"nonce": 0, "gas": 0, "gasPrice": 0})
            data = Web3.toBytes(hexstr = t['data'])
            if not target:
                target = t['to']

        return bytes(12) + Web3.toBytes(hexstr=target) + value.to_bytes(32, 'big') + data

    def transact(self, private_key, originator, target = None, value = 0, data = b'', nonce = None):
        self.w3.eth.sendTransaction({
            'to': self.address,
            'from': originator,
            'data': self.sign(private_key, target, value, data, nonce),
            'gasLimit': 100000000
        })

    def call(self, private_key, target = None, value = 0, data = b'', nonce = None, type=bytes):
        res = self.w3.eth.call({
            'to': self.address,
            'data': self.sign(private_key, target, value, data, nonce),
            'gasLimit': 100000000
        })
        if type == bytes:
            return res
        if type == int:
            return int.from_bytes(res, 'big')