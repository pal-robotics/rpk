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

# Re-export common symbols for backward compatibility
from rpk.common import (  # noqa: F401
    SELF_NAME,
    PKG_PATH,
    TPL_EXT,
    TEMPLATES_FAMILIES,
    ROBOTS_NAMES,
    ROBOTS_FEATURES,
    AVAILABLE_ROBOTS,
    Colors,
)

from rpk.rpk import main  # noqa: F401
