from time import localtime
from time import time
from time import struct_time
import hashlib

#TODO: add parsing of dest tuple for hashing and to_string
#TODO: turn all data into bytearray
#TODO: replace bytearray() with str(<variable>).encode('utf-8')

class Transaction:
    @staticmethod
    def parse_dest(dest):
        if type(dest) == type(('', )):
            x = ''
            for i in len(dest):
                x = x + ' ' + dest[i]
        else:
            raise Exceptions.TransactionError
        return x

    def to_string(self, trans, from_address, dest, amount, transaction_type, timestamp):
        x = ''
        tup = (trans_hash, from_address, dest, amount, transaction_type, timestamp)
        for i in len(tup):
            if i != 2:
                x = x + tup[i]
            elif i == 2:
                x = x + parse_dest(tup[i])
            else:
                raise TransactionError
        return x

    def get_timestamp():
        t1 = localtime(time())
        parsed = ''
        for i in range(t1.n_sequence_fields):
            parsed = parsed + ' /' + t1[i]
        return parsed

    def __init__(self, from_address, dest, amount, transaction_type):# dest IS A TUPLE
        self.from_address = bytearray(from_address, encoding='utf-8')
        self.num_of_dest = bytearray(len(dest), encoding='utf-8')
        #dest needs to include the from address as the first address in the tuple
        self.dest = bytearray(parse_dest(dest), encoding='utf-8')#dest is a tuple of to addresses.
        self.amount = bytearray(amount, encoding='utf-8')
        self.transaction_type = bytearray(transaction_type, encoding='utf-8')
        self.timestamp = bytearray(get_timestamp(), encoding='utf-8')
        #TODO: add hashing of data
        self.trans_hash = hashlib.sha256().digest()
        self.data = to_string(self.trans_hash, self.from_address, self.num_of_dest, dest, self.amount, self.transaction_type, self.timestamp)

    def get_from_address(self):
        return self.from_address

    def get_num_of_dest(self):
        return self.num_of_dest

    def get_dest(self):
        return self.dest

    def get_amount(self):
        return self.amount

    def get_transaction_type(self):
        return self.transaction_type

    def get_tans_hash(self):
        return self.trans_hash

    def get_data(self):
        return self.data
