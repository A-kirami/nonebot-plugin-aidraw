from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    ai_draw_api: str = "http://91.217.139.190:5010"
    ai_draw_token: str = ""
    ai_draw_cooldown: int = 60
    ai_draw_daily: int = 30
    ai_draw_timeout: int = 60
    ai_draw_revoke: int = 0


plugin_config = Config.parse_obj(get_driver().config)

api_url = plugin_config.ai_draw_api
token = plugin_config.ai_draw_token
cooldown_time = plugin_config.ai_draw_cooldown
daily_times = plugin_config.ai_draw_daily
timeout = plugin_config.ai_draw_timeout
revoke_time = plugin_config.ai_draw_revoke
