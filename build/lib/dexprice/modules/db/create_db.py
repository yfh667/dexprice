import os
import sqlite3

def initialize_table(db_folder, db_name, table_name):
    # 创建指定的文件夹（如果不存在）
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    # 连接到SQLite数据库，指定数据库路径
    db_path = os.path.join(db_folder, db_name)

    # 检查数据库文件是否已存在
    if os.path.exists(db_path):
        print(f"Database '{db_path}' already exists. Skipping table initialization.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建表的SQL语句
    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chainid TEXT NOT NULL,
        name TEXT NOT NULL,
        ca TEXT NOT NULL,
        pairaddress TEXT NOT NULL,
        creattime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    '''

    # 执行创建表的SQL语句
    cursor.execute(create_table_query)

    # 提交更改并关闭连接
    conn.commit()
    conn.close()

    print(f"Table '{table_name}' initialized in database '{db_path}'.")


