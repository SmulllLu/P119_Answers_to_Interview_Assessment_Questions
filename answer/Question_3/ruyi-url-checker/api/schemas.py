from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


# 单个URL的检查状态
class URLStatus(BaseModel):
    url: str
    is_available: bool
    status_code: Optional[int] = None
    response_time: Optional[float] = None  # 秒
    check_time: datetime
    error_msg: Optional[str] = None


# 单个board-image的检查结果
class BoardImageStatus(BaseModel):
    name: str  # board-image名称（如milkv-duo）
    version: str  # 版本号（如1.1.2）
    urls: List[URLStatus]


# 接口统一返回格式
class CheckResponse(BaseModel):
    success: bool
    data: Optional[List[BoardImageStatus]] = None
    message: Optional[str] = None
