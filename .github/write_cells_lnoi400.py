import inspect

from lnoi400 import _cells as cells
from lnoi400.config import PATH


def _can_resolve(module_path: str, name: str) -> bool:
    """Check if griffe can resolve a cell (skip alias resolution errors)."""
    try:
        import griffe

        loader = griffe.GriffeLoader()
        mod = loader.load(module_path)
        member = mod.members.get(name)
        if member and hasattr(member, "is_alias") and member.is_alias:
            member.resolve(loader)
        return True
    except Exception:
        return False


filepath = PATH.repo / "docs" / "cells_lnoi400.md"

skip = {}

skip_plot: tuple[str, ...] = ("",)
skip_settings: tuple[str, ...] = ()


with open(filepath, "w+") as f:
    f.write(
        """

Luxtelligence provides a library of components that have been fabricated in the reference material stack, and whose performance has been tested and validated. Here follows a list of the available parametric cells (gdsfactory.Component objects):


Cells lnoi400
=============================
"""
    )

    for name in sorted(cells.keys()):
        if name in skip or name.startswith("_"):
            continue
        print(name)
        sig = inspect.signature(cells[name])
        kwargs = ", ".join(
            [
                f"{p}={repr(sig.parameters[p].default)}"
                for p in sig.parameters
                if isinstance(sig.parameters[p].default, int | float | str | tuple)
                and p not in skip_settings
            ]
        )
        resolved = _can_resolve("lnoi400.cells", name)
        if name in skip_plot:
            f.write(f"\n\n## {name}\n\n")
            if resolved:
                f.write(f"\n::: lnoi400.cells.{name}\n\n")
        else:
            f.write(f"\n\n## {name}\n\n")
            if resolved:
                f.write(f"\n::: lnoi400.cells.{name}\n\n")
            f.write(
                f"""```python
import lnoi400

c = lnoi400.cells.{name}({kwargs}).copy()
c.draw_ports()
c.plot()
```
"""
            )
