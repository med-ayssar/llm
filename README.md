# llm

uv project with a Jupyter notebook you can run in VS Code and Zed. Both editors use the same environment: `.venv` (Python 3.12) and the kernel **Python (llm)**.

## First time

```bash
uv sync
uv run python -m ipykernel install --user --name llm --display-name "Python (llm)" --env VIRTUAL_ENV "$(pwd)/.venv"
```

The kernel is already registered on this machine. Run the install command again if you move the project.

## VS Code

Open this folder. Accept the recommended **Python** and **Jupyter** extensions.

Open `notebooks/getting_started.ipynb` and select the kernel **Python (llm)**. If it is not listed, choose **Python Environments** and `.venv/bin/python`.

`notebooks/getting_started.py` also works. VS Code treats each `# %%` block as a cell.

## Zed

Open this folder, then open `notebooks/getting_started.py`.

Run the cell under the cursor with `ctrl-shift-enter` (`repl: run`). Pick **Python (llm)** if Zed asks for a kernel. The `.venv` interpreter is the same environment.

If the kernel does not appear, run the task **uv: register Jupyter kernel**, then `repl: refresh kernelspecs` from the command palette.

JupyterLab is available with the task **uv: Jupyter Lab**, or:

```bash
uv run jupyter lab
```

Select the **Python (llm)** kernel inside Lab and open `notebooks/getting_started.ipynb`.

## Local package

`src/llm` is the package notebooks import. `uv sync` installs it in editable mode, so edits in `src/llm/` are picked up by the next import. Restart the kernel after the first sync, or after adding a new module.

```python
import llm
```

Add files under `src/llm/`, for example `src/llm/tokenize.py`, then `from llm.tokenize import ...` in a notebook.
