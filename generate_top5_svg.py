#!/usr/bin/env python3
"""Regenerate assets/top-5-llms.svg from leaderboard.csv.

Reads the five top-ranked rows from leaderboard.csv and renders the
polished top-5 chart used in README.md. The layout, gradients and
typography match the hand-crafted reference; only the rank-5 row, bar
widths, score positions and aria description are driven by the data.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parent
INPUT = ROOT / "leaderboard.csv"
OUTPUT = ROOT / "assets" / "top-5-llms.svg"

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


def read_top5() -> list[tuple[str, int]]:
    rows: list[tuple[int, str, int]] = []
    with INPUT.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                rank = int(row["rank"])
                score = int(row["score_total"])
            except (KeyError, ValueError):
                continue
            rows.append((rank, row["model"], score))
    rows.sort(key=lambda r: r[0])
    return [(display_name(m), s) for _, m, s in rows[:5]]


FONT = (
    'font-family="system-ui, -apple-system, BlinkMacSystemFont, '
    "'Segoe UI', sans-serif\""
)


def render(top5: list[tuple[str, int]]) -> str:
    names_scores = ", ".join(f"{n} at {s}" for n, s in top5)
    desc = f"Horizontal bar chart showing {names_scores}."

    rows_svg: list[str] = []
    for i, (name, score) in enumerate(top5, start=1):
        label_y = 384 + (i - 1) * 84
        rect_y = label_y - 36
        score_y = label_y - 3
        bar_w = round(956 * score / 100)
        score_x = 260 + bar_w + 36
        rows_svg.append(
            f'  <rect x="260" y="{rect_y}" width="956" height="48" rx="24" fill="#E7EDF5"/>\n'
            f'  <rect x="260" y="{rect_y}" width="{bar_w}" height="48" rx="24" fill="url(#bar{i})"/>\n'
            f'  <text x="132" y="{label_y}" fill="#0F172A" {FONT} font-size="28" font-weight="650">{escape(name)}</text>\n'
            f'  <text x="{score_x}" y="{score_y}" text-anchor="end" fill="#0F172A" {FONT} '
            f'font-size="24" font-weight="700">{score}</text>'
        )
    rows_block = "\n\n".join(rows_svg)

    return f"""<svg width="1400" height="900" viewBox="0 0 1400 900" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">Top 5 LLMs on the German Legal Agent Benchmark</title>
  <desc id="desc">{escape(desc)}</desc>
  <defs>
    <linearGradient id="bg" x1="88" y1="74" x2="1316" y2="826" gradientUnits="userSpaceOnUse">
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
      <stop stop-color="#0F766E"/>
      <stop offset="1" stop-color="#2DD4BF"/>
    </linearGradient>
    <linearGradient id="bar5" x1="0" y1="0" x2="720" y2="0" gradientUnits="userSpaceOnUse">
      <stop stop-color="#7C3AED"/>
      <stop offset="1" stop-color="#C084FC"/>
    </linearGradient>
    <filter id="shadow" x="78" y="62" width="1244" height="776" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
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

  <rect width="1400" height="900" fill="#F2EFE8"/>
  <g filter="url(#shadow)">
    <rect x="122" y="92" width="1156" height="720" rx="34" fill="url(#bg)"/>
  </g>

  <rect x="132" y="128" width="382" height="10" rx="5" fill="url(#headline)"/>
  <text x="132" y="188" fill="#0F172A" {FONT} font-size="46" font-weight="700">Top 5 LLMs</text>
  <text x="132" y="236" fill="#334155" {FONT} font-size="24" font-weight="500">German legal agent benchmark, score out of 100</text>

  <text x="132" y="306" fill="#64748B" {FONT} font-size="18" font-weight="600">0</text>
  <text x="395" y="306" fill="#64748B" {FONT} font-size="18" font-weight="600">25</text>
  <text x="658" y="306" fill="#64748B" {FONT} font-size="18" font-weight="600">50</text>
  <text x="921" y="306" fill="#64748B" {FONT} font-size="18" font-weight="600">75</text>
  <text x="1172" y="306" fill="#64748B" {FONT} font-size="18" font-weight="600">100</text>

  <line x1="260" y1="330" x2="260" y2="720" stroke="#CBD5E1" stroke-width="2"/>
  <line x1="523" y1="330" x2="523" y2="720" stroke="#E2E8F0" stroke-width="2"/>
  <line x1="786" y1="330" x2="786" y2="720" stroke="#E2E8F0" stroke-width="2"/>
  <line x1="1049" y1="330" x2="1049" y2="720" stroke="#E2E8F0" stroke-width="2"/>
  <line x1="1300" y1="330" x2="1300" y2="720" stroke="#CBD5E1" stroke-width="2"/>

{rows_block}

  <text x="132" y="776" fill="#64748B" {FONT} font-size="18" font-weight="500">Latest published leaderboard snapshot. Provider names intentionally omitted from this chart.</text>
</svg>
"""


def escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def main() -> int:
    top5 = read_top5()
    if len(top5) < 5:
        raise SystemExit(f"Expected 5 rows in {INPUT}, got {len(top5)}")
    OUTPUT.write_text(render(top5), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} from top 5 of {INPUT.name}:")
    for i, (name, score) in enumerate(top5, 1):
        print(f"  {i}. {name:30s} {score}/100")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
