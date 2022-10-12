import base64
from argparse import Namespace
from io import BytesIO
from urllib.parse import urljoin

import httpx
from nonebot import get_driver, on_command, on_shell_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment
from nonebot.adapters.onebot.v11.helpers import (
    Cooldown,
    CooldownIsolateLevel,
    extract_image_urls,
)
from nonebot.exception import ParserExit
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import Arg, CommandArg, ShellCommandArgs
from nonebot.rule import ArgumentParser
from nonebot.typing import T_State
from PIL import Image

from .config import Config

try:
    import ujson as json
except ImportError:
    import json


plugin_config = Config.parse_obj(get_driver().config)

api_url = plugin_config.ai_draw_api
token = plugin_config.ai_draw_token
cooldown_time = plugin_config.ai_draw_cooldown

cooldown = Cooldown(
    cooldown=cooldown_time, prompt="AI绘图冷却中……", isolate_level=CooldownIsolateLevel.USER
)

novel_parser = ArgumentParser()
novel_parser.add_argument("tags", default="", nargs="*", help="描述标签")
novel_parser.add_argument("-p", "--shape", default="", help="画布形状")
novel_parser.add_argument("-c", "--scale", type=float, help="规模")
novel_parser.add_argument("-s", "--seed", type=int, help="种子")
novel_parser.add_argument("-t", "--steps", type=int, help="步骤")
novel_parser.add_argument("-n", "--ntags", default="", nargs="*", help="负面标签")


async def get_tags(state: T_State, tags: str = Arg()):
    state["tags"] = tags


ai_novel = on_shell_command(
    "绘画", aliases={"画画", "画图", "作图", "绘图", "约稿"}, parser=novel_parser
)


@ai_novel.handle()
async def _(args: ParserExit = ShellCommandArgs()):
    await ai_novel.finish(args.message)


@ai_novel.handle([cooldown])
async def novel_draw(
    matcher: Matcher,
    state: T_State,
    args: Namespace = ShellCommandArgs(),
):
    shape = args.shape.lower()
    shape_list = ["landscape", "portrait", "square"]

    for s in shape_list:
        if s.startswith(shape):
            shape = s

    if shape not in shape_list:
        await ai_novel.finish("shape 的输入值不正确, 应为 landscape, portrait 或 square")

    args.shape = shape.capitalize()
    args.tags = " ".join(args.tags)
    args.ntags = " ".join(args.ntags)
    state["args"] = args
    if args.tags:
        matcher.set_arg("tags", Message(args.tags))


ai_novel.got("tags", prompt="请输入描述性的单词或短句")(get_tags)


@ai_novel.handle()
async def novel_draw_handle(state: T_State):
    await ai_novel.send("正在努力绘图中……")

    args = state["args"]
    args.tags = state["tags"]

    async with httpx.AsyncClient() as client:
        res = await client.get(
            urljoin(api_url, "got_image"),
            params={"token": token, **{k: v for k, v in vars(args).items() if v}},
            timeout=60,
        )
        if res.is_error:
            logger.error(f"{res.url} {res.status_code}")
            await ai_novel.finish("出现意外的网络错误")
        info = Image.open(BytesIO(res.content)).info
        if not info:
            await ai_novel.finish("token失效, 请更换token后重试")
        msg = (
            f"\n图像种子: {json.loads(info['Comment'])['seed']}\n"
            + f"提示标签: {info['Description']}\n"
            + MessageSegment.image(res.content)
        )
        await ai_novel.send(msg, at_sender=True)


ai_image = on_command("以图绘图", aliases={"以图生图", "以图制图"})


@ai_image.handle([cooldown])
async def image_draw(
    event: MessageEvent, matcher: Matcher, args: Message = CommandArg()
):
    message = reply.message if (reply := event.reply) else event.message

    if imgs := message["image"]:
        matcher.set_arg("imgs", Message(imgs))

    if tags := args.extract_plain_text().strip():
        matcher.set_arg("tags", Message(tags))


@ai_image.got("imgs", prompt="请发送基准图片")
async def get_image(state: T_State, imgs: Message = Arg()):
    urls = extract_image_urls(imgs)
    if not urls:
        await ai_image.reject("没有找到图片, 请重新发送")
    async with httpx.AsyncClient() as client:
        res = await client.get(urls[0])
        if res.is_error:
            await ai_image.finish("获取图片失败, 请更换图片重试")
        base_img = Image.open(BytesIO(res.content)).convert("RGB")

        if base_img.width > base_img.height:
            state["shape"] = "Landscape"
        elif base_img.width < base_img.height:
            state["shape"] = "Portrait"
        else:
            state["shape"] = "Square"

        base_img.thumbnail((768, 768), resample=Image.Resampling.LANCZOS)
        state["image_data"] = BytesIO()
        base_img.save(state["image_data"], format="JPEG")


ai_image.got("tags", prompt="请输入描述性的单词或短句")(get_tags)


@ai_image.handle()
async def image_draw_handle(state: T_State):
    await ai_novel.send("正在努力绘图中……")

    async with httpx.AsyncClient() as client:
        res = await client.post(
            urljoin(api_url, "got_image2image"),
            data=base64.b64encode(state["image_data"].getvalue()),  # type: ignore
            params={"token": token, "tags": state["tags"], "shape": state["shape"]},
            timeout=60,
        )
        if res.is_error:
            logger.error(f"{res.url} {res.status_code}")
            await ai_novel.finish("出现意外的网络错误")
        msg = "\n" + MessageSegment.image(res.content)
        await ai_image.send(msg, at_sender=True)
