from __future__ import annotations

import gdsfactory as gf
from gdsfactory.add_pins import add_pins


def _noop_pin(component: gf.Component, port: gf.Port, **kwargs: object) -> None:  # noqa: ARG001
    """No-op pin marker for logical-only electrical pins (no geometry added)."""


def add_electric_pins(component: gf.Component) -> None:
    """Register logical electrical pins on *component* without adding geometry.

    For each port whose ``port_type`` is ``"electrical"`` the port is already
    stored on the component; this function exists to make the intent explicit
    and to provide a future hook for adding physical pin markers (e.g. a PORT
    layer) when a pin_layer_map is available.
    """
    add_pins(component, port_type="electrical", function=_noop_pin)


_add_pins = add_electric_pins
