# LNOI400 GSG CPW ports and MZM pad wrapper

Tag: `lnoi400-gsg`

The LNOI400 CPW pad, uniform CPW, trail CPW, and unbalanced MZM cells expose
individual signal and ground conductors while retaining the existing aggregate
electrical ports for compatibility. GSG conductor ports use the names `S`,
`G_top`, and `G_bot` on pads, `bp1_*` and `bp2_*` on CPW cells, and `S1`,
`G1_top`, `G1_bot`, `S2`, `G2_top`, and `G2_bot` on MZMs.

`mzm_with_pads` is a registered LNOI400 cell. It connects a GSG pad to each
electrical side of an MZM through three-conductor tapers measured from the
actual TL geometry. Its public `e1` and `e2` ports remain on pad metal, while
`o1` and `o2` expose the wrapped MZM optical ports.
