# German Legal Agent Benchmark

This repository contains a small public benchmark for German legal research agents.

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

Current leaderboard as of `2026-06-14`.

Rows marked `LegalGenius` are runs of the same LegalGenius evaluation harness.
The provider and model columns identify the LLM used inside that harness. The
Libra row is an external reference.

![German legal benchmark comparison](assets/benchmark-comparison.svg)

| Rank | Harness | Provider | Model | Score | Valid Cases | Avg. on Valid Cases |
| --- | --- | --- | --- | ---: | ---: | ---: |
| 1 | LegalGenius | OpenRouter | `anthropic/claude-opus-4.7` | `92/100` | `10/10` | `9.20` |
| 2 | LegalGenius | Nebius | `zai-org/GLM-5.1` | `91/100` | `10/10` | `9.10` |
| 3 | LegalGenius | OpenRouter | `openai/gpt-5.4` | `87/100` | `10/10` | `8.70` |
| 4 | LegalGenius | OpenRouter | `z-ai/glm-5` | `86/100` | `10/10` | `8.60` |
| 5 | LegalGenius | OpenRouter | `qwen/qwen3.6-plus` | `85/100` | `10/10` | `8.50` |
| 6 | LegalGenius | OpenRouter | `qwen/qwen3.5-397b-a17b` | `80/100` | `10/10` | `8.00` |
| Ref | External reference | Libra | DeepThinking | `73/100` | `10/10` | `7.30` |
| 7 | LegalGenius | OpenRouter | `qwen/qwen3.5-122b-a10b` | `51/100` | `9/10` | `5.67` |
| 8 | LegalGenius | OpenRouter | `mistralai/mistral-small-3.2-24b-instruct` | `29/100` | `10/10` | `2.90` |
| 9 | LegalGenius | Nebius | `PrimeIntellect/INTELLECT-3` | `25/100` | `8/10` | `3.12` |
| 10 | LegalGenius | OpenRouter | `mistralai/mistral-large-2512` | `22/100` | `7/10` | `3.14` |
| 11 | LegalGenius | Nebius | `NousResearch/Hermes-4-405B` | `21/100` | `10/10` | `2.10` |
| 12 | LegalGenius | Nebius | `zai-org/GLM-5` | `16/100` | `8/10` | `2.00` |
| 13 | LegalGenius | Nebius | `NousResearch/Hermes-4-70B` | `16/100` | `10/10` | `1.60` |

## External Reference

Libra (Deep Thinking Mode) is included as a `73/100` (`73%`) external reference in
the README table and chart, with `10/10` valid cases. 

## Method

- Each model is run on the same `10` benchmark cases.
- For LegalGenius rows, the LegalGenius harness asks the named research model to
  produce the legal answer.
- The answer is judged against the gold answer by `gpt-5-2025-08-07`.
- The primary score is the sum of per-case scores on a `1-10` scale, reported as `x/100`.
- Some models fail to return a usable final answer on every case. That is why the table also includes `Valid Cases`.
- External references are shown separately when they were not produced by the LegalGenius harness.

## Notes

- The benchmark was produced from the LegalGenius evaluation workflow, but this repo is intentionally standalone and only contains the benchmark data and published results.
