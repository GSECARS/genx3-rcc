#!/usr/bin/env python
# ----------------------------------------------------------------------------------
# Project: GenX3-RCC
# File: genx3_rcc/commands/clean.py
# ----------------------------------------------------------------------------------
# Purpose:
# Removes the anaconda environment for GenX3
# ----------------------------------------------------------------------------------
# Copyright (c) 2026 Christofanis Skordas, The University of Chicago
# ----------------------------------------------------------------------------------

import shutil
import subprocess
import time
from argparse import Namespace
from pathlib import Path

from genx3_rcc.config import CONFIG_FILE, GenXConfig


def _shell(cmd: str) -> None:
    subprocess.run(["bash", "--login", "-c", cmd], check=True)


def run(args: Namespace) -> None:
    config = GenXConfig.load(CONFIG_FILE) if CONFIG_FILE.exists() else GenXConfig()

    env_path = Path.home() / ".conda" / "envs" / config.environment_name

    if not env_path.is_dir():
        print(f"Environment '{config.environment_name}' does not exist. Aborting.")
        return

    print("GenX3 anaconda environment cleanup")

    confirm = input(f"Remove environment '{config.environment_name}'? [y/N] ").strip().lower()
    if confirm not in ("y", "yes"):
        print("Aborted.")
        return

    start = time.monotonic()

    conda_sh = f"/software/python-{config.anaconda_module}-el7-x86_64/etc/profile.d/conda.sh"
    init = f"module load python/{config.anaconda_module} && module load {config.gcc_module} && source '{conda_sh}'"

    print(f"Removing environment '{config.environment_name}'...")
    _shell(f"{init} && conda env remove -n {config.environment_name} --yes")

    if env_path.is_dir():
        shutil.rmtree(env_path)

    elapsed = time.monotonic() - start
    minutes, seconds = divmod(int(elapsed), 60)
    print(f"\nElapsed time: {minutes} minutes and {seconds} seconds")

