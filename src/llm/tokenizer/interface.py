"""Tokenizer interface. A tokenizer is built from a plain-text vocabulary."""

from abc import ABC, abstractmethod

from pydantic import BaseModel, Field, field_validator

from llm.tokenizer.spliter import Spliter


class PlainTextVocab(BaseModel):
    """Vocabulary written as plain text. A ``Spliter`` decides where tokens end."""

    text: str

    @field_validator("text")
    @classmethod
    def require_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Vocabulary text is empty")
        return value


class Token(BaseModel):
    """One vocabulary token passed to ``encode``."""

    value: str = Field(min_length=1)


class TokenId(BaseModel):
    """One vocabulary id passed to ``decode``."""

    id: int = Field(ge=0)


class Tokenizer(BaseModel, ABC):
    """Interface for a tokenizer backed by a plain-text vocabulary.

    ``vocab`` is the plain text. ``spliter`` splits that text and the text passed
    to ``encode``. ``encode`` returns one id per token. ``decode`` accepts one
    id or a list of ids and joins the tokens with spaces.
    """

    vocab: PlainTextVocab
    spliter: Spliter

    def __init__(self, vocab: PlainTextVocab | str, spliter: Spliter, **data: object) -> None:
        super().__init__(vocab=vocab, spliter=spliter, **data)

    @field_validator("vocab", mode="before")
    @classmethod
    def vocab_from_text(cls, value: object) -> object:
        if isinstance(value, str):
            return PlainTextVocab(text=value)
        return value

    @abstractmethod
    def encode(self, text: str) -> list[int]:
        """Split ``text`` and return the id of each token."""

    @abstractmethod
    def decode(self, token_ids: int | list[int]) -> str:
        """Return the tokens for one id or a list of ids, joined with spaces.

        Spaces before ``,.?!"()'`` are removed.
        """
