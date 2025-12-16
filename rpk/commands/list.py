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

"""The 'list' command for rpk."""

from rpk.common import Colors, TEMPLATES_FAMILIES


def add_list_parser(subparsers):
    """Add the 'list' subparser to the argument parser."""
    list_tpl_parser = subparsers.add_parser(
        "list", help="List all available templates"
    )

    list_tpl_parser.add_argument(
        "-s",
        "--short",
        action="store_true",
        help="only display the template' names",
    )

    return list_tpl_parser


def run_list(args):
    """Execute the 'list' command."""
    for family in TEMPLATES_FAMILIES.keys():
        tpls = TEMPLATES_FAMILIES[family]
        if not args.short:
            print(
                f"\n{Colors.BOLD}{Colors.CYAN}# {tpls['name']} "
                f"templates{Colors.RESET} ({Colors.YELLOW}rpk create "
                f"{tpls['cmd']} ...{Colors.RESET}):")
        for tpl in tpls["src"].keys():
            if args.short:
                print(f"{family}/{tpl}")
            else:
                desc = tpls['src'][tpl]['short_desc']
                print(
                    f" - {Colors.GREEN}{tpl}{Colors.RESET}: {desc}")
