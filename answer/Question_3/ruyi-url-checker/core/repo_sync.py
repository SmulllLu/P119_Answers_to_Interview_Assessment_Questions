# core/repo_sync.py
import os
from git import Repo
from git.exc import GitCommandError

# 注意：先确保 logger 模块能正常导入，若 utils/logger.py 未创建，先补全
try:
    from utils.logger import logger
except ImportError:
    # 临时日志兜底（避免 logger 导入失败影响核心功能）
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("repo_sync")
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量读取配置（若未配置，用默认值）
REPO_URL = os.getenv("REPO_URL", "https://github.com/ruyisdk/packages-index.git")
REPO_LOCAL_PATH = os.getenv("REPO_LOCAL_PATH", "data/packages-index")


def sync_packages_index():
    """同步 packages-index 仓库到本地（核心函数，确保函数名拼写正确、无缩进错误）"""
    try:
        # 创建本地仓库目录（若不存在）
        os.makedirs(os.path.dirname(REPO_LOCAL_PATH), exist_ok=True)

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


# 测试函数（可选，验证函数能正常执行）
if __name__ == "__main__":
    sync_packages_index()
