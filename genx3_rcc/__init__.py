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

from genx3_rcc.commands import configure


def main() -> None:
    """Main entry point for genx-rcc console script."""
    parser = ArgumentParser("GenX-RCC CLI", description="University of Chicago RCC configuration scripts for GenX3.")
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    subparsers.add_parser("configure", help="Interactively configure the GenX3 installation.")

    args = parser.parse_args()

    match args.command:
        case "configure":
            configure.run(args)
        case _:
            parser.print_help()

