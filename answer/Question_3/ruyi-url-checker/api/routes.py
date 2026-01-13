# api/routes.py
import sqlite3
from fastapi import APIRouter, Query
from typing import List, Optional
from api.schemas import URLCheckResult, URLCheckResultList
from utils.logger import logger
from dotenv import load_dotenv

load_dotenv()
RESULT_DB_PATH = "data/results.db"
router = APIRouter(prefix="/api/v1", tags=["URL 检查结果"])

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(RESULT_DB_PATH)
    conn.row_factory = sqlite3.Row  # 支持按列名访问
    return conn

@router.get("/results", response_model=URLCheckResultList)
def get_check_results(
    board_name: Optional[str] = Query(None, description="按板卡名称过滤，如 openbsd-riscv64-live"),
    version: Optional[str] = Query(None, description="按版本过滤，如 7.6.0"),
    is_mirror: Optional[bool] = Query(None, description="是否为 mirror URL"),
    is_reachable: Optional[bool] = Query(None, description="是否可达")
):
    """查询 URL 检查结果（支持多条件过滤）"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # 构建查询条件
        query = "SELECT * FROM url_check_results WHERE 1=1"
        params = []
        if board_name:
            query += " AND board_name = ?"
            params.append(board_name)
        if version:
            query += " AND version = ?"
            params.append(version)
        if is_mirror is not None:
            query += " AND is_mirror = ?"
            params.append(is_mirror)
        if is_reachable is not None:
            query += " AND is_reachable = ?"
            params.append(is_reachable)
        # 执行查询
        cursor.execute(query, params)
        rows = cursor.fetchall()
        # 转换为模型列表
        results = [URLCheckResult(**dict(row)) for row in rows]
        conn.close()
        return {
            "total": len(results),
            "results": results
        }
    except Exception as e:
        logger.error(f"查询结果失败: {str(e)}")
        return {"total": 0, "results": []}

@router.get("/boards", response_model=List[str])
def get_all_boards():
    """获取所有已检查的板卡名称"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT board_name FROM url_check_results")
        rows = cursor.fetchall()
        conn.close()
        return [row["board_name"] for row in rows]
    except Exception as e:
        logger.error(f"获取板卡名称失败: {str(e)}")
        return []
