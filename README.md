<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-aidraw

_✨ 使用人工智能来一起画画吧! ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/A-kirami/nonebot-plugin-aidraw.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-aidraw">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-aidraw.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>


## 📖 介绍

使用第三方 API 的 NovelAI 绘图插件

## 💿 安装

<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-aidraw

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-aidraw
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-aidraw
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-aidraw
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-aidraw
</details>

打开 nonebot2 项目的 `bot.py` 文件, 在其中写入

    nonebot.load_plugin('nonebot_plugin_aidraw')

</details>


## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 |  说明 |
|:-----:|:----:|:----:|:----:|
| AI_DRAW_API | 否 | [API](https://lulu.uedbq.xyz)| 第三方 API 的地址 |
| AI_DRAW_TOKEN | 是 | 空 | 第三方 API 的 token, [点击这里获取](https://lulu.uedbq.xyz/token) |
| AI_DRAW_COOLDOWN | 否 | 60 | 使用后的冷却时间, 单位: 秒 |
| AI_DRAW_DAILY | 否 | 30 | 每日使用次数, 单位: 次 |
| AI_DRAW_TIMEOUT | 否 | 60 | 请求 API 的超时时间, 单位: 秒 |
| AI_DRAW_REVOKE | 否 | 0 |图片的撤回时间, 默认不撤回, 单位: 秒 |
| AI_DRAW_MESSAGE | 否 | mix | 消息发送方式<br>可选 mix(图文混合)、part(图文分离)、image(仅图片) |
| AI_DRAW_RANK | 否 | 10 | 标签统计排行的最大显示数量, 设置为0表示显示全部, 单位: 位 |
| AI_DRAW_DATA | 否 | 自身目录 | 插件保存数据文件夹的路径 |
| AI_DRAW_TEXT | 否 | \n图像种子: {seed}\n提示标签: {tags} | 文本消息模板, 支持参数有: <br>tags(标签), steps(迭代步数), seed(图像种子), strength(强度), scale(自由度), ntags(负面标签), 参数需以{}包裹 |
| AI_DRAW_DATABASE | 否 | True | 是否使用数据库, 如果为 False, 则不启用数据库, 标签统计功能将无法使用 |
## 🎉 使用
### 指令表
| 指令 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|
| 绘画/画画/画图/作图/绘图/约稿 |  否 | 群聊/私聊 | 使用描述性文本生成图画, 可用参数见[文本生成参数](#文本生成参数), 管理参数见[绘图管理参数](#绘图管理参数) |
| 以图绘图/以图生图/以图制图 | 否 | 群聊/私聊 | 在基准图像上使用描述性文本生成图画, 支持回复图片消息使用,<br>可用参数见[图像生成参数](#图像生成参数) |
| 个人标签排行/我的标签排行 | 否 | 群聊/私聊 | 查看我的所有使用过的标签的排行 |
| 群标签排行/本群标签排行 | 否 | 群聊 | 查看本期所有使用过的标签的排行 |

使用示例：

    /绘图 描述文本 -p l --scale 12

**注意**

默认情况下, 您应该在指令前加上命令前缀, 通常是 /

### 文本生成参数
| 参数名 | 简写 | 全写 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| shape |  -p | --shape | Portrait | 图像的形状, 可选 Portrait(纵向)、Landscape(横向)、Square(方形)<br>支持缩写为 p、l、s |
| scale | -c | --scale | 11 | 指示 AI 对提示的遵守程度，较大的值可以帮助 AI 更接近文本提示的整体意图 |
| seed | -s | --seed | 随机 | 随机种子。在其他条件不变的情况下，相同的种子代表生成相同的图 |
| steps | -t | --steps | 28  | 定义 AI 从最初创建时应优化的迭代次数 |
| ntags | -n | --ntags | 默认自带 | 不需要的内容，可以列出希望 AI 避免的任何内容 |

### 图像生成参数
| 参数名 | 简写 | 全写 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| strength |  -e | --strength | 0.6 | 允许 AI 改变图像的构成, 降低该值会产生更接近原始图像的效果 |

### 绘图管理参数

| 参数名  | 说明 |
|:-----:|:----:|
| 查看白名单 | 查看白名单模式下允许的群组 |
| 查看黑名单 | 查看黑名单模式下禁止的群组 |
| 添加白名单 + 群号 | 将群组添加到白名单中, 群号以逗号分隔 |
| 添加黑名单 + 群号 | 将群组添加到黑名单中, 群号以逗号分隔 |
| 删除白名单 + 群号 | 将群组从白名单中移除, 群号以逗号分隔 |
| 删除黑名单 + 群号 | 将群组从黑名单中移除, 群号以逗号分隔 |
| 切换白名单 | 切换到白名单模式, 只有白名单中的群组才允许使用 |
| 切换黑名单 | 切换到黑名单模式, 只有黑名单中的群组才禁止使用 |
| 添加屏蔽词 + 屏蔽内容 | 添加到屏蔽词过滤器中, 屏蔽词以逗号分隔 |
| 删除屏蔽词 + 屏蔽内容 | 从屏蔽词过滤器中删除, 屏蔽词以逗号分隔 |
| 查看屏蔽词 | 查看当前的屏蔽词 |

使用示例：

    /绘图添加黑名单 123456