#!/usr/bin/env python3

# This file is part of M1M3 tests suite.
#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

########################################################################
# Test Numbers: M13T-003
# Author:       CContaxis
# Description:  Individual hardpoint displacement test
# Steps:
# - Transition from standby to parked engineering state
# - Perform the following steps for each hardpoint actuator
#   - Perform the following steps for full extension and full retraction
#     - Issue hardpoint step command
#     - Verify hardpoint is moving
#     - Wait for hardpoint motion to complete or a limit switch is operated
#     - Issue stop hardpoint motion command
#     - Verify hardpoint is stopped
#     - Query EFD for hardpoint monitor data for test duration
#     - Query EFD for hardpoint actuator data for test duration
# - Transition from parked engineering to standby state
########################################################################

import unittest

from M13T004 import M13T004


class M13T003(M13T004):
    pass


if __name__ == "__main__":
    unittest.main()
