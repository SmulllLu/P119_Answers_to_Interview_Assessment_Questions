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

### 功能缺陷

#### 问题 1: 旧版IDE中，无法通过`Install New Software`安装`RuyiSDK Eclipse Plugins`

**1. 问题类型** : 功能缺陷 

**3. 问题描述**
>在`Add Repository`选择了`ruyisdk-eclipse-plugins.site.zip`之后，点击`Add`，显示`Could not find  jar:file:/home/smulll/env/ruyisdk-0.0.3-linux.gtk.x86_64/ruyisdk/plugins/ruyisdk-eclipse-plugins/sites.zip!/ `

**4. 复现步骤**
列出能让其他测试人员稳定复现该问题的步骤。
1.  启动Ruyi IDE，点击菜单 `File -> Help -> Install New Software`
2.  点击`Add Repository`,`name`处填写`RuyiSDK Plugins (Local)` `Location`处选择`ruyisdk-eclipse-plugins/sites.zip`
3.  点击`Add`

**5. 预期结果**
可以选择 RuyiSDK IDE 并安装

**6. 实际结果**
显示`Could not find  jar:file:/home/smulll/env/ruyisdk-0.0.3-linux.gtk.x86_64/ruyisdk/plugins/ruyisdk-eclipse-plugins/sites.zip!/` 

**7. 严重程度** : **主要** (重要功能受影响，但存在变通方法)

**8. 附件**
![](./assets/issue_1_could_not_find.png)
#### 问题 2: [简短明确的标题，如“安装向导在特定步骤卡顿”]

**1. 问题类型** (单选)
- [ ] 功能缺陷 (功能无法工作或行为错误)
- [ ] 易用性问题 (界面不清、操作繁琐)
- [ ] 稳定性缺陷 (崩溃、无响应)
- [ ] 兼容性问题 (与特定系统/软件不兼容)
- [ ] 文档缺陷 (说明缺失或错误)

**3. 问题描述**
清晰描述观察到的错误现象或不良体验。避免使用模糊词汇，力求具体。
> 例如：在使用“新建RISC-V项目”向导时，当在第二步选择“Nuclei SDK”作为开发板支持包后，点击“下一步”按钮无任何反应，界面卡死，只能强制关闭窗口。

**4. 复现步骤**
列出能让其他测试人员稳定复现该问题的步骤。
1.  第一步操作 (如：启动Eclipse，点击菜单 `File -> New -> RuyiSDK Project`)
2.  第二步操作
3.  ... (直到问题出现)
> *提示：步骤应详尽且可操作。*

**5. 预期结果**
描述按照设计或常识，正确操作后应该发生什么。
> 例如：点击“下一步”后，应正常进入向导的第三步，允许用户配置项目细节。

**6. 实际结果**
描述实际发生了什么，与预期不符的地方。
> 例如：点击“下一步”后，界面完全卡住，鼠标指针变为等待状态，持续超过2分钟无变化。Eclipse主界面仍可响应，但无法进行其他项目操作。

**7. 严重程度** (单选)
- [ ] **严重** (导致核心功能完全失效、数据丢失、系统崩溃)
- [ ] **主要** (重要功能受影响，但存在变通方法)
- [ ] **一般** (次要功能问题，对主要流程影响不大)
- [ ] **轻微** (界面错别字、布局轻微错位等)

**8. 附件 (如有)**
请附上相关截图、错误日志或屏幕录制文件，并将其上传至本次报告所在的GitHub仓库的 `assets/` 或 `screenshots/` 目录下。
*   **截图/日志文件名:** `issue_[编号]_[描述].png/log` (例如：`issue_01_wizard_stuck.png`)
*   **图片插入方式：** `![问题1截图](assets/issue_01_wizard_stuck.png)`



#### 问题 [编号]: [简短明确的标题，如“安装向导在特定步骤卡顿”]

**1. 问题类型** (单选)
- [ ] 功能缺陷 (功能无法工作或行为错误)
- [ ] 易用性问题 (界面不清、操作繁琐)
- [ ] 稳定性缺陷 (崩溃、无响应)
- [ ] 兼容性问题 (与特定系统/软件不兼容)
- [ ] 文档缺陷 (说明缺失或错误)

**3. 问题描述**
清晰描述观察到的错误现象或不良体验。避免使用模糊词汇，力求具体。
> 例如：在使用“新建RISC-V项目”向导时，当在第二步选择“Nuclei SDK”作为开发板支持包后，点击“下一步”按钮无任何反应，界面卡死，只能强制关闭窗口。

**4. 复现步骤**
列出能让其他测试人员稳定复现该问题的步骤。
1.  第一步操作 (如：启动Eclipse，点击菜单 `File -> New -> RuyiSDK Project`)
2.  第二步操作
3.  ... (直到问题出现)
> *提示：步骤应详尽且可操作。*

**5. 预期结果**
描述按照设计或常识，正确操作后应该发生什么。
> 例如：点击“下一步”后，应正常进入向导的第三步，允许用户配置项目细节。

**6. 实际结果**
描述实际发生了什么，与预期不符的地方。
> 例如：点击“下一步”后，界面完全卡住，鼠标指针变为等待状态，持续超过2分钟无变化。Eclipse主界面仍可响应，但无法进行其他项目操作。

**7. 严重程度** (单选)
- [ ] **严重** (导致核心功能完全失效、数据丢失、系统崩溃)
- [ ] **主要** (重要功能受影响，但存在变通方法)
- [ ] **一般** (次要功能问题，对主要流程影响不大)
- [ ] **轻微** (界面错别字、布局轻微错位等)

**8. 附件 (如有)**
请附上相关截图、错误日志或屏幕录制文件，并将其上传至本次报告所在的GitHub仓库的 `assets/` 或 `screenshots/` 目录下。
*   **截图/日志文件名:** `issue_[编号]_[描述].png/log` (例如：`issue_01_wizard_stuck.png`)
*   **图片插入方式：** `![问题1截图](assets/issue_01_wizard_stuck.png)`
