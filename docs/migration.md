# Migration Map

## TypeScript Source Layout

| TypeScript path | Purpose | Python target path | Port status |
|---|---|---|---|
| `packages/ai/src` | Unified LLM API with model discovery & provider configurations | `python/src/pi_mono/ai` | In-progress |
| `packages/agent/src` | General-purpose agent core, state & transport management | `python/src/pi_mono/agent` | Not started |
| `packages/tui/src` | Terminal UI layout, text styling, and editor helper utilities | `python/src/pi_mono/tui` | Not started |
| `packages/coding-agent/src` | Coding agent CLI, tools execution, session management | `python/src/pi_mono/coding_agent` | Not started |

## Entry Points

| TypeScript command/API | Behavior | Python equivalent |
|---|---|---|
| `pi-ai` (`packages/ai/src/cli.ts`) | Unified LLM configuration & interactive prompt tool | `python -m pi_mono.ai.cli` |
| `pi` (`packages/coding-agent/src/cli.ts`) | Coding Agent interactive TUI / CLI session | `python -m pi_mono.coding_agent.cli` |

## External Dependencies Mapping

| TypeScript dependency | Purpose | Python replacement | Notes |
|---|---|---|---|
| `@anthropic-ai/sdk` | Anthropic API integration | `anthropic` | Official SDK |
| `openai` | OpenAI API integration | `openai` | Official SDK |
| `@google/genai` | Google Gemini API integration | `google-genai` | Official SDK |
| `@mistralai/mistralai` | Mistral AI API integration | `mistralai` | Official SDK |
| `@aws-sdk/client-bedrock-runtime` | Bedrock Runtime integration | `boto3` | AWS Python SDK |
| `typebox` | Schema validation | `pydantic` or `dataclasses` | Pydantic matches typebox closely |
| `yaml` | YAML parsing & serialization | `ruamel.yaml` or `PyYAML` | PyYAML is standard |
| `get-east-asian-width` | Grapheme column width styling | `unicodedata` | Standard library functions |
| `@silvia-odwyer/photon-node` | Image resizing/processing | `Pillow` (PIL) | Python standard image lib |
| `diff` | Diffing file changes | `difflib` | Standard library |
| `glob` / `minimatch` | File matching and search | `fnmatch` / `glob` / `pathlib` | Standard library |

## Ported Modules

| Module | TypeScript source | Python target | Status | Test coverage | Notes |
|---|---|---|---|---|---|
| `sanitize-unicode` | `packages/ai/src/utils/sanitize-unicode.ts` | `python/src/pi_mono/utils/sanitize_unicode.py` | Completed | 100% | Handled surrogate character cleaning |
| `hash` | `packages/ai/src/utils/hash.ts` | `python/src/pi_mono/utils/hash.py` | Completed | 100% | Short deterministic string hash |
| `diagnostics` | `packages/ai/src/utils/diagnostics.ts` | `python/src/pi_mono/utils/diagnostics.py` | Completed | 100% | Error formatting and diagnostics |
| `json-parse` | `packages/ai/src/utils/json-parse.ts` | `python/src/pi_mono/utils/json_parse.py` | Completed | 100% | JSON parsing and repair utilities |
| `overflow` | `packages/ai/src/utils/overflow.ts` | `python/src/pi_mono/utils/overflow.py` | Completed | 100% | Context window overflow check |
| `abort-signals` | `packages/ai/src/utils/abort-signals.ts` | `python/src/pi_mono/utils/abort_signals.py` | Completed | 100% | AbortController/Signal emulation |
| `resolve-config-value` | `packages/coding-agent/src/core/resolve-config-value.ts` | `python/src/pi_mono/core/resolve_config_value.py` | Completed | 100% | Config value resolution ($ENV, !cmd) |
| `shell` | `packages/coding-agent/src/utils/shell.ts` | `python/src/pi_mono/utils/shell.py` | Completed | 100% | Shell config and environment resolver |

## Known Behavior Differences

| Area | TypeScript behavior | Python behavior | Reason | Approved? |
|---|---|---|---|---|

## Fixture Decisions

| Fixture | Purpose | Notes |
|---|---|---|
