#!/usr/bin/env python
# ----------------------------------------------------------------------------------
# Project: GenX3-RCC
# File: genx3_rcc/commands/patch.py
# ----------------------------------------------------------------------------------
# Purpose:
# Applies source patches to an existing GenX3 conda environment.
# ----------------------------------------------------------------------------------
# Copyright (c) 2026 Christofanis Skordas, The University of Chicago
# ----------------------------------------------------------------------------------

from argparse import Namespace
from pathlib import Path

from genx3_rcc.config import CONFIG_FILE, GenXConfig
from genx3_rcc.commands.install import _patch_main_window, _patch_parametergrid


def run(args: Namespace) -> None:
    if not CONFIG_FILE.exists():
        print(f"Error: {CONFIG_FILE} not found. Run 'genx-rcc configure' first.")
        return

    config = GenXConfig.load(CONFIG_FILE)
    env_path = Path.home() / ".conda" / "envs" / config.environment_name

    if not env_path.is_dir():
        print(f"Environment '{config.environment_name}' not found at {env_path}.")
        print("Run 'genx-rcc install' first.")
        return

    print(f"Applying patches to '{config.environment_name}'...")
    _patch_main_window(env_path, config.python_version)
    _patch_parametergrid(env_path, config.python_version)
    print("Done.")
