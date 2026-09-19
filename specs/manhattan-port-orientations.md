# Manhattan port orientations

Tag: `pdk-manhattan-ports`

The component regression suite checks the ports of each registered default cell in the LNOI400 and LTOI300 PDKs. A port is Manhattan when its shortest angular distance to a multiple of 90 degrees is at most 0.001 degrees. The tolerance is absolute and independent of the angle; angles wrap at 360 degrees. A fixed 1e-12 degree allowance absorbs floating-point rounding at the inclusive boundary.

All-angle components are exempt. Components excluded from the existing component regression suite remain excluded; the orientation-specific exclusion set is empty. Failures identify the PDK, component, port, and original orientation. This check does not alter cell geometry or port data.
