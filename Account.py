# -*- coding: latin1 -*-
import hashlib
import ecdsa
from ecdsa import SigningKey
from ecdsa import SECP256k1
import base58
import sqlite3
#13, 62, 84, 91, 117

class Account:
    def insert(id_num, address, privkey, pubkey, sig, sigtext, balance):
        try:
            conn = sqlite3.connect('wallet.db')#needs to specify file path
            c = conn.cursor()
            t = (bytes(id_num), bytes(address), bytes(privkey), bytes(pubkey), bytes(sig), bytes(sigtext), bytes(balance))
            c.execute('INSERT INTO accounts VALUES (?,?,?,?,?,?,?)', t)
            conn.commit()
            conn.close()
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

    def retrieve(variable, condition, location, location_value, is_like):#usage variable(desired data) condition(min max or none) location(WHERE variable) location (WHERE variable value) is_like(LIKE clause desired)
        conn = sqlite3.connect('wallet.db')
        c = conn.cursor()
        select_str = variable
        where_str = ''
        if location != None or location_value != None:
            where_str = '{}'.format(location)
            t = (location_value, )
        if condition == 'min' or condition == 'max':
            select_str = '{}({})'.format(condition.upper(), select_str)
        else:
            select_str = variable
        if location == None or location_value == None:
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
        return a
    def update(variable, value, location, location_value):
        """variable is the variably you want to change. value is the desired value for the variable"""
        try:
            conn = sqlite3.connect('wallet.db')#needs to specify file path
            c = conn.cursor()
            set_str = variable
            where_str = location
            t = (bytes(value), bytes(location_value))
            c.execute('UPDATE accounts SET {} = ? WHERE {} = ?'.format(set_str, where_str), t)
            conn.commit()
            conn.close()
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

    def exists():#NEEDS WORK
        return False

    def new_address():
        try:
            id_num = 0
            if exists():#if id_num exists
                id_num = retrieve('id_num', 'max', None, None, False)#needs to be turned to int type
            sk = SigningKey.generate(curve=SECP256k1)# private ecdsa key
            vk = sk.get_verifying_key()# verifying key j4kiks
            sigtext = b"signature"
            sig = sk.sign(signature)
            s1 = hashlib.sha256(sk.to_string()).digest()# sha hashing of public key in binary
            temp = hashlib.new('ripemd160')# make ripemd150 object
            temp.update(s1)# update the object
            s2 = temp.digest()# binary digest of ak
            s3 = (b"0x00"+s2)# add the version byte to bk
            s4 = hashlib.sha256(hashlib.sha256(s3).digest()).digest()# doulbe sha hash of ck
            s5 = s4[0:4]# take first 4 bytes
            s6 = (ck+s5)# add 4 bytes to end of ck
            address = base58.b58encode(s6)# do a base58 encode
            insert(id_num, address, sk, vk, sig, sigtext, 0)
            id_num = id_num + 1
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Wallet creation stopped")
        except EOFError:
            print("EOFError: Unexpected end of file")
        except InsertException as er:
            print("""InsertException: Database insert failed
            {}: {}
            Wallet creation failed""".format(er.error, er.__cause__))
    def create_wallet():
        try:
            conn = sqlite3.connect('wallet.db')#needs to specify file path
            c = conn.cursor()
            c.execute('''CREATE TABLE accounts
            (id_num INTEGER PRIMARY KEY ASC, address TEXT NOT NULL, privkey TEXT NOT NULL,
            pubkey TEXT NOT NULL, sig TEXT NOT NULL, sigtext, TEXT NOT NULL, balance REAL)''')
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
