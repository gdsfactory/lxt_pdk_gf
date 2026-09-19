# Ring resonator slab isolation

Tag: `ltoi300-ring-slab`

The LTOI300 single-mode and multimode point-coupler ring resonators in O-band
and C-band contain ridge and slab geometry for both the ring and the bus.
Changing the gap or building multiple resonators does not remove slab geometry
from subsequent components or from reusable ring and straight cells.

The resonator copies its bus ports and flattens its geometry before applying
sleeve-layer over-under cleanup. Cleanup acts on the resonator's own shapes.
Main ridge layers retain their geometry. The exported `o1` and `o2` ports retain
the bus positions, widths, orientations, and layers.
