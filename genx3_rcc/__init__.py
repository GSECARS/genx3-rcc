#!/usr/bin/env python
# ----------------------------------------------------------------------------------
# Project: Genx3-RCC
# File: genx3_rcc/__init__.py
# ----------------------------------------------------------------------------------
# Purpose:
# This file is used to initialize the genx3_rcc package.
# ----------------------------------------------------------------------------------
# Copyright (c) 2026 Christofanis Skordas, The University of Chicago
# ----------------------------------------------------------------------------------

from argparse import ArgumentParser


def main() -> None:
    """Main entry point for genx-rcc console script."""
    parser = ArgumentParser("GenX-RCC CLI")

    # List of CLI arguments
    args = parser.parse_args()

    parser.print_help()

