# 2026-11-17-050-historical-data-learning-and-local-ai-research

## Owner's request

The owner is leaning toward IDEAL collecting its own historical data and asked whether that history could later improve engines or learning ability. They reiterated that IDEAL's shared foundation is more important than rushing individual engines and requested research into local AI models/frameworks such as Jarvis and Hugging Face candidates, with deterministic scripts preferred over ongoing AI token use.

## Key design conclusions

1. Collect data first as an evidence-grade historical archive; treat model training as a later, separately governed use.
2. Preserve source, event/receive/ingest times, revisions, provenance, schema version, content hashes and licence/retention restrictions.
3. Do not assume every full-depth tick/order-book event must be retained forever. Define hot/warm/cold retention by research need, storage cost and source licence.
4. Keep market data, account/private financial records, personal data and AI interaction traces separated.
5. Build versioned point-in-time research datasets with explicit label maturity, chronological splits, purging/embargo, no look-ahead/survivorship leakage and realistic costs.
6. Separate assistant/agent workflow learning from quantitative market-model learning. Agent traces improve routing/tools/retrieval; they are not market labels or evidence of predictive alpha.
7. All model training/tuning remains offline and reproducible. No online weight updates or self-modifying live strategies. Promotion requires out-of-sample/walk-forward validation, realistic fees/funding/spread/slippage/latency/sizing, regime stability, independent verification and separate approval.
8. Deterministic scripts remain default for ingestion, validation, reconciliation, health, accounting, backtests and routine reports. AI is optional and bounded.

## Candidate research findings

- OpenJarvis (Apache-2.0) is the strongest current architectural study candidate for local-first personal AI: composable Intelligence/Engine/Agents/Tools-Memory/Learning, trace-driven learning/routing, multiple local runtimes, cost/energy/latency telemetry. Security review found material caveats: host shell execution can run as the user; sandbox/capability controls are off by default; capability policy needs explicit deny-by-default configuration; the documented enforce_tool_confirmation config is not enforced in every entry point. It is not approved as an IDEAL supervisor or financial execution authority.
- Hermes Agent (MIT) is a useful personal-assistant comparator with memory, skills and scheduling. Its default terminal backend can execute commands directly on the host; it must be isolated and least-privileged if ever tested.
- llama.cpp (MIT) and Ollama (MIT) are candidate interchangeable local inference runtimes for later PC testing.
- Amazon Chronos-2 (Apache-2.0, 120M parameters), Google TimesFM (Apache-2.0 repository), and IBM Granite Time Series PatchTST-FM-r2 (dual Apache-2.0/OpenMDW-1.0 per release material, approx. 385M) are candidate numerical time-series baselines, not proven trading signals.
- Salesforce Moirai 2.0-R-Small model card declares CC-BY-NC-4.0; excluded from a commercial-compatible shortlist absent legal clearance.
- FinGPT is a candidate for financial text/sentiment analysis only; sentiment is not a trade signal without validation.
- Qlib (MIT) is a quant research framework worth studying for offline data/feature/model/backtest workflow patterns. Its examples/data orientation is equity-centric; not a drop-in crypto perpetual engine.

Repository metadata checked on 17 Nov 2026:
- OpenJarvis: 15,789 stars, Apache-2.0, pushed 16 Nov 2026.
- Hermes Agent: 263,789 stars, MIT, pushed 16 Nov 2026.
- Qlib: 50,323 stars, MIT, pushed 4 Nov 2026.
- TimesFM: 35,597 stars, Apache-2.0, pushed 13 Nov 2026.
- llama.cpp: 135,301 stars, MIT, pushed 16 Nov 2026.
- Ollama: 187,192 stars, MIT, pushed 16 Nov 2026.
Stars and pushed timestamps are snapshots, not quality evidence.

## Documentation updates

- docs/DATA_INTEGRITY_AND_HEALTH.md: sections 12–13 added for archive-first collection, retention tiers, point-in-time datasets, distinct learning loops, offline model lifecycle, local AI candidates and evaluation criteria.
- docs/AI_MODEL_AND_LEARNING_RESEARCH.md: new research report with candidate frameworks, runtimes, time-series models, Qlib/FinGPT, security cautions and model governance.
- docs/FUTURE_SCOPE_IDEAS.md: F-007 historical archive/controlled learning and F-008 local AI/model research added; both Proposed.
- ROADMAP.md: Phase 02 checkpoint added; D-001 remains sole active initial trading scope; Phases 03–19 remain LOCKED.
- This conversation record and conversation index entry.

## Approval and operational status

No model/framework adopted. No data provider, paid feed, data retention implementation, model download, training job, hardware purchase, runtime package, credentials, hosting or account integration authorised. No code changed and no tests run. This is research and documentation only.

## Source links

- https://github.com/open-jarvis/OpenJarvis
- https://open-jarvis.github.io/OpenJarvis/architecture/overview/
- https://open-jarvis.github.io/OpenJarvis/user-guide/security/
- https://open-jarvis.github.io/OpenJarvis/user-guide/system-access/
- https://github.com/NousResearch/hermes-agent
- https://github.com/NousResearch/hermes-agent/security
- https://github.com/ggml-org/llama.cpp
- https://github.com/ollama/ollama
- https://huggingface.co/amazon/chronos-2
- https://github.com/google-research/timesfm
- https://huggingface.co/blog/ibm-research/ibm-releases-sota-granite-time-series
- https://huggingface.co/Salesforce/moirai-2.0-R-small
- https://github.com/AI4Finance-Foundation/FinGPT
- https://github.com/microsoft/qlib


## Fetch-back verification

All six changed files were fetched again from GitHub main after publication. Verified:
- docs/DATA_INTEGRITY_AND_HEALTH.md contains sections 12 and 13 for archive-first collection, point-in-time datasets, separate learning loops, offline model lifecycle and AI candidate review.
- docs/AI_MODEL_AND_LEARNING_RESEARCH.md exists and contains OpenJarvis, Hermes, local runtimes, time-series model candidates, Qlib, FinGPT, security review and promotion controls.
- docs/FUTURE_SCOPE_IDEAS.md contains F-007 and F-008, both Proposed.
- ROADMAP.md contains the Phase 02 checkpoint and confirms Phases 03–19 remain LOCKED.
- docs/CHATGPT_CONVERSATIONS/README.md contains the checkpoint 050 index entry.
- This conversation record was fetched back and verified.

GitHub content blob SHAs:
- docs/DATA_INTEGRITY_AND_HEALTH.md: dad371e3678289a46d5d8e4e36d01518e11e1df7
- docs/AI_MODEL_AND_LEARNING_RESEARCH.md: 9987bf71e75755423b4e826c765cadc3424bd1e0
- docs/FUTURE_SCOPE_IDEAS.md: 0a39e37abbc998bf2e6bb31e5fc678a590c6a608
- ROADMAP.md: f3e2221778d8a9738c884c2c14da65f5a3c3d290
- docs/CHATGPT_CONVERSATIONS/README.md: ba36b4924b07143b06eb8683c36aef9400951cec
- This record before verification addendum: b0d8e01bd857d852e1e3abe8a9a79002668ee0a0

No runtime code or dependencies changed. No tests, model downloads, data subscriptions or training runs were performed.
