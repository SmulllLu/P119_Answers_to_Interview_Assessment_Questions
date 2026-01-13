# main.py
import os
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from api.routes import router as api_router
from core.url_check import run_full_url_check
# 兜底日志（避免 logger 导入失败）
try:
    from utils.logger import logger
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("main")
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 全局定时任务调度器（避免重复创建）
scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI 生命周期管理：启动时初始化，关闭时清理"""
    logger.info("启动 Ruyi URL Checker Bot...")
    try:
        # 启动时立即执行一次全量检查
        run_full_url_check()
        # 配置定时任务（默认1天执行一次）
        check_interval = int(os.getenv("CHECK_INTERVAL", 86400))
        scheduler.add_job(
            run_full_url_check,
            "interval",
            seconds=check_interval,
            id="url_check_job",
            name="URL 可达性全量检查"
        )
        scheduler.start()
        logger.info("定时任务已启动，检查间隔：%d 秒", check_interval)
    except Exception as e:
        logger.error(f"初始化失败: {str(e)}")
    yield  # 服务运行中
    # 关闭时停止定时任务
    scheduler.shutdown()
    logger.info("定时任务已停止，服务正常关闭")

# 初始化 FastAPI 应用（绑定 lifespan）
app = FastAPI(
    title="Ruyi URL Checker Bot",
    version="1.0",
    lifespan=lifespan  # 关键：替换 on_event
)

# 注册接口路由
app.include_router(api_router)

# 根路径接口
@app.get("/")
def root():
    return {
        "message": "Ruyi URL Checker Bot 运行中",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

# 主函数
if __name__ == "__main__":
    host = os.getenv("FASTAPI_HOST", "0.0.0.0")
    port = int(os.getenv("FASTAPI_PORT", 7777))  # 你的端口是7777，保持一致
    # 启动服务（关闭 reload 可避免定时任务重复创建，开发阶段可保留）
    uvicorn.run("main:app", host=host, port=port, reload=True)
