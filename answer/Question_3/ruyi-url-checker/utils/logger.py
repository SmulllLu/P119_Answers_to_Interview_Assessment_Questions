# utils/logger.py
import logging
import os

# 创建 logs 目录
os.makedirs("logs", exist_ok=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/ruyi_url_checker.log", encoding="utf-8"),
        logging.StreamHandler()  # 同时输出到控制台
    ]
)

# 创建 logger 实例
logger = logging.getLogger("ruyi-url-checker")
