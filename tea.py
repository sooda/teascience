#!/usr/bin/env python3
from matplotlib import pyplot as plt
import numpy as np
import matplotlib
from math import fmod

# how does loadtxt or genfromtxt even work
def float_maybe(item):
    try:
        return float(item)
    except ValueError:
        return item
def parse_line(line, ncols):
    return list(map(float_maybe, line.strip().split(maxsplit=ncols-1)))
def load_series(fname, ncols=3):
    return [parse_line(line, ncols) for line in open(fname).readlines()]
def x(s):
    return [a[0] for a in s]
def y(s):
    return [a[1] for a in s]
def z(s):
    return [a[2] for a in s]

def plot_teas(ax, series_spec, data):
    ax.set_title("tea cooling down and being consumed")
    ax.set_xlabel("minutes in cup")
    ax.set_ylabel("temperature C")
    ax.set_ylim([0, 100])
    ax.set_xticks(np.arange(0, 101, 10))
    ax.set_yticks(np.arange(0, 101, 10))
    ax.grid(which="both")

    for (fname, color, linestyle) in series_spec:
        points = data[fname]
        ax.plot(x(points), y(points), linestyle=linestyle, marker="+", color=color, label=fname)

    ranges = [
        (100, "red"),
        (68, "yellow"),
        (60, "green"),
        (45, "yellow"),
        (39, "orange"),
        (20, "")
    ]

    for ((y1, c), (y0, _)) in zip(ranges, ranges[1:]):
        ax.fill_between([0, 90], [y1, y1], [y0, y0], color=c, alpha=0.4)

    for plot_text in [False, True]:
        for (fname, color, _) in series_spec:
            points = data[fname]
            for (i, pt) in enumerate(points):
                if len(pt) == 3:
                    xy = (pt[0], pt[1])
                    point_offset = i % 2
                    text = pt[2] if plot_text else ""
                    series_offset = int(fname[-1]) # lol hack
                    mult = -1 if "green" in fname else 1
                    if False:
                        xytext = (xy[0] + 0 * series_offset, xy[1] + mult * (3 * series_offset + 8 * point_offset))
                    else:
                        if "black" in fname:
                            xytext = (xy[0] + 10 * series_offset, xy[1] + 0)
                        else:
                            xytext = (xy[0] + 0, xy[1] - 15 * series_offset - 7 * point_offset)
                    arrowprops = dict(arrowstyle='->', color=color) if not plot_text else None
                    plt.annotate(text, xy=xy, xytext=xytext, arrowprops=arrowprops, rotation=0, color=color)
    legend_elements = [
        matplotlib.patches.Patch(facecolor="red", label="unhealthy", alpha=0.4),
        matplotlib.patches.Patch(facecolor="yellow", label="manageable", alpha=0.4),
        matplotlib.patches.Patch(facecolor="green", label="great", alpha=0.4),
        matplotlib.patches.Patch(facecolor="orange", label="black tea unhealthy,\ngreen manageable", alpha=0.4),
    ]
    leg = ax.legend()
    plt.gca().add_artist(leg)
    ax.legend(handles=legend_elements, loc="lower right")

def plot_quality(ax, qual_points):
    ax.set_title("tea quality while drinking")
    ax.set_xlabel("temperature in C")
    ax.set_ylabel("perceived enjoyment %")
    ax.set_xlim([0, 100])
    ax.set_ylim([-110, 110])
    ax.set_xticks(np.arange(0, 101, 10))
    ax.set_yticks(np.arange(-100, 101, 20))
    ax.axhline(y=0, color="black")
    ax.grid(which="both")

    ax.plot(x(qual_points), y(qual_points), color="black", label="black tea", linewidth=8, alpha=0.8, solid_capstyle="round")
    ax.plot(x(qual_points), z(qual_points), color="green", label="green tea", linewidth=8, alpha=0.8, solid_capstyle="round")

    ranges = [
        (100,  "green"),
        (60,   "yellow"),
        (30,   "orange"),
        (0,    "red"),
        (-100, "")
    ]

    for ((y1, c), (y0, _)) in zip(ranges, ranges[1:]):
        ax.fill_between([0, 100], [y1, y1], [y0, y0], color=c, alpha=0.4)
    legend_elements = [
        matplotlib.patches.Patch(facecolor="green",  label="great",      alpha=0.4),
        matplotlib.patches.Patch(facecolor="yellow", label="manageable", alpha=0.4),
        matplotlib.patches.Patch(facecolor="orange", label="unpleasant", alpha=0.4),
        matplotlib.patches.Patch(facecolor="red",    label="unhealthy",  alpha=0.4),
    ]
    leg = ax.legend()
    plt.gca().add_artist(leg)
    ax.legend(handles=legend_elements, loc="upper left")

def main():
    series_spec = [
        ("blacktea1", "blue",        "-"),
        ("blacktea2", "black",       "-."),
        ("blacktea3", "dimgrey",     "--"),
        ("greentea1", "forestgreen", "-"),
        ("greentea2", "limegreen",   "-."),
        ("greentea3", "olive",       "--"),
    ]
    data = { fname: load_series(fname + ".txt") for fname, _, _ in series_spec }
    qual_points = load_series("quality.txt", 4)

    plt.xkcd()

    fig = plt.figure(figsize=(20, 10), dpi=100)
    plot_teas(fig.add_subplot(111), series_spec, data)
    plt.savefig("measurements.png")
    plt.clf()

    plot_quality(fig.add_subplot(111), qual_points)
    plt.savefig("quality.png")
    plt.clf()

    # (for development only to see both in a tighter pic)
    plot_teas(fig.add_subplot(121), series_spec, data)
    plot_quality(fig.add_subplot(122), qual_points)
    plt.show()

if __name__ == "__main__":
    main()
