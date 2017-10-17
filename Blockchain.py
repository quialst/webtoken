import sqlite3
import sys
from subprocess import check_output
# update class needs exception handlers too

#9, 41, 65, 66, 69, 77, 80, 84, 91, 131

class Blockchain:
    def create_blockchain():
        try:
            co = check_output(["echo", "-n", "$BLOCKCHAIN_DB"]).decode('utf-8')#this does not echo the right variable
            conn = sqlite3.connect(co+'/blockchain.db')# needs file path
            del co
            c = conn.cursor()
            c.execute('''CREATE TABLE blocks
            (block_id INTEGER PRIMARY KEY, prevhash BLOB NOT NULL, data BLOB NOT NULL, block_hash BLOB NOT NULL, nonce BLOB NOT NULL)''')
            conn.commit()
            conn.close()
            update_chain()
            sys.exit(0)
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
        except InsertException as er:
            print("""InsertException: Database insert failed
            {}: {}
            Blockchain creation failed""".format(er.error, er.__cause__))
        finally:
            conn.rollback()
            conn.close()
            sys.exit(0)

    def update(variable, value, location, location_value):
        try:
            co = check_output(["find", "`pwd`", "-name", "blockchain.db"]).decode('utf-8')#this does not echo the right variable
            conn = sqlite3.connect(co)#needs to specify file path
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
            c.execute('UPDATE blocks SET {} = ? WHERE {} = ?'.format(set_str, where_str), t)
            conn.commit()
            conn.close()
            sys.exit(0)
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
            conn.rollback()
            conn.close()
            sys.exit(0)
    def retrieve(variable, condition, location, location_value, is_like):
        try:
            co = check_output(["find", "`pwd`", "-name", "blockchain.db"]).decode('utf-8')#this does not echo the right variable
            conn = sqlite3.connect(co)#file path need
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
            return a# a is in byte form unless block_id
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
            print("KeyboardInterrupt: Database insert stopped")
        finally:
            conn.rollback()
            conn.close()
            sys.exit(0)
    def insert(block_id, prevhash, data, block_hash, nonce):
        try:
            co = check_output(["find", "`pwd`", "-name", "blockchain.db"]).decode('utf-8')#this does not echo the right variable
            conn = sqlite3.connect(co)#needs to specify file path
            del co
            c = conn.cursor()
            t = (block_id, bytearray(prevhash, encoding='utf-8'), bytearray(data, encoding='utf-8'), bytearray(block_hash, encoding='utf-8'), bytes(nonce))
            c.execute('INSERT INTO blocks VALUES (?,?,?,?,?)', t)
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

    def update_chain():#add exception handlers
        co = check_output(["find", "`pwd`", "-name", "blockchain.db"]).decode('utf-8')#this does not echo the right variable
        conn = sqlite3.connect(co)
        del co
        c = conn.cursor()
        a = retrieve('block_id', 'max', None, None, False)# convert to int
        b = Node.block_retrieve('block_id', 'max', None, None, False)#convert to int
        while a[0] < b[0]:
            x = retrieve('block_id', 'max', None, None, False)
            data = Node.block_retrieve('*', None, 'block_id', x[0]+1, False)#convert x[0] to int
            insert(data[0], bytearray(data[1], encoding='utf-8'), bytearray(data[2], encoding='utf-8'), bytearray(data[3], encoding='utf-8'), bytearray(data[4]))
            a = retrieve('block_id', 'max', None, None, False)#NO CONVERSION
        else:
            print("Updated")
        print("Updated")
        conn.commit()
        conn.close()
        sys.exit(0)

    def genesis_block():
        genhash = bytearray('0000000000000000000000000000000000000000000000000000000000000000')
        gendata = #transaction object
        b = Block(0, genhash, gendata)
        sys.exit(0)

    def searchBlock():
        co = check_output(["find", "`pwd`", "-name", "blockchain.db"]).decode('utf-8')#this does not echo the right variable
        conn = sqlite3.connect(co)#file path needed
        del co
        c = conn.cursor()
        sys.exit(0)

    def replaceBlockchain():
        co = check_output(["find", "`pwd`", "-name", "blockchain.db"]).decode('utf-8')#this does not echo the right variable
        conn = sqlite3.connect(co)#file path needed
        del co
        c = conn.cursor()
        sys.exit(0)

    def searchTransaction():
