# P119_Answers_to_Interview_Assessment_Questions
中科院软件所面试题目解答
## Question 1
>阅读 ruyi 包管理器[文档](https://ruyisdk.org/docs/intro/) 安装并使用 ruyi 包管理器；安装 ruyisdk-eclipse-plugins 的[最新 pre-release](https://github.com/ruyisdk/ruyisdk-eclipse-plugins/releases/tag/continuous)，阅读其[旧版>文档](https://ruyisdk.org/docs/IDE/)，从用户视角出发寻找功能更新和功能缺陷。将测试报告以 md 文档辅以图片的形式提交到个人 GitHub 账号下的公开仓库中。


**测试环境**
*   **操作系统:** `Ubuntu 22.04 LTS`
*   **Eclipse版本:** `Eclipse 2025-12`
*   **ruyi 包管理器版本:** `0.44.0`
*   **插件版本:** `ruyisdk-eclipse-plugins 0.1.0`

### 功能更新

**基础功能模块**

|  PR 编号 | 作者  | 核心新增功能  |
|  ----  | ----  | ---- |
| #44  | @NanamiKite	 |  添加卸载软件包功能  |
| #46  | @NanamiKite	  |  projectcreator 插件（项目创建器）  |

**CI/CD 与构建模块**

|  PR 编号 | 作者  | 核心新增功能  |
|  ----  | ----  | ---- |
| #67  | @exceed-zk	 |  新增 GitHub Actions CI/CD 流程，实现 P2 仓库自动部署|
| #68  | @exceed-zk	  |  CI 流程启用代码格式化、checkstyle 配置 |

**视图与交互模块**

|  PR 编号 | 作者  | 核心新增功能  |
|  ----  | ----  | ---- |
| #70  | @pzhlkj6612	 |  1. 新增新闻视图；2. 新增 venv 视图及向导页面；3. 补充相关测试用例添加卸载软件包功能  |
| #73  | @pzhlkj6612	 |  1. 新闻视图自动加载新闻；2. 代码重构优化  |
| #76  | @pzhlkj6612	 |  1. 清理 Activator 类；2. 新闻 /venv 模块添加日志输出  |
| #77  | @pzhlkj6612	 |  1. venv 可应用到目标项目；2. 目标配置纳入 TM 组件  |
| #78  | @pzhlkj6612	 | 1. 新闻列表降序排列；2. 清理冗余代码 |
| #79  | @pzhlkj6612	 |  新增 venv / 新闻模块菜单入口 |

**版本与工程优化模块**

|  PR 编号 | 作者  | 核心新增功能  |
|  ----  | ----  | ---- |
| #74  | @pzhlkj6612	 |  1. CI 自动生成更新日志；2. venv 模块添加封装 TODO |
| #75  | @pzhlkj6612	 |  1. Tycho 配置目标文件；2. 固定目标平台；3. 测试模块无 POM 配置；4. 自动处理构建顺序  |
| #80  | @pzhlkj6612	 |  1. 版本升级至 0.1.0；2. 清理注释、优化变量命名  |
| #81  | @pzhlkj6612	 |  改用 Java 11 String::isBlank() 方法  |
| #91  | @pzhlkj6612	 | 优化 CI 发布流程|


### 功能缺陷

#### 问题 1：Esclipse中缺少相关选项

**1. 问题类型：** 易用性问题 

**2. 问题描述**
> 在创建C/C++project时，在esclipse中没有相关选项，而在RuyiSedk-IDE中可以直接创建C/C++project

**3. 复现步骤**
1.  启动Eclipse，点击菜单 `File -> New `
2.  在项目类型中没有C/C++项目
3.  启动RuyiSDK-IDE，点击菜单 `File -> New `
4.  在项目类型中有C/C++项目

**4. 预期结果**
> 在Eclipse中应该也出现相关选项

**5. 实际结果**
> 在Eclipse中没有C/C++project选项

**6. 严重程度** 
- **主要** (重要功能受影响，但存在变通方法)

**7. 附件**
*   **截图:** `issue_1_Eclipse.png` 
   
   ![问题1截图](./assets/issue_1_Eclipse.png)

*   **截图:** `issue_2_RuyiSDK-IDE.png` 
   
   ![问题1截图](./assets/issue_1_RuyiSDK-IDE.png)


#### 问题 2: Eclipse与RuyiSDK-IDE的Board-Model直接选项比较少并且在缺少相关Board-Model时，不能引导直接安装Board-Model

**1. 问题类型：** 易用性问题 

**2. 问题描述**
> 在选择创建新项目时，会要求用户选择`Board-Model`,但是默认只有`milkv-duo`与`default`两个选项,可供用户直接选的比较少

**3. 复现步骤**
1.  启动Eclipse或RuyiSDK-IDE，点击菜单 `File -> New -> RuyiSDK Project`
2.  `choose Board-Model`对话框，点击`Board-Model`下拉框

**4. 预期结果**
出现相关Board-Model选项，并且提供Board-Model的下载引导

**5. 实际结果**
只有`milkv-duo`与`default`两个选项，并且不提供相关`Board-Model`下载引导

**6. 严重程度** 
- **一般** (次要功能问题，对主要流程影响不大)

**7. 附件**
*   **截图:** `issue_2_Eclipse_choose-Board-Model对话框.png` 
   
![问题2截图](./assets/issue_2_Eclipse_choose-Board-Model对话框.png)

*   **截图:** `issue_2_RuyiSDK-IDE_choose-Board-Model对话框.png`

   ![问题2截图](./assets/issue_2_RuyiSDK-IDE_choose-Board-Model对话框.png)

#### 问题 3: [简短明确的标题，如“安装向导在特定步骤卡顿”]

**1. 问题类型：** 功能缺陷 

**2. 问题描述**
> 在使用Eclipse进行创建RuyiSDK项目是，创建结束只出现虚拟环境，而没有初始化项目，在RuyiSDK-IDE中可以自动创建初始化项目

**3. 复现步骤**
列出能让其他测试人员稳定复现该问题的步骤。
1.  启动Eclipse，点击菜单 `File -> New -> RuyiSDK Project`
2.  选择`Board-Model`，创建项目之后页面没有动静
3.  启动RuyiSDK-IDE，点击菜单 `File -> New -> RuyiSDK Project`
4.  选择`Board-Model`，创建项目之后会自动创建C语言初始项目

**4. 预期结果**
出现初始化程序

**5. 实际结果**
在Eclipse中没有初始化程序，在RuyiSDK-IDE有初始化程序

**6. 严重程度** 
- **主要** (重要功能受影响，但存在变通方法)

**7. 附件 (如有)**

*   **截图:** `issue_3_Eclipse无初始化程序.png` 

![问题3截图](assets/issue_3_Eclipse无初始化程序.png)

*   **截图:** `issue_3_RuyiSDK-IDE有初始化程序.png` 

![问题3截图](assets/issue_3_RuyiSDK-IDE有初始化程序.png)

