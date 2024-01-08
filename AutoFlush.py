#!/usr/bin/env python3

# This file is part of M1M3 test suite.
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

import io


class AutoFlush:
    """Automatic file flusher.

    Parameters
    ----------
    file : `file`
        File where message will be printed.
    flushAfter : `int`
        Fliush after this number of lines. Default to 10.
    """

    def __init__(self, file: io.TextIOWrapper, flushAfter:int=10):
        self._file = file
        self._flushAfter = flushAfter
        self._counter = 0

    def __getattr__(self, name:str) -> str:
        return getattr(self._file, name)

    def print(self, message: str) -> None:
        print(message, file=self._file)

        self._counter += 1
        if self._counter >= self._flushAfter:
            self._file.flush()
            self._counter = 0
