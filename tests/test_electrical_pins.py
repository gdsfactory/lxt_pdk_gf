"""Tests that logical electrical pins are registered on cells with electrical ports."""

from __future__ import annotations

import pytest

import lnoi400
import ltoi300

lnoi400.PDK.activate()


CELL_FACTORIES = [
    pytest.param("CPW_pad_linear", {}, id="CPW_pad_linear"),
    pytest.param("uni_cpw_straight", {"length": 200.0}, id="uni_cpw_straight"),
    pytest.param(
        "heater_straight_single", {"length": 150.0}, id="heater_straight_single"
    ),
    pytest.param(
        "eo_phase_shifter",
        {"modulation_length": 500.0, "draw_cpw": True},
        id="eo_phase_shifter",
    ),
    pytest.param(
        "eo_phase_shifter_high_speed",
        {"modulation_length": 500.0},
        id="eo_phase_shifter_high_speed",
    ),
    pytest.param("mzm_unbalanced", {"modulation_length": 500.0}, id="mzm_unbalanced"),
    pytest.param(
        "mzm_unbalanced_high_speed",
        {"modulation_length": 500.0},
        id="mzm_unbalanced_high_speed",
    ),
]

LTOI300_CELL_FACTORIES = [
    pytest.param(
        "unterminated_eo_phase_shifter_oband",
        {"modulation_length": 500.0},
        id="unterminated_eo_phase_shifter_oband",
    ),
    pytest.param(
        "terminated_eo_phase_shifter_oband",
        {"modulation_length": 500.0},
        id="terminated_eo_phase_shifter_oband",
    ),
    pytest.param(
        "unterminated_eo_phase_shifter_cband",
        {"modulation_length": 500.0},
        id="unterminated_eo_phase_shifter_cband",
    ),
    pytest.param(
        "terminated_eo_phase_shifter_cband",
        {"modulation_length": 500.0},
        id="terminated_eo_phase_shifter_cband",
    ),
    pytest.param(
        "terminated_mzm_1x2mmi_oband",
        {"modulation_length": 500.0, "bias_tuning_section_length": 0.0},
        id="terminated_mzm_1x2mmi_oband",
    ),
    pytest.param(
        "unterminated_mzm_1x2mmi_oband",
        {"modulation_length": 500.0, "bias_tuning_section_length": 0.0},
        id="unterminated_mzm_1x2mmi_oband",
    ),
    pytest.param(
        "terminated_mzm_2x2mmi_oband",
        {"modulation_length": 500.0, "bias_tuning_section_length": 0.0},
        id="terminated_mzm_2x2mmi_oband",
    ),
    pytest.param(
        "unterminated_mzm_2x2mmi_oband",
        {"modulation_length": 500.0, "bias_tuning_section_length": 0.0},
        id="unterminated_mzm_2x2mmi_oband",
    ),
    pytest.param(
        "terminated_mzm_1x2mmi_cband",
        {"modulation_length": 500.0, "bias_tuning_section_length": 0.0},
        id="terminated_mzm_1x2mmi_cband",
    ),
    pytest.param(
        "unterminated_mzm_1x2mmi_cband",
        {"modulation_length": 500.0, "bias_tuning_section_length": 0.0},
        id="unterminated_mzm_1x2mmi_cband",
    ),
    pytest.param(
        "terminated_mzm_2x2mmi_cband",
        {"modulation_length": 500.0, "bias_tuning_section_length": 0.0},
        id="terminated_mzm_2x2mmi_cband",
    ),
    pytest.param(
        "unterminated_mzm_2x2mmi_cband",
        {"modulation_length": 500.0, "bias_tuning_section_length": 0.0},
        id="unterminated_mzm_2x2mmi_cband",
    ),
]

EXPECTED_PIN_NAMES: dict[str, set[str]] = {
    "CPW_pad_linear": {"e1", "e2"},
    "uni_cpw_straight": {"e1", "e2", "bp1", "bp2"},
    "heater_straight_single": {"ht_start", "ht_end", "e1", "e2"},
    "eo_phase_shifter": {"e1", "e2"},
    "eo_phase_shifter_high_speed": {"e1", "e2"},
    "mzm_unbalanced": {"e1", "e2"},
    "mzm_unbalanced_high_speed": {"e1", "e2"},
    "unterminated_eo_phase_shifter_oband": {"e1", "e2"},
    "terminated_eo_phase_shifter_oband": {"e1", "_e2", "_term"},
    "unterminated_eo_phase_shifter_cband": {"e1", "e2"},
    "terminated_eo_phase_shifter_cband": {"e1", "_e2", "_term"},
    "terminated_mzm_1x2mmi_oband": {"e1", "_e2", "_term"},
    "unterminated_mzm_1x2mmi_oband": {"e1", "e2"},
    "terminated_mzm_2x2mmi_oband": {"e1", "_e2", "_term"},
    "unterminated_mzm_2x2mmi_oband": {"e1", "e2"},
    "terminated_mzm_1x2mmi_cband": {"e1", "_e2", "_term"},
    "unterminated_mzm_1x2mmi_cband": {"e1", "e2"},
    "terminated_mzm_2x2mmi_cband": {"e1", "_e2", "_term"},
    "unterminated_mzm_2x2mmi_cband": {"e1", "e2"},
}


@pytest.mark.parametrize("factory,kwargs", CELL_FACTORIES)
def test_lnoi400_logical_pin_registered(factory, kwargs) -> None:
    lnoi400.PDK.activate()
    c = lnoi400.PDK.get_component(factory, **kwargs)
    assert c.pins, f"{factory} should have logical pins"


@pytest.mark.parametrize("factory,kwargs", CELL_FACTORIES)
def test_lnoi400_port_type_is_electrical(factory, kwargs) -> None:
    lnoi400.PDK.activate()
    c = lnoi400.PDK.get_component(factory, **kwargs)
    for pin in c.pins:
        assert pin.pin_type == "DC", (
            f"{factory} pin {pin.name!r}: expected pin_type='DC', got {pin.pin_type!r}"
        )


@pytest.mark.parametrize("factory,kwargs", CELL_FACTORIES)
def test_lnoi400_expected_pin_names(factory, kwargs) -> None:
    lnoi400.PDK.activate()
    c = lnoi400.PDK.get_component(factory, **kwargs)
    expected = EXPECTED_PIN_NAMES[factory]
    actual = {pin.name for pin in c.pins}
    assert expected.issubset(actual), (
        f"{factory}: expected pins {expected} ⊄ actual {actual}"
    )


@pytest.mark.parametrize("factory,kwargs", LTOI300_CELL_FACTORIES)
def test_ltoi300_logical_pin_registered(factory, kwargs) -> None:
    ltoi300.PDK.activate()
    c = ltoi300.PDK.get_component(factory, **kwargs)
    assert c.pins, f"{factory} should have logical pins"


@pytest.mark.parametrize("factory,kwargs", LTOI300_CELL_FACTORIES)
def test_ltoi300_port_type_is_electrical(factory, kwargs) -> None:
    ltoi300.PDK.activate()
    c = ltoi300.PDK.get_component(factory, **kwargs)
    for pin in c.pins:
        assert pin.pin_type == "DC", (
            f"{factory} pin {pin.name!r}: expected pin_type='DC', got {pin.pin_type!r}"
        )


@pytest.mark.parametrize("factory,kwargs", LTOI300_CELL_FACTORIES)
def test_ltoi300_expected_pin_names(factory, kwargs) -> None:
    ltoi300.PDK.activate()
    c = ltoi300.PDK.get_component(factory, **kwargs)
    expected = EXPECTED_PIN_NAMES[factory]
    actual = {pin.name for pin in c.pins}
    assert expected.issubset(actual), (
        f"{factory}: expected pins {expected} ⊄ actual {actual}"
    )
