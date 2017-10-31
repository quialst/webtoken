import sqlite3
import sys
import subprocess
from time import localtime
from time import time
from time import struct_time
import os
#TODO: add sqlite3.OperationalError exception handlers
#TODO: should not be called for methods that are called by other methods
#TODO: raising and error as er does not work. Learn how to use __cause__
#TODO: replace bytearray() with str(<variable>).encode('utf-8')
#TODO: use type to verify that the database is a sqlite database
#TODO: insert is not working figure out why


class Blockchain:
    @staticmethod
    def create_blockchain():
        try:
            conn = sqlite3.connect('blockchain.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE blocks
            (block_id INTEGER PRIMARY KEY, prevhash BLOB NOT NULL, data BLOB NOT NULL, block_hash BLOB NOT NULL, nonce BLOB NOT NULL)''')
            conn.commit()
            conn.close()
            #update_chain()
        except sqlite3.Error as er:
            print("""error: {}
            Blockchain creation failed""".format(er.__cause__))
        except sqlite3.DatabaseError as er:
            print("""error: {}
            Blockchain creation failed""".format(er.__cause__))
        except sqlite3.IntegrityError as er:
            print("""error: {}
            Blockchain creation failed""".format(er.__cause__))
        except sqlite3.ProgrammingError as er:
            print("""error: {}
            Blockchain creation failed""".format(er.__cause__))
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Wallet creation stopped")
        except EOFError:
            print("EOFError: Unexpected end of file")
        except Exceptions.InsertException as er:
            print("""InsertException: Database insert failed
            {}: {}
            Blockchain creation failed""".format(er.error, er.__cause__))
        finally:
            """conn.rollback()
            conn.close()"""

    def update(variable, value, location, location_value):
        try:
            co = subprocess.check_output(["find", os.getcwd(), "-name", "blockchain.db"]).strip()
            conn = sqlite3.connect(str(co))
            c = conn.cursor()
            set_str = variable
            where_str = location
            if isinstance(value, str):
                if isinstance(location_value, str):
                    if location != 'block_id':
                        t = (value.encode(), location_value.encode)
                    elif location == 'block_id':
                        t = (value, location_value)
                    else:
                        raise TypeError('Invalid update argument')
                elif isinstance(location_value, int):
                    if location != 'block_id':
                        t = (value.encode(), bytes(location_value))
                    elif location == 'block_id':
                        t = (value, location_value)
                    else:
                        raise TypeError('Invalid update argument')
                else:
                    raise TypeError('Invalid update argument')
            elif isinstance(value, int):
                if isinstance(location_value, str):
                    if location != 'block_id':
                        t = (bytes(value), location_value.encode)
                    elif location == 'block_id':
                        t = (value, location)
                    else:
                        raise TypeError('Invalid update argument')
                elif isinstance(location_value, int):
                    if location != 'block_id':
                        t = (bytes(value), bytes(location_value))
                    elif location == 'block_id':
                        t = (value, location)
                    else:
                        raise TypeError('Invalid update argument')
                else:
                    raise TypeError('Invalid update argument')
            else:
                raise TypeError('Invalid update argument')
            c.execute('UPDATE blocks SET {} = ? WHERE {} = ?'.format(set_str, where_str), t)
            conn.commit()
            conn.close()
        except sqlite3.Error as er:
            raise UpdateException('Error', er.__cause__)
        except sqlite3.DatabaseError as er:
            raise UpdateException('DatabaseError', er.__cause__)
        except sqlite3.IntegrityError as er:
            raise UpdateException('IntegrityError', er.__cause__)
        except sqlite3.ProgrammingError as er:
            raise UpdateException('ProgrammingError', er.__cause__)
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Database update stopped")
        finally:
            """conn.rollback()
            conn.close()"""

    @staticmethod
    def retrieve(variable, condition, location, location_value, is_like):
        try:
            co = subprocess.check_output(["find", os.getcwd(), "-name", "blockchain.db"]).strip()
            conn = sqlite3.connect(str(co))
            c = conn.cursor()
            select_str = variable
            where_str = ''
            if condition == 'min' or condition == 'max':
                select_str = '{}({})'.format(condition.upper(), select_str)
            else:
                select_str = variable
            if location != None or location_value != None:
                where_str = '{}'.format(location)
                t = (location_value, )
                if is_like != True:
                    c.execute('SELECT {} FROM accounts WHERE {} = ?'.format(select_str, where_str), t)#usage: SELECT select_str(variable with condition) WHERE where_str(location) = location_value
                    a = c.fetchall()
                elif is_like == True:
                    c.execute('SELECT {} FROM accounts WHERE {} LIKE ?'.format(select_str, where_str), t)#usage: SELECT select_str(variable with condition) WHERE where_str(location) = location_value
                    a = c.fetchall()
                else:
                    raise Exceptions.RetrievalException('SQLite3ArgumentError', 'Invalid argument "{}"'.format(is_like))
            else:
                c.execute('SELECT {} FROM accounts'.format(select_str))
                a = c.fetchall()
            conn.close()
            return a# a is in byte form unless block_id
        except sqlite3.Error as er:
            raise Exceptions.RetrievalException('Error', er.__cause__)
        except sqlite3.DatabaseError as er:
            raise Exceptions.RetrievalException('DatabaseError', er.__cause__)
        except sqlite3.IntegrityError as er:
            raise Exceptions.RetrievalException('IntegrityError', er.__cause__)
        except sqlite3.ProgrammingError as er:
            raise Exceptions.RetrievalException('ProgrammingError', er.__cause__)
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Database insert stopped")
        finally:
            """conn.rollback()
            conn.close()"""

    @staticmethod
    def insert(block_id, prevhash, data, block_hash, nonce):
        try:
            co = subprocess.check_output(["find", os.getcwd(), "-name", "blockchain.db"]).strip()
            conn = sqlite3.connect(str(co))
            c = conn.cursor()
            t = (block_id, prevhash.encode(), data.encode(), block_hash.encode(), nonce.encode())
            c.execute('INSERT INTO blocks VALUES (?,?,?,?,?)', t)
            conn.commit()
            conn.close()
            #
        except sqlite3.Error as er:
            raise Exceptions.InsertException('Error', er.__cause__)
        except sqlite3.DatabaseError as er:
            raise Exceptions.InsertException('DatabaseError', er.__cause__)
        except sqlite3.IntegrityError as er:
            raise Exceptions.InsertException('IntegrityError', er.__cause__)
        except sqlite3.ProgrammingError as er:
            raise Exceptions.InsertException('ProgrammingError', er.__cause__)
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Database insert stopped")
        finally:
            """conn.rollback()
            conn.close()"""


    def update_chain():
        try:
            co = subprocess.check_output(["find", os.getcwd(), "-name", "blockchain.db"]).strip()
            conn = sqlite3.connect(str(co))
            c = conn.cursor()
            a = retrieve('block_id', 'max', None, None, False)
            b = Node.block_retrieve('block_id', 'max', None, None, False)
            while a[0] < b[0]:
                x = retrieve('block_id', 'max', None, None, False)
                data = Node.block_retrieve('*', None, 'block_id', x[0]+1, False)
                insert(data[0], data[1].encode(), data[2].encode(), data[3].encode(), data[4].encode())
                a = retrieve('block_id', 'max', None, None, False)
            else:
                print("Updated")
            print("Updated")
            conn.commit()
            conn.close()
        except sqlite3.Error as er:
            raise Exceptions.UpdateChainException('Error', er.__cause__)
        except sqlite3.DatabaseError as er:
            raise Exceptions.UpdateChainException('DatabaseError', er.__cause__)
        except sqlite3.IntegrityError as er:
            raise Exceptions.UpdateChainException('IntegrityError', er.__cause__)
        except sqlite3.ProgrammingError as er:
            raise Exceptions.UpdateChainException('ProgrammingError', er.__cause__)
        except Exceptions.InsertException as er:
            raise Exceptions.UpdateChainException('InsertException', er.__cause__)
        except subprocess.SubprocessError as er:
            raise Exceptions.UpdateChainException('SubprocessError', er.__cause__)
        except subprocess.TimeoutExpired as er:
            raise Exceptions.UpdateChainException('TimeoutExpired', er.__cause__)
        except subprocess.CalledProcessError as er:
            raise Exceptions.UpdateChainException('CalledProcessError', er.__cause__)
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Chain update stopped")

    """def genesis_block():#TODO: add exception handlers
        try:
            genhash = bytearray('0000000000000000000000000000000000000000000000000000000000000000')#TODO: make real hash
            Transaction('0000000000000000000000000000000000000000000000000000000000000000',)
            gendata = '000000000000000000000000000000000 - 5000000 > $$$\n$$$ - 5000000 > 16UwLL9Risc3QfPqBUvKofHmBQ7wMtjvM\n'
            b = Block(0, genhash, gendata)


    def searchBlock():
        try:
            co = subprocess.check_output(["find", os.getcwd(), "-name", "blockchain.db"]).strip()
            conn = sqlite3.connect(co)
            del co
            c = conn.cursor()


    def replaceBlockchain():
        try:
            co = subprocess.check_output(["find", os.getcwd(), "-name", "blockchain.db"]).strip()
            conn = sqlite3.connect(co)
            del co
            c = conn.cursor()
            """
#def searchTransaction():
Blockchain.create_blockchain()
Blockchain.insert(0, 'foo', 'bar', 'baq', 'qab')
print(str(Blockchain.retrieve('block_id', None, None, None, None)))
