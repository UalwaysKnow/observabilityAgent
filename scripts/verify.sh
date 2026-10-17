#!/bin/bash
# 仅验证当前脚本所在工作区，不自动格式化、提交或调用模型。
set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
    echo "uv 未找到：请安装 uv 0.12.23，并将其加入 PATH。" >&2
    exit 127
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd "$script_dir/.." && pwd)"
cd "$project_root"
echo "验证工作区：$project_root"

uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy
uv run --locked pytest

# 仅清理本脚本创建的临时目录；不触碰工作区中的 dist 或用户文件。
check_dir="$(mktemp -d "${TMPDIR:-/tmp}/observability-agent-verify.XXXXXX")"
trap 'rm -rf -- "$check_dir"' EXIT

uv build --out-dir "$check_dir/dist"
uv export --locked --no-dev --no-emit-project --format requirements-txt \
    --output-file "$check_dir/runtime-requirements.txt" >/dev/null
uv venv --python "$project_root/.venv/bin/python" "$check_dir/venv"
uv pip install --python "$check_dir/venv/bin/python" --no-deps \
    --requirement "$check_dir/runtime-requirements.txt"

wheels=("$check_dir"/dist/*.whl)
if [[ ${#wheels[@]} -ne 1 || ! -f "${wheels[0]}" ]]; then
    echo "分发包检查失败：预期恰好生成一个 wheel。" >&2
    exit 1
fi
uv pip install --python "$check_dir/venv/bin/python" --no-deps "${wheels[0]}"
uv pip check --python "$check_dir/venv/bin/python"

# 切出源码目录并移除 PYTHONPATH，证明导入的是刚安装的 wheel。
cd "$check_dir"
env -u PYTHONPATH "$check_dir/venv/bin/python" -I - <<'PY'
import sysconfig
from pathlib import Path

import observability_agent
from observability_agent.api.app import create_app

package_path = Path(observability_agent.__file__).resolve()
site_packages = Path(sysconfig.get_paths()["purelib"]).resolve()
if not package_path.is_relative_to(site_packages):
    raise SystemExit(f"导入来源不是隔离环境安装包：{package_path}")
app = create_app()
if not any(getattr(route, "path", None) == "/healthz" for route in app.routes):
    raise SystemExit("安装后的应用缺少 /healthz")
print(f"wheel 安装及应用创建检查通过：{package_path}")
PY

echo "统一验证通过。工厂创建检查不代表 lifespan、真实服务进程或外部依赖已验证。"
