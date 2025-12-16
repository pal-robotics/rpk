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

"""The 'create' command for rpk."""

import datetime
from jinja2 import Environment, select_autoescape, FileSystemLoader
import random
import re
import string
import sys
from pathlib import Path
import shutil

from rpk.common import (
    SELF_NAME,
    PKG_PATH,
    TPL_EXT,
    TEMPLATES_FAMILIES,
    ROBOTS_NAMES,
    ROBOTS_FEATURES,
    AVAILABLE_ROBOTS,
)


def random_id():
    """Generate a random 5-character lowercase ID."""
    rand_id = ''.join(random.choices(string.ascii_lowercase, k=5))
    print(f"Using random ID {rand_id}")
    return rand_id


def get_intents():
    """Get available intents from ROS message definitions."""
    intents = []

    try:
        from rosidl_runtime_py import get_interface_path
        from rosidl_adapter.parser import parse_message_file
    except ImportError:
        print(
            "rosidl_runtime_py or rosidl_adapter are not installed -- we "
            "cannot automatically generate the list of available intents"
        )
        return intents

    try:
        msg_def = parse_message_file(
            'hri_actions_msgs',
            get_interface_path('hri_actions_msgs/msg/Intent'))
    except LookupError:
        print(
            "Intent.msg not found. You can install it with 'apt install "
            "pal-alum-hri-actions-msgs'.\nFor now, not generating the list "
            "of available intents."
        )
        return intents

    # We will only extract the available intents for now, not the additional
    # fields (description and thematic roles) since rosidl parser ignores
    # comments below the message fields. To solve this, we should place the
    # long description of the intents before describing the msg fields.
    for c in msg_def.constants:
        if "__intent_" in c.value:
            intents.append({'intent': c.name,
                            'description': '',
                            'required_thematic_roles': [],
                            'optional_thematic_roles': []})
    if not intents:
        print(
            "Intent.msg empty :-( Not generating the intents handling code")
        return intents

    return intents


def interactive_create(id=None,
                       name=None,
                       family=None,
                       template=None,
                       robot=None,
                       yes=False):
    """Interactively prompt user for template creation parameters."""
    # apply subset of topic name rules to the ID, since it may be used in pkg topics names
    valid_id = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*$")

    if not id and yes:
        id = random_id()

    try:
        while not id:
            id = input(
                "ID of your application? (must be a valid ROS identifier without "
                "spaces or hyphens. eg 'robot_receptionist')\n"
            )

            if not valid_id.fullmatch(id):
                print("The chosen ID can only contain alphanumeric or '_' characters,"
                      " and cannot start with a number.")
                id = None

        if not name and not yes:
            name = input(
                "Full name of your skill/application? (eg 'The Receptionist Robot' or "
                "'Database connector', press Return to use the ID. You can change it later)\n"
            )

        if not name:
            name = id

        # get the user to choose between mission controller, skill or full
        # application
        while not family:
            print("\nWhat content do you want to create?")
            for idx, family in enumerate(TEMPLATES_FAMILIES.keys()):
                print("%s: %s" % (idx + 1, TEMPLATES_FAMILIES[family]["name"]))

            try:
                choice = int(input("\nYour choice? "))
                family = list(TEMPLATES_FAMILIES.keys())[choice - 1]
            except (ValueError, IndexError):
                family = ""

        tpls = TEMPLATES_FAMILIES[family]["src"]

        if not tpls:
            print("No templates available for %s. Exiting." % family)
            sys.exit(1)

        while not template:
            print("\nChoose a template:")
            for idx, tpl in enumerate(tpls.keys()):
                print("%s: %s" %
                      (idx + 1, tpls[tpl]["short_desc"]))

            try:
                if len(tpls) == 1:
                    # if only one template available, make it the default choice
                    choice = int(input(
                        "\nYour choice? (default: 1: "
                        f"{tpls[list(tpls.keys())[0]]['short_desc']}) ").strip() or 1)
                else:
                    choice = int(input("\nYour choice? ").strip())

                template = list(tpls.keys())[choice - 1]
            except (ValueError, IndexError):
                template = ""

        if not robot and yes:
            robot = AVAILABLE_ROBOTS[0]

        while not robot:
            print("\nWhat robot are you targeting?")
            for idx, r in enumerate(AVAILABLE_ROBOTS):
                print(f"{idx + 1}: {ROBOTS_NAMES[r]} ({r})")

            try:
                choice = int(
                    input(f"\nYour choice? (default: 1: {AVAILABLE_ROBOTS[0]}) ").strip() or 1)

                robot = AVAILABLE_ROBOTS[choice - 1]
            except (ValueError, IndexError):
                robot = ""
    except KeyboardInterrupt:
        sys.exit(1)

    return id, name, family, template, robot


def is_template_enabled(template, features):
    """Check if a template is enabled based on robot features."""
    if "only_if" not in template:
        return True

    # check if the template is enabled for the current robot features
    for feature in template["only_if"]:
        if feature.startswith("!"):
            if feature[1:] in features:
                return False
        else:
            if feature not in features:
                return False
    return True


def generate_skeleton(data, family, tpl_name, robot, root):
    """Generate a skeleton from a template."""
    print(f"Generating {family} skeleton in {root.resolve()}...")
    tpl = TEMPLATES_FAMILIES[family]["src"][tpl_name]

    data["dependencies"] = []

    # if needed, first generate the skeletons for the missions, skills and tasks
    # referenced in the template
    for additional_tpl in ["intent_extractor_templates",
                           "skill_templates",
                           "task_templates",
                           "mission_ctrl_templates"]:
        if additional_tpl in tpl:
            type = additional_tpl.split("_")[0]
            for a_tpl in tpl[additional_tpl]:
                tpl_name = list(a_tpl.keys())[0]
                if not is_template_enabled(a_tpl[tpl_name], data["features"]):
                    print(
                        f"Skipping {type} template {a_tpl} as it is not enabled for "
                        f"{robot} ({data['features']})")
                    continue
                a_data = dict(data)
                a_data["id"] = a_tpl[tpl_name]["id"].replace(
                    "{{id}}", data["id"]).replace("{{Id}}", data["Id"])
                a_data["Id"] = string.capwords(
                    a_data["id"], '_').replace("_", "")
                data["dependencies"].append(a_data["id"])
                a_data["name"] = a_tpl[tpl_name]["name"]
                generate_skeleton(a_data, type, tpl_name, robot, root)

    # then generate the skeleton for the current template
    tpl_paths = [PKG_PATH / "tpl" / p for p in tpl["tpl_paths"]]

    for tpl_path in tpl_paths:
        env = Environment(
            loader=FileSystemLoader(str(tpl_path)),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        j2_tpls = env.list_templates()

        if not j2_tpls:
            print(
                "Error! no app template found for %s. I was looking for "
                f"template files under <%s>. It seems {SELF_NAME} is not correctly "
                "installed."
                % (tpl, tpl_path)
            )
            sys.exit(1)

        for j2_tpl_name in j2_tpls:
            if (("pages_only_ari" in j2_tpl_name) and (robot not in j2_tpl_name)):
                continue

            # 'base' is the name of the package directory
            base = root / \
                tpl_path.name.replace("{{id}}", data["id"]).replace(
                    "{{Id}}", data["Id"])
            base.mkdir(parents=True, exist_ok=True)

            # Non-template file, copy file as is
            if j2_tpl_name.split('.')[-1] != TPL_EXT:
                source_filename = tpl_path / j2_tpl_name
                filename = base / j2_tpl_name
                filename.parent.mkdir(parents=True, exist_ok=True)
                print(f"Creating {filename}...")
                shutil.copy(source_filename, filename)
            else:
                j2_tpl = env.get_template(j2_tpl_name)
                j2_tpl_name = j2_tpl_name.replace(
                    "{{id}}", data["id"]).replace("{{Id}}", data["Id"])

                filename = base / j2_tpl_name[: -(1 + len(TPL_EXT))]
                filename.parent.mkdir(parents=True, exist_ok=True)
                print(f"Creating {filename}...")
                with open(filename, "w") as fh:
                    fh.write(j2_tpl.render(data))

    print("\n\033[32;1mDone!")
    print("\033[33;1m")
    print(tpl["post_install_help"].format(
        path=root.resolve(), id=data["id"]))
    print("\033[0m")


def add_create_parser(subparsers):
    """Add the 'create' subparser to the argument parser."""
    create_parser = subparsers.add_parser(
        "create", help="Create new application/task/skill skeletons"
    )

    create_parser.add_argument(
        "-r",
        "--robot",
        choices=AVAILABLE_ROBOTS,
        type=str,
        nargs="?",
        help="target robot",
    )

    family_subparsers = create_parser.add_subparsers(dest="family")
    for family in TEMPLATES_FAMILIES.keys():
        f_parser = family_subparsers.add_parser(
            family, help=TEMPLATES_FAMILIES[family]["help"]
        )

        f_parser.add_argument(
            "-y",
            "--yes",
            action="store_true",
            help="do not ask questions, automatically accept defaults",
        )

        f_parser.add_argument(
            "-t",
            "--template",
            choices=TEMPLATES_FAMILIES[family]["src"].keys(),
            type=str,
            nargs="?",
            help="Template to use.",
        )

        f_parser.add_argument(
            "-i",
            "--id",
            type=str,
            nargs="?",
            help="ID of your application. Must be a valid ROS2 identifier, without "
            "spaces or hyphens.",
        )

    create_parser.add_argument(
        "-p",
        "--path",
        type=str,
        nargs="?",
        const=".",
        default=".",
        help="path of the directory where the skeleton will be generated "
             "(default: .)",
    )

    return create_parser


def run_create(args):
    """Execute the 'create' command."""
    if not hasattr(args, "template"):
        print("You must select a type of content.\n"
              f"Type '{SELF_NAME} create --help' for details.")
        sys.exit(1)

    intents = get_intents()

    id, name, family, tpl_name, robot = interactive_create(
        args.id,
        name=None,
        family=args.family,
        template=args.template,
        robot=args.robot,
        yes=args.yes)

    data = {"id": id,
            "Id": string.capwords(id, '_').replace("_", ""),
            "name": name,
            "intents": intents,
            "robot": robot,
            "robot_name": ROBOTS_NAMES[robot],
            "features": ROBOTS_FEATURES[robot],
            "author": "TODO",
            "year": datetime.datetime.now().year}

    root = Path(args.path)
    root.mkdir(parents=True, exist_ok=True)

    generate_skeleton(data, family, tpl_name, robot, root)
