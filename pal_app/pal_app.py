#! /usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (c) 2024 PAL Robotics S.L. All rights reserved.

# Unauthorized copying of this file, via any medium is strictly prohibited,
# unless it was supplied under the terms of a license agreement or
# nondisclosure agreement with PAL Robotics SL. In this case it may not be
# copied or disclosed except in accordance with the terms of that agreement.

import sys
import argparse
from pathlib import Path
from jinja2 import Environment, select_autoescape, FileSystemLoader

import pal_app
PKG_PATH = (
    Path(pal_app.__file__).parent.parent.parent.parent.parent / "share" /
    "pal_app"
)

AVAILABLE_TEMPLATES = {
    "python": {
        "tpl_path": "python_script",
        "short_desc": "simple Python script",
        "post_install_help": "Check README.md in ./{path}/ and edit src/{id}/"
        "application_controller.py to implement your application logic.",
    }
}

AVAILABLE_ROBOTS = ["ARI"]

TPL_EXT = "j2"


def get_intents():

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
    except Exception:
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


def interactive_create(id=None, template=None, robot=None):

    if id and (" " in id or "-" in id):
        print("The chosen ID can not contain spaces or hyphens.")
        id = None

    while not id:
        id = input(
            "ID of your application? (must be a valid ROS identifier without "
            "spaces or hyphens. eg 'robot_receptionist')\n"
        )

        if " " in id or "-" in id:
            print("The chosen ID can not contain spaces or hyphens.")
            id = None

    name = input(
        "Full name of your application? (eg 'The Receptionist Robot', press "
        "Return to skip)\n"
    )

    if not name:
        name = id

    while not robot:
        print("\nWhat robot are you targeting?")
        for idx, r in enumerate(AVAILABLE_ROBOTS):
            print("%s: %s" % (idx + 1, r))

        try:
            choice = int(input("\nYour choice? "))

            robot = AVAILABLE_ROBOTS[choice - 1]
        except Exception:
            robot = ""

    while not template:
        print("\nWhat kind of application controller do you want to create?")
        for idx, tpl in enumerate(AVAILABLE_TEMPLATES.keys()):
            print("%s: %s" % (idx + 1, AVAILABLE_TEMPLATES[tpl]["short_desc"]))

        try:
            choice = int(input("\nYour choice? "))

            template = list(AVAILABLE_TEMPLATES.keys())[choice - 1]
        except Exception:
            template = ""

    return id, name, template, robot


def main():

    parser = argparse.ArgumentParser(
        description="Generate and manage application skeletons for ROS2-based "
                    "robots"
    )
    #     parser.add_argument(
    #         "-f",
    #         "--force",
    #         action="store_true",
    #         help="if set, force overwriting existing documentation",
    #     )
    #

    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser(
        "create", help="Create a new application skeleton"
    )
    create_parser.add_argument(
        "-i",
        "--id",
        type=str,
        nargs="?",
        help="ID of your application. Must be a valid ROS2 identifier, without "
             "spaces or hyphens.",
    )

    create_parser.add_argument(
        "-r",
        "--robot",
        choices=AVAILABLE_ROBOTS,
        type=str,
        nargs="?",
        help="target robot.",
    )

    create_parser.add_argument(
        "-t",
        "--template",
        choices=AVAILABLE_TEMPLATES.keys(),
        type=str,
        nargs="?",
        help="Template to use.",
    )

    create_parser.add_argument(
        "path",
        type=str,
        nargs="?",
        const=".",
        default=".",
        help="path of the directory where the skeleton will be generated "
             "(default: .)",
    )

    args = parser.parse_args()

    if not args.command:
        print("You must select a command.\nType 'pal_app --help' for details.")
        sys.exit(1)

    intents = get_intents()

    id, name, tpl, robot = interactive_create(
        args.id, args.template, args.robot)

    data = {"id": id, "name": name, "intents": intents, "robot": robot}

    root = Path(args.path) / id
    root.mkdir(parents=True, exist_ok=True)

    print("Generating application skeleton in %s..." % root)

    if tpl == "python":
        tpl_path = PKG_PATH / "tpl" / AVAILABLE_TEMPLATES[tpl]["tpl_path"]

        env = Environment(
            loader=FileSystemLoader(str(tpl_path)),
            autoescape=select_autoescape(),
            trim_blocks=True,
        )

        tpls = env.list_templates(extensions=TPL_EXT)

        if not tpls:
            print(
                "Error! no app template found for %s. I was looking for "
                "template files under <%s>. It seems pal_app is not correctly "
                "installed."
                % (tpl, tpl_path)
            )
            sys.exit(1)

        for tpl_name in tpls:
            j_tpl = env.get_template(tpl_name)
            tpl_name = tpl_name.replace("{{id}}", data["id"])
            filename = root / tpl_name[: -(1 + len(TPL_EXT))]
            filename.parent.mkdir(parents=True, exist_ok=True)
            print("Creating %s..." % filename)
            with open(filename, "w") as fh:
                fh.write(j_tpl.render(data))

        print("\n\033[32;1mDone!")
        print("\033[33;1m")
        print(AVAILABLE_TEMPLATES[tpl]["post_install_help"].format(
            path=root, id=id))
        print("\033[0m")

    else:
        print("No template available for %s! Cannot generate an app "
              "skeleton." % tpl)
        sys.exit(1)


if __name__ == "__main__":
    main()
