#! /usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (c) 2024 PAL Robotics S.L. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Main entry point for rpk - Robot Programming Kit."""

import argparse
import sys
from importlib.metadata import version

from rpk.common import (  # noqa: F401
    SELF_NAME,
    PKG_PATH,
    TPL_EXT,
    TEMPLATES_FAMILIES,
    ROBOTS_NAMES,
    ROBOTS_FEATURES,
    AVAILABLE_ROBOTS,
    Colors,
)

from rpk.commands.create import add_create_parser, run_create
from rpk.commands.list import add_list_parser, run_list
from rpk.commands.info import add_info_parser, run_info


def main(args=sys.argv[1:]):
    """Entry point for rpk CLI."""
    parser = argparse.ArgumentParser(
        description="Generate and manage application skeletons for "
                    "ROS 2-based robots"
    )

    parser.add_argument('--version', action='version',
                        version=f'{SELF_NAME} {version(SELF_NAME)}')

    subparsers = parser.add_subparsers(dest="command")

    # Add command parsers
    add_create_parser(subparsers)
    add_list_parser(subparsers)
    add_info_parser(subparsers)

    args = parser.parse_args(args)

    if not args.command:
        print(
            f"You must select a command.\n"
            f"Type '{SELF_NAME} --help' for details.")
        sys.exit(1)

    # Dispatch to command handlers
    if args.command == "create":
        run_create(args)
    elif args.command == "list":
        run_list(args)
    elif args.command == "info":
        run_info(args)


if __name__ == "__main__":
    main()
