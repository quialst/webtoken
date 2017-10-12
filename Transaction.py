from datetime import datetime

class Transaction:
    def __init__(self, from_address, dest, amount, transaction_type):
        self.from_address = from_address
        self.num_of_dest = len(dest)
        #dest needs to include the from address as the first address in the tuple
        self.dest = dest#dest is a tuple of to addresses.
        self.amount = amount
        self.transaction_type = transaction_type
        self.hash = #insert code for hashed to

    def to_string(self):
