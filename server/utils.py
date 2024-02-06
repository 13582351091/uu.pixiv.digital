import json
import os
import hashlib
import secrets
# 获取当前文件所在的目录
current_dir = os.path.dirname(os.path.realpath(__file__))
# 读取配置文件
with open(os.path.join(current_dir, 'uu.json'), 'r') as f:
    config = json.load(f)
