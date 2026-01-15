from loguru import logger
import os
from pathlib import Path

# 创建logs目录
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# 配置日志：同时输出到控制台+文件（按天滚动）
logger.add(
    LOG_DIR / "ruyi_url_checker.log",
    rotation="1 day",  # 每天生成新日志
    retention="7 days",  # 保留7天日志
    compression="zip",  # 旧日志压缩
    level="INFO"
)

# 导出logger实例
__all__ = ["logger"]
