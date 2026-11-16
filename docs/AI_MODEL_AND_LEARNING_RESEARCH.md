# IDEAL AI Model and Learning Research

**Date:** 17 November 2026  
**Phase:** 02 — research and architecture only  
**Status:** Candidate review; no adoption or runtime implementation authorised  
**Related:** F-007 and F-008 Proposed; D-019 accepted data-integrity principle

## 1. Executive assessment

IDEAL should not become an AI agent that runs everything. Deterministic software should perform routine and safety-critical work. AI is an optional, replaceable assistant/research capability, selected only where it measurably improves outcomes over scripts and conventional ML.

The strongest current candidate for architectural study is OpenJarvis, not because it should control IDEAL, but because its local-first composable design, model/runtime abstraction, trace-driven evaluation, cost/energy telemetry and learning primitives map well to the desired low-token system. Hermes Agent is a useful comparator for persistent personal-assistant workflows. Neither is approved for direct integration.

## 2. Important distinction: what does learning mean?

IDEAL may eventually have at least three distinct learning loops:

1. **Assistant workflow learning:** improve local model routing, retrieval, prompts, tool selection and reusable workflows from approved interaction traces. This is similar to OpenJarvis's trace-driven policies. It does not create trading alpha.
2. **Quantitative market learning:** train/test statistical and ML models on point-in-time market data with explicitly defined outcome labels. Examples include volatility/regime classification, return distributions, liquidity, execution cost, risk forecasts and candidate alpha features.
3. **Strategy research automation:** deterministic pipelines generate features, evaluate hypotheses, run backtests and compare results. LLMs may help formulate hypotheses or explain results, but they do not certify validity.

A larger historical database does not automatically create a better strategy. Data quality, label design, non-stationarity, market impact and leakage controls matter more than raw row count.

## 3. Candidate agent frameworks

| Project | Licence | Observed repository state (17 Nov 2026) | Relevance | Main caution |
|---|---|---|---|---|
| [OpenJarvis](https://github.com/open-jarvis/OpenJarvis) | Apache-2.0 | 15.8k stars; pushed 16 Nov 2026; active v1.0 release line | Local-first assistant architecture; composable intelligence/engine/agent/tools-memory/learning; trace-driven routing; energy/cost telemetry | Host shell tool runs as user unless sandboxed; sandbox and capability controls are off by default; capability policy requires explicit deny-by-default configuration; documented confirmation flag is not enforced in every entry point |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | MIT | 263.8k stars; pushed 16 Nov 2026 | Persistent personal agent, skills, memory, schedules, model/provider flexibility | Broad host/tool access; default terminal backend runs commands on host. Keep away from financial credentials and execution authority |
| [Qlib](https://github.com/microsoft/qlib) | MIT | 50.3k stars; pushed 4 Nov 2026 | Quant research pipeline, features, ML, backtesting, portfolio/risk abstractions | Equity-oriented examples and data assumptions; not a drop-in crypto perpetual engine; evaluate integration cost and current dependencies |

Repository statistics are point-in-time snapshots, not quality guarantees. GitHub's open issue count includes pull requests and is not a clean bug backlog metric.

### OpenJarvis detail

Official docs describe five composable primitives: Intelligence, Engine, Agents, Tools/Memory and Learning. Its learning system can store interaction traces and use them to improve routing and other stack behaviour. It supports local inference engines such as Ollama, vLLM, SGLang and llama.cpp, and optional cloud engines. It treats energy, FLOPs, latency and cost as evaluation metrics.

Security review matters. Its docs explicitly warn that shell execution runs arbitrary commands as the host user unless sandboxed. Sandbox and capability checks are off by default, and its capability defaults need explicit review. The documentation says the enforce_tool_confirmation setting is accepted by the configuration loader but is not currently enforced in every entry point. IDEAL must not rely on a model prompt or agent framework confirmation for authorisation. Permissions must be enforced by IDEAL-owned deterministic APIs and OS/container boundaries.

### Hermes detail

Hermes is MIT and supports model-provider flexibility, memory, skill creation and scheduling. It is useful as a reference for the user-facing assistant. Its security documentation describes a single-tenant trust envelope and direct host command execution by default. If evaluated, use isolated containers/VMs, minimal mounts, no credentials, no trading write tools and explicit network controls.

## 4. Local inference runtimes

- [llama.cpp](https://github.com/ggml-org/llama.cpp), MIT: broad CPU/GPU portability, quantisation, OpenAI-compatible server, schema-constrained JSON and tool/function calling. Candidate for future PC portability and low-cost local inference.
- [Ollama](https://github.com/ollama/ollama), MIT: simpler model management and local API, structured output and tool calling. Candidate for ease-of-use baseline.
- Keep an IDEAL-owned inference interface so either can be swapped or disabled without changing domain logic. Local model availability is not a reason to put LLMs in deterministic data pipelines.

## 5. Numerical time-series model candidates

| Model | Licence / size | Potential research use | Limitation |
|---|---|---|---|
| [Amazon Chronos-2](https://huggingface.co/amazon/chronos-2) | Apache-2.0; 120M parameters | Quantile forecasts; univariate, multivariate and covariate-informed forecasting; CPU/GPU inference | General-purpose pretrained TSFM; not proven to forecast tradable returns or microstructure |
| [Google TimesFM](https://github.com/google-research/timesfm) | Apache-2.0 repository; 3.0 checkpoint current in inspected repo | General time-series forecasting baseline | Not designed specifically for exchange microstructure; validate each checkpoint and data cadence |
| [IBM Granite Time Series PatchTST-FM-r2](https://huggingface.co/blog/ibm-research/ibm-releases-sota-granite-time-series) | Dual Apache-2.0 / OpenMDW-1.0 per release material; about 385M parameters | Probabilistic forecasts and imputation; medium-horizon research | Higher resource needs; exact artefact licence and data fit must be verified |
| [Salesforce Moirai 2.0-R-Small](https://huggingface.co/Salesforce/moirai-2.0-R-small) | CC-BY-NC-4.0 | Research comparison only if use is permitted | Non-commercial licence; do not include in a commercial-compatible deployment shortlist without legal review |
| [FinGPT](https://github.com/AI4Finance-Foundation/FinGPT) | Review code and each individual checkpoint/data licence | Financial text sentiment/classification and news/document analysis | Not a numerical market forecaster; output is not a trade signal without independent testing |

Chronos-2's model card reports 120M parameters, probabilistic quantile forecasts, support for multiple covariates and CPU/GPU inference. IBM's September 2026 release article describes PatchTST-FM-r2 as approximately 385M parameters with probabilistic forecasting and imputation. These are candidate technical properties, not evidence of trading profitability.

## 6. Quant research framework candidate: Qlib

Qlib is an MIT-licensed research platform with data handling, feature generation, supervised ML, market-dynamics and reinforcement-learning workflows, backtesting, risk and portfolio concepts. It is worth studying for reusable research patterns, not adopting wholesale. Its public datasets and examples have an equity focus. Crypto perpetuals require contract-specific funding, mark/index, liquidation, basis, fee, spread, leverage and market-microstructure modelling. Any Qlib experiment must be checked for point-in-time correctness and realistic costs.

## 7. Data collection as a future learning asset

The archive is valuable for:
- reproducible strategy and model evaluation;
- regime and volatility research;
- market microstructure and execution-cost analysis;
- risk and portfolio exposure estimation;
- feature stability and drift detection;
- cross-asset/hedging research;
- assistant workflow evaluation, if interaction traces are separately approved.

The archive must preserve source time, receive time, revisions and licence restrictions. Research datasets must be versioned, point-in-time and reproducible. Account/private data and assistant traces must not leak into market training data.

Labels must be explicit and mature only after the forecast horizon has elapsed. Training splits must be chronological, with purging/embargo where labels overlap. Use walk-forward validation, untouched out-of-sample periods, multiple regimes and realistic fees/funding/spread/slippage/latency/position sizing. Include survivorship and look-ahead controls. Compare against naive baselines and simple statistical models. Do not select models by in-sample Sharpe alone.

## 8. Model promotion and safety

No self-modifying live strategies. Training and tuning remain offline. Store model artefact hash, dataset manifest hash, source revisions, code commit, environment, parameters, random seed, metrics and limitations. Promotion requires a pre-registered acceptance threshold and independent verification. A future challenger may run in shadow mode; any paper/live transition remains subject to the existing phase and explicit approval gates.

AI tools must be least-privilege, sandboxed and treated as untrusted. No model can:
- validate its own input data as the sole authority;
- write directly to canonical ledgers or exchange adapters;
- access exchange credentials or issue orders by default;
- change risk limits or strategy configuration without explicit approval;
- change its own weights/prompts/tools in production without versioning, tests and approval.

## 9. Current recommendation

1. Use OpenJarvis as the primary architecture-study candidate for local-first assistant design and trace-based efficiency measurement.
2. Keep Hermes as a comparator, not the initial choice.
3. Evaluate llama.cpp and Ollama later on actual PC hardware; do not pick hardware yet.
4. Test Chronos-2, TimesFM and Granite TS as offline forecast baselines only after the historical data contract and dataset pipeline exist.
5. Study Qlib for quant research workflow ideas; do not couple it to IDEAL's runtime.
6. Keep FinGPT limited to financial-text experiments with source provenance.
7. Prefer scripts, statistical models and deterministic checks whenever they meet the requirement.

## 10. Sources

- OpenJarvis repository and release: https://github.com/open-jarvis/OpenJarvis
- OpenJarvis architecture: https://open-jarvis.github.io/OpenJarvis/architecture/overview/
- OpenJarvis security: https://open-jarvis.github.io/OpenJarvis/user-guide/security/
- OpenJarvis system access: https://open-jarvis.github.io/OpenJarvis/user-guide/system-access/
- Hermes Agent repository: https://github.com/NousResearch/hermes-agent
- Hermes security policy: https://github.com/NousResearch/hermes-agent/security
- llama.cpp: https://github.com/ggml-org/llama.cpp
- Ollama API: https://github.com/ollama/ollama/blob/main/docs/api.md
- Chronos-2 model card: https://huggingface.co/amazon/chronos-2
- TimesFM: https://github.com/google-research/timesfm
- IBM Granite Time Series: https://huggingface.co/blog/ibm-research/ibm-releases-sota-granite-time-series
- Moirai 2.0-R-Small: https://huggingface.co/Salesforce/moirai-2.0-R-small
- FinGPT: https://github.com/AI4Finance-Foundation/FinGPT
- Qlib: https://github.com/microsoft/qlib

No code, model weights, dependencies, data feeds, credentials, hardware, hosting or training jobs were installed or run during this research checkpoint.
