from __future__ import annotations

from functools import partial

from gdsfactory.add_pins import add_electric_pins

# Logical-only mode: empty pin_layer_map suppresses all pin geometry while
# still registering logical pins via component.create_pin() for SPICE / netlist
# export.  A future pass will map metal layers to pin layers once they are
# finalised.
_add_pins = partial(add_electric_pins, pin_layer_map={})
