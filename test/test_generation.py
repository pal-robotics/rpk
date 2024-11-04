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

from ament_pep257.main import main as pep257_main
from ament_flake8.main import main_with_errors as flake8_main_with_errors
from ament_copyright.main import main as copyright_main
from pathlib import Path
import pytest
import tempfile

from rpk import rpk
rpk.PKG_PATH = (
    Path(rpk.__file__).parent.parent
)


@pytest.mark.parametrize('category, template, id, robot, path',
                         [
                            (category, tpl, 'test_skill', 'generic', tempfile.mkdtemp())
                            for category, tpls in rpk.TEMPLATES_FAMILIES.items()
                            for tpl in tpls["src"].keys()
                         ])
@pytest.mark.linter
@pytest.mark.pep257
@pytest.mark.flake8
@pytest.mark.copyright
def test_generation(category, template, id, robot, path):

    rpk.main(['create',
              '--robot', robot,
              '--path', path,
              category,
              '--template', template,
              '--yes'])

    rc = pep257_main(argv=[path, 'test'])
    assert rc == 0, 'Found PEP-257 code style errors / warnings'

    rc, errors = flake8_main_with_errors(argv=[path])
    assert rc == 0, \
        'Found PEP-008 %d code style errors / warnings:\n' % len(errors) + \
        '\n'.join(errors)

    rc = copyright_main(argv=[path, 'test'])
    assert rc == 0, 'Found copyright-related errors'
