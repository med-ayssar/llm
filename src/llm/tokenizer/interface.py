"""Tokenizer interface. A tokenizer is built from a plain-text vocabulary."""

from abc import ABC, abstractmethod

from pydantic import BaseModel, Field, field_validator


class PlainTextVocab(BaseModel):
    """Vocabulary written as plain text. Tokens are separated by whitespace."""

    text: str

    @field_validator("text")
    @classmethod
    def require_tokens(cls, value: str) -> str:
        if not value.split():
            raise ValueError("Vocabulary text does not contain any tokens")
        return value

    def tokens(self) -> list[str]:
        """Unique tokens in the order they first appear."""
        seen: dict[str, None] = {}
        for token in self.text.split():
            seen.setdefault(token, None)
        return list(seen)


class Token(BaseModel):
    """One vocabulary token passed to ``encode``."""

    value: str = Field(min_length=1)


class TokenId(BaseModel):
    """One vocabulary id passed to ``decode``."""

    id: int = Field(ge=0)


class Tokenizer(BaseModel, ABC):
    """Interface for a tokenizer backed by a plain-text vocabulary.

    ``encode`` returns the id of one token. ``decode`` returns the token for one id.
    """

    vocab: PlainTextVocab

    @field_validator("vocab", mode="before")
    @classmethod
    def vocab_from_text(cls, value: object) -> object:
        if isinstance(value, str):
            return PlainTextVocab(text=value)
        return value

    @abstractmethod
    def encode(self, token: str) -> int:
        """Return the id of ``token``."""

    @abstractmethod
    def decode(self, token_id: int) -> str:
        """Return the token stored at ``token_id``."""
