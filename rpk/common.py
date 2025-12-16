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

"""Common utilities and constants for rpk."""

import sys
from pathlib import Path
import yaml

import rpk

SELF_NAME = "rpk"

# not using ament, so that is also work outside of a ROS environment
PKG_PATH = (
    Path(rpk.__file__).parent.parent.parent.parent.parent / "share" /
    "rpk"
)

# Path to the templates configuration file
TEMPLATES_YAML_PATH = Path(rpk.__file__).parent / "templates.yaml"

# Template file extension
TPL_EXT = "j2"


def load_templates():
    """Load templates from the external YAML file."""
    with open(TEMPLATES_YAML_PATH, 'r') as f:
        config = yaml.safe_load(f)

    # Extract robots configuration
    robots_names = {k: v['name'] for k, v in config['robots'].items()}
    robots_features = {k: v['features'] for k, v in config['robots'].items()}

    # Extract template families and their sources
    skill_templates = config['skill_templates']
    intent_extractor_templates = config['intent_extractor_templates']
    task_templates = config['task_templates']
    mission_ctrl_templates = config['mission_ctrl_templates']
    application_templates = config['application_templates']

    # Build templates families dict with sources linked
    templates_families = {}
    family_config = config['template_families']

    templates_families['intent'] = {
        'src': intent_extractor_templates,
        'name': family_config['intent']['name'],
        'cmd': family_config['intent']['cmd'],
        'help': family_config['intent']['help']
    }
    templates_families['skill'] = {
        'src': skill_templates,
        'name': family_config['skill']['name'],
        'cmd': family_config['skill']['cmd'],
        'help': family_config['skill']['help']
    }
    templates_families['task'] = {
        'src': task_templates,
        'name': family_config['task']['name'],
        'cmd': family_config['task']['cmd'],
        'help': family_config['task']['help']
    }
    templates_families['mission'] = {
        'src': mission_ctrl_templates,
        'name': family_config['mission']['name'],
        'cmd': family_config['mission']['cmd'],
        'help': family_config['mission']['help']
    }
    templates_families['app'] = {
        'src': application_templates,
        'name': family_config['app']['name'],
        'cmd': family_config['app']['cmd'],
        'help': family_config['app']['help']
    }

    return (
        robots_names,
        robots_features,
        templates_families,
    )


# Load templates at module initialization
ROBOTS_NAMES, ROBOTS_FEATURES, TEMPLATES_FAMILIES = load_templates()
AVAILABLE_ROBOTS = list(ROBOTS_NAMES.keys())


class Colors:
    """
    ANSI color codes for terminal output.

    Colors are disabled if stdout is not a TTY.
    """

    _use_colors = sys.stdout.isatty()

    BOLD = "\033[1m" if _use_colors else ""
    CYAN = "\033[36m" if _use_colors else ""
    GREEN = "\033[32m" if _use_colors else ""
    YELLOW = "\033[33m" if _use_colors else ""
    RED = "\033[31m" if _use_colors else ""
    RESET = "\033[0m" if _use_colors else ""
