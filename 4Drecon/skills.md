# 4D Reconstruction — Skills

## Methods
- MACE, qGGMRF denoising, DCT-I temporal filtering
- Cone-beam CT forward/back projection (mbirjax)
- Multi-GPU JAX (configure_devices, ThreadPoolExecutor)

## Tools
- `mbirjax`, `jax`, `scipy.fft`

## Visualization
- Use `mbirjax.slice_viewer` (interactive, blocks until closed) over ThinLinc/X11 rather than building a substitute viewer — see 4D_MACE/skills.md for details.

## To Learn
