from argparse import Namespace
from typing import Literal, Set, Union

from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    MessageEvent,
    PrivateMessageEvent,
)
from nonebot.matcher import Matcher
from nonebot.params import ShellCommandArgs
from nonebot.permission import SUPERUSER

from .database import setting

add_word = {"添加", "增加", "设置"}
del_word = {"删除", "移除", "解除"}
see_word = {"查看", "检查"}
change_word = {"切换", "管理"}


async def group_checker(
    bot: Bot, event: Union[GroupMessageEvent, PrivateMessageEvent]
) -> bool:
    if await SUPERUSER(bot, event) or isinstance(event, PrivateMessageEvent):
        return True
    group_list: Set[int] = getattr(setting, setting.type)
    check = event.group_id in group_list
    return check if setting.type == "whitelist" else not check


def handle_namelist(
    action: Literal["add", "del"],
    type_: Literal["blacklist", "whitelist"],
    groups: Set[int],
) -> str:
    group_list: Set[int] = getattr(setting, type_)
    if action == "add":
        group_list.update(groups)
        _mode = "添加"
    elif action == "del":
        group_list.difference_update(groups)
        _mode = "删除"
    setattr(setting, type_, group_list)
    setting.save()
    _type = "黑" if type_ == "blacklist" else "白"
    return f"已{_mode} {len(groups)} 个{_type}名单: {','.join(map(str, groups))}"


async def group_manager(
    bot: Bot,
    event: MessageEvent,
    matcher: Matcher,
    args: Namespace = ShellCommandArgs(),
):
    if not await SUPERUSER(bot, event):
        matcher.skip()

    manage_type, *groups = args.tags
    action, class_, group = manage_type[:2], manage_type[2:5], manage_type[5:]
    type_ = "blacklist" if class_ == "黑名单" else "whitelist"

    if action in add_word:
        action = "add"
    elif action in del_word:
        action = "del"
    elif action in see_word:
        await matcher.finish(
            f"当前{class_}: {','.join(map(str, getattr(setting, type_)))}"
        )
    elif action in change_word:
        setting.type = type_
        setting.save()
        await matcher.finish(f"已切换为 {class_} 模式")
    else:
        matcher.skip()

    groups.insert(0, group)
    groups = " ".join(groups).split(",")

    msg = handle_namelist(
        action, type_, {int(group) for group in groups if group.strip().isdigit()}
    )
    await matcher.finish(msg)
