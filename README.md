# P119_Answers_to_Interview_Assessment_Questions
中科院软件所面试题目解答

## Question 1

>阅读 ruyi 包管理器[文档](https://ruyisdk.org/docs/intro/) 安装并使用 ruyi 包管理器；安装 ruyisdk-eclipse-plugins 的[最新 pre-release](https://github.com/ruyisdk/ruyisdk-eclipse-plugins/releases/tag/continuous)，阅读其[旧版>文档](https://ruyisdk.org/docs/IDE/)，从用户视角出发寻找功能更新和功能缺陷。将测试报告以 md 文档辅以图片的形式提交到个人 GitHub 账号下的公开仓库中。



## Question 2
>阅读 ruyi-litester [文档](https://github.com/weilinfox/ruyi-litester/blob/master/README_zh.md)和运行测试时使用的 [Dockerfile](https://github.com/weilinfox/ruyi-litester/blob/master/docker/distros/archlinux.Dockerfile)（此处只给出其中一个的链接），研究和实现在 locale 为 ``zh_CN.UTF-8 UTF-8`` 和 ``en_SG.UTF-8 UTF-8`` 下的测试。


## Question 3

>理解 [ruyi-packaging](https://github.com/ruyisdk/ruyi-packaging/) 项目，这个项目试图实现 [packages-index/board-image](https://github.com/ruyisdk/packages-index/tree/main/manifests/board-image) 的自动更新，使用 ``check`` 命令检查上游更新，使用 ``manifests`` 命令生成指定版本的 toml 配置。其中以 [openbsd-riscv64-live](https://github.com/ruyisdk/packages-index/blob/main/manifests/board-image/openbsd-riscv64-live/7.6.0.toml#L12) 为例，其使用了 ``mirror://`` 格式的 url，其声明见 [config.toml](https://github.com/ruyisdk/packages-index/blob/main/config.toml#L47)，不难发现 ``openbsd`` 声明的 url 中并不是每个 url 都有相关资源可供下载。请实现一个 bot，定期检查这些资源的可用性（url 是否可达），并以 Fast API 的方式提供查询接口。对于 ``mirror://`` 格式 url 的资源，则需要标记其中每个 url 的可用性。将代码提交到个人 GitHub 账号下的公开仓库中。

