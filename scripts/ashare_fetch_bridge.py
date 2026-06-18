#!/usr/bin/env python
"""把 serenity-skill-ashare 的数据请求转发给同级 a-share-intelligence 项目。"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def parse_object(raw: str, label: str) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{label} 必须是 JSON 对象：{exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"{label} 必须是 JSON 对象")
    return value


def parse_calls(raw: str) -> list[dict[str, Any]]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"--calls 必须是 JSON 列表：{exc}") from exc
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise SystemExit("--calls 必须是由对象组成的 JSON 列表")
    return value


def parse_scalar(raw: str) -> Any:
    lowered = raw.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered == "null":
        return None
    try:
        return int(raw)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        return raw


def parse_key_values(items: list[str]) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    for item in items:
        if "=" not in item:
            raise SystemExit(f"--kw 必须使用 key=value 形式；当前值为 {item!r}")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise SystemExit("--kw 的键不能为空")
        parsed[key] = parse_scalar(value.strip())
    return parsed


def default_project() -> Path:
    here = Path(__file__).resolve()
    return here.parents[2] / "a-share-intelligence"


def run_one(project: Path, call: dict[str, Any], retry: int) -> dict[str, Any]:
    script = project / "scripts" / "a_share_fetch.py"
    if not script.exists():
        return {
            "ok": False,
            "error": f"缺少 a-share-intelligence 脚本：{script}",
            "call": call,
        }

    source = str(call.get("source", "")).strip()
    method = str(call.get("method", "")).strip()
    symbol = str(call.get("symbol", "")).strip()
    kwargs = call.get("kwargs", {})
    if not source or not method:
        return {"ok": False, "error": "source 和 method 为必填项", "call": call}
    if not isinstance(kwargs, dict):
        return {"ok": False, "error": "kwargs 必须是对象", "call": call}

    cmd = [
        sys.executable,
        str(script),
        "--source",
        source,
        "--method",
        method,
        "--indent",
        "0",
    ]
    if symbol:
        cmd.extend(["--symbol", symbol])
    if kwargs:
        cmd.extend(["--kwargs", json.dumps(kwargs, ensure_ascii=False)])

    attempts = []
    for index in range(retry + 1):
        proc = subprocess.run(
            cmd,
            cwd=str(project),
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
        )
        raw = proc.stdout.strip()
        parsed: Any
        try:
            parsed = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            parsed = None
        attempt = {
            "attempt": index + 1,
            "returncode": proc.returncode,
            "stdout_json": parsed,
            "stdout_raw": raw if parsed is None else "",
            "stderr": proc.stderr.strip(),
        }
        attempts.append(attempt)
        if proc.returncode == 0:
            return {
                "ok": True,
                "source": source,
                "method": method,
                "symbol": symbol,
                "kwargs": kwargs,
                "attempts": attempts,
                "data": parsed,
            }

    return {
        "ok": False,
        "source": source,
        "method": method,
        "symbol": symbol,
        "kwargs": kwargs,
        "attempts": attempts,
        "error": attempts[-1].get("stderr") or attempts[-1].get("stdout_raw") or "调用失败",
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, add_help=False)
    parser._positionals.title = "位置参数"
    parser._optionals.title = "选项"
    parser.add_argument("-h", "--help", action="help", help="显示帮助信息并退出")
    parser.add_argument("--project", default="", help="a-share-intelligence 项目路径")
    parser.add_argument("--source", default="", help="数据源名称，例如 chain/eastmoney")
    parser.add_argument("--method", default="", help="数据源方法名")
    parser.add_argument("--symbol", default="", help="A 股代码")
    parser.add_argument("--kwargs", default="", help="传给数据源方法的 JSON 对象")
    parser.add_argument("--kw", action="append", default=[], help="key=value 形式的数据源参数，可重复传入")
    parser.add_argument("--calls", default="", help="调用对象组成的 JSON 列表")
    parser.add_argument("--calls-file", default="", help="包含调用对象列表的 UTF-8 JSON 文件")
    parser.add_argument("--retry", type=int, default=1, choices=[0, 1], help="失败调用默认重试一次")
    args = parser.parse_args()

    project = Path(args.project).resolve() if args.project else default_project()
    if args.calls_file:
        calls = parse_calls(Path(args.calls_file).read_text(encoding="utf-8-sig"))
    elif args.calls:
        calls = parse_calls(args.calls)
    else:
        kwargs = parse_object(args.kwargs, "--kwargs")
        kwargs.update(parse_key_values(args.kw))
        calls = [{
            "source": args.source,
            "method": args.method,
            "symbol": args.symbol,
            "kwargs": kwargs,
        }]

    bundle = {
        "ok": True,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "project": str(project),
        "results": [],
    }
    for call in calls:
        result = run_one(project, call, args.retry)
        bundle["results"].append(result)
        if not result.get("ok"):
            bundle["ok"] = False

    print(json.dumps(bundle, ensure_ascii=False, indent=2, default=str))
    return 0 if bundle["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
