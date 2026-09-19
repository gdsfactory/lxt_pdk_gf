# LNOI400 chip edge and singulation

Tag: `lnoi400-chip-edge`

`die_phix_rf` uses the LXT `chip_frame`, containing `CHIP_CONTOUR` (6/0)
and `CHIP_EXCLUSION_ZONE` (6/1). The outside edge of 6/1 defines the physical
chip edge. Layer 6/0 is a separate contour and does not define the edge-coupler
straight extension.

The default edge-coupler tip extends 5 µm beyond 6/1 on each enabled side.
Its constant-width straight section is 10 µm long: 5 µm outside the chip and
5 µm inside. `double_linear_inverse_taper_mirror` defaults to this straight
length through `input_ext=10`. Lengthening `input_ext` to approximately 30 µm
for polishing leaves the tip at the same 5 µm overhang and extends the straight
section farther inside the chip. The minimum singulation straight length is
10 µm; the additional polishing allowance preserves the tip width after polish.

Without polishing, unnecessarily long straight tips increase the distance over
which the large optical mode interacts with silicon and can increase insertion
loss. The recommended unpolished setting is 10 µm.

The die wrapper preserves pad/fiducial offsets relative to 6/0 when adding the
exclusion-zone border. Chip dimensions obey `chip_frame` size constraints and
snapping: nominal 5000 µm maps to 4950 µm, 10000 to 10000, and 20000 to 20100.
As in `chip_frame`, a nominal 5000-by-5000 µm die is unsupported.

Custom couplers must provide the required constant-width straight section;
custom `fiber_coupler_xoffset` values override the standard 5 µm overhang.
