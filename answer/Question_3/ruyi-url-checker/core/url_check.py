# core/url_check.py
import time
import requests
import sqlite3
import os
from utils.logger import logger
from dotenv import load_dotenv

load_dotenv()
URL_CHECK_TIMEOUT = int(os.getenv("URL_CHECK_TIMEOUT", 10))
RESULT_DB_PATH = "data/results.db"

# 初始化 SQLite 数据库
def init_db():
    """初始化结果数据库"""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(RESULT_DB_PATH)
    cursor = conn.cursor()
    # 创建表：存储 URL 检查结果
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS url_check_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        board_name TEXT NOT NULL,
        version TEXT NOT NULL,
        original_url TEXT NOT NULL,
        actual_url TEXT NOT NULL,
        is_mirror BOOLEAN NOT NULL,
        is_reachable BOOLEAN NOT NULL,
        status_code INTEGER,
        error_msg TEXT,
        check_time TIMESTAMP NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def check_url_reachable(url):
    """检查单个 URL 是否可达"""
    try:
        # 使用 HEAD 请求（更轻量），失败则用 GET
        response = requests.head(
            url,
            timeout=URL_CHECK_TIMEOUT,
            allow_redirects=True,
            headers={"User-Agent": "ruyi-url-checker/1.0"}
        )
    except requests.exceptions.HeadNotSupported:
        response = requests.get(
            url,
            timeout=URL_CHECK_TIMEOUT,
            allow_redirects=True,
            headers={"User-Agent": "ruyi-url-checker/1.0"}
        )
    except Exception as e:
        return False, None, str(e)
    # 状态码 200-299 视为可达
    is_reachable = 200 <= response.status_code < 300
    return is_reachable, response.status_code, None

def run_full_url_check():
    """执行全量 URL 检查，并保存结果"""
    from core.repo_sync import sync_packages_index
    from core.toml_parser import parse_board_image_urls

    # 1. 先同步仓库
    if not sync_packages_index():
        return False
    # 2. 初始化数据库
    init_db()
    # 3. 解析需要检查的 URL
    url_items = parse_board_image_urls()
    if not url_items:
        logger.error("无需要检查的 URL")
        return False

    # 4. 逐个检查 URL 并保存结果
    conn = sqlite3.connect(RESULT_DB_PATH)
    cursor = conn.cursor()
    check_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for item in url_items:
        board_name = item["board_name"]
        version = item["version"]
        original_url = item["original_url"]
        actual_urls = item["actual_urls"]
        is_mirror = item["is_mirror"]

        for actual_url in actual_urls:
            logger.info(f"检查 URL: {actual_url} (board: {board_name}, version: {version})")
            is_reachable, status_code, error_msg = check_url_reachable(actual_url)
            # 插入数据库
            cursor.execute('''
            INSERT INTO url_check_results 
            (board_name, version, original_url, actual_url, is_mirror, is_reachable, status_code, error_msg, check_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                board_name, version, original_url, actual_url, is_mirror,
                is_reachable, status_code, error_msg, check_time
            ))
    conn.commit()
    conn.close()
    logger.info(f"全量检查完成，共检查 {len(url_items)} 个 URL 项")
    return True
