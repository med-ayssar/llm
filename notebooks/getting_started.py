# %%
# Zed: run each cell with ctrl-shift-enter (repl: run).
# Kernel: Python (llm), the uv environment in .venv.
# VS Code: this file is also a notebook. Use the Run Cell button
# and select the same .venv interpreter.
import sys

print(sys.executable)
print(sys.version)

# %%
values = [1, 1, 2, 3, 5, 8]
print("sum", sum(values))
print("in project venv", ".venv" in sys.executable)

# %%
# Download https://www.kaggle.com/datasets/rakibulhasanshaon69/the-verdict-txt
# into data/the-verdict-txt/. A public download works without a token.
# If Kaggle asks you to sign in, put an API token in ~/.kaggle/access_token
# or a legacy ~/.kaggle/kaggle.json from https://www.kaggle.com/settings/api.
from pathlib import Path

import kagglehub

project_root = Path.cwd()
if not (project_root / "pyproject.toml").exists():
    project_root = project_root.parent

output_dir = project_root / "data" / "the-verdict-txt"
output_dir.mkdir(parents=True, exist_ok=True)

dataset_path = kagglehub.dataset_download(
    "rakibulhasanshaon69/the-verdict-txt",
    output_dir=str(output_dir),
)

verdict = Path(dataset_path) / "the-verdict.txt"
print(verdict)
print(f"{verdict.stat().st_size} bytes")

# %%
# The uv environment installs src/llm in editable mode.
# Add modules under src/llm/, then import them here.
import llm

print(llm.__version__)
print(llm.__file__)
