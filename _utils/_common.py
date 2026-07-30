from __future__ import annotations

from gdsfactory.add_pins import add_electric_pins

# Combined electrical drawing layers for both lxt_pdk_gf sub-packages.
# lnoi400: TL=(21,0) RF transmission line, HT=(21,1) Heater
# ltoi300: M1=(20,0) Metal 1, HRL=(23,0) Heater resistor layer
_ELECTRICAL_DRAWING_LAYERS = (
    (21, 0),  # TL  — lnoi400 RF transmission line
    (21, 1),  # HT  — lnoi400 Heater
    (20, 0),  # M1  — ltoi300 Metal 1
    (23, 0),  # HRL — ltoi300 Heater resistor layer
)


def _add_pins(component) -> None:
    """Register logical electrical pins; geometric pin drawing disabled pending reference GDS update."""
    add_electric_pins(
        component,
        pin_layer_map={
            component.kcl.layer(*s): None for s in _ELECTRICAL_DRAWING_LAYERS
        },
    )
