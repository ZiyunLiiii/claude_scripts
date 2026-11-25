# Blueprint tools

These scripts made or published the blueprint sets of the 4D CT project.  The HTML pages of a set
are the record.  After a page is edited by hand, do not run its build script again.

- `make_publish_index.py` makes the publish copy of a front page for the Artifact tool.  The other
  pages of a set are published as they are.
- `build_4dct_blueprints.py` made the first version of the 4D CT reconstruction set (2026-11-25).
  Its MathML helper functions can be reused for a new page.
- `convert_temporal_filter_math.py` rewrote the math of the temporal filter set in MathML
  (2026-11-25).

Chrome 105 on the Mac does not typeset MathML.  Check a page with Firefox:
`firefox --headless --no-remote --profile <scratch folder> --window-size=1000,3600 --screenshot out.png file://<page>`.
