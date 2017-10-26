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
#TODO: sys.exit(0) should not be called for methods that are called by other methods
#TODO: use type to verify that the database is a sqlite database

class Account:
    def create_wallet():
        try:
            co = check_output(["find", os.getcwd(), "-name", "wallet.db"]).strip()
            conn = sqlite3.connect(co)
            del co
            c = conn.cursor()
            c.execute('''CREATE TABLE accounts
            (id_num INTEGER PRIMARY KEY ASC, address BLOB NOT NULL, privkey BLOB NOT NULL,
            pubkey BLOB NOT NULL, sig BLOB NOT NULL, sigtext, BLOB NOT NULL, balance BLOB)''')
            new_wallet()
            conn.commit()
            conn.close()
        except sqlite3.Error as er:
            print("""error: {}
            Wallet creation failed""".format(er.__cause__))
        except sqlite3.DatabaseError as er:
            print("""error: {}
            Wallet creation failed""".format(er.__cause__))
        except sqlite3.IntegrityError as er:
            print("""error: {}
            Wallet creation failed""".format(er.__cause__))
        except sqlite3.ProgrammingError as er:
            print("""error: {}
            Wallet creation failed""".format(er.__cause__))
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Wallet creation stopped")
        except EOFError:
            print("EOFError: Unexpected end of file")
        except InsertException as er:
            print("""InsertException: Database insert failed
            {}: {}
            Wallet creation failed""".format(er.error, er.__cause__))
        finally:
            conn.rollback()
            conn.close()
            sys.exit(0)

    def insert(id_num, address, privkey, pubkey, sig, sigtext, balance):
        try:
            co = check_output(["find", os.getcwd(), "-name", "wallet.db"]).strip()
            conn = sqlite3.connect(co)
            del co
            c = conn.cursor()
            t = (id_num, bytearray(address, endocing='utf-8'), bytearray(privkey, endocing='utf-8'), bytearray(pubkey, endocing='utf-8'), bytearray(sig, endocing='utf-8'), bytearray(sigtext, endocing='utf-8'), bytearray(balance, endocing='utf-8'))
            c.execute('INSERT INTO accounts VALUES (?,?,?,?,?,?,?)', t)
            conn.commit()
            conn.close()
            sys.exit(0)
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
            conn.rollback()
            conn.close()
            sys.exit(0)

    def retrieve(variable, condition, location, location_value, is_like):#usage variable(desired data) condition(min max or none) location(WHERE variable) location (WHERE variable value) is_like(LIKE clause desired)
        co = check_output(["find", os.getcwd(), "-name", "wallet.db"]).strip()
        conn = sqlite3.connect(co)
        del co
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
        return a#a is in bytes if not block_id
        sys.exit(0)

    def update(variable, value, location, location_value):
        """variable is the variably you want to change. value is the desired value for the variable"""
        try:
            co = check_output(["find", os.getcwd(), "-name", "wallet.db"]).strip()
            conn = sqlite3.connect(co)
            del co
            c = conn.cursor()
            set_str = variable
            where_str = location
            if isinstance(value, str):
                if isinstance(location_value, str):
                    t = (bytearray(value, encoding='utf-8'), bytearray(location_value, encoding='utf-8'))
                elif isinstance(location_value, int):
                    t = (bytearray(value, encoding='utf-8'), bytearray(location_value))
                else:
                    raise TypeError('Invalid update argument')
            elif isinstance(value, int):
                if isinstance(location_value, str):
                    t = (bytearray(value, encoding='utf-8'), bytearray(location_value, encoding='utf-8'))
                elif isinstance(location_value, int):
                    t = (bytearray(value, encoding='utf-8'), bytearray(location_value))
                else:
                    raise TypeError('Invalid update argument')
            else:
                raise TypeError('Invalid update argument')
            c.execute('UPDATE accounts SET {} = ? WHERE {} = ?'.format(set_str, where_str), t)
            conn.commit()
            conn.close()
            sys.exit(0)
        except sqlite3.Error as er:
            raise Exceptions.RetrievalException('Error', er.__cause__)
        except sqlite3.DatabaseError as er:
            raise Exceptions.RetrievalException('DatabaseError', er.__cause__)
        except sqlite3.IntegrityError as er:
            raise Exceptions.RetrievalException('IntegrityError', er.__cause__)
        except sqlite3.ProgrammingError as er:
            raise Exceptions.RetrievalException('ProgrammingError', er.__cause__)
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Database update stopped")
        finally:
            conn.rollback()
            conn.close()
            sys.exit(0)

    def new_address():
        try:
            id_num = retrieve('id_num', 'max', None, None, False)
            if id_num == None:
                id_num = 0
            else:
                id_num = id_num + 1
            id_num = retrieve('id_num', 'max', None, None, False)
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
            id_num = id_num + 1
            insert(id_num, address, sk, vk, sig, sigtext, 0)
            sys.exit(0)
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Wallet creation stopped")
        except EOFError:
            print("EOFError: Unexpected end of file")
        except InsertException as er:
            print("""InsertException: Database insert failed
            {}: {}
            Wallet creation failed""".format(er.error, er.__cause__))
        finally:
            sys.exit(0)
