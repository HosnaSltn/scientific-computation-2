"""Integrate equally spaced samples using Simpson's 1/3 rule."""

import argparse
import math


def paired_samples(x, y):
    nodes = list(x)
    values = list(y)
    if len(nodes) != len(values):
        raise ValueError("x and y must contain the same number of samples.")
    if not all(math.isfinite(v) for v in nodes + values):
        raise ValueError("All samples must be finite.")
    return nodes, values


def uniform_step(nodes):
    intervals = len(nodes) - 1
    step = (nodes[-1] - nodes[0]) / intervals
    if not math.isfinite(step) or step == 0 or not all(
        math.isclose(right - left, step, rel_tol=1e-9)
        for left, right in zip(nodes, nodes[1:])
    ):
        raise ValueError("The selected x samples must be equally spaced and ordered.")
    return step


def composite_simpson(x, y):
    """Return the signed integral over the complete uniform grid."""
    nodes, values = paired_samples(x, y)
    intervals = len(nodes) - 1
    if intervals < 2 or intervals % 2:
        raise ValueError("Composite Simpson's rule needs an even number of intervals, at least two.")

    step = uniform_step(nodes)
    odd_sum = math.fsum(values[1:-1:2])
    even_sum = math.fsum(values[2:-1:2])
    return step / 3 * (values[0] + 4 * odd_sum + 2 * even_sum + values[-1])


def simpson_panel(x, y, index):
    """Integrate the three adjacent samples starting at the zero-based index."""
    nodes, values = paired_samples(x, y)
    if not isinstance(index, int) or not 0 <= index <= len(nodes) - 3:
        raise ValueError("The panel index must leave three samples in the grid.")

    return composite_simpson(nodes[index:index + 3], values[index:index + 3])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--x", type=float, nargs="+", required=True, help="equally spaced integration nodes")
    parser.add_argument("--y", type=float, nargs="+", required=True, help="sample values")
    parser.add_argument("--panel", type=int, help="also integrate three samples starting at this index")
    args = parser.parse_args()
    try:
        total = composite_simpson(args.x, args.y)
        panel = None if args.panel is None else simpson_panel(args.x, args.y, args.panel)
    except ValueError as error:
        parser.error(str(error))

    print(f"Composite integral = {total:.10g}")
    if panel is not None:
        print(f"Panel integral [{args.x[args.panel]:g}, {args.x[args.panel + 2]:g}] = {panel:.10g}")


if __name__ == "__main__":
    main()
