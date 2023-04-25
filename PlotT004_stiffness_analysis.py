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


# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import math
import numpy as np
import os

# Define command line arguments
parser = argparse.ArgumentParser(
    description="Plot Hardpoints data", usage="%(prog)s [files..]"
)
parser.add_argument("files", type=str, nargs="+", help="files to plot")
parser.add_argument(
    "-z",
    dest="zero",
    action="store",
    type=int,
    default=450,
    help="plot only regions around 0 force",
)
parser.add_argument(
    "-s",
    dest="scale",
    action="store",
    type=float,
    default=0.2442,
    help="scale factor for x-axis",
)

# Parse command line arguments
args = parser.parse_args()


# Define function to plot data from a file
def plot(fn):
    print(f"Plotting {fn}")

    # Read data from file into a pandas dataframe
    df = pd.read_csv(fn)

    # Limit data to region around zero force if specified
    if args.zero is not None:
        df_sort = df.iloc[(df[df.columns[2]]).abs().argsort()[:2]]
        zindex = df_sort.index.tolist()[0]
        df = df[max(0, zindex - args.zero) : zindex + args.zero]

    # Scale x-axis data
    df[df.columns[3]] *= args.scale

    # Extract x and y data
    x = df[df.columns[3]]
    y = df[df.columns[2]]

    # Find value of x at zero force
    zero_force = df.loc[df[df.columns[2]].abs().idxmin(), df.columns[3]]

    points = 100  # number of points around zero force for linear fit

    # Extract x and y data around zero force
    x_near_zero = x[
        (x > zero_force - points * args.scale) & (x < zero_force + points * args.scale)
    ]
    y_near_zero = y[
        (x > zero_force - points * args.scale) & (x < zero_force + points * args.scale)
    ]

    # Calculate slope of linear fit to data around zero force
    m, b = np.polyfit(x_near_zero, y_near_zero, 1)

    # Extract x data for full plot and zoomed-in plot
    x_new = x[(x > zero_force - 110 * args.scale) & (x < zero_force + 110 * args.scale)]
    x_new_2 = x[
        (x > zero_force - 400 * args.scale) & (x < zero_force + 400 * args.scale)
    ]

    # Plot data and linear fits
    df.plot(df.columns[3], df.columns[2])
    plt.plot(
        x_new_2,
        m * x_new_2 + b,
        color="red",
        linewidth=2,
        label=f"Mean Stiffness = {m:.2f} N/μm \nEncoder Fitting Range =  {round(x_near_zero.min(),2)} - {round(x_near_zero.max(),2)} μm",
    )
    plt.plot(
        x_new,
        100 * (x_new - zero_force),
        color="green",
        linewidth=2,
        label=f"Spect. Stiffness = 100 N/μm",
    )

    # Add title and axis labels
    plt.title(f"{os.path.basename(fn)}")
    plt.xlabel("Encoder (μm)")
    plt.ylabel("Force (N)")

    # Add grid and legend to plot
    plt.grid(True, linestyle="--", linewidth=0.5)
    plt.legend()

    # Modify x-axis to have zero in the middle
    ax = plt.gca()
    ax.spines["bottom"].set_position("zero")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.set_ticks_position("bottom")

    # Return filename, slope, and encoder for this plot
    return (os.path.basename(fn), m, zero_force)


# Loop through all files and plot data
results = []
for hp in args.files:
    result = plot(hp)
    results.append(result)

# Save results to a CSV file
df_results = pd.DataFrame(results, columns=["file", "slope", "encoder"])
df_results.to_csv("result.csv", index=False)

# Show all plots
plt.show()
