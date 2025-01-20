
import sqlite3
import os
from abc import ABC, abstractmethod
from dexprice.modules.utilis.define import Config,TokenInfo,TokenPriceHistory,Tokendb
import  dexprice.modules.utilis.define as define
# 插入数据的函数


class CexDatabaseInterface(ABC):
    # @abstractmethod
    # def insertpricehistory(self,tokenpricehistory):
    #     pass
    @abstractmethod
    def delete_table(self):
        pass





    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def insert_data(self, table_name,name,  chaind ):
        pass




    @abstractmethod
    def close(self):
        pass
    @abstractmethod
    def initialize_table(self):
        pass
    @abstractmethod
    def readdbtoken(self):
        pass

    # @abstractmethod
    # def readprice(self, tokenid):
    #     pass



class   CexSQLiteDatabase(CexDatabaseInterface):
        def __init__(self, db_folder, db_name):
            self.db_path = os.path.join(db_folder, db_name)
            self.conn = None
            self.db_folder = db_folder
            self.db_name = db_name
        # def insert_data(self, table_name, chain_id, name):
        #     # 只插入需要的字段
        #     insert_query = f"""
        #     INSERT INTO {table_name} (chainid, name) VALUES (?, ?)
        #     """
        #     cursor = self.conn.cursor()
        #     try:
        #         cursor.execute(insert_query, (chain_id, name))
        #         self.conn.commit()
        #         print("Data inserted successfully")
        #     except sqlite3.OperationalError as e:
        #         print(f"SQLite Error: {e}")
        #         raise

        def insert_data(self, table_name, chain_id, name):
            # 使用 INSERT OR IGNORE
            insert_query = f"""
            INSERT OR IGNORE INTO {table_name} (chainid, name)
            VALUES (?, ?)
            """
            cursor = self.conn.cursor()
            try:
                cursor.execute(insert_query, (chain_id, name))
                self.conn.commit()
                print(f"Inserted: {name}")
            except sqlite3.IntegrityError as e:
                print(f"IntegrityError: {e}")
        def insert_Multidata(self,  tokendb:list[define.CexTokenInfo ]):
            table_name = 'token_pairs'
            if len(tokendb) != 0:
                for token in tokendb:
                    self.insert_data( table_name, token.chainid ,token.name   )

        def collect_ovhl_data(self, ovhl_data_list:list[define.OvhlFromCex]):
            token_price_history_list = []
            for OvhlFromCexData in ovhl_data_list:
                name = OvhlFromCexData.name
                tokenid = self.FindParetokenid(name)
                if tokenid:
                    if(OvhlFromCexData):
                        ovhl = define.TokenPriceHistory(
                            tokenid,
                            OvhlFromCexData.open,
                            OvhlFromCexData.high,
                            OvhlFromCexData.low,
                            OvhlFromCexData.close,
                            OvhlFromCexData.time,
                            OvhlFromCexData.volume
                        )
                        token_price_history_list.append(ovhl)
            return token_price_history_list
        def insert_multiple_price_history(self, token_price_history_list:list[TokenPriceHistory]):
            table_name = "price_history"
            insert_query = f'''
                INSERT INTO {table_name} (tokenid, openprice, highprice, lowprice, closeprice, time, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(tokenid, time) DO UPDATE SET
                    openprice = excluded.openprice,
                    highprice = excluded.highprice,
                    lowprice = excluded.lowprice,
                    closeprice = excluded.closeprice,
                    volume = excluded.volume;
            '''
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

            cursor = self.conn.cursor()
            cursor.executemany(insert_query, data_to_insert)
            self.conn.commit()
            print(f"批量插入或更新了 {len(data_to_insert)} 条记录到 {table_name}。")
        #
        #


        def close(self):
            if self.conn:
                # 获取数据库中的所有表名
                cursor = self.conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()

                # 遍历每张表，检查重复记录并去重
                for table in tables:
                    table_name = table[0]

                    # 获取每张表的字段名
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = cursor.fetchall()
                    column_names = [col[1] for col in columns]  # 获取所有字段的名称

                    if not column_names:
                        print(f"No columns found for table {table_name}. Skipping.")
                        continue

                    # 构造 GROUP BY 子句和 DELETE 子句
                    column_names_str = ", ".join(column_names)

                    # 查询表中的重复记录，获取所有字段完全重复的数据
                    find_duplicates_query = f'''
                    SELECT {column_names_str}
                    FROM {table_name}
                    GROUP BY {column_names_str}
                    HAVING COUNT(*) > 1;
                    '''
                    cursor.execute(find_duplicates_query)
                    duplicates = cursor.fetchall()

                    if duplicates:
                        print(f"Found duplicates in {table_name}. Removing duplicates...")

                        # 删除重复记录，保留其中一条
                        delete_duplicates_query = f'''
                        DELETE FROM {table_name}
                        WHERE rowid NOT IN (
                            SELECT MIN(rowid)
                            FROM {table_name}
                            GROUP BY {column_names_str}
                        );
                        '''
                        cursor.execute(delete_duplicates_query)
                        self.conn.commit()
                        print(f"Removed duplicates from {table_name}.")

                # 关闭数据库连接
                if self.conn:
                    self.conn.close()
                    print("Database connection closed.")
        # def insert_OvhlFromDex(self, OvhlFromDexData: define.OvhlFromDex):
        #     pairaddress = OvhlFromDexData.pairaddress
        #     tokenid = self.FindParetokenid(pairaddress)
        #     if tokenid:
        #         # 使用 OvhlFromDexData 的属性而不是下标访问
        #         if(OvhlFromDexData):
        #             ovhl = define.TokenPriceHistory(
        #                 tokenid,
        #                 OvhlFromDexData.open,
        #                 OvhlFromDexData.high,
        #                 OvhlFromDexData.low,
        #                 OvhlFromDexData.close,
        #                 OvhlFromDexData.time,
        #                 OvhlFromDexData.volume
        #             )
        #             self.insertpricehistory(ovhl)
        #
        # def insertpricehistory(self, tokenpricehistory: define.TokenPriceHistory):
        #     table_name = f"{self.chainid}_price_history"
        #
        #     # 检查是否已存在相同的记录
        #     check_query = f'''
        #     SELECT COUNT(*) FROM {table_name}
        #     WHERE tokenid = ? AND time = ?;
        #     '''
        #     cursor = self.conn.cursor()
        #     cursor.execute(check_query, (tokenpricehistory.tokenid, tokenpricehistory.time))
        #     count = cursor.fetchone()[0]
        #
        #     # 如果记录不存在，则插入
        #     if count == 0:
        #         insert_query = f'''
        #         INSERT INTO {table_name} (tokenid, openprice, highprice, lowprice, closeprice, time, volume)
        #         VALUES (?, ?, ?, ?, ?, ?, ?);
        #         '''
        #         cursor.execute(insert_query, (tokenpricehistory.tokenid, tokenpricehistory.open, tokenpricehistory.high,
        #                                       tokenpricehistory.low, tokenpricehistory.close, tokenpricehistory.time, tokenpricehistory.volume))
        #         self.conn.commit()
        #         print(f"Data inserted into {table_name} successfully.")
        #     else:
        #         print(f"Duplicate entry found for tokenid {tokenpricehistory.tokenid} at time {tokenpricehistory.time}. Skipping insertion.")
        # def insertMultipricehistory(self, tokenpricehistorys:list[define.TokenPriceHistory]):
        #     table_name = f"{ self.chainid }_price_history"
        #     for tokenpricehistory in tokenpricehistorys:
        #         self.insertpricehistory(tokenpricehistory)
        #
        #
        # # print(f"Data inserted into {table_name} successfully.")
        # def insertMultipricedexscreen(self, TokenInfos:list[define.TokenInfo]):
        #     for token in TokenInfos:
        #         self.insertpricedexscreen(token)

        # get the price from the dexscreen
        # def insertpricedexscreen(self, TokenInfo:define.TokenInfo):
        #     table_name = f"{self.chainid}_pricedexscreen"
        #
        #     # 检查表是否存在，不存在则创建
        #     create_table_query = f'''
        #         CREATE TABLE IF NOT EXISTS {table_name} (
        #             tokenid INTEGER,  -- tokenid 可以重复
        #             price REAL,
        #             time TEXT
        #         );
        #     '''
        #
        #     # 确保表已创建
        #     cursor = self.conn.cursor()
        #     cursor.execute(create_table_query)
        #
        #
        #     tokenid =  self.FindCAtokenid( TokenInfo)
        #
        #
        #     # 插入数据的 SQL 语句
        #     insert_query = f'''
        #         INSERT INTO {table_name} (tokenid, price, time)
        #         VALUES (?, ?, ?);
        #     '''
        #
        #     # 执行插入操作
        #     cursor.execute(insert_query, (
        #         tokenid,
        #         TokenInfo.price_usd,
        #         TokenInfo.timestamp
        #     ))
        #
        #     # 提交事务并关闭游标
        #     self.conn.commit()
        #     print(f"Data inserted into {table_name} successfully.")
        # def getpricedexscreen(self,  tokenid: int):
        #     """
        # 根据给定的 tokenid 从 pricedexscreen 表中检索所有价格记录。
        #
        # :param tokenid: 要查询的 tokenid
        # :return: 包含 (price, time) 元组的列表，每个元组对应一条价格记录
        # """
        #     table_name = f"{self.chainid}_pricedexscreen"
        #     select_query = f'''
        #         SELECT price, time
        #         FROM {table_name}
        #         WHERE tokenid = ?;
        #     '''
        #
        #     cursor = self.conn.cursor()
        #     cursor.execute(select_query, (tokenid,))
        #     rows = cursor.fetchall()  # 获取所有符合条件的记录
        #
        #     # 将查询结果转换成 (price, time) 的列表并返回
        #     price_records = [(tokenid,row[0], row[1]) for row in rows]
        #
        #     return price_records
        #
        # def FindCAtokenid(self, TokenInfo:define.TokenInfo):
        #     """
        #     根据 TokenInfo 的 address (CA) 查找对应的 id。
        #
        #     :param token_info: TokenInfo 对象，包含 address 字段
        #     :return: 返回对应的 id，若未找到则返回 None
        #     """
        #     table_name = 'token_pairs'
        #     CA = TokenInfo.address
        #     if self.cursor is None:
        #         self.cursor = self.conn.cursor()
        #
        #     # 查询 token_pairs 表中与 CA 匹配的 id
        #     query = f"SELECT id FROM {table_name} WHERE ca = ?"
        #     self.cursor.execute(query, (CA,))
        #     result = self.cursor.fetchone()
        #
        #     if result:
        #         return result[0]  # 返回找到的 id
        #     else:
        #         return None  # 如果找不到则返回 None
        def FindParetokenid(self, name:str):
            """
            根据 TokenInfo 的 address (CA) 查找对应的 id。

            :param token_info: TokenInfo 对象，包含 address 字段
            :return: 返回对应的 id，若未找到则返回 None
            """
            table_name = 'token_pairs'
            #  pa = pairaddress
            if self.cursor is None:
                self.cursor = self.conn.cursor()

            # 查询 token_pairs 表中与 CA 匹配的 id
            query = f"SELECT id FROM {table_name} WHERE name = ?"
            self.cursor.execute(query, (name,))
            result = self.cursor.fetchone()

            if result:
                return result[0]  # 返回找到的 id
            else:
                return None  # 如果找不到则返回 None


        def initialize_table(self):
            # 连接到SQLite数据库
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 初始化主表的SQL语句
            table_name = 'token_pairs'
            create_table_query = f'''
             CREATE TABLE IF NOT EXISTS token_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chainid TEXT,
                name TEXT NOT NULL UNIQUE,  -- name 必须唯一且非空
                ca TEXT,                    -- ca 允许为空
                pairaddress TEXT,           -- pairaddress 允许为空
                creattime TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 默认当前时间
            );
            '''

            # 执行创建表的SQL语句
            cursor.execute(create_table_query)

            # 提交更改并关闭连接
            conn.commit()
            conn.close()

            print(f"Table '{table_name}' initialized in database '{self.db_path}'.")

        def delete_table(self):
            """
            删除指定的表。

            :param table_name: 要删除的表的名称
            """
            # 连接到SQLite数据库
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            table_name = f"{self.chainid}_pricedexscreen"

            try:
                # 构建清空表数据的 SQL 语句
                clear_table_query = f"DELETE FROM {table_name};"

                # 执行清空表数据的 SQL 语句
                cursor.execute(clear_table_query)

                # 提交更改
                conn.commit()
                print(f"Table '{table_name}' cleared successfully in database '{self.db_path}'.")

            except sqlite3.Error as e:
                print(f"Error clearing table '{table_name}': {e}")

            finally:
                # 关闭连接
                conn.close()
        def delete_table2(self):
            """
            删除指定的表。

            :param table_name: 要删除的表的名称
            """
            # 连接到SQLite数据库
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            table_name = 'token_pairs'

            try:
                # 构建清空表数据的 SQL 语句
                clear_table_query = f"DELETE FROM {table_name};"

                # 执行清空表数据的 SQL 语句
                cursor.execute(clear_table_query)

                # 提交更改
                conn.commit()
                print(f"Table '{table_name}' cleared successfully in database '{self.db_path}'.")

            except sqlite3.Error as e:
                print(f"Error clearing table '{table_name}': {e}")

            finally:
                # 关闭连接
                conn.close()
        # def delete_token(self, paireaddress: str):
        #     """
        #     根据 paireaddress 删除 token_pairs 表中的记录，并删除 tokenpricehistory 表中的相关历史记录。
        #     """
        #     # 确保数据库连接和游标已初始化
        #     cursor = self.conn.cursor()
        #
        #     # Step 1: 查找 token_pairs 表中匹配的 tokenid
        #     query = "SELECT id FROM token_pairs WHERE pairaddress = ?"
        #     cursor.execute(query, (paireaddress,))
        #     result = cursor.fetchone()
        #
        #     if result:
        #         tokenid = result[0]
        #
        #         # Step 2: 删除 tokenpricehistory 表中的相关记录
        #         table_name_price_history = f"{self.chainid}_price_history"
        #         delete_history_query = f"DELETE FROM {table_name_price_history} WHERE tokenid = ?"
        #         cursor.execute(delete_history_query, (tokenid,))
        #         print(f"Deleted tokenpricehistory records for tokenid {tokenid}.")
        #
        #         # Step 3: 删除 token_pairs 表中的记录
        #         delete_token_query = "DELETE FROM token_pairs WHERE id = ?"
        #         cursor.execute(delete_token_query, (tokenid,))
        #         print(f"Deleted token_pairs record for paireaddress {paireaddress} with tokenid {tokenid}.")
        #
        #         # 提交更改
        #         self.conn.commit()
        #     else:
        #         print(f"No record found for paireaddress {paireaddress}.")
        #
        #     # 关闭游标
        #     cursor.close()

        def connect(self):
            # 创建指定的文件夹（如果不存在）
            if not os.path.exists(self.db_folder):
                os.makedirs(self.db_folder)

            # 连接到SQLite数据库
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()  # 初始化游标
            print("Database connection established and cursor initialized.")

            # 检查并创建主表
            self.initialize_table()  # 调用表初始化函数

            # 检查并创建其他必要的表
            table_name = f"price_history"
            create_table_query = f'''
            
            CREATE TABLE IF NOT EXISTS {table_name} (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
            tokenid INTEGER,
            openprice REAL,
            highprice REAL,
            lowprice REAL,
            closeprice REAL,
            time TEXT,
            volume REAL,
            UNIQUE(tokenid, time)
            );
            '''

            self.cursor.execute(create_table_query)
            self.conn.commit()
            print(f"Table {table_name} created or already exists.")
        def readdbtoken(self):
            # 打开数据库连接
            cursor = self.conn.cursor()

            # 查询 token_pairs 表中的 id, chainid, pairaddress, 和 creattime 字段
            query = '''
            SELECT id, chainid, name,ca,pairaddress, creattime
            FROM token_pairs;
            '''

            # 执行查询
            cursor.execute(query)

            # 获取所有查询结果
            rows = cursor.fetchall()

            # 将结果组织成字典形式，并返回数组
            tokens = []
            for row in rows:
                # 使用字典形式存储每条记录
                token_data = Tokendb(
                    tokenid=row[0],
                    chainid=row[1],
                    name=row[2],
                    address=row[3],

                    pair_address=row[4],
                    creattime=row[5]
                )
                tokens.append(token_data)

            # 关闭游标
            cursor.close()

            # 返回 token 数据数组
            return tokens

        def read_token_withid(self, tokenid: float) -> Tokendb:
            # 打开数据库连接
            cursor = self.conn.cursor()

            # 查询 token_pairs 表中特定 tokenid 的记录
            query = '''
                SELECT id,chainid,name, ca, pairaddress, creattime
                FROM token_pairs
                WHERE id = ?;
                '''

            # 执行查询并传递 tokenid 作为参数
            cursor.execute(query, (tokenid,))

            # 获取查询结果
            row = cursor.fetchone()

            # 检查是否获取到了结果
            if row:
                # 将结果组织成 Tokendb 类的实例
                token_data = Tokendb(
                    tokenid=row[0],  # 对应数据库中的 id 字段

                    chainid=row[1],
                    name = row[2],
                    address=row[3],
                    pair_address=row[4],
                    creattime=row[5]
                )
                # 关闭游标
                cursor.close()
                # 返回 token 数据
                return token_data
            else:
                # 如果没有找到匹配的记录，返回 None
                cursor.close()
                return None
        # def readprice(self, tokenid: float) -> list[TokenPriceHistory]:
        #     table_name = f"{self.chainid}_price_history"
        #
        #     select_query = f'''
        #     SELECT tokenid, openprice, highprice, lowprice, closeprice, time, volume
        #     FROM {table_name}
        #     WHERE tokenid = ?;
        #     '''
        #
        #     cursor = self.conn.cursor()
        #     cursor.execute(select_query, (tokenid,))
        #     rows = cursor.fetchall()
        #
        #     self.conn.commit()
        #     print(f"Data retrieved from {table_name} successfully.")
        #
        #     # 将查询结果初始化为 TokenPriceHistory 实例列表
        #     token_price_history_list = [
        #         TokenPriceHistory(
        #             tokenid=row[0],
        #             open=row[1],
        #             high=row[2],
        #             low=row[3],
        #             close=row[4],
        #             time=row[5],
        #             volume=row[6]
        #         ) for row in rows
        #     ]
        #
        #     return token_price_history_list





        # def retrieve_token_price_history(db,Tokendb:Tokendb):
        #     tokenid= Tokendb.tokenid
        #     tokenprice = db.readprice(tokenid)
        #     #    print(tokenprice)
        #     return tokenprice


        # tokendis: [1 3 5]
        #tokendb:Tokendb(tokenid=2994, chainid=solana, pair_address=7XPjKcaRvvjuBqGDV92w2EL4sXzQhBr2JUCaDi9n1MZ, creattime=2024-09-03 11:32:33),
        def read_token_andid(db,tokenids):
            tokendb = []
            for tokenid in tokenids:
                print(tokenid)
                tokendb.append(db.read_token_withid(tokenid))
            return tokendb
