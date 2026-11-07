"""Read files stored under the project ``data`` directory."""

from collections.abc import Iterable
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class DataFile(BaseModel):
    """One file under ``data``."""

    name: str
    extension: str
    path: str

    @field_validator("extension")
    @classmethod
    def normalize_extension(cls, value: str) -> str:
        return _normalize_extension(value)


class Data(BaseModel):
    """List and read downloaded files in the project ``data`` directory."""

    root: Path = Field(default_factory=lambda: _project_root() / "data")

    def list(self, *, extension: str | Iterable[str] | None = None) -> list[DataFile]:
        """Return every file under ``data``, including nested directories.

        Each item has the file ``name``, its ``extension`` (with the leading dot),
        and ``path`` relative to ``data``. Pass ``extension`` to keep only those
        suffixes, for example ``extension="txt"`` or ``extension=[".txt", ".csv"]``.
        """
        root = self.root
        if not root.is_dir():
            raise FileNotFoundError(f"Data directory does not exist: {root}")

        allowed = None if extension is None else _extensions(extension)
        files: list[DataFile] = []
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(root)
            if any(part.startswith(".") for part in relative.parts):
                continue
            suffix = path.suffix.lower()
            if allowed is not None and suffix not in allowed:
                continue
            files.append(
                DataFile(name=path.name, extension=suffix, path=relative.as_posix())
            )
        files.sort(key=lambda item: item.path)
        return files

    def data(self, path: str | Path) -> str | bytes:
        """Return the contents of a file under ``data``.

        ``path`` is relative to the data directory, or an absolute path inside it.
        Text that decodes as UTF-8 is returned as ``str``. Other files are returned
        as ``bytes``.
        """
        file_path = self._resolve(path)
        content = file_path.read_bytes()
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return content

    def _resolve(self, path: str | Path) -> Path:
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = self.root / candidate
        resolved = candidate.resolve()
        root = self.root.resolve()
        if not resolved.is_relative_to(root):
            raise ValueError(f"Path is outside the data directory: {path}")
        if not resolved.is_file():
            raise FileNotFoundError(resolved)
        return resolved


def _project_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").is_file():
            return parent
    raise FileNotFoundError("Could not find the project root from the llm package.")


def _extensions(extension: str | Iterable[str]) -> set[str]:
    values = [extension] if isinstance(extension, str) else list(extension)
    return {_normalize_extension(value) for value in values}


def _normalize_extension(extension: str) -> str:
    value = extension.strip().lower()
    if value == "" or value.startswith("."):
        return value
    return f".{value}"
