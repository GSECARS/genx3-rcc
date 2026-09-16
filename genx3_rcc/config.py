#!/usr/bin/env python
# ----------------------------------------------------------------------------------
# Project: GenX3-RCC
# File: genx3_rcc/config.py
# ----------------------------------------------------------------------------------
# Purpose:
# Dataclass representing the GenX3 configuration and helpers.
# ----------------------------------------------------------------------------------
# Copyright (c) 2026 Christofanis Skordas, The University of Chicago
# ----------------------------------------------------------------------------------

import subprocess
from dataclasses import dataclass
from pathlib import Path

CONFIG_FILE = Path("genx3.conf")


@dataclass
class GenXConfig:

    anaconda_module: str = "miniforge-26.5.3"
    gcc_module: str = "gcc/12.2.0"
    environment_name: str = "genxENV"
    python_version: str = "3.13"
    anaconda_packages: str = "contourpy h5py matplotlib mpi4py numba scipy wxpython"
    pypi_packages: str = "appdirs psutil pymysql vtk genx3"
    custom_model_path: str = "models"

    @property
    def env_path(self) -> Path:
        """Absolute path to the conda environment directory."""
        return Path.home() / ".conda" / "envs" / self.environment_name

    @property
    def python_bin(self) -> Path:
        """Absolute path to the Python binary inside the conda environment."""
        return self.env_path / "bin" / "python"

    def get_python_version(self) -> str:
        """Ask the environment's own Python binary for its major.minor version.

        This is always authoritative — it reflects what conda actually created,
        regardless of what python_version was requested in the config.
        """
        result = subprocess.run(
            [str(self.python_bin), "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
            capture_output=True, text=True, check=True,
        )
        return result.stdout.strip()

    def save(self, path: Path = CONFIG_FILE) -> None:
        lines = [
            f"anaconda_module={self.anaconda_module}",
            f"gcc_module={self.gcc_module}",
            f"environment_name={self.environment_name}",
            f"python_version={self.python_version}",
            f"anaconda_packages='{self.anaconda_packages}'",
            f"pypi_packages='{self.pypi_packages}'",
            f"custom_model_path={self.custom_model_path}",
        ]
        path.write_text("\n".join(lines) + "\n")

    @classmethod
    def load(cls, path: Path = CONFIG_FILE) -> "GenXConfig":
        config = cls()
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or "=" not in line:
                continue
            key, _, value = line.partition("=")
            value = value.strip("'")
            if hasattr(config, key):
                setattr(config, key, value)
        return config

