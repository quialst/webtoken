import sqlite3
import sys
from subprocess import check_output
from time import localtime
from time import time
from time import struct_time
import os
import Exceptions
#TODO: add sqlite3.OperationalError exception handlers
#TODO: some stuff should not be called for methods that are called by other methods


class Blockchain:
    def update_chain():
        try:
            co = check_output(["find", os.getcwd(), "-name", "blockchain.db"]).strip()
            conn = sqlite3.connect(str(co.decode()))
            c = conn.cursor()
            a = retrieve('block_id', 'max', None, None, False)
            b = Node.block_retrieve('block_id', 'max', None, None, False)
            while a[0] < b[0]:
                x = retrieve('block_id', 'max', None, None, False)
                data = Node.query_data()
                insert(data[0], data[1].encode(), data[2].encode(), data[3].encode(), data[4].encode())
                a = retrieve('block_id', 'max', None, None, False)
            else:
                print("Updated")
            print("Updated")
            conn.commit()
            conn.close()
        except:
            print('\aError:\nCould not update the blockcain')
        finally:
            sys.exit(0)

    def create_blockchain():
        try:
            co = check_output(["find", os.getcwd(), "-name", "blockchain.db"]).strip()
            conn = sqlite3.connect(str(co.decode()))
            c = conn.cursor()
            c.execute('''CREATE TABLE blocks
            (block_id INTEGER PRIMARY KEY, prevhash BLOB NOT NULL, data BLOB NOT NULL, block_hash BLOB NOT NULL, nonce BLOB NOT NULL)''')
            conn.commit()
            conn.close()
            update_chain()
        except:
            print('\aError:\nCould not create blockchain')
        finally:
            sys.exit(0)

    def update(variable, value, location, location_value):
        try:
            co = check_output(["find", os.getcwd(), "-name", "blockchain.db"]).strip()
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
                        raise BaseException
                elif isinstance(location_value, int):
                    if location != 'block_id':
                        t = (value.encode(), bytes(location_value))
                    elif location == 'block_id':
                        t = (value.encode(), location_value)
                    else:
                        raise BaseException
                else:
                    raise BaseException
            elif isinstance(value, int):
                if isinstance(location_value, str):
                    if location != 'block_id':
                        t = (bytes(value), location_value.encode)
                    elif location == 'block_id':
                        t = (value, location)
                    else:
                        raise BaseException
                elif isinstance(location_value, int):
                    if location != 'block_id':
                        t = (bytes(value), bytes(location_value))
                    elif location == 'block_id':
                        t = (value, location)
                    else:
                        raise BaseException
                else:
                    raise BaseException
            else:
                raise BaseException
            c.execute('UPDATE blocks SET {} = ? WHERE {} = ?'.format(set_str, where_str), t)
            conn.commit()
            conn.close()
        except:
            print('\aError:\nCould not update block')
        finally:
            sys.exit(0)

    def retrieve(variable = '*', condition = None, location = None, location_value = None, is_like = False):
        try:
            co = check_output(["find", os.getcwd(), "-name", "blockchain.db"]).strip()
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
                    raise BaseException
            else:
                c.execute('SELECT {} FROM blocks'.format(select_str))
                a = c.fetchall()
            conn.close()
            return a# a is in byte form unless block_id
        except:
            print('\aError:\nCould not retrieve block')
        finally:
            sys.exit(0)

    def insert(block_id, prevhash, data, block_hash, nonce):
        try:
            co = check_output(["find", os.getcwd(), "-name", "blockchain.db"]).strip()
            conn = sqlite3.connect(str(co.decode()))
            c = conn.cursor()
            t = (block_id, prevhash.encode(), data.encode(), block_hash.encode(), nonce.encode())
            c.execute('INSERT INTO blocks VALUES (?,?,?,?,?)', t)
            conn.commit()
            conn.close()
        except:
            print('\aError:\nCould not insert block')
        finally:
            sys.exit(0)

    def genesis_block():
        try:
            t = Transaction('0000000000000000000000000000000000000000000000000000000000000000', ('16UwLL9Risc3QfPqBUvKofHmBQ7wMtjvM', ), '5000000', 'GEN-CUR')
            prevhash = '0000000000000000000000000000000000000000000000000000000000000000'#TODO: make real hash
            gendata = t.data
            b = Block(0, prevhash, gendata)
            return b
            # returns Block object
        except:
            print('\aError:\nCould not load genesis block')
        finally:
            sys.exit(0)

    def replaceBlockchain(primer_id, node_ip):#TODO: add parsing of data from Node.query_data()
        x = 0
        while True:
            block = Node.query_data(time=2, id_num=(primer_id+x), node=node_ip)
            if block == None:
                break
            #parsing goes wherever "block" is called in Blockchain.update(). "block" is a stand in
            Blockchain.update('prevhash', block, 'block_id', (primer_id+x))
            Blockchain.update('data', block, 'block_id', (primer_id+x))
            Blockchain.update('block_hash', block, 'block_id', (primer_id+x))
            Blockchain.update('nonce', block, 'block_id', (primer_id+x))
            Blockchain.update('balance', block, 'block_id', (primer_id+x))
            x = x + 1
