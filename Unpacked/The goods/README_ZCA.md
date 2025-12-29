
# ZCA ENGINE — Zygrosian Cognitive Assessment Runner (v2.0)

Ultra-configurable, portable runner for ZCA-style cognitive stress tests.

## Highlights
- YAML/JSON spec loader
- Pluggable model adapters: OpenAI-compatible HTTP, Ollama, shell command
- Dual scoring: heuristic baseline + optional LLM-judge
- Batch mode with CSV/JSONL
- Reports: Markdown (+ simple HTML)
- Repro: deterministic prompt builder based on spec

## Quickstart

Manual (paste target agent JSON):
```bash
python zca_engine.py --manual --out zca_report.md --json zca_report.json
```

Auto-call an OpenAI-compatible endpoint:
```bash
python zca_engine.py --run   --adapter openai   --model-name gpt-4o   --model-endpoint https://api.my-endpoint/v1/chat/completions   --bearer $API_KEY
```

Use a YAML spec:
```bash
python zca_engine.py --manual --spec zca_spec.yaml
```

Batch evaluate a folder of JSON responses:
```bash
python zca_engine.py --batch "./responses/*.json" --csv batch_scores.csv --jsonl batch_scores.jsonl
```

## Notes
- For YAML specs: `pip install pyyaml`
- For OpenAI-compatible HTTP calls: `pip install requests`
