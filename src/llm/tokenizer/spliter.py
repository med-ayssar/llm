"""Split text with one regular expression."""

import re
from typing import Self

from pydantic import BaseModel, Field, field_validator, model_validator

# Punctuation, a double hyphen, and whitespace. re.split keeps these pieces
# when the pattern is one capturing group.
DEFAULT_PATTERN = '[,:;?_!"{}()\']|--|\\s'


class Spliter(BaseModel):
    """Split text into tokens.

    ``pattern`` is given to ``re.split``. Separators in the pattern are kept.
    Whitespace-only pieces are dropped.
    """

    pattern: str = DEFAULT_PATTERN
    tokens: list[str] = Field(default_factory=list)

    @field_validator("pattern")
    @classmethod
    def must_compile(cls, value: str) -> str:
        re.compile(value)
        return value

    @model_validator(mode="after")
    def sort(self) -> Self:
        """Sort tokens after the fields are set. Repeated tokens are kept once."""
        self.tokens = sorted(set(self.tokens))
        return self

    def split(self, text: str) -> list[str]:
        pattern = self.pattern
        if not (pattern.startswith("(") and pattern.endswith(")")):
            pattern = f"({pattern})"
        parts = re.split(pattern, text)
        return [part.strip() for part in parts if part.strip()]
