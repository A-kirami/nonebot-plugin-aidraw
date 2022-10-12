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

| 配置项 | 必填 | 说明 |
|:-----:|:----:|:----:|
| AI_DRAW_API | 否 | 第三方 API 的地址 |
| AI_DRAW_TOKEN | 是 |  第三方 API 的 token, [点击这里获取](http://91.217.139.190:5010/token) |
| AI_DRAW_COOLDOWN | 否 |  插件的冷却时间, 默认60秒 |

## 🎉 使用
### 指令表
| 指令 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|
| 绘画/画画/画图/作图/绘图/约稿 |  否 | 群聊/私聊 | 使用描述性文本生成图画, 可用参数见[附表](###附表) |
| 以图绘图/以图生图/以图制图 | 否 | 群聊/私聊 | 在基准图像上使用描述性文本生成图画, 支持回复图片消息使用 |

### 附表
| 参数名 | 简写 | 全写 | 说明 |
|:-----:|:----:|:----:|:----:|
| shape |  -p | --shape | 可选 Portrait(纵向)、Landscape(横向)、Square(方形)，默认图像为纵向, 支持缩写为 p、l、s |
| scale | -c | --scale | 指示 AI 对提示的遵守程度，较大的值可以帮助 AI 更接近文本提示的整体意图 |
| seed | -s | --seed | 随机种子。在其他条件不变的情况下，相同的种子代表生成相同的图 |
| steps | -t | --steps | 定义 AI 从最初创建提示时应优化的迭代次数 |
| ntags | -n | --ntags | 不需要的内容，可以列出希望 AI 避免的任何内容 |

使用示例：

    绘图 描述文本 -p l --scale 12