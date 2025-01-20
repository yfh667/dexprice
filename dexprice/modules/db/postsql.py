import psycopg2
from psycopg2 import sql
from abc import ABC, abstractmethod
from dexprice.modules.utilis.define import Config, TokenInfo, TokenPriceHistory, Tokendb
import dexprice.modules.utilis.define as define
import dexprice.modules.db.insert_db as insert_db


import sqlite3
import os
from abc import ABC, abstractmethod
from dexprice.modules.utilis.define import Config,TokenInfo,TokenPriceHistory,Tokendb
import  dexprice.modules.utilis.define as define
# 插入数据的函数

class PostgreSQLDatabase(insert_db.DatabaseInterface):
    def __init__(self, db_config, chainid):
        self.conn = None
        self.cursor = None
        self.chainid = chainid
        self.db_config = db_config  # A dictionary containing database connection parameters

    def connect(self):
        try:
            # Connect to PostgreSQL database
            self.conn = psycopg2.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            print("Database connection established and cursor initialized.")

            # Initialize main table
            self.initialize_table()

            # Initialize price history table
            self.create_price_history_table()
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL database: {e}")

    def initialize_table(self):
        # Initialize main table 'token_pairs'
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS token_pairs (
            id SERIAL PRIMARY KEY,
            chainid TEXT NOT NULL,
            name TEXT NOT NULL,
            ca TEXT NOT NULL UNIQUE,
            pairaddress TEXT NOT NULL,
            creattime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        self.cursor.execute(create_table_query)
        self.conn.commit()
        print("Table 'token_pairs' initialized.")

    def create_price_history_table(self):
        # Initialize price history table
        table_name = f"{self.chainid}_price_history"
        create_table_query = sql.SQL('''
        CREATE TABLE IF NOT EXISTS {table} (
            id SERIAL PRIMARY KEY,
            tokenid INTEGER,
            openprice REAL,
            highprice REAL,
            lowprice REAL,
            closeprice REAL,
            time TEXT,
            volume REAL,
            UNIQUE(tokenid, time)
        );
        ''').format(table=sql.Identifier(table_name))
        self.cursor.execute(create_table_query)
        self.conn.commit()
        print(f"Table '{table_name}' initialized.")

    def insert_data(self, table_name, name, ca, pairaddress, creattime):
        insert_query = '''
        INSERT INTO token_pairs (chainid, name, ca, pairaddress, creattime)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (ca) DO NOTHING;
        '''
        try:
            self.cursor.execute(insert_query, (self.chainid, name, ca, pairaddress, creattime))
            self.conn.commit()
            print(f"Data inserted successfully for ca: {ca}")
        except psycopg2.IntegrityError:
            self.conn.rollback()
            print(f"Skipping insertion. The ca value '{ca}' already exists.")
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error inserting data for ca '{ca}': {e}")

    def collect_ovhl_data(self, ovhl_data_list: list[define.OvhlFromDex]) -> list[define.TokenPriceHistory]:

        token_price_history_list = []
        for OvhlFromDexData in ovhl_data_list:
            pairaddress = OvhlFromDexData.pairaddress
            tokenid = self.FindParetokenid(pairaddress)
            if tokenid:
                if OvhlFromDexData:
                    ovhl = define.TokenPriceHistory(
                        tokenid,
                        OvhlFromDexData.open,
                        OvhlFromDexData.high,
                        OvhlFromDexData.low,
                        OvhlFromDexData.close,
                        OvhlFromDexData.time,
                        OvhlFromDexData.volume
                    )
                    token_price_history_list.append(ovhl)
        return token_price_history_list

    def insert_multiple_price_history(self, token_price_history_list):
        table_name = f"{self.chainid}_price_history"
        insert_query = sql.SQL('''
            INSERT INTO {table} (tokenid, openprice, highprice, lowprice, closeprice, time, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (tokenid, time) DO UPDATE SET
                openprice = EXCLUDED.openprice,
                highprice = EXCLUDED.highprice,
                lowprice = EXCLUDED.lowprice,
                closeprice = EXCLUDED.closeprice,
                volume = EXCLUDED.volume;
        ''').format(table=sql.Identifier(table_name))
        data_to_insert = [
            (
                history.tokenid,
                history.open,
                history.high,
                history.low,
                history.close,
                history.time,
                history.volume
            )
            for history in token_price_history_list
        ]

        try:
            self.cursor.executemany(insert_query, data_to_insert)
            self.conn.commit()
            print(f"Batch inserted or updated {len(data_to_insert)} records into {table_name}.")
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error inserting multiple price histories: {e}")

    def close(self):
        if self.conn:
            # Optionally, remove duplicates (if necessary)
            # PostgreSQL can enforce constraints to avoid duplicates

            # Close cursor and connection
            if self.cursor:
                self.cursor.close()
            self.conn.close()
            print("Database connection closed.")

    def insert_OvhlFromDex(self, OvhlFromDexData: define.OvhlFromDex):
        pairaddress = OvhlFromDexData.pairaddress
        tokenid = self.FindParetokenid(pairaddress)
        if tokenid:
            if OvhlFromDexData:
                ovhl = define.TokenPriceHistory(
                    tokenid,
                    OvhlFromDexData.open,
                    OvhlFromDexData.high,
                    OvhlFromDexData.low,
                    OvhlFromDexData.close,
                    OvhlFromDexData.time,
                    OvhlFromDexData.volume
                )
                self.insertpricehistory(ovhl)

    def insertpricehistory(self, tokenpricehistory: define.TokenPriceHistory):
        table_name = f"{self.chainid}_price_history"
        insert_query = sql.SQL('''
        INSERT INTO {table} (tokenid, openprice, highprice, lowprice, closeprice, time, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (tokenid, time) DO NOTHING;
        ''').format(table=sql.Identifier(table_name))
        try:
            self.cursor.execute(insert_query, (
                tokenpricehistory.tokenid,
                tokenpricehistory.open,
                tokenpricehistory.high,
                tokenpricehistory.low,
                tokenpricehistory.close,
                tokenpricehistory.time,
                tokenpricehistory.volume
            ))
            self.conn.commit()
            print(f"Data inserted into {table_name} successfully.")
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error inserting price history: {e}")

    def insertMultipricehistory(self, tokenpricehistorys: list[define.TokenPriceHistory]):
        for tokenpricehistory in tokenpricehistorys:
            self.insertpricehistory(tokenpricehistory)

    def insertMultipricedexscreen(self, TokenInfos: list[define.TokenInfo]):
        for token in TokenInfos:
            self.insertpricedexscreen(token)

    def insertpricedexscreen(self, TokenInfo: define.TokenInfo):
        table_name = f"{self.chainid}_pricedexscreen"
        # Create table if it doesn't exist
        create_table_query = sql.SQL('''
            CREATE TABLE IF NOT EXISTS {table} (
                tokenid INTEGER,
                price REAL,
                time TEXT
            );
        ''').format(table=sql.Identifier(table_name))
        self.cursor.execute(create_table_query)
        self.conn.commit()

        tokenid = self.FindCAtokenid(TokenInfo)

        insert_query = sql.SQL('''
            INSERT INTO {table} (tokenid, price, time)
            VALUES (%s, %s, %s);
        ''').format(table=sql.Identifier(table_name))

        try:
            self.cursor.execute(insert_query, (
                tokenid,
                TokenInfo.price_usd,
                TokenInfo.timestamp
            ))
            self.conn.commit()
            print(f"Data inserted into {table_name} successfully.")
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error inserting pricedexscreen data: {e}")

    def getpricedexscreen(self, tokenid: int):
        table_name = f"{self.chainid}_pricedexscreen"
        select_query = sql.SQL('''
            SELECT price, time
            FROM {table}
            WHERE tokenid = %s;
        ''').format(table=sql.Identifier(table_name))

        try:
            self.cursor.execute(select_query, (tokenid,))
            rows = self.cursor.fetchall()
            price_records = [(tokenid, row[0], row[1]) for row in rows]
            return price_records
        except psycopg2.Error as e:
            print(f"Error retrieving pricedexscreen data: {e}")
            return []

    def FindCAtokenid(self, TokenInfo: define.TokenInfo):
        table_name = 'token_pairs'
        CA = TokenInfo.address

        query = '''
        SELECT id FROM token_pairs WHERE ca = %s;
        '''
        try:
            self.cursor.execute(query, (CA,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except psycopg2.Error as e:
            print(f"Error finding tokenid for CA '{CA}': {e}")
            return None

    def FindParetokenid(self, pairaddress: str):
        table_name = 'token_pairs'

        query = '''
        SELECT id FROM token_pairs WHERE pairaddress = %s;
        '''
        try:
            self.cursor.execute(query, (pairaddress,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except psycopg2.Error as e:
            print(f"Error finding tokenid for pairaddress '{pairaddress}': {e}")
            return None

    def delete_table(self):
        table_name = f"{self.chainid}_pricedexscreen"
        delete_query = sql.SQL('DELETE FROM {table};').format(table=sql.Identifier(table_name))

        try:
            self.cursor.execute(delete_query)
            self.conn.commit()
            print(f"Table '{table_name}' cleared successfully.")
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error clearing table '{table_name}': {e}")

    def delete_table2(self):
        table_name = 'token_pairs'
        delete_query = sql.SQL('DELETE FROM {table};').format(table=sql.Identifier(table_name))

        try:
            self.cursor.execute(delete_query)
            self.conn.commit()
            print(f"Table '{table_name}' cleared successfully.")
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error clearing table '{table_name}': {e}")

    def delete_token(self, pairaddress: str):
        # Step 1: Find tokenid
        query = '''
        SELECT id FROM token_pairs WHERE pairaddress = %s;
        '''
        try:
            self.cursor.execute(query, (pairaddress,))
            result = self.cursor.fetchone()
            if result:
                tokenid = result[0]

                # Step 2: Delete related records in price history table
                table_name_price_history = f"{self.chainid}_price_history"
                delete_history_query = sql.SQL('''
                    DELETE FROM {table} WHERE tokenid = %s;
                ''').format(table=sql.Identifier(table_name_price_history))
                self.cursor.execute(delete_history_query, (tokenid,))
                print(f"Deleted price history records for tokenid {tokenid}.")

                # Step 3: Delete from token_pairs table
                delete_token_query = '''
                DELETE FROM token_pairs WHERE id = %s;
                '''
                self.cursor.execute(delete_token_query, (tokenid,))
                self.conn.commit()
                print(f"Deleted token_pairs record for pairaddress {pairaddress} with tokenid {tokenid}.")
            else:
                print(f"No record found for pairaddress {pairaddress}.")
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error deleting token with pairaddress '{pairaddress}': {e}")

    def readdbtoken(self):
        query = '''
        SELECT id, chainid, name, ca, pairaddress, creattime
        FROM token_pairs;
        '''
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            tokens = []
            for row in rows:
                token_data = Tokendb(
                    tokenid=row[0],
                    chainid=row[1],
                    name=row[2],
                    address=row[3],
                    pair_address=row[4],
                    creattime=row[5]
                )
                tokens.append(token_data)

            return tokens
        except psycopg2.Error as e:
            print(f"Error reading tokens: {e}")
            return []

    def read_token_withid(self, tokenid: float) -> Tokendb:
        query = '''
            SELECT id, chainid, name, ca, pairaddress, creattime
            FROM token_pairs
            WHERE id = %s;
        '''
        try:
            self.cursor.execute(query, (tokenid,))
            row = self.cursor.fetchone()

            if row:
                token_data = Tokendb(
                    tokenid=row[0],
                    chainid=row[1],
                    name=row[2],
                    address=row[3],
                    pair_address=row[4],
                    creattime=row[5]
                )
                return token_data
            else:
                return None
        except psycopg2.Error as e:
            print(f"Error reading token with id '{tokenid}': {e}")
            return None

    def readprice(self, tokenid: float) -> list[TokenPriceHistory]:
        table_name = f"{self.chainid}_price_history"

        select_query = sql.SQL('''
        SELECT tokenid, openprice, highprice, lowprice, closeprice, time, volume
        FROM {table}
        WHERE tokenid = %s;
        ''').format(table=sql.Identifier(table_name))

        try:
            self.cursor.execute(select_query, (tokenid,))
            rows = self.cursor.fetchall()

            token_price_history_list = [
                TokenPriceHistory(
                    tokenid=row[0],
                    open=row[1],
                    high=row[2],
                    low=row[3],
                    close=row[4],
                    time=row[5],
                    volume=row[6]
                ) for row in rows
            ]

            print(f"Data retrieved from {table_name} successfully.")
            return token_price_history_list
        except psycopg2.Error as e:
            print(f"Error reading price history: {e}")
            return []


def retrieve_token_price_history(db, Tokendb: Tokendb):
    tokenid = Tokendb.tokenid
    tokenprice = db.readprice(tokenid)
    return tokenprice


def read_token_andid(db, tokenids):
    tokendb = []
    for tokenid in tokenids:
        print(tokenid)
        tokendb.append(db.read_token_withid(tokenid))
    return tokendb
