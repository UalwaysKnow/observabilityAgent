"""进程级配置；创建应用时加载，导入模块时不读取环境。"""

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="OBS_AGENT_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(default="observabilityAgent", min_length=1)
    environment: Literal["development", "test", "production"] = "development"
