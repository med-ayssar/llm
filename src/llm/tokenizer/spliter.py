"""Split text with one regular expression."""

import re

from pydantic import BaseModel, field_validator

# Punctuation, a double hyphen, and whitespace. re.split keeps these pieces
# when the pattern is one capturing group.
DEFAULT_PATTERN = '[,:;?_!"{}()\']|--|\\s'


class Spliter(BaseModel):
    """Split text into tokens.

    ``pattern`` is given to ``re.split``. Separators in the pattern are kept.
    Whitespace-only pieces are dropped.
    """

    pattern: str = DEFAULT_PATTERN

    @field_validator("pattern")
    @classmethod
    def must_compile(cls, value: str) -> str:
        re.compile(value)
        return value

    def split(self, text: str) -> list[str]:
        pattern = self.pattern
        if not (pattern.startswith("(") and pattern.endswith(")")):
            pattern = f"({pattern})"
        parts = re.split(pattern, text)
        return [part.strip() for part in parts if part.strip()]
