"""验证干净环境启动、配置优先级与非法配置快速失败。"""

import socket
from pathlib import Path
from typing import Any

import httpx
import pytest
from pydantic import ValidationError

from observability_agent.api.app import create_app


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(autouse=True)
def isolated_environment(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("OBS_AGENT_APP_NAME", raising=False)
    monkeypatch.delenv("OBS_AGENT_ENVIRONMENT", raising=False)


@pytest.mark.anyio
async def test_starts_without_model_credentials_or_external_services(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)

    def disallow_connection(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("启动及存活检查不应建立外部连接")

    monkeypatch.setattr(socket.socket, "connect", disallow_connection)
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_environment_overrides_dotenv(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    (tmp_path / ".env").write_text("OBS_AGENT_APP_NAME=from-file\n", encoding="utf-8")
    monkeypatch.setenv("OBS_AGENT_APP_NAME", "from-environment")

    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        schema = (await client.get("/openapi.json")).json()

    assert schema["info"]["title"] == "from-environment"


def test_invalid_environment_fails_at_startup(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OBS_AGENT_ENVIRONMENT", "typo")

    with pytest.raises(ValidationError, match="environment"):
        create_app()
