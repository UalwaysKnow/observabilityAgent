"""应用工厂；通过 uvicorn 的 --factory 参数启动。"""

from typing import Literal

from fastapi import FastAPI

from observability_agent.config import Settings


def create_app() -> FastAPI:
    settings = Settings()
    app = FastAPI(title=settings.app_name)

    @app.get("/healthz", tags=["health"])
    async def health() -> dict[str, Literal["ok"]]:
        """仅表示 HTTP 进程可响应，不表示模型或数据库已就绪。"""
        return {"status": "ok"}

    return app
