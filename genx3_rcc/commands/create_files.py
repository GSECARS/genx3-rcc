# ----------------------------------------------------------------------------------
# Project: GenX3-RCC
# File: genx3_rcc/commands/create_files.py
# ----------------------------------------------------------------------------------
# Purpose:
# Generates start_genx3 and sbatch_genx3.example from templates.
# ----------------------------------------------------------------------------------
# Copyright (c) 2026 Christofanis Skordas, The University of Chicago
# ----------------------------------------------------------------------------------

import stat
from argparse import Namespace
from pathlib import Path
from string import Template

from genx3_rcc.config import CONFIG_FILE, GenXConfig

_TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


def _render(template_name: str, mapping: dict) -> str:
    return Template((_TEMPLATES_DIR / template_name).read_text()).substitute(mapping)


def _make_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def run(args: Namespace) -> None:
    if not CONFIG_FILE.exists():
        print(f"Error: {CONFIG_FILE} not found. Run 'genx-rcc configure' first.")
        return

    config = GenXConfig.load(CONFIG_FILE)
    mapping = {
        "anaconda_module": config.anaconda_module,
        "gcc_module": config.gcc_module,
        "environment_name": config.environment_name,
    }

    for template_name, output_name in [
        ("start_genx3.template", "start_genx3"),
        ("sbatch_genx3.example.template", "sbatch_genx3.example"),
    ]:
        output = Path(output_name)
        output.write_text(_render(template_name, mapping))
        _make_executable(output)
        print(f"Created {output}")

    link = Path.home() / "start_genx3"
    if link.is_symlink():
        link.unlink()
    link.symlink_to(Path("start_genx3").resolve())
    print(f"Linked {link} -> {link.resolve()}")

