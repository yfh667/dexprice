import json
import os

def update_config(nodes, file_path):
    """
    更新配置文件，删除 dns-in 和 dns-out 配置，并添加新的 inbounds、outbounds 和 rules。

    :param nodes: 节点列表，每个节点对应一个新的 inbound 和 outbound 配置
    :param file_path: JSON 配置文件的路径
    """
    # 加载配置文件
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            config = json.load(file)
    else:
        print(f"文件 {file_path} 不存在。请检查路径。")
        return

    # 删除包含 "dns-in" 的 inbound 配置
    config["inbounds"] = [
        inbound for inbound in config.get("inbounds", [])
        if not (inbound.get("tag") == "dns-in" and inbound.get("type") == "direct" and inbound.get("listen_port") == 53)
    ]

    # 删除包含端口 53 且 outbound 为 "dns-out" 的路由规则
    config["route"]["rules"] = [
        rule for rule in config.get("route", {}).get("rules", [])
        if not (rule.get("port") == 53 and rule.get("outbound") == "dns-out")
    ]

    # 设置初始端口
    listen_port = 30001

    # 添加新的 inbounds、outbounds 和 rules
    for index, node in enumerate(nodes):
        # 创建 inbound
        inbound = {
            "type": "http",
            "tag": f"inbound{index + 1}",
            "listen": "::",
            "listen_port": listen_port
        }
        config["inbounds"].append(inbound)

        # 创建 outbound
        outbound = {
            "type": "selector",
            "tag": f"outbound{index + 1}",
            "outbounds": [node]
        }
        config["outbounds"].append(outbound)

        # 创建规则
        rule = {
            "inbound": f"inbound{index + 1}",
            "outbound": f"outbound{index + 1}"
        }
        config["route"]["rules"].append(rule)

        # 递增端口号
        listen_port += 1

    # 写回文件
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=2)

    print(f"文件 {file_path} 已成功更新，添加了 {len(nodes)} 个节点配置，并删除了旧的 dns-in 和 dns-out 配置。")

# 示例调用
nodes = [
    "美国 1 | 猎户座",
    "美国 2 | 猎户座",
    "新加坡 1 | 猎户座",
    "新加坡 2 | 猎户座",
    "首尔 1 | 猎户座",
    "美国 1 | 专线",
    "美国 2 | 专线",
    "美国 3 | 专线",
    "新加坡 1 | 专线",
    "新加坡 2 | 专线",
    "新加坡 3 | 专线",
    "新加坡 4 | 专线",
    "新加坡 5 | 专线",
    "新加坡 6 | 专线",
    "日本 1 | 专线",
    "日本 2 | 专线",
    "日本 3 | 专线",
    "日本 4 | 专线",
    "日本 5 | 专线",
    "日本 6 | 专线",
    "日本 7 | 专线",
    "日本 8 | 专线"
]

file_path = "/home/yfh/Desktop/linshi/config2.json"
update_config(nodes, file_path)
