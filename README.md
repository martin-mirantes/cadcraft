Synthetic reproductions for three CADCraft gaps (no real drawings). Measured on `storytold/cadcraft` main 2ce75fcb, `cadcraft-cli` release build, Linux.

- `mk_ole.py` -> `ole-bitmap.dxf`: one OLE2FRAME whose compound file is a Paint ("PBrush") picture: a 24-bit BMP in the `\x01Ole10Native` stream, after the 98-byte frame envelope. `python3 mk_ole.py out.dxf`.
- `mk_hatch.py` -> `solid-hatch.dxf`: one SOLID hatch, a 400-vertex outer loop with a square island.
- `mk_fonts.py` -> `fonts.dxf`: four TEXT styles named `arial.ttf`, `verdana.ttf`, `georgia.ttf`, `GOTHIC.TTF`.

Commands: `cadcraft-cli convert X.dxf X.pdf`, `cadcraft-cli convert X.dxf X.png`, `cadcraft-cli convert X.dxf X.dwg`.
