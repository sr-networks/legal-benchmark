# German Legal Agent Benchmark

This repository contains a small public benchmark for German legal research agents. I use this test to assess changes to LLMs and the agent harness for the [legalgenius](https://legalgenius.de) app.

The benchmark currently consists of `10` curated legal research cases in [data/cases2021_eval.csv](data/cases2021_eval.csv)

The cases are short German legal fact patterns paired with gold answers derived from the target case law. Evaluation is run by GPT-5.5 on Openrouter (ChatGPT app for Libra). 

Prompt for Evaluation: "Du bist ein juristischer Experte und sollst die Antwort auf eine juristische Recherche-Arbeit bewerten und mit der Gold-Antwort vergleichen. Schätze die Korrektheit der Antwort auf einer Skala von 1 bis 10 ein und begründe. Bewerte nur die juristische Korrektheit und nicht die Form der Antwort.

Frage: 
...

Goldantwort: 
...

Antwort:
...
"

## Leaderboard

Current leaderboard as of `2026-06-20` (judge: GPT-5.5).

Rows marked `LegalGenius` are runs of the same LegalGenius evaluation harness.
The provider and model columns identify the LLM used inside that harness, and the
`Reasoning` column records the thinking level used. The Libra and ChatGPT rows are
external references.

![German legal benchmark comparison](assets/benchmark-comparison.svg)

| Rank | Harness | Provider | Model | Reasoning | Score | Valid Cases | Avg. on Valid Cases | Tokens/case (in / out) | Cost/case |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | LegalGenius | OpenRouter | `anthropic/claude-opus-4.8` | `standard (OpenRouter)` | `92/100` | `10/10` | `9.20` | 51.5k / 2.5k | $0.32 |
| 2 | LegalGenius | Nebius | `zai-org/GLM-5.2` | `high` | `89/100` | `10/10` | `8.90` | 56.6k / 1.8k | €0.076 |
| 3 | LegalGenius | OpenRouter | `openai/gpt-5.5` | `high (OpenRouter)` | `89/100` | `10/10` | `8.90` | 76.2k / 3.2k | $0.48 |
| Ref | External reference | ChatGPT | high thinking + web | `high + web search` | `89/100` | `10/10` | `8.90` | — | — |
| Ref | External reference | Libra | DeepThinking | `DeepThinking` | `73/100` | `10/10` | `7.30` | — | — |
| 4 | LegalGenius | OpenRouter | `openai/gpt-5.4-mini` | `default (OpenRouter)` | `67/100` | `10/10` | `6.70` | 23.5k / 0.7k | $0.021 |

`Claude Opus 4.8` leads at `92/100` (`9.20` average); `GLM-5.2` and `GPT-5.5` tie at
`89/100`. GLM-5.2 ran at reasoning effort `high` on Nebius. The OpenRouter models:
GPT-5.5 ran at reasoning effort `high`; Claude Opus 4.8 ran in `standard` mode,
because its extended thinking is not engageable via OpenRouter (verified — the
`reasoning` parameter produced no thinking tokens and no extra cost), so its `92/100`
is without extended thinking. Libra is shown at its `DeepThinking` mode. A cheap,
lower-tier model — `GPT-5.4 mini` (67/100, ~$0.021/case) — is included as a reference
to show the harness discriminates between tiers (the top scores are not a ceiling
artifact).

### Tokens & cost

`Tokens/case` is the harness-measured prompt/completion token count, averaged over
the 10 benchmark cases. `Cost/case` uses each provider's list price at run time
(2026-06-19):

> cost/case = (avg input tokens × price_in + avg output tokens × price_out) ÷ 1,000,000

| Model | Price in / out (per 1M) | Cost/case calculation |
| --- | --- | --- |
| GLM-5.2 (Nebius) | €1.20 / €4.40 | (56,610 × 1.20 + 1,750 × 4.40) / 1e6 = **€0.076** |
| Claude Opus 4.8 (OpenRouter) | $5.00 / $25.00 | (51,460 × 5.00 + 2,502 × 25.00) / 1e6 = **$0.320** |
| GPT-5.5 (OpenRouter) | $5.00 / $30.00 | (76,189 × 5.00 + 3,210 × 30.00) / 1e6 = **$0.477** |
| GPT-5.4 mini (OpenRouter) | $0.75 / $4.50 | (23,544 × 0.75 + 730 × 4.50) / 1e6 = **$0.021** |

- **Currencies differ:** GLM-5.2 (Nebius) is priced in **EUR**, the OpenRouter models
  in **USD** (~1.08 FX) — the ~4–6× cost gap dwarfs the conversion.
- Cost is **input-dominated** (input ≈ 97% of tokens), so per-case cost tracks prompt
  size and agent-step count more than answer length.
- **Libra** and **ChatGPT** are external references with no token/result data, so no
  tokens or cost are shown.

## External Reference

Libra (DeepThinking) is included as a `73/100` (`73%`) external reference in
the README table and chart, with `10/10` valid cases. It is not a LegalGenius
harness run and is therefore not ranked in [leaderboard.csv](leaderboard.csv) or
backed by a raw result file in [results/](results/).

ChatGPT (OpenAI's consumer app, run with high thinking and web search enabled) is
included as an `89/100` (`89%`) external reference with `10/10` valid cases. Like
Libra it was run directly, not through the LegalGenius harness, so it is not in
[leaderboard.csv](leaderboard.csv) and has no raw result file (self-reported).

The Nebius `zai-org/GLM-5.2` row is the current published GLM-5.2 benchmark result.
It reached `89/100` with all `10/10` cases valid, at reasoning effort `high`.

## Method

- Each model is run on the same `10` benchmark cases.
- For LegalGenius rows, the LegalGenius harness asks the named research model to
  produce the legal answer.
- The answer is judged against the gold answer by **GPT-5.5** (on OpenRouter; the
  ChatGPT app was used as judge for the Libra reference).
- The primary score is the sum of per-case scores on a `1-10` scale, reported as `x/100`.
- The `Reasoning` column records the thinking level: GLM-5.2 at `high` (Nebius);
  GPT-5.5 at `high` and Claude Opus 4.8 at `standard` (both via OpenRouter — Opus's
  extended thinking is not engageable through OpenRouter); Libra at `DeepThinking`.
- Some models fail to return a usable final answer on every case. That is why the table also includes `Valid Cases`.
- External references are shown separately when they were not produced by the LegalGenius harness.

## Notes

- The benchmark was produced from the LegalGenius evaluation workflow, but this repo is intentionally standalone and only contains the benchmark data and published results.
