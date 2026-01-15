import sqlite3
from datetime import datetime

# 数据库路径
DB_PATH = "data/results.db"

def query_url_status(filter_name: str = None):
    """
    查询URL可达性信息
    :param filter_name: 筛选名称（如"revyos"，留空查所有）
    """
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 按列名读取数据
    cursor = conn.cursor()

    # 构建查询语句
    if filter_name:
        sql = """
            SELECT name, version, url, is_available, status_code, response_time, check_time, error_msg
            FROM check_results
            WHERE name LIKE ?
            ORDER BY check_time DESC
        """
        cursor.execute(sql, (f"%{filter_name}%",))
    else:
        sql = """
            SELECT name, version, url, is_available, status_code, response_time, check_time, error_msg
            FROM check_results
            ORDER BY check_time DESC
        """
        cursor.execute(sql)

    # 获取结果并格式化输出
    results = cursor.fetchall()
    if not results:
        print("⚠️ 数据库中暂无URL检查数据")
        return

    print(f"📊 共查询到 {len(results)} 条URL检查记录：")
    print("-" * 120)
    for row in results:
        # 格式化可达性状态
        status = "✅ 可达" if row["is_available"] else "❌ 不可达"
        # 格式化响应时间（空值显示0）
        resp_time = row["response_time"] or 0.0
        # 输出
        print(f"名称：{row['name']}-{row['version']}")
        print(f"URL：{row['url']}")
        print(f"状态：{status} | HTTP状态码：{row['status_code'] or '无'} | 响应时间：{resp_time}秒")
        print(f"检查时间：{row['check_time']}")
        if row["error_msg"]:
            print(f"错误信息：{row['error_msg']}")
        print("-" * 120)

    conn.close()

# 调用示例：查询revyos相关的URL
if __name__ == "__main__":
    query_url_status(filter_name="revyos")  # 改为None查所有
