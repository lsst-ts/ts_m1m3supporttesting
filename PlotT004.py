#!/usr/bin/env python3

# This file is part of ts_salobj.
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

import argparse
import math

import matplotlib.pyplot as plt
import pandas as pd

parser = argparse.ArgumentParser(
    description="Plot Hardpoints data", usage="%(prog)s [files..]"
)
parser.add_argument("files", type=str, nargs="+", help="files to plot")
parser.add_argument(
    "-z",
    dest="zero",
    action="store",
    type=int,
    default=None,
    help="plot only regions around 0 force",
)

args = parser.parse_args()

rowscols = math.ceil(math.sqrt(len(args.files)))
maxcols = math.ceil(len(args.files) / rowscols)

print(f"Subplots: {rowscols}, {maxcols}")
fig, axes = plt.subplots(rowscols, maxcols)

count = 0


def plot(fn):
    global count, args
    print(f"Plotting {fn}", end="")
    df = pd.read_csv(fn)
    print(" .", end="")

    if args.zero is not None:
        df_sort = df.iloc[(df[df.columns[2]]).abs().argsort()[:2]]
        zindex = df_sort.index.tolist()[0]
        df = df[max(0, zindex - args.zero) : zindex + args.zero]

    if len(args.files) == 1:
        df.plot(df.columns[3], df.columns[2])
    else:
        df.plot(df.columns[3], df.columns[2], ax=axes.reshape(-1)[count])
    count += 1
    print(" done")


for hp in args.files:
    plot(hp)

plt.show()
