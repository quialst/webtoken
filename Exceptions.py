
#TODO: get help with this class. so much is wrong

class RetrievalException(Exception):
    def __init__(self, error, message):
        Exception.__init__(self)
        self.error = error
        self.message = message
    msg = self.message
class InsertException(Exception):
    def __init__(self, error, message):
        Exception.__init__(self)
        self.error = error
        self.message = message
    msg = self.message
class UpdateException(Exception):
    def __init__(self, error, message):
        Exception.__init__(self)
        self.error = error
        self.message = message
    msg = self.message
class UpdateChainException(Exception):
    def __init__(self, error, message):
        Exception.__init__(self)
        self.error = error
        self.message = message
    msg = self.message
class BlockError(Exception):
    def __init__(self, error, message):
        Exception.__init(self)
        self.error = message
        self.message = message
    msg = self.message
class TransactionError(Exception):
    def __init__(self, error, message):
        Exception.__init(self)
        self.error = message
        self.message = message
    msg = self.message
