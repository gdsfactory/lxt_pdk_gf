import gdsfactory as gf
import numpy as np
from gdsfactory.typings import ComponentSpec

from lnoi400.tech import LAYER


def _measure_gsg_edges(component: gf.Component, port_name: str) -> dict:
    """Measure the y-extents of each GSG conductor at a port's x-coordinate.

    Returns dict with keys 'signal', 'ground_top', 'ground_bot', each a (y_min, y_max) tuple.
    """
    port = component.ports[port_name]
    x_port = port.dcenter[0]
    x_port_nm = x_port * 1000

    tl_layer_idx = None
    ly = component.kcl.layout
    for li in component.get_polygons().keys():
        info = ly.get_info(li)
        if (info.layer, info.datatype) == (LAYER.TL[0], LAYER.TL[1]):
            tl_layer_idx = li
            break

    conductors = []
    for poly in component.get_polygons()[tl_layer_idx]:
        pts = np.array([(pt.x, pt.y) for pt in poly.each_point_hull()], dtype=float)
        n = len(pts)
        y_crossings = []
        for j in range(n):
            p1, p2 = pts[j], pts[(j + 1) % n]
            if (p1[0] - x_port_nm) * (p2[0] - x_port_nm) <= 0 and abs(
                p2[0] - p1[0]
            ) > 0.1:
                t = (x_port_nm - p1[0]) / (p2[0] - p1[0])
                y_crossings.append((p1[1] + t * (p2[1] - p1[1])) / 1000)
        if y_crossings:
            conductors.append((min(y_crossings), max(y_crossings)))

    conductors.sort(key=lambda c: (c[0] + c[1]) / 2)
    return {
        "ground_bot": conductors[0],
        "signal": conductors[1],
        "ground_top": conductors[2],
    }


def _gsg_taper(
    length: float,
    edges_start: dict,
    edges_end: dict,
    layer: tuple[int, int],
) -> gf.Component:
    """Three-conductor GSG taper defined by exact edge positions on each side.

    Port e1 at x=0 (start side), port e2 at x=length (end side).
    """
    c = gf.Component()

    for key in ("signal", "ground_top", "ground_bot"):
        y_bot_s, y_top_s = edges_start[key]
        y_bot_e, y_top_e = edges_end[key]
        c.add_polygon(
            [(0, y_bot_s), (0, y_top_s), (length, y_top_e), (length, y_bot_e)],
            layer=layer,
        )

    sig_start = edges_start["signal"]
    sig_end = edges_end["signal"]

    c.add_port(
        name="e1",
        center=(0, (sig_start[0] + sig_start[1]) / 2),
        width=sig_start[1] - sig_start[0],
        orientation=180,
        layer=layer,
        port_type="electrical",
    )
    c.add_port(
        name="e2",
        center=(length, (sig_end[0] + sig_end[1]) / 2),
        width=sig_end[1] - sig_end[0],
        orientation=0,
        layer=layer,
        port_type="electrical",
    )
    return c


@gf.cell
def mzm_with_pads(
    mzm: ComponentSpec = "mzm_unbalanced_high_speed",
    pad: ComponentSpec = "pad_gsg",
    taper_length: float = 50.0,
) -> gf.Component:
    """MZM with GSG pads connected to both electrical ports.

    Places a pad_gsg on each side of the MZM (input e1, output e2)
    with a GSG taper that smoothly bridges the exact conductor edges
    of the pad and the MZM, including the ground planes.

    Args:
        mzm: MZM component spec.
        pad: GSG pad component spec.
        taper_length: length of the GSG taper between pad and MZM.
    """
    c = gf.Component()

    mzm_component = gf.get_component(mzm)
    mzm_ref = c << mzm_component
    pad_component = gf.get_component(pad)

    pad_edges_e2 = _measure_gsg_edges(pad_component, "e2")
    pad_edges_e1 = _measure_gsg_edges(pad_component, "e1")
    mzm_edges_e1 = _measure_gsg_edges(mzm_component, "e1")
    mzm_edges_e2 = _measure_gsg_edges(mzm_component, "e2")

    tl_layer = LAYER.TL

    # --- Input side: pad.e2 → taper → MZM.e1 ---
    taper_in = c << _gsg_taper(
        length=taper_length,
        edges_start=pad_edges_e2,
        edges_end=mzm_edges_e1,
        layer=tl_layer,
    )
    taper_in.connect("e2", mzm_ref.ports["e1"], allow_width_mismatch=True)

    pad_in = c << pad_component
    pad_in.connect("e2", taper_in.ports["e1"])

    # --- Output side: MZM.e2 → taper → pad.e1 ---
    taper_out = c << _gsg_taper(
        length=taper_length,
        edges_start=mzm_edges_e2,
        edges_end=pad_edges_e1,
        layer=tl_layer,
    )
    taper_out.connect("e1", mzm_ref.ports["e2"], allow_width_mismatch=True)

    pad_out = c << pad_component
    pad_out.connect("e1", taper_out.ports["e2"])

    # Expose optical ports from the MZM
    c.add_port("o1", port=mzm_ref.ports["o1"])
    c.add_port("o2", port=mzm_ref.ports["o2"])

    # Expose outer pad ports for probing, offset 10 µm outward so they
    # sit flush beyond the pad edge.
    port_offset = 10.0

    e1 = pad_in.ports["e1"].copy()
    e1.dcenter = (e1.dcenter[0] - port_offset, e1.dcenter[1])
    c.add_port("e1", port=e1)

    e2 = pad_out.ports["e2"].copy()
    e2.dcenter = (e2.dcenter[0] + port_offset, e2.dcenter[1])
    c.add_port("e2", port=e2)

    return c
