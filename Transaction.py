from datetime import datetime
import hashlib

#add parsing of dest tuple for hashing and to_string

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

    def to_string(self, trans, from_address, dest, amount, transaction_type):
        x = ''
        tup = (trans_hash, from_address, dest, amount, transaction_type)
        for i in len(tup):
            if i != 2:
                x = x + tup[i]
            elif i == 2:
                x = x + parse_dest(tup[i])
            else:
                raise TransactionError
        return x

    def __init__(self, from_address, dest, amount, transaction_type):
        self.from_address = from_address
        self.num_of_dest = len(dest)
        #dest needs to include the from address as the first address in the tuple
        self.dest = parse_dest(dest)#dest is a tuple of to addresses.
        self.amount = amount
        self.transaction_type = transaction_type
        #add hashing of data
        self.trans_hash = hashlib.sha256(bytearray(self.from_address, encoding='utf-8'))
        self.data = to_string(self.trans_hash, self.from_address, self.num_of_dest, dest, self.amount, self.transaction_type)

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
