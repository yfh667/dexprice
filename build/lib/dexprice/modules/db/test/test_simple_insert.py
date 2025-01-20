


from modules.db.insert_db import insert_data

from modules.db.create_db import initialize_table


# 测试代码
if __name__ == "__main__":
    db_folder = '/home/yfh/Desktop/mywork/pgp2/bestdex/DexPrice/Data'  # 数据库存储文件夹
    db_name = 'crypto_data.db'  # 数据库文件名
    table_name = 'token_pairs'  # 表名

    # 初始化表
    initialize_table(db_folder, db_name, table_name)

    # 模拟的 TokenInfo 数据
    token_info = {
        'chainid': 'solana',
        'name': 'KEN',
        'ca': 'KENMdm22KMgjgGhQ19yLtsLD4vaheJBmg3v9KwuFnM3',
        'pairaddress': '14TAnpeomRgQmgQD7kfpDMxFF8MxkdGypikeqkmbF2aY',
        'creattime': '2024-08-12 18:14:57'
    }

    # 插入数据
    insert_data(db_folder, db_name, table_name,
                token_info['chainid'],
                token_info['name'],
                token_info['ca'],
                token_info['pairaddress'],
                token_info['creattime'])

    print("Data inserted successfully.")