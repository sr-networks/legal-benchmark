#!/usr/bin/env python3
"""Regenerate assets/benchmark-comparison.svg from leaderboard.csv.

Reads the three top-ranked LegalGenius harness rows from leaderboard.csv,
then appends the external Libra DeepThinking reference used in README.md.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parent
INPUT = ROOT / "leaderboard.csv"
OUTPUT = ROOT / "assets" / "benchmark-comparison.svg"
CHART_LEGALGENIUS_COUNT = 3
EXTERNAL_REFERENCES = [("Libra (DeepThinking)", 73, "External reference")]

# Short display names for the chart. Fallback: derive from the model id
# by stripping the vendor prefix and tidying up separators.
DISPLAY_NAMES: dict[str, str] = {
    "anthropic/claude-opus-4.7": "Claude Opus 4.7",
    "z-ai/glm-5.1": "GLM-5.1",
    "z-ai/glm-5": "GLM-5",
    "openai/gpt-5.4": "GPT-5.4",
    "qwen/qwen3.5-397b-a17b": "Qwen3.5-397B-A17B",
    "qwen/qwen3.5-122b-a10b": "Qwen3.5-122B-A10B",
    "qwen/qwen3.6-plus": "Qwen3.6 Plus",
    "mistralai/mistral-small-3.2-24b-instruct": "Mistral Small 3.2 24B",
    "mistralai/mistral-large-2512": "Mistral Large 2512",
    "PrimeIntellect/INTELLECT-3": "Intellect-3",
    "NousResearch/Hermes-4-405B": "Hermes-4 405B",
    "NousResearch/Hermes-4-70B": "Hermes-4 70B",
    "zai-org/GLM-5": "GLM-5",
    "zai-org/GLM-5.1": "GLM-5.1",
}


def display_name(model_id: str) -> str:
    if model_id in DISPLAY_NAMES:
        return DISPLAY_NAMES[model_id]
    tail = model_id.split("/", 1)[-1]
    return tail.replace("_", " ")


def read_chart_rows() -> list[tuple[str, int, str]]:
    rows: list[tuple[int, str, str, int]] = []
    with INPUT.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                rank = int(row["rank"])
                score = int(row["score_total"])
            except (KeyError, ValueError):
                continue
            rows.append((rank, row.get("harness", "LegalGenius"), row["model"], score))
    rows.sort(key=lambda r: r[0])
    chart_rows = [
        (f"{harness} + {display_name(model)}", score, "Our harness")
        for _, harness, model, score in rows[:CHART_LEGALGENIUS_COUNT]
    ]
    chart_rows.extend(EXTERNAL_REFERENCES)
    return chart_rows


FONT = (
    'font-family="system-ui, -apple-system, BlinkMacSystemFont, '
    "'Segoe UI', sans-serif\""
)


def render(chart_rows: list[tuple[str, int, str]]) -> str:
    names_scores = ", ".join(f"{n} at {s} percent" for n, s, _ in chart_rows)
    desc = f"Horizontal bar chart showing {names_scores}."

    rows_svg: list[str] = []
    bar_x = 132
    bar_max_w = 1050
    for i, (name, score, note) in enumerate(chart_rows, start=1):
        label_y = 330 + (i - 1) * 104
        rect_y = label_y + 18
        score_y = rect_y + 25
        bar_w = round(bar_max_w * score / 100)
        rows_svg.append(
            f'  <text x="{bar_x}" y="{label_y}" fill="#0F172A" {FONT} font-size="24" font-weight="650">{escape(name)}</text>\n'
            f'  <text x="1182" y="{label_y}" text-anchor="end" fill="#64748B" {FONT} font-size="17" font-weight="600">{escape(note)}</text>\n'
            f'  <rect x="{bar_x}" y="{rect_y}" width="{bar_max_w}" height="34" rx="17" fill="#E7EDF5"/>\n'
            f'  <rect x="{bar_x}" y="{rect_y}" width="{bar_w}" height="34" rx="17" fill="url(#bar{i})"/>\n'
            f'  <text x="1218" y="{score_y}" text-anchor="end" fill="#0F172A" {FONT} '
            f'font-size="23" font-weight="750">{score}%</text>'
        )
    rows_block = "\n\n".join(rows_svg)

    return f"""<svg width="1400" height="860" viewBox="0 0 1400 860" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">German Legal Benchmark Comparison</title>
  <desc id="desc">{escape(desc)}</desc>
  <defs>
    <linearGradient id="bg" x1="88" y1="74" x2="1316" y2="786" gradientUnits="userSpaceOnUse">
      <stop stop-color="#F7F4ED"/>
      <stop offset="1" stop-color="#E9F0F8"/>
    </linearGradient>
    <linearGradient id="headline" x1="132" y1="146" x2="514" y2="146" gradientUnits="userSpaceOnUse">
      <stop stop-color="#F97316"/>
      <stop offset="1" stop-color="#0F172A"/>
    </linearGradient>
    <linearGradient id="bar1" x1="0" y1="0" x2="720" y2="0" gradientUnits="userSpaceOnUse">
      <stop stop-color="#EA580C"/>
      <stop offset="1" stop-color="#FB923C"/>
    </linearGradient>
    <linearGradient id="bar2" x1="0" y1="0" x2="720" y2="0" gradientUnits="userSpaceOnUse">
      <stop stop-color="#D97706"/>
      <stop offset="1" stop-color="#FBBF24"/>
    </linearGradient>
    <linearGradient id="bar3" x1="0" y1="0" x2="720" y2="0" gradientUnits="userSpaceOnUse">
      <stop stop-color="#2563EB"/>
      <stop offset="1" stop-color="#38BDF8"/>
    </linearGradient>
    <linearGradient id="bar4" x1="0" y1="0" x2="720" y2="0" gradientUnits="userSpaceOnUse">
      <stop stop-color="#475569"/>
      <stop offset="1" stop-color="#94A3B8"/>
    </linearGradient>
    <filter id="shadow" x="78" y="62" width="1244" height="746" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
      <feFlood flood-opacity="0" result="BackgroundImageFix"/>
      <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
      <feOffset dy="14"/>
      <feGaussianBlur stdDeviation="22"/>
      <feComposite in2="hardAlpha" operator="out"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.0588235 0 0 0 0 0.0901961 0 0 0 0 0.164706 0 0 0 0.15 0"/>
      <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_1_1"/>
      <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_1_1" result="shape"/>
    </filter>
  </defs>

  <rect width="1400" height="860" fill="#F2EFE8"/>
  <g filter="url(#shadow)">
    <rect x="122" y="92" width="1156" height="690" rx="34" fill="url(#bg)"/>
  </g>

  <rect x="132" y="128" width="382" height="10" rx="5" fill="url(#headline)"/>
  <text x="132" y="188" fill="#0F172A" {FONT} font-size="46" font-weight="700">German Legal Benchmark</text>
  <text x="132" y="236" fill="#334155" {FONT} font-size="24" font-weight="500">LegalGenius harness results plus Libra reference, score out of 100</text>

  <text x="132" y="286" fill="#64748B" {FONT} font-size="18" font-weight="600">0</text>
  <text x="390" y="286" fill="#64748B" {FONT} font-size="18" font-weight="600">25</text>
  <text x="653" y="286" fill="#64748B" {FONT} font-size="18" font-weight="600">50</text>
  <text x="915" y="286" fill="#64748B" {FONT} font-size="18" font-weight="600">75</text>
  <text x="1164" y="286" fill="#64748B" {FONT} font-size="18" font-weight="600">100</text>

  <line x1="132" y1="302" x2="132" y2="704" stroke="#CBD5E1" stroke-width="2"/>
  <line x1="395" y1="302" x2="395" y2="704" stroke="#E2E8F0" stroke-width="2"/>
  <line x1="657" y1="302" x2="657" y2="704" stroke="#E2E8F0" stroke-width="2"/>
  <line x1="920" y1="302" x2="920" y2="704" stroke="#E2E8F0" stroke-width="2"/>
  <line x1="1182" y1="302" x2="1182" y2="704" stroke="#CBD5E1" stroke-width="2"/>

{rows_block}

  <text x="132" y="748" fill="#64748B" {FONT} font-size="18" font-weight="500">LegalGenius rows are our harness runs with the named model. Libra is an external DeepThinking reference.</text>
</svg>
"""


def escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def main() -> int:
    chart_rows = read_chart_rows()
    expected_rows = CHART_LEGALGENIUS_COUNT + len(EXTERNAL_REFERENCES)
    if len(chart_rows) < expected_rows:
        raise SystemExit(f"Expected at least {expected_rows} chart rows, got {len(chart_rows)}")
    OUTPUT.write_text(render(chart_rows), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} from {INPUT.name}:")
    for i, (name, score, note) in enumerate(chart_rows, 1):
        print(f"  {i}. {name:38s} {score}/100 ({note})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
