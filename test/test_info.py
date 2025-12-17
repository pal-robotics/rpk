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

import pytest
import rpk
from rpk.common import TEMPLATES_FAMILIES

# Find a valid template to test with.
# We'll grab the first available one to ensure the test works with whatever templates are defined.
FIRST_FAMILY = list(TEMPLATES_FAMILIES.keys())[0]
FIRST_TEMPLATE = list(TEMPLATES_FAMILIES[FIRST_FAMILY]['src'].keys())[0]
VALID_TEMPLATE_ID = f"{FIRST_FAMILY}/{FIRST_TEMPLATE}"


def test_info_valid(capsys):
    rpk.main(['info', VALID_TEMPLATE_ID])
    captured = capsys.readouterr()

    assert "Template:" in captured.out
    assert VALID_TEMPLATE_ID in captured.out
    assert "Description:" in captured.out
    assert "Language:" in captured.out
    assert "Template paths:" in captured.out


def test_info_invalid_format(capsys):
    # This is caught by argparse choices now if it doesn't match any known template string
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        rpk.main(['info', 'invalidformat'])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2

    captured = capsys.readouterr()
    assert "invalid choice" in captured.err


def test_info_unknown_family(capsys):
    # Caught by argparse choices
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        rpk.main(['info', 'unknownfamily/template'])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2

    captured = capsys.readouterr()
    assert "invalid choice" in captured.err


def test_info_unknown_template(capsys):
    # Caught by argparse choices
    family = list(TEMPLATES_FAMILIES.keys())[0]

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        rpk.main(['info', f'{family}/unknowntemplate'])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2

    captured = capsys.readouterr()
    assert "invalid choice" in captured.err
