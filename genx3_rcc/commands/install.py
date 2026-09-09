#!/usr/bin/env python
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


_SPLASH_PATCHES = [
    # 1. Add _safe_destroy_splash helper and make WriteSplash resilient
    (
        "    def WriteSplash(self, text, progress=0.0):\n"
        "        image = self.splash.GetBitmap()\n"
        "        self._draw_bmp(image, text, progress=progress)\n"
        "        self.splash.Refresh()\n"
        "        self.splash.Update()\n"
        "        wx.YieldIfNeeded()\n",
        "    def _safe_destroy_splash(self):\n"
        "        try:\n"
        "            self.splash.Destroy()\n"
        "        except RuntimeError:\n"
        "            pass\n"
        "\n"
        "    def WriteSplash(self, text, progress=0.0):\n"
        "        try:\n"
        "            image = self.splash.GetBitmap()\n"
        "        except RuntimeError:\n"
        "            return\n"
        "        self._draw_bmp(image, text, progress=progress)\n"
        "        try:\n"
        "            self.splash.Refresh()\n"
        "            self.splash.Update()\n"
        "        except RuntimeError:\n"
        "            return\n"
        "        wx.YieldIfNeeded()\n",
    ),
    # 2. Guard the direct self.splash.Destroy() call
    (
        "        if self.open_file is None:\n"
        "            self.splash.Destroy()\n"
        "            if first_init:\n",
        "        if self.open_file is None:\n"
        "            try:\n"
        "                self.splash.Destroy()\n"
        "            except RuntimeError:\n"
        "                pass\n"
        "            if first_init:\n",
    ),
    # 3. Replace wx.CallAfter(self.splash.Destroy) with _safe_destroy_splash
    (
        "            wx.CallAfter(self.splash.Destroy)\n"
        "            return 1\n",
        "            wx.CallAfter(self._safe_destroy_splash)\n"
        "            return 1\n",
    ),
    (
        "        wx.CallAfter(self.splash.Destroy)\n"
        "        wx.CallLater(",
        "        wx.CallAfter(self._safe_destroy_splash)\n"
        "        wx.CallLater(",
    ),
]


def _patch_main_window(env_path: Path, python_version: str) -> None:
    target = env_path / "lib" / f"python{python_version}" / "site-packages" / "genx" / "gui" / "main_window.py"
    if not target.exists():
        print(f"Warning: {target} not found, skipping splash patch.")
        return
    source = target.read_text()
    for old, new in _SPLASH_PATCHES:
        if old in source:
            source = source.replace(old, new)
        elif new not in source:
            print(f"Warning: splash patch chunk not found and not already applied:\n  {old[:60]!r}...")
    target.write_text(source)
    print(f"Splash patch applied to {target}")


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

    print(f"Creating environment '{config.environment_name}'...")
    _shell(f"{init} && conda create -n {config.environment_name} python={config.python_version} {config.anaconda_packages} --yes")

    print("Updating pip and installing PyPI packages...")
    pip = env_path / "bin" / "pip"
    subprocess.run([str(pip), "install", "-U", "pip", "setuptools"], check=True)
    subprocess.run([str(pip), "install"] + config.pypi_packages.split(), check=True)

    print("Applying splash screen patch...")
    _patch_main_window(env_path, config.python_version)

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

