from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from api.routes import router
from core.url_check import batch_check_all_urls, init_db
from utils.logger import logger
import uvicorn
import os


# 初始化FastAPI
app = FastAPI(
    title="Ruyi URL Checker",
    version="1.0.0",
    docs_url="/docs"
)
app.include_router(router)  # 注册接口路由


# 启动定时任务
def start_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
    # 立即执行一次检查
    batch_check_all_urls()
    # 每小时检查一次
    scheduler.add_job(
        batch_check_all_urls,
        "interval",
        seconds=3600,
        id="url_check_job"
    )
    scheduler.start()
    logger.info("⏰ 定时任务已启动（每小时检查一次）")
    return scheduler


# 初始化数据库
init_db()
# 启动调度器
scheduler = start_scheduler()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True  # 开发模式开启热重载
    )
