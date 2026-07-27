#!/usr/bin/env python
# ----------------------------------------------------------------------------------
# Project: GenX3-RCC
# File: genx3_rcc/commands/configure.py
# ----------------------------------------------------------------------------------
# Purpose:
# Interactive configuration wizard
# ----------------------------------------------------------------------------------
# Copyright (c) 2026 Christofanis Skordas, The University of Chicago
# ----------------------------------------------------------------------------------

from argparse import Namespace

from genx3_rcc.config import CONFIG_FILE, GenXConfig


def _prompt(label: str, default: str) -> str:
    value = input(f"{label} [{default}]: ").strip()
    return value if value else default


def run(args: Namespace) -> None:
    existing = GenXConfig.load(CONFIG_FILE) if CONFIG_FILE.exists() else GenXConfig()

    config = GenXConfig(
        anaconda_module=_prompt("Anaconda module", existing.anaconda_module),
        gcc_module=_prompt("GCC module", existing.gcc_module),
        environment_name=_prompt("Environment name", existing.environment_name),
        python_version=_prompt("Python version", existing.python_version),
        anaconda_packages=_prompt("Anaconda packages", existing.anaconda_packages),
        pypi_packages=_prompt("PyPI packages", existing.pypi_packages),
        custom_model_path=_prompt("Custom model path", existing.custom_model_path),
    )

    config.save()
    print(f"Configuration saved to {CONFIG_FILE}")
