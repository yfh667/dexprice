import os

def find_project_root(current_dir, marker="settings.py"):
    """
    递归向上查找项目根目录，通过指定的标识文件定位。
    :param current_dir: 当前文件所在目录
    :param marker: 用于标识项目根目录的文件名
    :return: 项目根目录的绝对路径
    """
    while current_dir:
        if marker in os.listdir(current_dir):
            return current_dir
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:  # 已经到达根目录
            break
        current_dir = parent_dir
    raise FileNotFoundError(f"Project root not found. Marker '{marker}' missing.")

# # 当前脚本所在目录
# current_dir = os.path.dirname(os.path.abspath(__file__))
#
# # 定位项目根目录
# PROJECT_ROOT = find_project_root(current_dir)
#
# # 数据文件夹路径
# DATA_FOLDER = os.path.join(PROJECT_ROOT, "Data")
#
# # 示例其他路径
# CONFIG_FILE = os.path.join(DATA_FOLDER, "config.json")
#
# # 测试打印路径
# print(f"项目根目录: {PROJECT_ROOT}")
# print(f"数据文件夹路径: {DATA_FOLDER}")
# print(f"配置文件路径: {CONFIG_FILE}")