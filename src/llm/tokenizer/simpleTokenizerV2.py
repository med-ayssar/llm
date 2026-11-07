"""Tokenizer with ids for unknown tokens and the end of a document."""

import re

from llm.tokenizer.interface import Token, TokenId
from llm.tokenizer.simpleTokenizer import SimpleTokenizer
from llm.tokenizer.tokens import DOCEND, UNK


class SimpleTokenizerV2(SimpleTokenizer):
    """Same vocabulary ids as ``SimpleTokenizer``, plus two ids after the last one.

    ``<UNK>`` is last + 1 and ``<DOCEND>`` is last + 2. Neither token is stored in
    the vocabulary dict. An unknown token encodes as the ``<UNK>`` id.
    """

    @property
    def unk_id(self) -> int:
        return len(self._token_to_id)

    @property
    def docend_id(self) -> int:
        return len(self._token_to_id) + 1

    def encode(self, text: str) -> list[int]:
        ids: list[int] = []
        for token in self.spliter.split(text):
            parsed = Token(value=token)
            if parsed.value == DOCEND:
                ids.append(self.docend_id)
            elif parsed.value == UNK:
                ids.append(self.unk_id)
            else:
                ids.append(self._token_to_id.get(parsed.value, self.unk_id))
        return ids

    def decode(self, token_ids: int | list[int]) -> str:
        ids = [token_ids] if isinstance(token_ids, int) else token_ids
        tokens = [self._text_for_id(token_id) for token_id in ids]
        text = " ".join(tokens)
        text = re.sub(r"\s+([,.?!\"()'])", r"\1", text)
        return re.sub(r"(?<=')\s+", "", text)

    def _text_for_id(self, token_id: int) -> str:
        parsed = TokenId(id=token_id)
        if parsed.id == self.docend_id:
            return DOCEND
        if parsed.id == self.unk_id or parsed.id not in self._id_to_token:
            return UNK
        return self._id_to_token[parsed.id]
