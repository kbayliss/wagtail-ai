import re

import pytest
from test_utils.settings import (
    custom_ai_backend_class,
    custom_ai_backend_settings,
)
from wagtail_ai.ai import InvalidAIBackendError, get_ai_backend
from wagtail_ai.ai.echo import EchoBackend


@custom_ai_backend_class("wagtail_ai.ai.echo.EchoBackend")
def test_get_configured_backend_instance():
    backend = get_ai_backend("default")
    assert isinstance(backend, EchoBackend)


@custom_ai_backend_class("some.random.not.existing.path")
def test_get_invalid_backend_class_instance():
    with pytest.raises(
        InvalidAIBackendError,
        match=re.escape(
            'Invalid AI backend: "AI backend "default" settings: "CLASS" '
            '("some.random.not.existing.path") is not importable.'
        ),
    ):
        get_ai_backend("default")


@custom_ai_backend_settings(
    new_value={
        "CLASS": "wagtail_ai.ai.echo.EchoBackend",
        "CONFIG": {
            "MODEL_ID": "echo",
            "TOKEN_LIMIT": 123123,
            "MAX_WORD_SLEEP_SECONDS": 150,  # type: ignore
        },
    }
)
def test_get_backend_instance_with_custom_setting():
    backend = get_ai_backend("default")
    assert isinstance(backend, EchoBackend)
    assert backend.config.model_id == "echo"
    assert backend.config.max_word_sleep_seconds == 150
    assert backend.config.token_limit == 123123


@custom_ai_backend_settings(
    new_value={
        "CLASS": "wagtail_ai.ai.echo.EchoBackend",
        "CONFIG": {
            "MODEL_ID": "echo",
            "TOKEN_LIMIT": 123123,
            "MAX_WORD_SLEEP_SECONDS": 0,  # type: ignore
        },
    }
)
def test_prompt_with_context():
    backend = get_ai_backend("default")
    response = backend.prompt_with_context(
        pre_prompt="Translate the following context to French.",
        context="I like trains.",
    )
    assert response.text() == "This is an echo backend: I like trains."


@custom_ai_backend_settings(
    new_value={
        "CLASS": "wagtail_ai.ai.echo.EchoBackend",
        "CONFIG": {
            "MODEL_ID": "echo",
            "TOKEN_LIMIT": 123123,
            "MAX_WORD_SLEEP_SECONDS": 0,  # type: ignore
        },
    }
)
def test_prompt_with_context_iterator():
    backend = get_ai_backend("default")
    response = backend.prompt_with_context(
        pre_prompt="Translate the following context to French.",
        context="I like trains.",
    )
    assert list(response) == [
        "This",
        "is",
        "an",
        "echo",
        "backend:",
        "I",
        "like",
        "trains.",
    ]
