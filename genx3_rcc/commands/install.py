# ----------------------------------------------------------------------------------
# Project: GenX3-RCC
# File: genx3_rcc/commands/install.py
# ----------------------------------------------------------------------------------
# Purpose:
# Sets up the anaconda environment and installs GenX3 package.
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
    if not CONFIG_FILE.exists():
        print(f"Error: {CONFIG_FILE} not found. Run 'genx-rcc configure' first.")
        return

    config = GenXConfig.load(CONFIG_FILE)

    conda_sh = f"/software/python-{config.anaconda_module}-el7-x86_64/etc/profile.d/conda.sh"
    env_path = Path.home() / ".conda" / "envs" / config.environment_name

    if env_path.is_dir():
        print(f"Environment '{config.environment_name}' already exists. Aborting.")
        return

    print("Preparing anaconda environment for GenX3")

    start = time.monotonic()

    init = f"module load python/{config.anaconda_module} && module load {config.gcc_module} && source '{conda_sh}'"

    print("Adding conda-forge channel...")
    _shell(f"{init} && conda config --add channels conda-forge")

    print(f"Creating environment '{config.environment_name}'...")
    _shell(f"{init} && conda create -n {config.environment_name} python={config.python_version} {config.anaconda_packages} --yes")

    print("Updating pip and installing PyPI packages...")
    pip = env_path / "bin" / "pip"
    subprocess.run([str(pip), "install", "-U", "pip", "setuptools"], check=True)
    subprocess.run([str(pip), "install"] + config.pypi_packages.split(), check=True)

    print("Copying custom models...")
    models_dir = env_path / "lib" / f"python{config.python_version}" / "site-packages" / "genx" / "models"
    custom = Path(config.custom_model_path)
    if custom.is_file():
        shutil.copy(custom, models_dir)
        print(f"Copied {custom} to {models_dir}")
    elif custom.is_dir():
        for f in custom.iterdir():
            shutil.copy(f, models_dir)
        print(f"Copied models from {custom} to {models_dir}")
    else:
        print("No custom models added.")

    elapsed = time.monotonic() - start
    minutes, seconds = divmod(int(elapsed), 60)
    print(f"\nElapsed time: {minutes} minutes and {seconds} seconds")

    selection = input("\nDo you want to start GenX3? [Y/n] ").strip().lower() or "y"
    if selection in ("y", "yes"):
        _shell(f"{init} && conda activate {config.environment_name} && genx")

