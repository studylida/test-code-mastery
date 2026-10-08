"""[Day 01] 학습자가 직접 손코딩으로 완성한 외부 통신 차단(monkeypatch) 드릴."""

import httpx
import pytest


@pytest.fixture
def block_external_http(monkeypatch: pytest.MonkeyPatch) -> None:
    """[손코딩 14 Fixture] httpx.Client.post 호출을 가로채서 강제 차단하는 원숭이 패치."""
    def block(*args: object, **kwargs: object) -> None:
        raise RuntimeError("외부 통신 금지!")

    monkeypatch.setattr("httpx.Client.post", block)


def test_external_call_is_blocked(block_external_http: None) -> None:
    """[손코딩 14] 외부 통신 차단기가 작동하여 RuntimeError를 발생시키는지 with pytest.raises 로 검증."""
    with pytest.raises(RuntimeError) as exc_info:
        client = httpx.Client()
        client.post("https://api.openai.com/v1/chat")

    assert "외부 통신 금지!" in str(exc_info.value)
