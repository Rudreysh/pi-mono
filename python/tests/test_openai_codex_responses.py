import base64
import json

import inspect

from pi_mono.ai.providers.openai_codex_responses import (
    _build_request_body,
    _build_sse_headers,
    _extract_account_id,
    _parse_sse,
    _resolve_codex_url,
    stream_openai_codex_responses,
    stream_simple_openai_codex_responses,
)


def _token(account_id: str) -> str:
    payload = (
        base64.urlsafe_b64encode(
            json.dumps({"https://api.openai.com/auth": {"chatgpt_account_id": account_id}}).encode()
        )
        .decode()
        .rstrip("=")
    )
    return f"aaa.{payload}.bbb"


def test_resolve_codex_url():
    assert (
        _resolve_codex_url("https://chatgpt.com/backend-api")
        == "https://chatgpt.com/backend-api/codex/responses"
    )
    assert (
        _resolve_codex_url("https://chatgpt.com/backend-api/codex")
        == "https://chatgpt.com/backend-api/codex/responses"
    )
    assert (
        _resolve_codex_url("https://chatgpt.com/backend-api/codex/responses")
        == "https://chatgpt.com/backend-api/codex/responses"
    )


def test_extract_account_id_from_token():
    assert _extract_account_id(_token("acc_test")) == "acc_test"


def test_stream_functions_are_synchronous():
    assert not inspect.iscoroutinefunction(stream_openai_codex_responses)
    assert not inspect.iscoroutinefunction(stream_simple_openai_codex_responses)


def test_build_sse_headers():
    headers = _build_sse_headers(None, None, "acc_test", _token("acc_test"), "session-1")
    assert headers["Authorization"].startswith("Bearer ")
    assert headers["chatgpt-account-id"] == "acc_test"
    assert headers["OpenAI-Beta"] == "responses=experimental"
    assert headers["accept"] == "text/event-stream"
    assert headers["session-id"] == "session-1"


def test_build_request_body_sends_off_effort_when_omitted():
    model = {
        "id": "gpt-5.4",
        "provider": "openai-codex",
        "api": "openai-codex-responses",
        "reasoning": True,
        "thinkingLevelMap": {"off": "none", "low": "low"},
    }
    context = {"systemPrompt": "sys", "messages": [{"role": "user", "content": "hi"}]}
    body = _build_request_body(model, context, {})
    assert body["reasoning"]["effort"] == "none"


def test_parse_sse_does_not_flush_partial_json_mid_stream():
    import asyncio

    class FakeResponse:
        async def aiter_text(self):
            yield 'data: {"type": "response.created", "n": '
            yield "1}\n\n"

    async def run():
        return [event async for event in _parse_sse(FakeResponse(), None)]

    events = asyncio.run(run())
    assert events == [{"type": "response.created", "n": 1}]
