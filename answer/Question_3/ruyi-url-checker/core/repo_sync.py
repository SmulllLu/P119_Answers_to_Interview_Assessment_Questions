import git
from git.exc import GitCommandError
from pathlib import Path
from utils.logger import logger
from utils.exceptions import RepoSyncError


# 配置（可移到.env，这里先写死适配结构）
PACKAGES_INDEX_URL = "https://github.com/ruyisdk/packages-index.git"
LOCAL_REPO_PATH = Path("data/packages-index")
BOARD_IMAGE_PATH = LOCAL_REPO_PATH / "manifests" / "board-image"


def sync_repo() -> None:
    """拉取/更新本地packages-index仓库"""
    try:
        if LOCAL_REPO_PATH.exists():
            # 已存在：pull更新
            repo = git.Repo(str(LOCAL_REPO_PATH))
            origin = repo.remotes.origin
            origin.pull()
            logger.info("✅ 仓库已更新")
        else:
            # 不存在：clone克隆
            git.Repo.clone_from(PACKAGES_INDEX_URL, str(LOCAL_REPO_PATH))
            logger.info("✅ 仓库已克隆")
    except GitCommandError as e:
        logger.error(f"❌ 仓库操作失败: {str(e)}")
        raise RepoSyncError(f"仓库同步失败: {str(e)}")


def get_all_toml_files() -> list[Path]:
    """获取所有board-image下的TOML文件"""
    if not BOARD_IMAGE_PATH.exists():
        logger.warning("⚠️ board-image目录不存在")
        return []
    toml_files = list(BOARD_IMAGE_PATH.rglob("*.toml"))
    logger.info(f"🔍 找到{len(toml_files)}个TOML文件")
    return toml_files
