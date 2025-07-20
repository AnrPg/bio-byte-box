#!/usr/bin/env python3
"""
pretty_nested.py

Print any nested dict/list/tuple/set so that:
 - Each container starts on a new line with its own braces/brackets/parentheses
 - Each item or key: value is on its own line, indented by level
(using Rich for rendering).
"""

from collections.abc import Mapping
from typing import Any

from rich.console import Console

_console = Console()


def pretty_log(
    obj: Any,
    indent: int = 0,
    indent_step: int = 4,
    tabular: bool = True,
) -> None:
    """
    Recursively print nested dicts, lists, tuples, and sets
    with one item per line via Rich.

    Args:
        obj: The object to print.
        indent: Current indent (in spaces).
        indent_step: Spaces per nesting level.
    """
    space = " " * indent

    # --- DICT ---
    if isinstance(obj, Mapping):
        _console.print(f"{space}{{")
        for key, value in obj.items():
            _console.print(f"{space}{' ' * indent_step}{repr(key)}: ", end="")
            pretty_log(value, indent + indent_step, indent_step)
        _console.print(f"{space}}}")

    # --- LIST ---
    elif isinstance(obj, list):
        # If requested and this is a list of dicts, render as a table
        if tabular and obj and all(isinstance(i, Mapping) for i in obj):
            from rich.table import Table

            # Build table with columns from the union of all keys
            cols = {k for item in obj for k in item.keys()}
            table = Table(show_header=True, header_style="bold", box=None)
            for col in cols:
                table.add_column(col)
            for item in obj:
                table.add_row(*(repr(item.get(c, "")) for c in cols))
            _console.print("\n")
            _console.print(table)
        else:
            _console.print(f"{space}[")
            for item in obj:
                pretty_log(item, indent + indent_step, indent_step, tabular=tabular)
            _console.print(f"{space}]")

    # --- TUPLE ---
    elif isinstance(obj, tuple):
        _console.print(f"{space}(")
        for item in obj:
            pretty_log(item, indent + indent_step, indent_step, tabular=tabular)
        _console.print(f"{space})")

    # --- SET ---
    elif isinstance(obj, set):
        _console.print(f"{space}{{  # set")
        for item in obj:
            pretty_log(item, indent + indent_step, indent_step, tabular=tabular)
        _console.print(f"{space}}}")

    # --- PRIMITIVE ---
    else:
        _console.print(repr(obj))


# if __name__ == "__main__":
#     data = {
#         "alpha": 1,
#         "beta": {
#             "b1": [10, (20, 30), {"x", "y"}],
#             "b2": {"x": "X", "y": "Y"}
#         },
#         "gamma": "end"
#     }
#     pretty_log(data)
