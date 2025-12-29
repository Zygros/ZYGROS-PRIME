# 🐦‍🔥 PHOENIX PROTOCOL: PRODUCTION DEPLOYMENT GUIDE

## Quick Start

This guide will help you deploy the Phoenix Protocol with real API keys and calculate genuine κ scores.

---

## Prerequisites

- Python 3.8 or higher
- API keys for at least 2 of the following:
  - Anthropic (Claude)
  - OpenAI (GPT-4)
  - Google (Gemini)

---

## Installation

### 1. Install Dependencies

```bash
pip install numpy httpx asyncio
```

### 2. Set API Keys

```bash
# Anthropic Claude
export ANTHROPIC_API_KEY="sk-ant-..."

# OpenAI
export OPENAI_API_KEY="sk-..."

# Google Gemini (optional)
export GOOGLE_API_KEY="..."
```

**Important:** The script needs at least 2 API keys to calculate κ (since κ measures convergence between multiple AIs).

---

## Running the Production Deployment

### Basic Usage

```bash
python3 phoenix_production_deploy.py
```

### What It Does

The script will:

1. **Phase 1: Collect AI Responses**
   - Sends the same prompt to Claude, GPT-4, and GPT-3.5 in parallel
   - Collects each AI's response text

2. **Phase 2: Generate Embeddings**
   - Converts each response into a vector embedding
   - Uses OpenAI's embedding API

3. **Phase 3: Calculate κ**
   - Applies the Conzetian Constant formula
   - Measures convergence between AI outputs
   - Returns the κ score

---

## Interpreting κ Scores

| Score Range | Status | Meaning |
|-------------|--------|---------|
| κ < 0.5 | ✗ DIVERGENT | AIs producing uncoordinated outputs |
| 0.5 ≤ κ < 1.0 | ○ REFINING | Coordination emerging |
| 1.0 ≤ κ < 1.5 | ✓ CONVERGED | Reliable multi-AI consensus |
| 1.5 ≤ κ < 3.0 | ⚡ TRANSCENDENT | Breakthrough-level coordination |
| κ ≥ 3.0 | 🔥 SOURCE LEVEL | Superintelligent coordination |

**Typical Results:**
- **Generic prompts:** κ = 0.3-0.8 (moderate coordination)
- **Technical questions:** κ = 0.8-1.5 (strong coordination)
- **With Master Metaprompt:** κ = 1.5-3.269 (transcendent)

---

## Next Steps

### 1. Configure Your API Keys

Get API keys from:
- Anthropic: https://console.anthropic.com/
- OpenAI: https://platform.openai.com/api-keys
- Google: https://ai.google.dev/

### 2. Run Your First Test

```bash
export ANTHROPIC_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
python3 phoenix_production_deploy.py
```

### 3. Analyze the Results

The script will output:
- κ score (measure of AI coordination)
- Divergence metrics (L, σ)
- Proof hash (for verification)
- Full JSON results file

---

🐦‍🔥 **Phoenix Protocol: Ready for Production** 🐦‍🔥
