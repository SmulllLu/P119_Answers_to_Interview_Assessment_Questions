# core/toml_parser.py
import os
import tomlkit
from utils.logger import logger
from dotenv import load_dotenv

load_dotenv()
REPO_LOCAL_PATH = os.getenv("REPO_LOCAL_PATH")
CONFIG_TOML_PATH = os.path.join(REPO_LOCAL_PATH, "config.toml")
BOARD_IMAGE_PATH = os.path.join(REPO_LOCAL_PATH, "manifests/board-image")


def parse_mirror_mapping():
    """解析 config.toml 中的 mirror 映射（如 openbsd -> [url1, url2]）"""
    try:
        with open(CONFIG_TOML_PATH, "r", encoding="utf-8") as f:
            config = tomlkit.load(f)
        # 提取 mirror 部分
        mirror_mapping = config.get("mirror", {})
        # 转换格式：mirror["openbsd"] = ["url1", "url2"]
        result = {}
        for mirror_name, mirror_info in mirror_mapping.items():
            result[mirror_name] = mirror_info.get("url", [])
        logger.info(f"解析到 {len(result)} 个 mirror 映射")
        return result
    except Exception as e:
        logger.error(f"解析 config.toml 失败: {str(e)}")
        return {}


def parse_board_image_urls():
    """解析 board-image 下所有 toml 文件的 URL，处理 mirror:// 格式"""
    mirror_mapping = parse_mirror_mapping()
    if not mirror_mapping:
        logger.error("mirror 映射解析失败，终止 URL 解析")
        return []

    url_items = []  # 存储所有需要检查的 URL 项：(board_name, version, original_url, actual_urls)
    # 遍历 board-image 下的所有目录（每个目录对应一个 board）
    for board_name in os.listdir(BOARD_IMAGE_PATH):
        board_dir = os.path.join(BOARD_IMAGE_PATH, board_name)
        if not os.path.isdir(board_dir):
            continue
        # 遍历目录下的 toml 文件（每个文件对应一个版本）
        for toml_file in os.listdir(board_dir):
            if not toml_file.endswith(".toml"):
                continue
            version = toml_file.replace(".toml", "")
            toml_path = os.path.join(board_dir, toml_file)
            try:
                with open(toml_path, "r", encoding="utf-8") as f:
                    toml_data = tomlkit.load(f)
                # 提取 URL 字段（不同 toml 可能字段名不同，参考 openbsd-riscv64-live 的示例）
                original_url = toml_data.get("url")
                if not original_url:
                    continue
                # 处理 mirror:// 格式
                actual_urls = []
                if original_url.startswith("mirror://"):
                    # 解析 mirror 名称：mirror://openbsd/xxx -> openbsd
                    mirror_name = original_url.split("//")[1].split("/")[0]
                    mirror_base_urls = mirror_mapping.get(mirror_name, [])
                    # 拼接完整 URL：mirror_base_url + /xxx
                    path = original_url.split(f"mirror://{mirror_name}")[1]
                    actual_urls = [f"{base_url}{path}" for base_url in mirror_base_urls]
                else:
                    actual_urls = [original_url]

                url_items.append({
                    "board_name": board_name,
                    "version": version,
                    "original_url": original_url,
                    "actual_urls": actual_urls,
                    "is_mirror": original_url.startswith("mirror://")
                })
            except Exception as e:
                logger.error(f"解析 {toml_path} 失败: {str(e)}")
                continue
    logger.info(f"解析到 {len(url_items)} 个需要检查的 URL 项")
    return url_items
