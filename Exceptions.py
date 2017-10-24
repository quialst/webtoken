
#TODO: add update chain Exception

class RetrievalException(Exception):
    def __init__(self, error, message):
        Exception.__init__(self)
        self.error = error
        self.message = message
    __cause__ = self.message
class InsertException(Exception):
    def __init__(self, error, message):
        Exception.__init__(self)
        self.error = error
        self.message = message
    __cause__ = self.message
class UpdateException(Exception):
    def __init__(self, error, message):
        Exception.__init__(self)
        self.error = error
        self.message = message
    __cause__ = self.message
class UpdateException(Exception):
    def __init__(self, error, message):
        Exception.__init__(self)
        self.error = error
        self.message = message
    __cause__ = self.message
class BlockError(Exception):
    def __init__(self, error, message):
        Exception.__init(self)
        self.error = message
        self.message = message
    __cause__ = self.message
class TransactionError(Exception):
    def __init__(self, error, message):
        Exception.__init(self)
        self.error = message
        self.message = message
    __cause__ = self.message
