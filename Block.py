from time import localtime
from time import time
from time import struct_time
import hashlib
#TODO: add append data


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

    def append_data(self, new_data):
        self.data = self.data + str(new_data).encode()
