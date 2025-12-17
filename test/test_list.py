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

import rpk
from rpk.common import TEMPLATES_FAMILIES


def test_list_all(capsys):
    rpk.main(['list'])
    captured = capsys.readouterr()

    # Check for some expected content structure
    assert "#" in captured.out  # Header indicator
    assert "templates" in captured.out
    assert "rpk create" in captured.out
    assert " - " in captured.out  # List item indicator

    # Verify all templates from templates.yaml are listed
    for family in TEMPLATES_FAMILIES.keys():
        for tpl in TEMPLATES_FAMILIES[family]['src'].keys():
            assert tpl in captured.out


def test_list_short(capsys):
    rpk.main(['list', '--short'])
    captured = capsys.readouterr()

    # In short mode, we expect "family/template" format
    assert "/" in captured.out

    # We expect NO headers or list item indicators
    assert "#" not in captured.out
    assert " - " not in captured.out

    # Check for at least one known template family
    assert "skill/" in captured.out
