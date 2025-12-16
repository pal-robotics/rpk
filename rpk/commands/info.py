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

"""The 'info' command for rpk."""

import sys

from rpk.common import Colors, TEMPLATES_FAMILIES


def add_info_parser(subparsers):
    """Add the 'info' subparser to the argument parser."""
    info_parser = subparsers.add_parser(
        "info", help="Show detailed information about a template"
    )

    # Build list of all available templates for autocompletion
    all_templates = []
    for family in TEMPLATES_FAMILIES.keys():
        for tpl in TEMPLATES_FAMILIES[family]["src"].keys():
            all_templates.append(f"{family}/{tpl}")

    info_parser.add_argument(
        "template",
        type=str,
        choices=all_templates,
        metavar="TEMPLATE",
        help="Template name in format 'family/template' "
             "(e.g., 'skill/base_python'). "
             "Use 'rpk list --short' to see all available templates.",
    )

    return info_parser


def run_info(args):
    """Execute the 'info' command."""
    # Parse the template argument
    try:
        family, tpl_name = args.template.split("/", 1)
    except ValueError:
        print(f"{Colors.RED}Error:{Colors.RESET} Invalid template format. "
              f"Use 'family/template' format (e.g., 'skill/base_python').")
        sys.exit(1)

    if family not in TEMPLATES_FAMILIES:
        print(f"{Colors.RED}Error:{Colors.RESET} Unknown family '{family}'.")
        sys.exit(1)

    tpls = TEMPLATES_FAMILIES[family]["src"]
    if tpl_name not in tpls:
        print(
            f"{Colors.RED}Error:{Colors.RESET} Unknown template "
            f"'{tpl_name}' in family '{family}'.")
        sys.exit(1)

    tpl = tpls[tpl_name]

    # Display template info
    print(
        f"\n{Colors.BOLD}{Colors.CYAN}Template:{Colors.RESET} "
        f"{Colors.GREEN}{family}/{tpl_name}{Colors.RESET}")
    print(f"{Colors.BOLD}Description:{Colors.RESET} {tpl['short_desc']}")
    lang = tpl.get('prog_lang', 'N/A')
    print(f"{Colors.BOLD}Language:{Colors.RESET} {lang}")
    paths = ', '.join(tpl['tpl_paths'])
    print(f"{Colors.BOLD}Template paths:{Colors.RESET} {paths}")

    # Display dependencies
    dep_types = [
        ("skill_templates", "Skill dependencies"),
        ("task_templates", "Task dependencies"),
        ("intent_extractor_templates", "Intent extractor dependencies"),
        ("mission_ctrl_templates", "Mission controller dependencies"),
    ]

    has_deps = False
    for dep_key, dep_label in dep_types:
        if dep_key in tpl:
            if not has_deps:
                print(
                    f"\n{Colors.BOLD}{Colors.YELLOW}"
                    f"Dependencies:{Colors.RESET}")
                has_deps = True
            print(f"  {Colors.CYAN}{dep_label}:{Colors.RESET}")
            for dep in tpl[dep_key]:
                dep_name = list(dep.keys())[0]
                dep_config = dep[dep_name]
                dep_id = dep_config.get('id', '<id>')
                dep_desc = dep_config.get('name', '')
                only_if = dep_config.get('only_if', [])
                if only_if:
                    only_if_str = f" (only if: {', '.join(only_if)})"
                else:
                    only_if_str = ""
                print(
                    f"    - {Colors.GREEN}{dep_name}{Colors.RESET} "
                    f"(id: {dep_id}){only_if_str}")
                if dep_desc:
                    print(f"      {dep_desc}")

    if not has_deps:
        print(f"\n{Colors.BOLD}Dependencies:{Colors.RESET} None")

    # Usage hint
    print(f"\n{Colors.BOLD}Usage:{Colors.RESET}")
    print(f"  rpk create {family} -t {tpl_name} -i <your_id>")
    print()
