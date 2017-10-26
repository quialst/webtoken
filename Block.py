from time import localtime
from time import time
from time import struct_time
import hashlib

#TODO: replace bytearray() with str(<variable>).encode('utf-8')


class Block:

    def get_timestamp():
        t1 = localtime(time())
        parsed = ''
        for i in range(t1.n_sequence_fields):
            parsed = parsed + ' /' + t1[i]
        return parsed

    def __init__(self, block_id, prevhash, data):
        self.block_id = block_id
        self.timestamp = str(get_timestamp()).encode()
        self.prevhash = str(prevhash).encode()
        self.data = str(data).encode()
        self.hashdata = (str(block_id) + str(prevhash) + str(data)).encode()
        self.hash = hashlib.sha256(self.hashdata.encode()).digest()
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
