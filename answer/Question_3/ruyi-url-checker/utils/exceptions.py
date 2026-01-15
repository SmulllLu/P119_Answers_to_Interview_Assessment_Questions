class RepoSyncError(Exception):
    """仓库同步失败异常"""
    pass


class TOMLParseError(Exception):
    """TOML文件解析异常"""
    pass


class URLCheckError(Exception):
    """URL检查异常"""
    pass
