# MAR + Multi-Slice Fusion — Skills

## Methods Used

- MACE-3 multi-slice fusion: PnP-ADMM consensus over a tomographic
  forward-model proximal map and three DRUNet denoiser agents, one per
  slice orientation (`mbirtorch/experiments/drunet/{agents.py,mace.py}`).
- `mbirjax.preprocess.recon_plastic_metal`: alternating beam-hardening
  correction and MBIR reconstruction for metal artifact reduction.
- Cross-framework reconstruction: mbirtorch (PyTorch) for the fusion stage,
  mbirjax (JAX) for the production MAR stage, connected by a saved `.npy`
  volume rather than in-process.

## Key Tools / Libraries

- `mbirtorch` — PyTorch cone-beam CT modeling, used here for the fusion
  stage's forward model and standard qGGMRF recon.
- `mbirjax` — the production MAR pipeline.
- `deepinv` — supplies the pretrained DRUNet denoiser.
- SLURM (`sbatch`) on the Gautschi cluster: `--account=bouman
  --partition=ai --gpus-per-node=<n>`. The login node has no GPU and a
  10 GiB per-user memory cap (see rules.md); real work goes through sbatch.

## Visualization

- Use `mbirjax.slice_viewer` over a live ThinLinc/X11 session — same
  guidance as `4D_MACE/skills.md`.
- `SliceViewer` forces every dataset into a full in-memory `np.asarray`, so
  passing several large recon volumes at once can exceed the login node's
  memory cap. Load with `mmap_mode='r'` and pass a strided slice, e.g.
  `vol[::2, ::2, ::2]`, to cut memory roughly 8x per volume before handing
  it to the viewer.
- The viewer blocks until closed, so launch it detached:
  `DISPLAY=:N MPLBACKEND=TkAgg nohup <mbirjax-env>/bin/python
  launch_viewer.py > log 2>&1 & disown`. Confirm the window actually opened
  with `DISPLAY=:N xwininfo -root -tree | grep -i figure`, since the
  process can still be loading data with no window yet.

## To Learn / Improve

- Whether the fusion-seeded and FDK-seeded MAR results differ mainly
  because of the fusion seed's content or partly because of the sub-voxel
  grid misalignment between mbirtorch and mbirjax — not yet isolated by a
  controlled comparison (relative RMSE 15.8%, correlation 0.987 observed
  between the two on the Autoinjector_HighRes_Horizontal run, at
  `beta=0`).
- Whether `mace.py`'s consensus loop could be extended to distribute its
  eight-volume state across multiple GPUs, which would remove the need to
  downsample below native resolution.
