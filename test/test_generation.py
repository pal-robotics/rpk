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

from pathlib import Path
import subprocess
import pytest
import tempfile

from ament_pep257.main import main as pep257_main
from ament_flake8.main import main_with_errors as flake8_main_with_errors
from ament_copyright.main import main as copyright_main

from rpk import rpk
rpk.PKG_PATH = (
    Path(rpk.__file__).parent.parent
)


@pytest.mark.parametrize('category, template, robot',
                         [
                            (category, tpl, robot)
                            for robot in rpk.AVAILABLE_ROBOTS
                            for category, tpls in rpk.TEMPLATES_FAMILIES.items()
                            for tpl in tpls["src"].keys()
                         ])
@pytest.mark.linter
@pytest.mark.pep257
@pytest.mark.flake8
@pytest.mark.copyright
def test_generation_linting(category, template, robot):

    path = tempfile.mkdtemp()

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


@pytest.mark.parametrize('category, template, robot',
                         [
                            (category, tpl, robot)
                            # for robot in rpk.AVAILABLE_ROBOTS
                            for robot in ['generic']
                            for category, tpls in rpk.TEMPLATES_FAMILIES.items()
                            for tpl in tpls["src"].keys()
                         ])
def test_generation_compile(category, template, robot):

    ws_dir = Path(tempfile.mkdtemp(suffix='_ws'))

    rpk.main(['create',
              '--robot', robot,
              '--path', str(ws_dir / "src"),
              category,
              '--template', template,
              '--id', 'test_node',
              '--yes'])

    # someone, somewhere, though it would be clever to force python not to write bytecode
    # when called in a subprocess. This is a problem when using colcon, as it will try to
    # compile the python files and will fail if it can't write the bytecode.
    # We need to unset this variable in order to compile
    completed_process = subprocess.run(" ".join(['PYTHONDONTWRITEBYTECODE=""',
                                                 'colcon',
                                                 '--log-level', 'error',
                                                 'build',
                                                 '--base-paths', str(ws_dir),
                                                 '--build-base', str(ws_dir / "build"),
                                                 '--install-base', str(ws_dir / "install"),
                                                 ]), shell=True, capture_output=True, check=True)

    # for some reason, the return code is always 0
    # assert completed_process.returncode == 0

    # ...instead, we need to check that there are no errors in the stderr
    assert completed_process.stderr == b'', (f"Error in template {category}/{template} "
                                             f"(robot: {robot}):\n"
                                             f"{completed_process.stderr.decode('utf-8')}")
