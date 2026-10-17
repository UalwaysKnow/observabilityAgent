"""检查验证入口的工作区定位和失败语义；实际打包由真实脚本执行。"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture
def verify_workspace(tmp_path: Path) -> tuple[Path, dict[str, str], Path]:
    # 带空格的路径同时验证脚本和产物路径的引用是否正确。
    root = tmp_path / "project with spaces"
    scripts = root / "scripts"
    scripts.mkdir(parents=True)
    source = Path(__file__).resolve().parents[1] / "scripts" / "verify.sh"
    shutil.copy2(source, scripts / "verify.sh")
    (root / "src" / "nested").mkdir(parents=True)
    tools = tmp_path / "tools"
    tools.mkdir()
    log = tmp_path / "uv-calls.jsonl"
    uv = tools / "uv"
    uv.write_text(
        f"#!{sys.executable}\n"
        "import json, os, pathlib, sys\n"
        "args = sys.argv[1:]\n"
        "with open(os.environ['VERIFY_UV_LOG'], 'a') as log:\n"
        "    log.write(json.dumps({'cwd': os.getcwd(), 'args': args}) + '\\n')\n"
        "if args == ['run', '--locked', 'ruff', 'check', '.'] "
        "and os.environ.get('VERIFY_FAIL_LINT') == '1':\n"
        "    sys.exit(42)\n"
        "if args[0] == 'build':\n"
        "    output = pathlib.Path(args[args.index('--out-dir') + 1])\n"
        "    output.mkdir(parents=True)\n"
        "    (output / 'example.whl').write_text('stub')\n"
        "if args[0] == 'venv':\n"
        "    python = pathlib.Path(args[-1]) / 'bin' / 'python'\n"
        "    python.parent.mkdir(parents=True)\n"
        "    python.write_text('#!/bin/sh\\nexit 0\\n')\n"
        "    python.chmod(0o755)\n",
        encoding="utf-8",
    )
    uv.chmod(0o755)
    environment = dict(os.environ)
    environment["PATH"] = f"{tools}:/usr/bin:/bin"
    environment["VERIFY_UV_LOG"] = str(log)
    environment.pop("VERIFY_FAIL_LINT", None)
    environment["TMPDIR"] = str(tmp_path)
    return root, environment, log


@pytest.mark.parametrize("start_directory", [".", "src/nested"])
def test_verifies_own_workspace_from_root_or_subdirectory(
    verify_workspace: tuple[Path, dict[str, str], Path], start_directory: str
) -> None:
    root, environment, log = verify_workspace
    result = subprocess.run(
        [str(root / "scripts" / "verify.sh")],
        cwd=root / start_directory,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    calls = [json.loads(line) for line in log.read_text().splitlines()]
    assert len(calls) == 11
    assert all(call["cwd"] == str(root) for call in calls)
    assert calls[0]["args"] == ["sync", "--locked"]
    assert calls[-1]["args"][:2] == ["pip", "check"]
    assert not list(root.parent.glob("observability-agent-verify.*"))


def test_failure_preserves_exit_code_and_stops_later_checks(
    verify_workspace: tuple[Path, dict[str, str], Path],
) -> None:
    root, environment, log = verify_workspace
    environment["VERIFY_FAIL_LINT"] = "1"
    result = subprocess.run(
        [str(root / "scripts" / "verify.sh")],
        cwd=root,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 42
    calls = [json.loads(line) for line in log.read_text().splitlines()]
    assert len(calls) == 2
    assert calls[-1]["args"] == ["run", "--locked", "ruff", "check", "."]


def test_missing_uv_explains_requirement(tmp_path: Path) -> None:
    script = Path(__file__).resolve().parents[1] / "scripts" / "verify.sh"
    environment = dict(os.environ)
    environment["PATH"] = str(tmp_path)
    result = subprocess.run(
        [str(script)], env=environment, capture_output=True, text=True, check=False
    )

    assert result.returncode == 127
    assert "uv 未找到" in result.stderr
