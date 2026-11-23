"""Evaluate an interpolating polynomial with Neville–Aitken recursion."""

import argparse
import math


def neville_table(x, y, at):
    """Return the triangular table, with each row indexed by polynomial degree."""
    nodes = list(x)
    values = list(y)
    if not nodes or len(nodes) != len(values):
        raise ValueError("x and y must contain the same nonzero number of samples.")
    if not math.isfinite(at) or not all(math.isfinite(v) for v in nodes + values):
        raise ValueError("All samples and the evaluation point must be finite.")
    if len(set(nodes)) != len(nodes):
        raise ValueError("The interpolation nodes must be distinct.")

    table = [values]
    for degree in range(1, len(nodes)):
        previous = table[-1]
        current = []
        for i in range(len(nodes) - degree):
            left = nodes[i]
            right = nodes[i + degree]
            width = right - left
            value = (right - at) / width * previous[i] + (at - left) / width * previous[i + 1]
            current.append(value)
        table.append(current)
    return table


def neville_aitken(x, y, at):
    """Return the value of the interpolating polynomial at a single point."""
    return neville_table(x, y, at)[-1][0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--x", type=float, nargs="+", required=True, help="distinct interpolation nodes")
    parser.add_argument("--y", type=float, nargs="+", required=True, help="sample values")
    parser.add_argument("--at", type=float, required=True, help="where to evaluate the polynomial")
    parser.add_argument("--show-table", action="store_true", help="show the intermediate interpolants")
    args = parser.parse_args()
    try:
        table = neville_table(args.x, args.y, args.at)
    except ValueError as error:
        parser.error(str(error))

    if args.show_table:
        for degree, row in enumerate(table):
            print(f"Degree {degree}: {'  '.join(f'{value:.10g}' for value in row)}")
    print(f"P({args.at:g}) = {table[-1][0]:.10g}")


if __name__ == "__main__":
    main()
