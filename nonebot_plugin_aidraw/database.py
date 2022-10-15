from pathlib import Path
from typing import Any, Dict, Literal, Set

from pydantic import BaseModel, Field, root_validator

try:
    import ujson as json
except ModuleNotFoundError:
    import json


class Setting(BaseModel):
    type: Literal["blacklist", "whitelist"] = "blacklist"
    """名单类型"""
    blacklist: Set[int] = Field(default_factory=set)
    """黑名单"""
    whitelist: Set[int] = Field(default_factory=set)
    """白名单"""
    shield: Set[str] = Field(default_factory=set)
    """过滤词"""

    __file_path: Path = Path(__file__).parent / "setting.json"

    @property
    def file_path(self) -> Path:
        return self.__class__.__file_path

    @root_validator(pre=True)
    def init(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if cls.__file_path.is_file():
            return json.loads(cls.__file_path.read_text("utf-8"))
        return values

    def save(self) -> None:
        self.file_path.write_text(self.json(), encoding="utf-8")


setting = Setting()
