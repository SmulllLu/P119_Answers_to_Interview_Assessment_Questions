# core/repo_sync.py
import os
from git import Repo
from git.exc import GitCommandError
from utils.logger import logger
from dotenv import load_dotenv

load_dotenv()

REPO_URL = os.getenv("REPO_URL")
REPO_LOCAL_PATH = os.getenv("REPO_LOCAL_PATH")

def sync_packages_index():
    """同步 packages-index 仓库到本地"""
    try:
        # 如果本地仓库不存在，克隆
        if not os.path.exists(REPO_LOCAL_PATH):
            logger.info(f"克隆仓库 {REPO_URL} 到 {REPO_LOCAL_PATH}")
            Repo.clone_from(REPO_URL, REPO_LOCAL_PATH)
        else:
            # 如果已存在，拉取最新代码
            logger.info("拉取仓库最新代码")
            repo = Repo(REPO_LOCAL_PATH)
            origin = repo.remote(name="origin")
            origin.pull()
        return True
    except GitCommandError as e:
        logger.error(f"仓库同步失败: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"未知错误: {str(e)}")
        return False
