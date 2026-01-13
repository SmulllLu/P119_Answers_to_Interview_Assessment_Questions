# api/schemas.py
from pydantic import BaseModel
from typing import Optional, List

# 单个检查结果的模型
class URLCheckResult(BaseModel):
    id: int
    board_name: str
    version: str
    original_url: str
    actual_url: str
    is_mirror: bool
    is_reachable: bool
    status_code: Optional[int]
    error_msg: Optional[str]
    check_time: str

# 批量结果的模型
class URLCheckResultList(BaseModel):
    total: int
    results: List[URLCheckResult]
