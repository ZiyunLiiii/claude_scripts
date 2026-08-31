# 4D Reconstruction — Skills

## Methods
- MACE, qGGMRF denoising, DCT-I temporal filtering
- Cone-beam CT forward/back projection (mbirjax)
- Multi-GPU JAX (configure_devices, ThreadPoolExecutor)

## Tools
- `mbirjax`, `jax`, `scipy.fft`
- `mbirtorch`, `deepinv` — used for MAR + multi-slice fusion; see `mar_fusion/skills.md`

## Visualization
- Use `mbirjax.slice_viewer` (interactive, blocks until closed) over ThinLinc/X11 rather than building a substitute viewer — see 4D_MACE/skills.md for details.
- Passing several large recon volumes to `slice_viewer` at once can exceed the login node's per-user memory cap; load with `mmap_mode='r'` and pass a strided slice (e.g. `vol[::2, ::2, ::2]`) — see `mar_fusion/skills.md`.

## To Learn
