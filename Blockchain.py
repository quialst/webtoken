import sqlite3
import sys
import subprocess
from time import localtime
from time import time
from time import struct_time
import os
import Exceptions
#TODO: add sqlite3.OperationalError exception handlers
#TODO: some stuff should not be called for methods that are called by other methods
#TODO: find out how to rollback a connection in a finally clause


class Blockchain:
    def update_chain():
        try:
            co = subprocess.check_output(["find", os.getcwd(), "-name", "blockchain.db"]).strip()
            conn = sqlite3.connect(str(co.decode()))
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
            raise Exceptions.UpdateChainException('Error', 'foo')
        except sqlite3.DatabaseError as er:
            raise Exceptions.UpdateChainException('DatabaseError', 'foo')
        except sqlite3.IntegrityError as er:
            raise Exceptions.UpdateChainException('IntegrityError', 'foo')
        except sqlite3.ProgrammingError as er:
            raise Exceptions.UpdateChainException('ProgrammingError', 'foo')
        except Exceptions.InsertException as er:
            raise Exceptions.UpdateChainException('InsertException', 'foo')
        except subprocess.SubprocessError as er:
            raise Exceptions.UpdateChainException('SubprocessError', 'foo')
        except subprocess.TimeoutExpired as er:
            raise Exceptions.UpdateChainException('TimeoutExpired', 'foo')
        except subprocess.CalledProcessError as er:
            raise Exceptions.UpdateChainException('CalledProcessError', 'foo')
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Chain update stopped")

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
        #except sqlite3.Error as er:
            #print('sqlite eror')
            #print("""error: {}
            #Blockchain creation failed""".format('foo'))
        #except sqlite3.DatabaseError as er:
            #print('database')
            #print("""error: {}
            #Blockchain creation failed""".format('foo'))
        #except sqlite3.IntegrityError as er:
            #print('integrity')
            #print("""error: {}
            #Blockchain creation failed""".format('foo'))
        #except sqlite3.ProgrammingError as er:
            #print('programming')
            #print("""error: {}
            #Blockchain creation failed""".format('foo'))
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Wallet creation stopped")
        except EOFError:
            print("EOFError: Unexpected end of file")
        except Exceptions.InsertException as er:
            print('insert exception')
            #print("""InsertException: Database insert failed
            #{}: {}
            #Blockchain creation failed""".format('bar', 'foo'))
        finally:
            pass
            #conn.rollback()
            #conn.close()

    def update(variable, value, location, location_value):
        try:
            co = subprocess.check_output(["find", os.getcwd(), "-name", "blockchain.db"]).strip()
            conn = sqlite3.connect(str(co.decode()))
            c = conn.cursor()
            set_str = variable
            where_str = location
            if isinstance(value, str):
                if isinstance(location_value, str):
                    if location != 'block_id':
                        t = (value.encode(), location_value.encode())
                    elif location == 'block_id':
                        t = (value, location_value)
                    else:
                        raise TypeError('Invalid update argument')
                elif isinstance(location_value, int):
                    if location != 'block_id':
                        t = (value.encode(), bytes(location_value))
                    elif location == 'block_id':
                        t = (value.encode(), location_value)
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
            raise UpdateException('Error', 'foo')
        except sqlite3.DatabaseError as er:
            raise UpdateException('DatabaseError', 'foo')
        except sqlite3.IntegrityError as er:
            raise UpdateException('IntegrityError', 'foo')
        except sqlite3.ProgrammingError as er:
            raise UpdateException('ProgrammingError', 'foo')
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Database update stopped")
        finally:
            pass
            #conn.rollback()
            #conn.close()

    @staticmethod
    def retrieve(variable, condition, location, location_value, is_like):
        try:
            co = subprocess.check_output(["find", os.getcwd(), "-name", "blockchain.db"]).strip()
            conn = sqlite3.connect(str(co.decode()))
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
                    c.execute('SELECT {} FROM blocks WHERE {} = ?'.format(select_str, where_str), t)#usage: SELECT select_str(variable with condition) WHERE where_str(location) = location_value
                    a = c.fetchall()
                elif is_like == True:
                    c.execute('SELECT {} FROM blocks WHERE {} LIKE ?'.format(select_str, where_str), t)#usage: SELECT select_str(variable with condition) WHERE where_str(location) = location_value
                    a = c.fetchall()
                else:
                    raise Exceptions.RetrievalException('SQLite3ArgumentError', 'Invalid argument "{}"'.format(is_like))
            else:
                c.execute('SELECT {} FROM blocks'.format(select_str))
                a = c.fetchall()
            conn.close()
            return a# a is in byte form unless block_id
        except sqlite3.Error as er:
            raise Exceptions.RetrievalException('Error', 'foo')
        except sqlite3.DatabaseError as er:
            raise Exceptions.RetrievalException('DatabaseError', 'foo')
        except sqlite3.IntegrityError as er:
            raise Exceptions.RetrievalException('IntegrityError', 'foo')
        except sqlite3.ProgrammingError as er:
            raise Exceptions.RetrievalException('ProgrammingError', 'foo')
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Database insert stopped")
        finally:
            pass
            #conn.rollback()
            #conn.close()

    @staticmethod
    def insert(block_id, prevhash, data, block_hash, nonce):
        try:
            co = subprocess.check_output(["find", os.getcwd(), "-name", "blockchain.db"]).strip()
            conn = sqlite3.connect(str(co.decode()))
            c = conn.cursor()
            t = (block_id, prevhash.encode(), data.encode(), block_hash.encode(), nonce.encode())
            c.execute('INSERT INTO blocks VALUES (?,?,?,?,?)', t)
            conn.commit()
            conn.close()
        except sqlite3.Error as er:
            pass
            #raise Exceptions.InsertException('Error', 'foo')
        except sqlite3.DatabaseError as er:
            pass
            #raise Exceptions.InsertException('DatabaseError', 'foo')
        except sqlite3.IntegrityError as er:
            pass
            #raise Exceptions.InsertException('IntegrityError', 'foo')
        except sqlite3.ProgrammingError as er:
            pass
            #raise Exceptions.InsertException('ProgrammingError', 'foo')
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Database insert stopped")
        finally:
            pass
            #conn.rollback()
            #conn.close()

    def genesis_block():#TODO: add exception handlers
        try:
            t = Transaction('0000000000000000000000000000000000000000000000000000000000000000', ('16UwLL9Risc3QfPqBUvKofHmBQ7wMtjvM', ), '5000000', 'GEN-CUR')
            prevhash = '0000000000000000000000000000000000000000000000000000000000000000'#TODO: make real hash
            gendata = t.data
            b = Block(0, prevhash, gendata)
            return b
            # returns Block object
        except Exceptions.TransactionError as er:
            print('error: ')
            #Failed to retrieve genesis block""".format(er.message)


    def searchBlock():
        try:
            co = subprocess.check_output(["find", os.getcwd(), "-name", "blockchain.db"]).strip()
            conn = sqlite3.connect(co)
            del co
            c = conn.cursor()
        except:
            pass

    def replaceBlockchain():
        try:
            co = subprocess.check_output(["find", os.getcwd(), "-name", "blockchain.db"]).strip()
            conn = sqlite3.connect(co)
            del co
            c = conn.cursor()
        except:
            pass
