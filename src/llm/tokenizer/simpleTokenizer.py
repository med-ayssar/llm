"""A tokenizer that assigns an id to each token in a plain-text vocabulary."""

from typing import Self

from pydantic import PrivateAttr, model_validator

from llm.tokenizer.interface import Token, TokenId, Tokenizer


class SimpleTokenizer(Tokenizer):
    """Map vocabulary tokens to ids in first-seen order, starting at 0."""

    _token_to_id: dict[str, int] = PrivateAttr(default_factory=dict)
    _id_to_token: dict[int, str] = PrivateAttr(default_factory=dict)

    @model_validator(mode="after")
    def index_vocabulary(self) -> Self:
        tokens = list(dict.fromkeys(self.spliter.split(self.vocab.text)))
        if not tokens:
            raise ValueError("Vocabulary text does not contain any tokens")
        self._token_to_id = {token: index for index, token in enumerate(tokens)}
        self._id_to_token = {index: token for token, index in self._token_to_id.items()}
        return self

    def encode(self, text: str) -> list[int]:
        ids: list[int] = []
        for token in self.spliter.split(text):
            parsed = Token(value=token)
            try:
                ids.append(self._token_to_id[parsed.value])
            except KeyError:
                raise KeyError(f"Unknown token: {parsed.value}") from None
        return ids

    def decode(self, token_id: int) -> str:
        parsed = TokenId(id=token_id)
        try:
            return self._id_to_token[parsed.id]
        except KeyError:
            raise KeyError(f"Unknown token id: {parsed.id}") from None
