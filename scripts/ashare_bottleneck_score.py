#!/usr/bin/env python
"""为 A 股产业链卡点候选对象打分。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


POSITIVE_WEIGHTS = {
    "demand_pressure": 12,
    "scarce_layer_control": 18,
    "supplier_concentration": 10,
    "qualification_barrier": 10,
    "capacity_expansion_difficulty": 10,
    "official_evidence": 14,
    "financial_confirmation": 10,
    "timing_visibility": 8,
    "market_misclassification": 8,
}

NEGATIVE_WEIGHTS = {
    "valuation_crowding": 8,
    "financing_pressure": 8,
    "accounting_quality": 8,
    "governance_or_related_party": 7,
    "liquidity_or_pledge": 6,
    "concept_hype": 8,
    "substitution_risk": 8,
    "cycle_or_policy_risk": 7,
}

POSITIVE_LABELS = {
    "demand_pressure": "需求压力",
    "scarce_layer_control": "稀缺环节控制力",
    "supplier_concentration": "供应商集中度",
    "qualification_barrier": "认证壁垒",
    "capacity_expansion_difficulty": "扩产难度",
    "official_evidence": "官方证据强度",
    "financial_confirmation": "财务验证",
    "timing_visibility": "时间窗口清晰度",
    "market_misclassification": "市场分类偏差",
}

NEGATIVE_LABELS = {
    "valuation_crowding": "估值拥挤",
    "financing_pressure": "融资压力",
    "accounting_quality": "会计质量风险",
    "governance_or_related_party": "治理或关联交易风险",
    "liquidity_or_pledge": "流动性或质押风险",
    "concept_hype": "题材炒作风险",
    "substitution_risk": "替代风险",
    "cycle_or_policy_risk": "周期或政策风险",
}

TEMPLATE = {
    "symbol": "600519",
    "company": "示例公司",
    "theme": "AI 半导体",
    "scarce_layer": "先进封装材料",
    "positive": {key: 0 for key in POSITIVE_WEIGHTS},
    "negative": {key: 0 for key in NEGATIVE_WEIGHTS},
    "evidence": [
        {
            "claim": "证据要点",
            "source_type": "公告/财报/新闻/研报/资金流/题材",
            "source": "来源或 URL",
            "date": "YYYY-MM-DD",
            "strength": "强/中/弱",
        }
    ],
    "missing_checks": ["还需要验证的事实"],
    "disconfirming_facts": ["什么事实会让排序下调"],
}


def rating(value: Any, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise SystemExit(f"{label} 必须是 0 到 5 之间的数字")
    if number < 0 or number > 5:
        raise SystemExit(f"{label} 必须在 0 到 5 之间")
    return number


def read_json(path: str) -> dict[str, Any]:
    if path == "-":
        raw = sys.stdin.read()
    else:
        data = Path(path).read_bytes()
        for encoding in ("utf-8-sig", "utf-16"):
            try:
                raw = data.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            raise SystemExit("无法按 UTF-8 或 UTF-16 读取输入文件")
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"JSON 无效：{exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit("输入必须是 JSON 对象")
    return value


def score(data: dict[str, Any]) -> dict[str, Any]:
    positive = data.get("positive", {})
    negative = data.get("negative", {})
    if not isinstance(positive, dict) or not isinstance(negative, dict):
        raise SystemExit("positive 和 negative 必须是对象")

    positive_points = {}
    positive_total = 0.0
    for key, weight in POSITIVE_WEIGHTS.items():
        r = rating(positive.get(key, 0), f"positive.{key}")
        points = r / 5 * weight
        positive_points[key] = {"rating": r, "weight": weight, "points": round(points, 2)}
        positive_total += points

    negative_points = {}
    negative_total = 0.0
    for key, weight in NEGATIVE_WEIGHTS.items():
        r = rating(negative.get(key, 0), f"negative.{key}")
        points = r / 5 * weight
        negative_points[key] = {"rating": r, "weight": weight, "points": round(points, 2)}
        negative_total += points

    final = max(0.0, min(100.0, positive_total - negative_total))
    if final >= 78:
        label = "优先深挖"
    elif final >= 62:
        label = "进入重点跟踪"
    elif final >= 45:
        label = "线索保留"
    else:
        label = "暂不靠前"

    return {
        "symbol": data.get("symbol", ""),
        "company": data.get("company", ""),
        "theme": data.get("theme", ""),
        "scarce_layer": data.get("scarce_layer", ""),
        "positive_total": round(positive_total, 2),
        "negative_total": round(negative_total, 2),
        "final_score": round(final, 2),
        "label": label,
        "positive_details": positive_points,
        "negative_details": negative_points,
        "evidence": data.get("evidence", []),
        "missing_checks": data.get("missing_checks", []),
        "disconfirming_facts": data.get("disconfirming_facts", []),
    }


def to_markdown(result: dict[str, Any]) -> str:
    title = f"{result.get('symbol') or '未知代码'} {result.get('company') or ''}".strip()
    lines = [
        f"# A 股卡点评分：{title}",
        "",
        f"主题：{result.get('theme', '')}",
        f"稀缺环节：{result.get('scarce_layer', '')}",
        f"得分：**{result['final_score']} / 100**",
        f"结论：**{result['label']}**",
        f"正向分：{result['positive_total']}",
        f"风险扣分：{result['negative_total']}",
        "",
        "## 正向因子",
        "| 因子 | 评分 | 权重 | 得分 |",
        "| --- | ---: | ---: | ---: |",
    ]
    for key, item in result["positive_details"].items():
        lines.append(f"| {POSITIVE_LABELS.get(key, key)} | {item['rating']} | {item['weight']} | {item['points']} |")
    lines.extend(["", "## 风险扣分", "| 风险 | 评分 | 权重 | 扣分 |", "| --- | ---: | ---: | ---: |"])
    for key, item in result["negative_details"].items():
        lines.append(f"| {NEGATIVE_LABELS.get(key, key)} | {item['rating']} | {item['weight']} | {item['points']} |")

    evidence = result.get("evidence") or []
    if evidence:
        lines.extend(["", "## 证据"])
        for item in evidence:
            if isinstance(item, dict):
                bits = [str(item.get("strength", "")).strip(), str(item.get("claim", "")).strip()]
                source = str(item.get("source", "")).strip()
                date = str(item.get("date", "")).strip()
                lines.append(f"- [{' / '.join(bit for bit in bits if bit)}] {source} {date}".rstrip())

    for heading, key in [("缺失检查", "missing_checks"), ("证伪事实", "disconfirming_facts")]:
        values = [str(v).strip() for v in result.get(key, []) if str(v).strip()]
        if values:
            lines.extend(["", f"## {heading}"])
            lines.extend(f"- {value}" for value in values)

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, add_help=False)
    parser._positionals.title = "位置参数"
    parser._optionals.title = "选项"
    parser.add_argument("-h", "--help", action="help", help="显示帮助信息并退出")
    parser.add_argument("input", nargs="?", help="JSON 文件，或用 '-' 从标准输入读取")
    parser.add_argument("--template", action="store_true", help="打印 JSON 模板")
    parser.add_argument("--format", choices=["json", "md", "both"], default="json")
    args = parser.parse_args()

    if args.template:
        print(json.dumps(TEMPLATE, ensure_ascii=False, indent=2))
        return 0
    if not args.input:
        parser.error("除非使用 --template，否则必须提供 input")

    result = score(read_json(args.input))
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "md":
        print(to_markdown(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("\n---\n")
        print(to_markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
