from datetime import datetime
import hashlib

#9

class Block:
    def __init__(self, block_id, prevhash, data):
        self.block_id = bytes(block_id)
        self.timestamp = bytes(now())#datetime has not attribute now fix
        self.prevhash = bytes(prevhash)
        self.data = bytes(data)
        self.hashdata = bytes(str(block_id) + str(prevhash) + str(data))
        self.hash = bytes(hashlib.sha256(self.hashdata).digest())
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
