# -*- coding: latin1 -*-
import hashlib
import ecdsa
from ecdsa import SigningKey
from ecdsa import SECP256k1
import base58
import sqlite3
import sys
from subprocess import check_output
import os
import Exceptions
#TODO: sys.exit(0) should not be called for methods that are called by other methods
#TODO: use type to verify that the database is a sqlite database
class Account:
    @staticmethod
    def create_wallet():
        try:
            conn = sqlite3.connect('wallet.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE accounts
            (id_num INTEGER PRIMARY KEY ASC, address BLOB NOT NULL, privkey BLOB NOT NULL,
            pubkey BLOB NOT NULL, sig BLOB NOT NULL, sigtext BLOB NOT NULL, balance BLOB)''')
            conn.commit()
            conn.close()
        except sqlite3.Error as er:
            print("""error: {}
            Wallet creation failed""".format(er.msg))
        except sqlite3.DatabaseError as er:
            print("""error: {}
            Wallet creation failed""".format(er.msg))
        except sqlite3.IntegrityError as er:
            print("""error: {}
            Wallet creation failed""".format(er.msg))
        except sqlite3.ProgrammingError as er:
            print("""error: {}
            Wallet creation failed""".format(er.msg))
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Wallet creation stopped")
        except EOFError:
            print("EOFError: Unexpected end of file")
        finally:
            pass

    def insert(id_num, address, privkey, pubkey, sig, sigtext, balance):
        try:
            co = check_output(["find", os.getcwd(), "-name", "wallet.db"]).strip()
            conn = sqlite3.connect(str(co.decode()))
            del co
            c = conn.cursor()
            t = (id_num, address, privkey, pubkey, sig, sigtext, balance)
            c.execute('INSERT INTO accounts VALUES (?,?,?,?,?,?,?)', t)
            conn.commit()
            conn.close()
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Database insert stopped")
        finally:
            pass

    def retrieve(variable = '*', condition = None, location = None, location_value = None, is_like = False):#usage variable(desired data) condition(min max or none) location(WHERE variable) location (WHERE variable value) is_like(LIKE clause desired)
        co = check_output(["find", os.getcwd(), "-name", "wallet.db"]).strip()
        conn = sqlite3.connect(str(co.decode()))
        del co
        c = conn.cursor()
        select_str = variable
        where_str = ''
        if condition == 'min' or condition == 'max':
            select_str = '{}({})'.format(condition.upper(), select_str)
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
        return a #a is in bytes if not block_id
        sys.exit(0)

    def update(variable, value, location, location_value):
        """variable is the variably you want to change. value is the desired value for the variable"""
        try:
            co = check_output(["find", os.getcwd(), "-name", "wallet.db"]).strip()
            conn = sqlite3.connect(str(co.decode()))
            c = conn.cursor()
            set_str = variable
            where_str = location
            if isinstance(value, str):
                if location != 'block_id':
                    t = (value.encode(), location_value)
                elif location == 'block_id':
                    t = (value, location_value)
                else:
                    raise TypeError('Invalid update argument')
            elif isinstance(value, int):
                if location != 'block_id':
                    t = (str(value).encode(), location_value)
                elif location == 'block_id':
                    t = (value, location)
                else:
                    raise TypeError('Invalid update argument')
            else:
                raise TypeError('Invalid update argument')
            print(set_str)
            print(where_str)
            print(t)
            c.execute('UPDATE accounts SET {} = ? WHERE {} = ?'.format(set_str, where_str), t)
            conn.commit()
            conn.close()
        except sqlite3.Error as er:
            raise Exceptions.RetrievalException('Error', er.msg)
        except sqlite3.DatabaseError as er:
            raise Exceptions.RetrievalException('DatabaseError', er.msg)
        except sqlite3.IntegrityError as er:
            raise Exceptions.RetrievalException('IntegrityError', er.msg)
        except sqlite3.ProgrammingError as er:
            raise Exceptions.RetrievalException('ProgrammingError', er.msg)
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Database update stopped")
        finally:
            pass

    def new_address():
        try:
            id_num = Account.retrieve('id_num', 'max')[0][0]
            if id_num == None:
                id_num = 0
            else:
                id_num = id_num + 1
            sk = SigningKey.generate(curve=SECP256k1)# private ecdsa key
            vk = sk.get_verifying_key()# verifying key j4kiks
            sigtext = b"signature"
            sig = sk.sign(sigtext)
            s1 = hashlib.sha256(sk.to_string()).digest()# sha hashing of public key in binary
            temp = hashlib.new('ripemd160')# make ripemd150 object
            temp.update(s1)# update the object
            s2 = temp.digest()# binary digest of ak
            s3 = (b'\x30'+s2)# add the version byte to bk
            s4 = hashlib.sha256(hashlib.sha256(s3).digest()).digest()# doulbe sha hash of ck
            s5 = s4[0:4]# take first 4 bytes
            s6 = (s3+s5)# add 4 bytes to end of ck
            address = base58.b58encode(s6)# do a base58 encode
            Account.insert(id_num, address.encode(), sk.to_string(), vk.to_string(), sig, sigtext, 0)
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Wallet creation stopped")
        except EOFError:
            print("EOFError: Unexpected end of file")
        finally:
            pass
