import time
import httpx
import sqlite3
from datetime import datetime
from pathlib import Path
from utils.logger import logger
from core.repo_sync import sync_repo, get_all_toml_files
from core.toml_parser import load_mirror_config, resolve_mirror_url, parse_toml_file
from api.schemas import URLStatus, BoardImageStatus
from utils.exceptions import URLCheckError

# 配置
URL_TIMEOUT = 10
MAX_REDIRECTS = 3
DB_PATH = Path("data/results.db")


# 初始化数据库
def init_db():
    """创建results.db的表结构（修复：自动创建目录+校验数据库有效性）"""
    # 第一步：确保data目录存在
    DB_PATH.parent.mkdir(exist_ok=True, parents=True)

    # 第二步：删除无效的数据库文件（如果存在且不是有效SQLite文件）
    if DB_PATH.exists():
        try:
            # 尝试连接，验证是否为有效SQLite数据库
            conn = sqlite3.connect(DB_PATH)
            conn.execute("SELECT 1")  # 简单校验
            conn.close()
        except sqlite3.DatabaseError:
            logger.warning("⚠️ 发现无效的数据库文件，自动删除")
            DB_PATH.unlink()  # 删除无效文件

    # 第三步：重新创建/连接数据库并建表
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # 关键修复：SQL注释用--而非#，避免语法错误
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS check_results
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           name
                           TEXT
                           NOT
                           NULL,
                           version
                           TEXT
                           NOT
                           NULL,
                           url
                           TEXT
                           NOT
                           NULL,
                           is_available
                           BOOLEAN
                           NOT
                           NULL,
                           status_code
                           INTEGER,
                           response_time
                           REAL,
                           check_time
                           DATETIME
                           NOT
                           NULL,
                           error_msg
                           TEXT,
                           UNIQUE
                       (
                           name,
                           version,
                           url
                       ) -- 避免重复存储同一版本的同一URL
                           )
                       ''')
        conn.commit()
        conn.close()
        logger.info("✅ 数据库初始化成功")
    except sqlite3.Error as e:
        logger.error(f"❌ 数据库初始化失败: {str(e)}")
        raise URLCheckError(f"数据库初始化失败: {str(e)}")


def check_single_url(url: str) -> URLStatus:
    """检查单个URL的可达性"""
    check_time = datetime.now()
    try:
        start = time.time()
        with httpx.Client(timeout=URL_TIMEOUT, max_redirects=MAX_REDIRECTS) as client:
            # 优先HEAD，失败则用GET
            try:
                resp = client.head(url, follow_redirects=True)
            except httpx.HTTPError:
                resp = client.get(url, follow_redirects=True)
        resp_time = round(time.time() - start, 3)
        return URLStatus(
            url=url,
            is_available=resp.status_code in [200, 206],
            status_code=resp.status_code,
            response_time=resp_time,
            check_time=check_time,
            error_msg=None
        )
    except Exception as e:
        resp_time = round(time.time() - start, 3)
        return URLStatus(
            url=url,
            is_available=False,
            status_code=None,
            response_time=resp_time,
            check_time=check_time,
            error_msg=str(e)
        )


def batch_check_all_urls() -> list[BoardImageStatus]:
    init_db()  # 确保数据库表存在
    try:
        # 1. 同步仓库
        sync_repo()
        # 2. 加载mirror配置
        mirror_config = load_mirror_config()
        # 3. 获取所有TOML文件
        toml_files = get_all_toml_files()
        if not toml_files:
            logger.warning("⚠️ 未找到任何TOML文件")
            return []

        results = []
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        logger.info(f"✅ 成功连接数据库，准备写入数据")

        for toml_file in toml_files:
            # 提取name和version（从路径）
            rel_path = toml_file.relative_to(Path("data/packages-index/manifests/board-image"))
            name = rel_path.parent.name
            version = rel_path.stem
            logger.debug(f"📝 处理[{name}-{version}]，开始解析URL")

            # 解析TOML中的URL
            raw_urls = parse_toml_file(toml_file)
            if not raw_urls:
                logger.warning(f"⚠️ 「{name}-{version}」无有效URL")
                continue

            # 解析mirror URL
            target_urls = []
            for url in raw_urls:
                target_urls.extend(resolve_mirror_url(url, mirror_config))
            if not target_urls:
                logger.warning(f"⚠️ 「{name}-{version}」解析后无URL")
                continue

            # 检查每个URL
            url_statuses = [check_single_url(url) for url in target_urls]
            logger.debug(f"🔍 [{name}-{version}] 完成URL检查，共{len(url_statuses)}个URL")

            # ========== 关键：添加写入日志 ==========
            try:
                for status in url_statuses:
                    # 打印要写入的数据（调试用）
                    logger.debug(f"准备写入数据：name={name}, version={version}, url={status.url}, is_available={status.is_available}")
                    cursor.execute('''
                        REPLACE INTO check_results 
                        (name, version, url, is_available, status_code, response_time, check_time, error_msg)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        name,
                        version,
                        status.url,
                        1 if status.is_available else 0,
                        status.status_code,
                        status.response_time,
                        status.check_time.strftime("%Y-%m-%d %H:%M:%S"),
                        status.error_msg
                    ))
                # 每处理一个文件就提交一次（避免事务积压）
                conn.commit()
                logger.info(f"✅ [{name}-{version}] 数据已成功写入数据库")
            except Exception as e:
                logger.error(f"❌ [{name}-{version}] 写入数据库失败：{str(e)}")
                conn.rollback()  # 写入失败回滚
                continue
            # ======================================

            # 构建返回结果
            results.append(BoardImageStatus(
                name=name,
                version=version,
                urls=url_statuses
            ))
            logger.info(f"✅ 完成「{name}-{version}」检查（{len(url_statuses)}个URL）")

        # 最终提交+关闭连接
        conn.commit()
        conn.close()
        logger.info(f"🎉 所有检查完成，共写入{len(results)}条board-image数据到数据库")
        return results
    except Exception as e:
        logger.error(f"❌ 批量检查失败: {str(e)}")
        # 异常时关闭连接
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        raise URLCheckError(f"批量检查失败: {str(e)}")


def get_all_results() -> list[BoardImageStatus]:
    """从数据库获取所有检查结果"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 按列名取数据
    cursor = conn.cursor()

    # 按name+version分组
    cursor.execute('''
        SELECT name, version, url, is_available, status_code, response_time, check_time, error_msg
        FROM check_results
        ORDER BY name, version, check_time DESC
    ''')
    rows = cursor.fetchall()
    conn.close()

    # 分组整理成BoardImageStatus格式
    result_map = {}
    for row in rows:
        key = (row["name"], row["version"])
        if key not in result_map:
            result_map[key] = BoardImageStatus(
                name=row["name"],
                version=row["version"],
                urls=[]
            )
        # 转换datetime字符串为datetime对象
        check_time = datetime.strptime(row["check_time"], "%Y-%m-%d %H:%M:%S")
        result_map[key].urls.append(URLStatus(
            url=row["url"],
            is_available=bool(row["is_available"]),
            status_code=row["status_code"],
            response_time=row["response_time"],
            check_time=check_time,
            error_msg=row["error_msg"]
        ))
    return list(result_map.values())


def get_results_by_name(name: str) -> list[BoardImageStatus]:
    """从数据库按名称模糊查询结果"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT name, version, url, is_available, status_code, response_time, check_time, error_msg
        FROM check_results
        WHERE name LIKE ?
        ORDER BY name, version, check_time DESC
    ''', (f"%{name}%",))
    rows = cursor.fetchall()
    conn.close()

    # 分组整理
    result_map = {}
    for row in rows:
        key = (row["name"], row["version"])
        if key not in result_map:
            result_map[key] = BoardImageStatus(
                name=row["name"],
                version=row["version"],
                urls=[]
            )
        check_time = datetime.strptime(row["check_time"], "%Y-%m-%d %H:%M:%S")
        result_map[key].urls.append(URLStatus(
            url=row["url"],
            is_available=bool(row["is_available"]),
            status_code=row["status_code"],
            response_time=row["response_time"],
            check_time=check_time,
            error_msg=row["error_msg"]
        ))
    return list(result_map.values())
