# 4D MACE — Skills

## Methods Used
- MACE (Multi-Agent Consensus Equilibrium)
- qGGMRF denoising
- DCT-I temporal filtering
- Cone-beam CT forward/back projection (mbirjax)
- Multi-GPU JAX (configure_devices, ThreadPoolExecutor)

## To Learn / Improve
<!-- Add gaps here -->

## Key Tools / Libraries
- `mbirjax` — CT modeling and reconstruction
- `jax` — GPU computation
- `scipy.fft` — DCT filtering

## Visualization
- To show a reconstructed volume, use `mbirjax.slice_viewer` directly — it opens a real interactive window, not a substitute (e.g. a web scrubber built from saved PNGs).
- Works over a ThinLinc/X11 remote session: check `$DISPLAY` is set, then launch from the `mbirjax` conda env and run in the background, since `slice_viewer` blocks until the window is closed.
- Example, scrubbing a fixed-x slice across all time bins: `mj.slice_viewer(arr[:, x, :, :], slice_axis=0, slice_label='t', vmin=..., vmax=...)`.
