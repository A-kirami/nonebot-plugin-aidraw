from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    ai_draw_api: str = "http://91.217.139.190:5010"
    ai_draw_token: str = ""
    ai_draw_cooldown: int = 60
    ai_draw_timeout: int = 60
