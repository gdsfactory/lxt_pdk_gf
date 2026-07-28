"""Tests that all PCells with electrical ports expose those ports correctly.

Logical-only mode: add_electric_pins() registers ports without adding geometry.
No GDS diff is performed here — only port-type checks.
"""

from __future__ import annotations

import pytest

import lnoi400
import ltoi300

lnoi400.PDK.activate()


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _electrical_ports(component):
    return [p for p in component.ports if p.port_type == "electrical"]


# ---------------------------------------------------------------------------
# lnoi400 cells
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "factory,kwargs",
    [
        ("CPW_pad_linear", {}),
        ("uni_cpw_straight", {"length": 200.0}),
        ("heater_straight_single", {"length": 150.0}),
        ("eo_phase_shifter", {"modulation_length": 500.0, "draw_cpw": True}),
    ],
)
def test_lnoi400_electrical_ports(factory, kwargs):
    lnoi400.PDK.activate()
    component = lnoi400.PDK.get_component(factory, **kwargs)
    ports = _electrical_ports(component)
    assert len(ports) >= 2, (
        f"{factory} has {len(ports)} electrical port(s); expected >= 2"
    )


# ---------------------------------------------------------------------------
# ltoi300 cells
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "factory,kwargs",
    [
        ("unterminated_eo_phase_shifter_oband", {"modulation_length": 500.0}),
        ("terminated_eo_phase_shifter_oband", {"modulation_length": 500.0}),
        ("unterminated_eo_phase_shifter_cband", {"modulation_length": 500.0}),
        ("terminated_eo_phase_shifter_cband", {"modulation_length": 500.0}),
        (
            "unterminated_mzm_1x2mmi_oband",
            {"modulation_length": 500.0, "bias_tuning_section_length": 0.0},
        ),
        (
            "terminated_mzm_1x2mmi_oband",
            {"modulation_length": 500.0, "bias_tuning_section_length": 0.0},
        ),
        (
            "unterminated_mzm_1x2mmi_cband",
            {"modulation_length": 500.0, "bias_tuning_section_length": 0.0},
        ),
        (
            "terminated_mzm_1x2mmi_cband",
            {"modulation_length": 500.0, "bias_tuning_section_length": 0.0},
        ),
    ],
)
def test_ltoi300_electrical_ports(factory, kwargs):
    ltoi300.PDK.activate()
    component = ltoi300.PDK.get_component(factory, **kwargs)
    ports = _electrical_ports(component)
    assert len(ports) >= 2, (
        f"{factory} has {len(ports)} electrical port(s); expected >= 2"
    )
