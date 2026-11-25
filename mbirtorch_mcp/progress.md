# MBIRTorch MCP server: progress

### 2026-11-03
Stage 1 works end to end.  `server.py` has four tools: `list_files`, `load_volume`,
`list_volumes`, and `show_slice`.  It runs on Gautschi in `~/venvs/mbirtorch_mcp` (anaconda
Python 3.13.9, mcp 2.3.0) and is registered in Claude Code at local scope for the mbirtorch
project folder as `mbirtorch-gautschi`.  `claude mcp list` reports it as connected.

**Checks**
- The planes the server reads match numpy indexing for every axis of a 3D and a 4D test
  volume, stored as `.npy` and as mbirtorch HDF5 (`export_recon_hdf5`).
- Over ssh, the server opened the 2.5 GB TCT MBIR recon on depot in 0.54 s and showed a row
  slice in 3.8 s.  The 4D rack-and-pinion phantom showed motion between time 0 and time 6.
  Its `.h5` and `.npy` copies gave identical PNGs.
- Starting the server over ssh took 2.9 s.

**Test data**: `~/mbirtorch_mcp_test/rack4d.{h5,npy}` on Gautschi (12 x 64 x 64 x 64, from
mbirtorch's rack-and-pinion phantom).

**Environment state on 2026-11-03**: the scratch file system failed on every login node
("Cannot send after transport endpoint shutdown").  The `mbirtorch` conda env and all outputs
under `~/Desktop/data` were unreachable.  The RCAC proxy also timed out, so pip ran without it.

**Open items**
- `show_slice` uses the slice minimum and maximum as the display range.  The TCT board slice
  has low contrast for that reason.  A percentile range would fix it.

**Repository**: the code moved into the new private repository `ZiyunLiiii/mcp_sandbox`
(first commit 613e0c0).  It holds `server.py`, the README with the setup, `requirements.txt`,
and three scripts in `tests/`: `check_server.py` (local check against numpy and a stdio
round trip), `make_rack4d.py` (writes the 4D test phantom), and `check_remote.py` (all tools
over ssh).  The Mac clone is `~/Desktop/Research_Purdue/repository/mcp_sandbox`, and the
Gautschi clone is `~/PycharmProjects/mcp_sandbox`.  Claude Code runs the Gautschi clone, and
`claude mcp list` reports it as connected.  `check_server.py` passed on the Mac, and
`check_remote.py` gave the same images as before the move.
