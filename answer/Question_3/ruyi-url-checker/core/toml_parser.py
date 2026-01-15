import toml
from pathlib import Path
from utils.logger import logger
from utils.exceptions import TOMLParseError
from core.repo_sync import LOCAL_REPO_PATH

# 配置文件路径（关联packages-index仓库）
CONFIG_TOML_PATH = LOCAL_REPO_PATH / "config.toml"


def load_mirror_config() -> dict:
    """
    核心修复：加载config.toml并转换为{镜像ID: {urls: 地址列表}}的字典
    解决[[mirrors]]数组无法通过ID直接读取的问题
    """
    try:
        if not CONFIG_TOML_PATH.exists():
            logger.warning(f"⚠️ config.toml不存在: {CONFIG_TOML_PATH}")
            return {}

        with open(CONFIG_TOML_PATH, "r", encoding="utf-8") as f:
            config = toml.load(f)

        # 关键：将[[mirrors]]数组转换为镜像ID映射的字典
        mirror_config = {}
        for mirror in config.get("mirrors", []):
            mirror_id = mirror.get("id")
            mirror_urls = mirror.get("urls", [])
            if mirror_id and mirror_urls:
                mirror_config[mirror_id] = {"urls": mirror_urls}

        # 调试日志：确认revyos配置是否加载
        if "revyos" in mirror_config:
            logger.info(f"✅ 成功加载revyos镜像配置: {mirror_config['revyos']['urls']}")
        else:
            logger.error(f"❌ 未加载到revyos镜像配置！已加载的镜像ID: {list(mirror_config.keys())}")

        return mirror_config
    except Exception as e:
        logger.error(f"❌ 加载mirror配置失败: {str(e)}")
        raise TOMLParseError(f"mirror配置解析失败: {str(e)}")


def resolve_mirror_url(url: str, mirror_config: dict) -> list[str]:
    """
    核心修复：读取urls（复数）而非url（单数），完善异常处理
    """
    if not url.startswith("mirror://"):
        return [url]

    try:
        # 拆分mirror名称和路径，处理空值
        mirror_part = url.replace("mirror://", "").split("/", 1)
        if not mirror_part or not mirror_part[0]:
            logger.warning(f"⚠️ 无效的mirror URL格式: {url}")
            return []

        mirror_name = mirror_part[0].strip()
        path = mirror_part[1].strip() if len(mirror_part) > 1 else ""

        # 核心修复：读取urls（复数）
        mirror_item = mirror_config.get(mirror_name, {})
        mirror_urls = mirror_item.get("urls", [])

        if not mirror_urls:
            logger.warning(f"⚠️ mirror「{mirror_name}」无配置URL | 已加载镜像: {list(mirror_config.keys())}")
            return []

        # 拼接完整URL，避免//重复
        full_urls = []
        for base in mirror_urls:
            clean_base = base.rstrip("/")
            clean_path = path.lstrip("/")
            full_url = f"{clean_base}/{clean_path}" if clean_path else clean_base
            full_urls.append(full_url)

        logger.debug(f"解析mirror URL: {url} → {full_urls}")
        return full_urls
    except IndexError as e:
        logger.error(f"❌ 解析mirror URL失败: URL格式异常 {url} | 错误: {str(e)}")
        raise TOMLParseError(f"mirror URL格式异常 {url}: {str(e)}")
    except Exception as e:
        logger.error(f"❌ 解析mirror URL失败: {str(e)}")
        raise TOMLParseError(f"mirror URL解析失败: {str(e)}")


def parse_toml_file(toml_path: Path) -> list[str]:
    """解析单个TOML文件，提取所有待检查的URL（逻辑不变）"""
    try:
        with open(toml_path, "r", encoding="utf-8") as f:
            data = toml.load(f)

        urls = []
        # 格式1：[[distfiles]]数组
        distfiles = data.get("distfiles", [])
        if isinstance(distfiles, list):
            for df in distfiles:
                urls.extend(df.get("urls", []))
        # 格式2：source.url
        source_url = data.get("source", {}).get("url")
        if source_url:
            urls.append(source_url)

        return list(set(urls))  # 去重
    except Exception as e:
        logger.error(f"❌ 解析TOML文件「{toml_path}」失败: {str(e)}")
        raise TOMLParseError(f"TOML文件解析失败: {str(e)}")
