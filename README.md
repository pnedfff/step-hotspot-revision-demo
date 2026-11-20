# STEP hotspot revision demo

A small CAD regression fixture for a proposed browser-based rugged laptop viewer. Both assemblies are synthetic boxes, not an EVAK product model or company CAD.

- Revision A: `Ethernet Jack`, connector X = 18 mm.
- Revision B: renamed to `Connector 07` and moved to X = 31 mm.
- `mapping.json` declares the stable `LAN_1` feature and the local marker offset.
- The check imports both STEP files, locates the unique connector by dimensions without using its label, and verifies the marker moves from (26, 0, 8) to (39, 0, 8) mm. Missing and ambiguous matches must fail.

Run `python fixture_check.py` with a Python interpreter that can import FreeCAD and Import. Use `--generate` to regenerate the STEP fixtures first. On macOS with the bundled FreeCAD Python:

```sh
R=/Applications/FreeCAD.app/Contents/Resources
PYTHONPATH="$R/lib" "$R/bin/python" fixture_check.py
```

This tests a single axis-aligned case. It does not implement rotated or nested assembly matching, GLB export, a viewer, or Devin Bot integration.
