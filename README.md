# GenX3-RCC

University of Chicago RCC configuration scripts for [GenX3](https://github.com/aglavic/genx).

## Usage

Clone the repository and navigate to the project directory:

```bash
git clone https://gitlab.com/gsecars/genx3-rcc.git && cd genx3-rcc
```

Run the setup script to configure, generate files, and install GenX3:

```bash
./setup
```

To remove the GenX3 environment:

```bash
./cleanup
```

## CLI Reference

The `genx-rcc` CLI is available after `uv sync` and can be used directly via `uv run genx-rcc <command>`.

| Command | Description |
|---|---|
| `configure` | Interactively set anaconda module, environment name, python version, packages, and custom model path. Writes `genx3.conf`. |
| `create-files` | Generates `start_genx3` and `sbatch_genx3.example` from config. Creates a symlink to `start_genx3` in `$HOME`. |
| `install` | Creates the conda environment, installs packages, copies custom models, and optionally launches GenX3. |
| `clean` | Removes the conda environment after confirmation. |

## After Installation

Move or symlink `start_genx3` to the directory you want to run it from, or use the `$HOME/start_genx3` symlink created automatically by `create-files`.

## License

MIT — see [LICENSE](LICENSE).

---

[Christofanis Skordas](mailto:skordasc@uchicago.edu) — The University of Chicago
