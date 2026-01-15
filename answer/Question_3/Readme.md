# Ruyi URL Checker Bot

>一个自动化 `Bot`，用于定期检查 `ruyisdk/packages-index` 项目中 `board-image` 目录下 `TOML` 配置文件的资源 `URL` 可达性（含 `mirror://` 格式 `URL`），并基于 `FastAPI` 提供查询接口。
## Question 3
>理解 ruyi-packaging 项目，这个项目试图实现 packages-index/board-image 的自动更新，使用 check 命令检查上游更新，使用 manifests 命令生成指定版本的 toml 配置。其中以 openbsd-riscv64-live 为例，其使用了 mirror:// 格式的 url，其声明见 config.toml，不难发现 openbsd 声明的 url 中并不是每个 url 都有相关资源可供下载。请实现一个 bot，定期检查这些资源的可用性（url 是否可达），并以 Fast API 的方式提供查询接口。对于 mirror:// 格式 url 的资源，则需要标记其中每个 url 的可用性。将代码提交到个人 GitHub 账号下的公开仓库中。


## 核心功能
* 自动同步远程 packages-index 仓库到本地，保证配置文件最新
* 解析 config.toml 中的 mirror 映射，处理 mirror:// 格式 URL 为实际可访问地址
* 定期检查所有 URL 可达性，支持超时控制和异常捕获
* 轻量级 SQLite 存储检查结果，支持多条件查询
* FastAPI 提供 RESTful API，自动生成接口文档，便于快速使用
* 后台定时任务（默认每日执行），无需人工干预


## 环境搭建
1. 克隆仓库
```bash
git clone 
cd ruyi-url-checker
```
2. 创建并激活虚拟环境

>避免污染系统 Python 环境，Ubuntu 等系统需强制使用虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境（Linux/Mac）
source venv/bin/activate

# 激活虚拟环境（Windows）
venv\Scripts\activate
```
激活后终端提示符会显示 `(venv)`，表示进入虚拟环境。

3. 安装依赖

```bash
pip install -r requirements.txt
```
若手动安装，执行以下命令：

```bash
pip install fastapi uvicorn requests tomlkit apscheduler gitpython python-dotenv
```


4. 配置环境变量
复制并修改 `.env` 配置文件（项目根目录创建 `.env`）：

```bash
# .env 配置示例
# 远程仓库地址
REPO_URL=https://github.com/ruyisdk/packages-index.git
# 本地仓库存储路径
REPO_LOCAL_PATH=data/packages-index
# URL 检查超时时间（秒）
URL_CHECK_TIMEOUT=10
# 定时检查间隔（秒，86400=1天）
CHECK_INTERVAL=86400
# FastAPI 运行地址
FASTAPI_HOST=0.0.0.0
# FastAPI 运行端口
FASTAPI_PORT=7777
```

## 快速启动

```bash
# 激活虚拟环境（若未激活）
source venv/bin/activate
# 启动服务
python main.py
```

## 项目结构
``` 
ruyi-url-checker/
├── .env                # 环境配置文件（需手动创建）
├── .gitignore          # Git 忽略规则
├── main.py             # 项目入口（FastAPI + 定时任务）
├── requirements.txt    # 依赖清单
├── core/               # 核心业务逻辑
│   ├── repo_sync.py    # 同步 packages-index 仓库
│   ├── toml_parser.py  # 解析 TOML 配置文件
│   └── url_check.py    # URL 可达性检查 + 数据库操作
├── api/                # FastAPI 接口层
│   ├── routes.py       # 接口路由定义
│   └── schemas.py      # Pydantic 数据模型（请求/响应）
├── utils/              # 工具函数
│   └── logger.py       # 日志配置
├── data/               # 数据存储（自动生成）
│   ├── packages-index/ # 同步的仓库副本
│   ├── results.db      # SQLite 结果数据库
│   └── logs/           # 日志文件
└── venv/               # 虚拟环境（git 忽略）
```
