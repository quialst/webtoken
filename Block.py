from datetime import datetime
import hashlib

class Block:
    def __init__(self, block_id, prevhash, data):
        self.block_id = block_id
        self.timestamp = now()
        self.prevhash = prevhash
        self.data = data
        self.hashdata = str(block_id) + str(prevhash) + str(data)
        self.hash = hashlib.sha256(self.hashdata).digest()
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
