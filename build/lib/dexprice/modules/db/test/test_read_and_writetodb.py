
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from create_db import initialize_table
from readjson import extract_chain_and_ca,read_json_file



if __name__ == "__main__":
    db_folder = '/home/yfh/Desktop/mywork/pgp2/bestdex/DexPrice/Data'  # 数据库存储文件夹
    db_name = 'crypto_data.db'  # 数据库文件名
    table_name = 'base'  # 表名

    initialize_table(db_folder, db_name, table_name)
    file_path = '/home/yfh/Desktop/linshi/result.json'  # 将路径替换为你的 JSON 文件路径
    json_data = read_json_file(file_path)

    # 从 JSON 数据中提取所有链和合约地址
    results = extract_chain_and_ca(json_data)

    # 输出所有结果
    for result in results:
        print(f"Chain: {result['chain']}, CA: {result['ca']}")


