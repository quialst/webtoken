import sqlite3
# update class needs exception handlers too

class Blockchain:
    def create_blockchain():
        try:
            conn = sqlite3.connect('blockchain.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE blocks
            (block_id INTEGER PRIMARY KEY, prevhash TEXT, data TEXT, hash TEXT, nonce INTEGER)''')
        except:

        finally:

    def update(variable, value, location, location_value):
        try:
            conn = sqlite3.connect('blockchain.db')#needs to specify file path
            c = conn.cursor()
            set_str = variable
            where_str = location
            t = (value, location_value)
            c.execute('UPDATE accounts SET {} = ? WHERE {} = ?'.format(set_str, where_str), t)
            conn.commit()
            conn.close()
        except sqlite3.Error as er:
            raise RetrievalException('Error', er.__cause__)
        except sqlite3.DatabaseError as er:
            raise RetrievalException('DatabaseError', er.__cause__)
        except sqlite3.IntegrityError as er:
            raise RetrievalException('IntegrityError', er.__cause__)
        except sqlite3.ProgrammingError as er:
            raise RetrievalException('ProgrammingError', er.__cause__)
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Database update stopped")
        finally:
            conn.rollback()
            conn.close()
    def update_chain():
        conn = sqlite3.connect('blockchain.db')
        c = conn.cursor()
        a = retrieve('block_id', 'max', None, None, False)
        b = Node.block_retrieve('block_id', 'max', None, None, False)
        while a[0] < b[0]:
            x = retrieve('block_id', 'max', None, None, False)
            data = Node.block_retrieve('*', None, 'block_id', x[0]+1, False)
            insert(data[0], data[1], data[2], data[3], data[4])
            a = retrieve('block_id', 'max', None, None, False)
        else:
            print("Updated")
    def genesis_block():
        genhash = b'0000000000000000000000000000000000000000000000000000000000000000'
        gendata = b''
        b = Block(0, genhash, gendata)
    def searchBlock():
        conn = sqlite3.connect('blockchain.db')
        c = conn.cursor()

    def replaceBlockchain():
        conn = sqlite3.connect('blockchain.db')
        c = conn.cursor()

    def searchTransaction():

    def retrieve():

    def insert():
