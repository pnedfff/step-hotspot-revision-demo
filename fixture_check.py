"""Generate and verify two synthetic, axis-aligned STEP fixtures with FreeCAD."""
import json
import sys
from pathlib import Path

import FreeCAD as CAD
import Import

ROOT = Path(__file__).resolve().parent
CASES = {"rev-a": ("Ethernet Jack", 18), "rev-b": ("Connector 07", 31)}


def generate():
    for revision, (label, x) in CASES.items():
        doc = CAD.newDocument()
        chassis = doc.addObject("Part::Box", "Chassis")
        chassis.Length, chassis.Width, chassis.Height = 80, 45, 3
        port = doc.addObject("Part::Box", "Port")
        port.Label = label
        port.Length, port.Width, port.Height = 16, 12, 10
        port.Placement.Base = CAD.Vector(x, 0, 3)
        doc.recompute()
        Import.export([chassis, port], str(ROOT / "fixtures" / f"{revision}.step"))
        CAD.closeDocument(doc.Name)


def hotspot(solids, size, offset):
    matches = []
    for solid in solids:
        box = solid.BoundBox
        if all(abs(a-b) < 1e-6 for a,b in zip(
            (box.XLength, box.YLength, box.ZLength), size
        )):
            matches.append(box)
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one connector; found {len(matches)}")
    box = matches[0]
    return [a+b for a,b in zip((box.XMin, box.YMin, box.ZMin), offset)]


def verify():
    mapping = json.loads((ROOT / "mapping.json").read_text())
    size, offset = mapping["connector_size_mm"], mapping["hotspot_offset_from_min_mm"]
    for revision, (label, x) in CASES.items():
        path = ROOT / "fixtures" / f"{revision}.step"
        assert label in path.read_text(), f"Missing exported label {label}"
        doc = CAD.newDocument()
        try:
            Import.insert(str(path), doc.Name)
            solids = [s for o in doc.RootObjects if hasattr(o, "Shape")
                      for s in o.Shape.Solids]
            point = hotspot(solids, size, offset)
            assert point == [x+8, 0, 8], point
            for bad in ([], solids + solids):
                try:
                    hotspot(bad, size, offset)
                except ValueError:
                    pass
                else:
                    raise AssertionError("Expected missing/ambiguous match to fail")
            print(f"{revision}: {label} → {mapping['feature']} at {point} mm")
        finally:
            CAD.closeDocument(doc.Name)


if __name__ == "__main__":
    if "--generate" in sys.argv:
        generate()
    verify()
