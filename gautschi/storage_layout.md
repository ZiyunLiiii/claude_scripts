# Where to Store Things on Gautschi — and the One-Folder-Per-Experiment Rule

The filesystem layout and naming conventions used in
`/home/li5273/PycharmProjects/lilly_exp/nsi` and `/home/li5273/Desktop/data/output`.
Read this before creating a new experiment; the two halves are **which filesystem** and
**how to name the folder so nothing gets overwritten**.

---

## 1. The three filesystems

Check current usage any time with `myquota`.

| Filesystem | Path | Quota | Backed up | What goes here |
|---|---|---|---|---|
| **home** | `/home/li5273` | **25 GB** (≈7 GB used) | yes | code, scripts, notes, small logs, git repos. **Nothing large, ever.** |
| **scratch** | `/scratch/gautschi/li5273` | 200 TB, 10 M files | **no — purged** | all recon outputs, `.npy`/`.h5` volumes, extracted datasets, job workdirs |
| **depot** | `/depot/bouman` | 10 TB (shared, ~70 % used) | yes | the group's source datasets, read-mostly |

Two symlinks make scratch feel like home — **both point at scratch, not home**:

```
/home/li5273/Desktop/data                          -> /scratch/gautschi/li5273/data
/home/li5273/PycharmProjects/lilly_exp/nsi/demo_data -> /scratch/gautschi/li5273/data
```

So `~/Desktop/data/output/...` is a scratch path. That is the single most useful thing to
know here: **a path that looks like home but starts with `Desktop/data` is safe for big
files.**

> **The 25 GB home quota is a real failure mode, not a theoretical one.** A full-res
> recon's `.h5` plus per-pass logs alone can exceed it. Jobs in `0716/mar_ps_sweep`
> FAILED with *disk-quota-exceeded* purely because the job workdir was on home. That is
> why `run_gpu.sbatch` sets `WORKDIR=/home/li5273/Desktop/data/lilly_exp_scratch/...`.

> **Scratch is not backed up and is subject to purge.** Anything you'd be upset to lose —
> a figure for a paper, a small summary CSV, the sbatch script itself — belongs in the git
> repo on home as well. Big volumes you can regenerate stay on scratch only.

### Source datasets

Read them from depot; don't copy them into your own tree:

```
/depot/bouman/data/Lilly/4DCT/Phantom_30s_Run1_Dec2024
/depot/bouman/data/Lilly/4DCT/Kwikpen_4D_2mms
/depot/bouman/data/Lilly/4DCT/Tella_15cP_Run3_April2024
/depot/bouman/data/Lilly/Hearing_Aid.tgz
/depot/bouman/data/Lilly/Connected_Autoinjector_Vertical.tgz          ... etc.
```

In scripts, hand the depot path to `mj.download_and_extract`, which extracts into the
scratch-backed `demo_data` symlink:

```python
dataset_url  = "/depot/bouman/data/Lilly/4DCT/Phantom_30s_Run1_Dec2024.tgz"
download_dir = "/home/li5273/PycharmProjects/lilly_exp/nsi/demo_data/"   # -> scratch
dataset_dir  = mj.download_and_extract(dataset_url, download_dir)
```

---

## 2. The two parallel trees: code vs. output

Every experiment exists in **two places with the same date stem**:

```
CODE   (home, git-tracked, small)
/home/li5273/PycharmProjects/lilly_exp/nsi/<YEAR>/<MMDD>/[<subexp>/]
    <experiment>.py
    submit_<experiment>.sbatch
    slurm_logs/            <- %j.out / %j.err, created before the first sbatch
    README.md  or  RESULTS_LOG.md

OUTPUT (scratch, big, disposable)
/home/li5273/Desktop/data/output/<YEAR>/<MMDD>/<run_name>/
    recon_4d_<hours>h.npy
    init/init_image.npy
    timing_log.csv
    *.png / *.gif
```

`<MMDD>` is the **Thursday of the work week**, the day of the group meeting (`0903`,
`0910`, `0917`).  Folders from before that convention carry the Monday instead
(`0716`, `0723`, `0730`, `0806`, `0813`), so both appear in the tree.  Either way the
year folders read as a weekly lab notebook. A week with several distinct
experiments gets subfolders on the code side — `0716/v6/`, `0716/mar_ps_sweep/`,
`0716/jitter_fdk_phantom/` — each with its own `slurm_logs/` and its own README.

Keep the two trees' names aligned so a result can be traced back to the script that made
it: code `2026/0813/…_v6_p_new_new.py` → output `2026/0813/phantom_version6p_newnew/`.

### Shared, reused artifacts

Things more than one week's experiment consumes go in a shared folder, **not** copied into
each date folder:

```
/home/li5273/Desktop/data/output/2026/4D_shared/
    48_24_init/phantom_init_image.npy      <- the expensive saved init volume
    144_24_init/  72_24_init/  4824fdk/
    qggmrf_recon/  vidnet_recon/  dejitter/
    fdk_recon_4d_4D_Phantom_30s_Run1_Dec2024.npy
```

This is the deliberate exception to "one folder per experiment": a ~19 GB init volume that
ten runs all read gets computed once and shared, because duplicating it is pure waste and
nobody mutates it. Rule of thumb — **share it if it is read-only and expensive; copy it if
anything writes to it.**

---

## 3. One experiment, one folder — never overwrite

The core rule: **a new run means a new output folder.** Two runs must never be able to
write the same file, because the older result is usually the one you need for comparison,
and you will not notice it's gone until you go looking for it.

### 3a. How the names actually vary

Real examples from `output/2026/`:

```
0806/phantom_version6p          0813/phantom_version6p          0716/phantom_version6
0806/phantom_version6p_new      0813/phantom_version6p_newnew   0716/phantom_version6_test
0806/phantom_version6p_newnew   0813/register_dejitter_test     0716/mar_ps_sweep/gpu1
0806/phantom_version6p_test     0813/gifs                       0716/mar_ps_sweep/gpu4
```

Three ways to distinguish a run, in ascending order of preference:

1. **A variant word** — `_test`, `_new`, `_newnew`. Honest about history; goes bad past
   `_newnew` (the third "new" tells you nothing about what changed).
2. **The varied parameter, in the name** — `mar_ps_sweep/gpu1`, `mar_ps_sweep/gpu4`,
   `phantom_version6p`. This is the one to reach for: the folder name states the
   experimental condition, so a `ls` is a legible summary of the sweep.
3. **A `--tag` flag**, so one script can produce many runs with no edits. Best for
   anything with more than two variants.

### 3b. The `--tag` pattern (copy this)

From `0730/optimize_4d/4D_MACE_qggmrf_phantom_48_24_dejitter_v6.py`:

```python
parser.add_argument("--tag", type=str, default="",
                    help="Suffix appended to the default output dir / timing log / recon "
                         "filename, so test runs don't overwrite each other or the full run. "
                         "Ignored if --output-dir is given.")
parser.add_argument("--output-dir", type=str, default=None,
                    help="Exact output directory to use, overriding the default path + --tag.")
args = parser.parse_args()

output_path = args.output_dir if args.output_dir is not None else \
    "/home/li5273/Desktop/data/output/2026/0730/phantom_version6"
if args.output_dir is None and args.tag:
    output_path = f"{output_path}_{args.tag}"
os.makedirs(output_path, exist_ok=True)
```

Which gives a whole sweep with no file edits between runs:

```bash
python ..._v6.py --n-time-bins 8 --max-mace-itr 2 --tag m0_baseline
python ..._v6.py --n-time-bins 8 --max-mace-itr 2 --tag m1_no_wsnap_copy
python ..._v6.py --n-time-bins 8 --max-mace-itr 2 --tag m2m3_test
```
→ `phantom_version6_m0_baseline/`, `..._m1_no_wsnap_copy/`, `..._m2m3_test/`, each with its
own `init/`, `timing_log.csv`, and `recon_4d_*.npy`. And from the sbatch side:

```bash
python -u 4D_MACE_..._v6.py --output-dir /home/li5273/Desktop/data/output/2026/0730/new_4Dmace
```

### 3c. Put the cost in the filename

```python
run_time = (time.time() - time0) / 3600
np.save(os.path.join(output_path, f"recon_4d_{run_time:.2f}h.npy"), recon_4d)
```

`recon_4d_0.46h.npy`, `recon_mbir_ai_349.3s.npy`,
`recon_fusion_init_3_1_ai_alpha1_beta0.002_gamma0.1_651.8s.npy` — the timing and the
hyperparameters are in the name, so two runs can't collide and you can read the sweep off
`ls` without opening a log.

### 3d. `exist_ok=True` is not permission to overwrite

`os.makedirs(output_path, exist_ok=True)` only means "don't crash if the folder is there".
It happily lets a second run clobber `recon_4d_*.npy` inside it. The protection is the
**distinct `output_path`**, not the `makedirs` call. If you're about to rerun with the same
path, change the tag first.

### 3e. When wiping *is* right

Deleting is correct when the leftover data is stale and would silently corrupt the new
result — a scratch workdir, not a results dir. `0716/mar_ps_sweep/run_gpu.sbatch`:

```bash
WORKDIR="/home/li5273/Desktop/data/lilly_exp_scratch/mar_ps_sweep/workdir_gpu${GPU_COUNT}"
RESULTS_DIR="/home/li5273/Desktop/data/output/2026/0716/mar_ps_sweep/gpu${GPU_COUNT}"
mkdir -p "$WORKDIR" "$RESULTS_DIR"
rm -rf "$WORKDIR"/*                       # <- clears the previous run's ./output, ./logs
cp -f "$REPO_DIR/test_mar_ps.sh" "$REPO_DIR/Lilly_recon_ps.py" "$WORKDIR/"
```

The comment on that `rm -rf` names the reason: without it, a previous GPU count's
`./output` and `./logs` leak into this run's results. Note the split — the **workdir** is
wiped, the **results dir** is per-condition (`gpu${GPU_COUNT}`) and never wiped. Keep that
separation; `rm -rf` inside an unparameterized path is how a week of runs disappears.

---

## 4. Per-run bookkeeping that pays for itself

`mar_ps_sweep` writes into each `RESULTS_DIR`, and it's worth copying wholesale:

- `timing.txt` — `start:`/`end:` ISO timestamps plus `exit_code:`
- `devcheck.out` / `devcheck.err` — what JAX saw, so a bad node is diagnosable after the fact
- `SUCCESS` or `FAILED` — a **sentinel file**, so a driver script can tell at a glance which
  conditions finished without parsing logs
- `run.log`, `time_verbose.txt` (`/usr/bin/time -v`) — stdout and peak RSS
- the Slurm `.out`/`.err`, **mirrored** into the results dir on any exit path:
  ```bash
  mirror_logs() {
      cp -f "$SCRIPT_DIR/slurm_logs/${SLURM_JOB_ID}.out" "$RESULTS_DIR/" 2>/dev/null
      cp -f "$SCRIPT_DIR/slurm_logs/${SLURM_JOB_ID}.err" "$RESULTS_DIR/" 2>/dev/null
  }
  trap mirror_logs EXIT
  ```
  The `trap ... EXIT` is the point: the logs land next to the results even when the job
  fails, which is exactly when you need them.

Long jobs should also checkpoint per iteration (`per_iter_save_dir`,
`convergence_log_path` in the v6 MACE scripts) — the AI-dataset run hit the 4 h walltime
after 1 of 10 iterations, and the checkpoints were the only reason that run wasn't wasted.

Alongside the code, keep a `RESULTS_LOG.md` (see `0730/optimize_4d/`) with one entry per
run: exact command, status, timings, what it showed. It is what makes a folder full of
`_new_newnew` names interpretable three weeks later.

---

## 5. Checklist for a new experiment

```bash
DATE=0917            # Thursday of the work week, the meeting day
EXP=my_experiment
CODE=/home/li5273/PycharmProjects/lilly_exp/nsi/2026/$DATE/$EXP
OUT=/home/li5273/Desktop/data/output/2026/$DATE/$EXP        # -> scratch

mkdir -p "$CODE/slurm_logs" "$OUT"
```

1. Code, sbatch, README in `$CODE` (home, git).
2. Every output path in the script under `$OUT` (scratch). Nothing big on home.
3. `slurm_logs/` created **before** the first `sbatch`, `-o`/`-e` absolute, with `%j`.
4. Output folder name states the condition; add `--tag`/`--output-dir` if there'll be more
   than two variants.
5. Timing and key hyperparameters in the saved filename.
6. Reuse the shared init/FDK volumes from `output/2026/4D_shared/` instead of recomputing.
7. `rm -rf` only inside a parameterized **workdir**, never a results dir.
8. Record the run in `RESULTS_LOG.md` when it finishes.
