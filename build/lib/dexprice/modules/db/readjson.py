import json
import  re
import os
# def extract_chain_and_ca(data):
#     results = []
#
#     # 遍历 messages 列表中的每一条消息
#     for message in data['messages']:
#         chain = None
#         ca = None
#
#         text_entities = message.get('text_entities', [])
#     #    print(text_entities)
#
#         # 遍历 text_entities 列表中的每一个实体
#         for entity in text_entities:
#             # 检查类型为 bold 的实体，并提取链信息
#             if entity['type'] == 'bold' and chain is None:
#                 chain = entity['text'].lower()
#
#             # 检查类型为 code 的实体，并提取合约地址
#             if entity['type'] == 'text_link' and ca is None:
#                 href = entity.get('href', '')
#                 # 使用正则表达式提取 href 中的合约地址部分
#                 match = re.search(r'https://dexscreener\.com/\w+/([^/?]+)', href)
#                 if match:
#                     ca = match.group(1)
#                     break  # 已经找到合约地址，不需要再继续查找
#
#
#         # 如果找到 chain 和 ca，就将它们添加到结果中
#         if chain and ca:
#             results.append({'chain': chain, 'ca': ca})
#
#     return results
#
# def read_json_file(file_path):
#     with open(file_path, 'r') as file:
#         data = json.load(file)
#     return data
#
#
# def process_all_json_files(directory):
#     """遍历目录中的所有 JSON 文件，提取信息并汇总结果"""
#     all_results = []
#     # 列出目录中的所有文件
#     for filename in os.listdir(directory):
#         if filename.endswith('.json'):
#             file_path = os.path.join(directory, filename)
#             json_data = read_json_file(file_path)
#             # 提取所需的信息
#             results = extract_chain_and_ca(json_data)
#             all_results.extend(results)
#     return all_results


def gettokenca(files):
    token = []
    lines = []
    with open(files, 'r') as file:
        for line in file:
            lines.append(lines)
            if (len(line) > 120):
                base_url_position = line.find("https://dexscreener.com/")
                if base_url_position != -1:
                    base_url_position = line.find("https://dexscreener.com/")
                    start_pos = line.find("/", base_url_position + len("https://dexscreener.com/"))
                    chiand = line[base_url_position + 24:start_pos]
                    question_mark_position = line.find('?')
                    address = line[start_pos + 1:question_mark_position]
                    token.append({
                        'chain': chiand,
                        'ca': address
                    })

    return token
def process_all_json_files2(directory):
    """遍历目录中的所有 JSON 文件，提取信息并汇总结果"""
    all_results = []
    # 列出目录中的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
                        # 提取所需的信息
            results = gettokenca(file_path)
            all_results.extend(results)
    return all_results

def gettokenCAaddress(files,chainid):
    token = []
    lines = []
    # with open(files, 'r') as file:
    #     for line in file:
    #         lines.append(lines)
    #         if (len(line) > 120):
    #             base_url_position = line.find("https://dexscreener.com/")
    #             if base_url_position != -1:
    #                 base_url_position = line.find("https://dexscreener.com/")
    #                 start_pos = line.find("/", base_url_position + len("https://dexscreener.com/"))
    #                 chiand = line[base_url_position + 24:start_pos]
    #                 question_mark_position = line.find('?')
    #                 address = line[start_pos + 1:question_mark_position]
    #                 token.append({
    #                     'chain': chiand,
    #                     'ca': address
    #                 })
    #     code_lines = []

    with open(files, 'r', encoding='utf-8') as file:
        for line in file:
            # 尝试解析当前行的 JSON 数据
            line = line.strip()  # 去除行首行尾的空白符
            if '"type": "code"' in line:

                  #  data = json.loads(line)
                    next_line = file.readline().strip()
                    # 使用正则表达式提取 "text" 字段的值
                    match = re.search(r'"text":\s*"([^"]+)"', next_line)

                    if match:
                        text_value = match.group(1)
                        token.append({
                            'chain': chainid,
                            'ca': text_value
                        })
                        #token.append(text_value)
                       # print("提取的 text 值:", text_value)
                    else:
                        pass
                        #print("未找到匹配的 text 值")

                    # 检查是否包含 "type": "code" 的结构
                    # if isinstance(data, dict) and data.get("type") == "code":
                    #     code_lines.append(data)


    return token