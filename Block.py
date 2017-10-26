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
        self.timestamp = bytearray(get_timestamp(), encoding='utf-8')#datetime has not attribute now fix
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
