from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

# 验证环境变量
print(f"TZ: {os.getenv('TZ')}")