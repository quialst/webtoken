from datetime import datetime
import hashlib

#9

class Block:
    def __init__(self, block_id, prevhash, data):
        self.block_id = block_id)
        self.timestamp = bytearray(now(), encoding='utf-8')#datetime has not attribute now fix
        self.prevhash = bytearray(prevhash, encoding='utf-8')
        self.data = bytearray(data, encoding='utf-8')
        self.hashdata = bytearray(str(block_id) + str(prevhash) + str(data), encoding='utf-8')
        self.hash = bytearray(hashlib.sha256(self.hashdata).hexdigest(), encoding='utf-8')
    def get_block_id(self):
        return self.block_id
    def get_timestamp(self):
        return self.timestamp
    def get_prevhash(self):
        return self.prevhash
    def get_data(self):
        return self.data
    def get_hash(self):
        return self.hash
