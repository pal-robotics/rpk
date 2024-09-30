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

import sys
import argparse
from pathlib import Path
from jinja2 import Environment, select_autoescape, FileSystemLoader

import rpk

SELF_NAME = "rpk"

# not using ament, so that is also work outside of a ROS environment
PKG_PATH = (
    Path(rpk.__file__).parent.parent.parent.parent.parent / "share" /
    "rpk"
)

SKILL_TEMPLATES = {
    "base_python": {
        "tpl_paths": ["skills/base_python/{{id}}"],
        "short_desc": "base skill template. Written in Python",
        "post_install_help": "Check README.md in ./{path}/ and edit src/{id}/skill_impl.py to implement your skill logic.",
    },
    "db_connector_python": {
        "tpl_paths": ["skills/db_connector_python/{{id}}", "skills/sample_skill_msgs"],
        "short_desc": "simple skill template, mocking-up a database connector. Written in Python",
        "post_install_help": "Check README.md in ./{path}/ and edit src/{id}/skill_impl.py to implement your skill logic.",
    },
    "ollama_connector_python": {
        "tpl_paths": ["skills/ollama_connector_python/{{id}}", "skills/llm_msgs"],
        "short_desc": "skill example, offering a bridge to LLMs via ollama. Written in Python",
        "post_install_help": "Check README.md in ./{path}/ and edit src/{id}/skill_impl.py to implement your skill logic.",
    }
}

TASK_TEMPLATES = {
    "greet_task_python": {
        "tpl_paths": ["tasks/greet_task_python/{{id}}", "tasks/greet_task_msgs"],
        "short_desc": "simple task template, implementing a very basic greeting activity. Written in Python",
        "post_install_help": "Check README.md in ./{path}/ and edit src/{id}/task_impl.py to implement your task logic.",
        "skill_templates": [{"db_connector_python": {"id": "db_connector", "name": "Custom database connector"}}],
    }
}

MISSION_CTRL_TEMPLATES = {
    "base_python": {
        "tpl_paths": ["mission_ctrls/base_python/{{id}}"],
        "short_desc": "robot supervisor implemented as a simple Python script",
        "post_install_help": "Check README.md in ./{path}/ and edit src/{id}/mission_controller.py to implement your application logic.",
    },
    "llm_supervisor_python": {
        "tpl_paths": ["mission_ctrls/llm_supervisor_python/{{id}}"],
        "short_desc": "sample Python supervisor, using LLM to manage interactions with users",
        "post_install_help": "Check README.md in ./{path}/ and edit src/{id}/mission_controller.py to customize your application logic.",
        "task_templates": [{"greet_task_python": {"id": "greet_task", "name": "'greet' task"}}],
        "skill_templates": [{"ollama_connector_python": {"id": "ollama_connector", "name": "Bridge with a ollama server"}}],
    }
}


APPLICATION_TEMPLATES = {
    "llm_chatbot_python": {
        "tpl_paths": ["apps/python/{{id}}"],
        "short_desc": "a full sample application, using LLM to interact with users. It includes a supervisor and custom tasks and skills.",
        "post_install_help": "Check README.md in ./{path}/ to learn how to configure and start your application.",
        "mission_ctrl_templates": [{"llm_supervisor_python": {"id": "llm_supervisor", "name": "LLM-based mission controller"}}],
    }
}

TEMPLATES_FAMILIES = {
    "skill": {"src": SKILL_TEMPLATES,
              "name": "skill",
              "help": "short-term 'atomic' robot action, to be re-used by tasks and mission controllers. Examples: 'go to', 'say', 'perform pre-recorded motion'"},
    "task": {"src": TASK_TEMPLATES,
              "name": "task",
              "help": "time-limited robot activity, started by the mission controller. Might use skills. Examples: 'greet person', 'fetch object'"},
    "mission": {"src": MISSION_CTRL_TEMPLATES,
                "name": "mission controller",
                "help": "manages the whole behaviour of the robot. Examples: 'receptionist', 'waiter'"},
    "app": {"src": APPLICATION_TEMPLATES,
            "name": "application",
            "help": "complete application including a mission controller, a sample task and skill, and sample resources"}
}

AVAILABLE_ROBOTS = ["generic", "ari", "tiago"]

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
    except LookupError:
        # template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        # message = template.format(type(ex).__name__, ex.args)
        # print(message)
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


def interactive_create(id=None, family=None, template=None, robot=None):

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
        "Full name of your skill/application? (eg 'The Receptionist Robot' or 'Database connector', press "
        "Return to use the ID. You can change it later)\n"
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
        except IndexError:
            family = ""

    tpls = TEMPLATES_FAMILIES[family]["src"]
    while not template:
        print("\nWhat kind of mission controller do you want to create?")
        for idx, tpl in enumerate(tpls.keys()):
            print("%s: %s" %
                  (idx + 1, tpls[tpl]["short_desc"]))

        try:
            if len(tpls) == 1:
                # if only one template available, make it the default choice
                choice = int(input(
                    f"\nYour choice? (default: 1: {tpls[list(tpls.keys())[0]]['short_desc']}) ").strip() or 1)
            else:
                choice = int(input("\nYour choice? ").strip())

            template = list(tpls.keys())[choice - 1]
        except IndexError:
            template = ""

    while not robot:
        print("\nWhat robot are you targeting?")
        for idx, r in enumerate(AVAILABLE_ROBOTS):
            print("%s: %s" % (idx + 1, r))

        try:
            choice = int(
                input(f"\nYour choice? (default: 1: {AVAILABLE_ROBOTS[0]}) ").strip() or 1)

            robot = AVAILABLE_ROBOTS[choice - 1]
        except IndexError:
            robot = ""

    return id, name, family, template, robot

def generate_skeleton(data, family, tpl_name, robot, root):
    
    print(f"Generating {family} skeleton in {root}...")
    tpl = TEMPLATES_FAMILIES[family]["src"][tpl_name]

    data["dependencies"] = []

    # if needed, first generate the skeletons for the missions, skills and tasks
    # referenced in the template
    for additional_tpl in ["skill_templates", "task_templates", "mission_ctrl_templates"]:
        if additional_tpl in tpl:
            type = additional_tpl.split("_")[0]
            for a_tpl in tpl[additional_tpl]:
                tpl_name = list(a_tpl.keys())[0]
                a_data = dict(data)
                a_data["id"] = a_tpl[tpl_name]["id"]
                data["dependencies"].append(a_data["id"])
                a_data["name"] = a_tpl[tpl_name]["name"]
                generate_skeleton(a_data, type, tpl_name , robot, root)

    # then generate the skeleton for the current template
    tpl_paths = [PKG_PATH / "tpl" / p for p in tpl["tpl_paths"]]

    for tpl_path in tpl_paths:
        env = Environment(
            loader=FileSystemLoader(str(tpl_path)),
            autoescape=select_autoescape(),
            trim_blocks=True,
        )

        j2_tpls = env.list_templates(extensions=TPL_EXT)

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
            j2_tpl = env.get_template(j2_tpl_name)
            j2_tpl_name = j2_tpl_name.replace("{{id}}", data["id"])

            # 'base' is the name of the package directory
            base = root / tpl_path.name.replace("{{id}}", data["id"])
            base.mkdir(parents=True, exist_ok=True)

            filename = base / j2_tpl_name[: -(1 + len(TPL_EXT))]
            filename.parent.mkdir(parents=True, exist_ok=True)
            print(f"Creating {filename}...")
            with open(filename, "w") as fh:
                fh.write(j2_tpl.render(data))


    print("\n\033[32;1mDone!")
    print("\033[33;1m")
    print(tpl["post_install_help"].format(
        path=root, id=data["id"]))
    print("\033[0m")


def main():

    parser = argparse.ArgumentParser(
        description="Generate and manage application skeletons for ROS2-based "
                    "robots"
    )

    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser(
        "create", help="Create new application/task/skill skeletons"
    )

    create_parser.add_argument(
        "-r",
        "--robot",
        choices=AVAILABLE_ROBOTS,
        type=str,
        nargs="?",
        help="target robot.",
    )

    family_subparsers = create_parser.add_subparsers(dest="family")
    for family in TEMPLATES_FAMILIES.keys():
        f_parser = family_subparsers.add_parser(
            family, help=TEMPLATES_FAMILIES[family]["help"]
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

    args = parser.parse_args()

    if not args.command:
        print(f"You must select a command.\nType '{SELF_NAME} --help' for details.")
        sys.exit(1)

    if args.command == "create" and not hasattr(args, "template"):
        print(f"You must select a type of content.\nType '{SELF_NAME} create --help' for details.")
        sys.exit(1)

    intents = get_intents()

    id, name, family, tpl_name, robot = interactive_create(
        args.id, args.family, args.template, args.robot)

    data = {"id": id, "name": name, "intents": intents, "robot": robot}

    root = Path(args.path)
    root.mkdir(parents=True, exist_ok=True)

    generate_skeleton(data, family, tpl_name, robot, root)


if __name__ == "__main__":
    main()
