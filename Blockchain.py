import sqlite3
# update class needs exception handlers too

#9, 41, 65, 66, 68, 77, 80, 84, 91, 131

class Blockchain:
    def create_blockchain():
        try:
            conn = sqlite3.connect('blockchain.db')# needs file path
            c = conn.cursor()
            c.execute('''CREATE TABLE blocks
            (block_id INTEGER PRIMARY KEY, prevhash TEXT, data TEXT, block_hash TEXT, nonce INTEGER)''')
            conn.commit()
            conn.close()
            update_chain()
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
    def update(variable, value, location, location_value):
        try:
            conn = sqlite3.connect('blockchain.db')#needs to specify file path
            c = conn.cursor()
            set_str = variable
            where_str = location
            t = (value, location_value)
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
            conn.rollback()
            conn.close()
    def update_chain():
        conn = sqlite3.connect('blockchain.db')
        c = conn.cursor()
        a = retrieve('block_id', 'max', None, None, False)# convert to int
        b = Node.block_retrieve('block_id', 'max', None, None, False)#convert to int
        while a[0] < b[0]:
            x = retrieve('block_id', 'max', None, None, False)#convert to int
            data = Node.block_retrieve('*', None, 'block_id', x[0]+1, False)
            insert(bytes(data[0]), bytes(data[1]), bytes(data[2]), bytes(data[3]), bytes(data[4]))
            a = retrieve('block_id', 'max', None, None, False)#NO CONVERSION
        else:
            print("Updated")
        print("Updated")
    def genesis_block():
        genhash = bytes('0000000000000000000000000000000000000000000000000000000000000000')
        gendata = #transaction object
        b = Block(bytes(0), genhash, gendata)
    def searchBlock():
        conn = sqlite3.connect('blockchain.db')#file path needed
        c = conn.cursor()

    def replaceBlockchain():
        conn = sqlite3.connect('blockchain.db')#file path needed
        c = conn.cursor()

    def searchTransaction():

    def retrieve(variable, condition, location, location_value, is_like):
        try:
            conn = sqlite3.connect('blockchain.db')#file path need
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
    def insert(block_id, prevhash, data, block_hash, nonce):
        try:
            conn = sqlite3.connect('blockchain.db')#needs to specify file path
            c = conn.cursor()
            t = (bytes(block_id), bytes(prevhash), bytes(data), bytes(block_hash), bytes(nonce))
            c.execute('INSERT INTO blocks VALUES (?,?,?,?,?)', t)
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
