# Submitting Jobs on Gautschi

Slurm how-to for the Purdue RCAC **Gautschi** cluster, as actually used in
`/home/li5273/PycharmProjects/scripts`. Covers both cases:

- **A — from a Gautschi shell** (login node terminal, OnDemand shell, or a Claude Code
  session already running on `login0X.gautschi`). You are on the cluster; just `sbatch`.
- **B — from the local machine over SSH** (the Mac). You `ssh` in, or push the command
  through SSH in one line.

> **Login nodes are not compute.** `login00`–`login07` are for editing, `git`, small
> plots, and submitting. Anything that touches a GPU or runs more than a few minutes
> goes through `sbatch` (batch) or `sinteractive`/`salloc` (interactive).

---

## 1. My account / partition facts

| Thing | Value |
|---|---|
| Slurm account | `bouman` (`-A bouman`) |
| QOS available | `normal`, `preemptible`, `standby` |
| Usual partition | `ai` (H100) |
| Conda env | `mbirjax` (`/home/li5273/.conda/envs/mbirjax`) |
| Conda module | `module load conda` (currently resolves to conda 2026.03) |

Check any of this yourself:
```bash
sacctmgr show assoc user=li5273 format=account,partition,qos
sinfo -o "%20P %5a %10l %6D %10G %N"
```

### Partitions

| Partition | Nodes | GPUs/node | CPUs/node | Max walltime | Use for |
|---|---|---|---|---|---|
| `ai` | `h[000-019]` | 8× H100 | 112 | 14 days | all the 4D MACE / MBIR / MAR work |
| `cocosys` | `i[000-002]` | 8× H200 | — | 14 days | not mine |
| `smallgpu` | `g[000-005]` | 2× L40 | 128 | 12 h | small/quick GPU tests |
| `cpu` | `a[002-337]` | — | 192 | 14 days | pure CPU (preprocessing, analysis) |
| `highmem` | `b[000-005]` | — | — | 1 day | big-RAM, no GPU |

**CPU-to-GPU ratio on `ai`: 112 CPUs / 8 GPUs = 14 CPUs per GPU.** That is exactly why the
existing scripts use `-n14` for a 1-GPU job and `-n56` for a 4-GPU job. Keep that ratio —
asking for more cores than your GPU share entitles you to just makes the job queue longer.

---

## 2. The sbatch header I actually use

Two equivalent styles are in the repo; both work. **Short style** (most of `2026/`):

```bash
#!/bin/bash
#SBATCH -A bouman
#SBATCH -N1
#SBATCH -n56
#SBATCH --gpus-per-node=4
#SBATCH -q normal
#SBATCH -p ai
#SBATCH -t 08:00:00
#SBATCH -o /home/li5273/PycharmProjects/scripts/2026/0813/slurm_logs/%j.out
#SBATCH -e /home/li5273/PycharmProjects/scripts/2026/0813/slurm_logs/%j.err
```

**Long style** (`0730/optimize_4d`, `0903`), same meaning, more readable:

```bash
#SBATCH --job-name=4dmace_optimized
#SBATCH --account=bouman
#SBATCH --partition=ai
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=56
#SBATCH --gres=gpu:4
#SBATCH --time=8:00:00
#SBATCH --output=.../slurm_%j.out
#SBATCH --error=.../slurm_%j.err
```

Rules that matter:

- **`-o`/`-e` paths must be absolute and the directory must already exist.** Slurm will
  not create `slurm_logs/` for you — the job dies instantly with no log if it's missing.
  `mkdir -p slurm_logs` when you create the experiment folder.
- `%j` = job ID. Always include it, so two runs never overwrite each other's logs.
- Add `--job-name=` so `squeue` is readable; the short-style scripts skip it and it makes
  a queue of five jobs unreadable.
- Walltime: pad it. A job killed at the limit loses everything not checkpointed. The 4D
  MACE phantom run measured ~48 min/outer iteration × 10 iterations, which is why those
  scripts ask for 8–12 h, not 4.

### Body template

```bash
set -x

SCRIPT_DIR="/home/li5273/PycharmProjects/scripts/2026/MMDD/expname"
cd "$SCRIPT_DIR"

module load conda
conda activate mbirjax

python my_script.py
```

Two ways to get the interpreter, both in use:

```bash
module load conda && conda activate mbirjax && python -u script.py   # env-based
/home/li5273/.conda/envs/mbirjax/bin/python -u script.py             # absolute path
```

Use the absolute path when one job needs **two different envs** (see
`0903/run_fusion_mar_recon.sbatch`, which chains an mbirtorch stage and an mbirjax stage
without `conda activate` churn). Use `-u` so stdout is unbuffered and the `.out` file
updates live while the job runs — without it you stare at an empty log for an hour.

---

## 3. GPU sanity gate (do not skip this on multi-GPU jobs)

A broken GPU on an `ai` node makes JAX's backend init abort with an **uncatchable** XLA
`Check failed` + core dump, not a Python exception. Your script's `try/except` never sees
it; every config "fails" in ~7 s and a driver loop can wrongly mark itself complete.
This really happened on node `h009` (job 13351866).

So check the devices in the *shell*, by exit status, before trusting the node:

```bash
DEVICE_CHECK_OUT=$(python -c "import jax; d=jax.devices(); print(len(d)); [print(x) for x in d]" \
    2>"slurm_logs/${SLURM_JOB_ID}_devcheck.err")
N_DEVICES=$(echo "$DEVICE_CHECK_OUT" | head -1)
echo "job $SLURM_JOB_ID on $(hostname): jax sees $N_DEVICES device(s)"

if [ "$N_DEVICES" != "4" ]; then
    echo "GPU SANITY CHECK FAILED: expected 4 devices, jax sees $N_DEVICES"
    echo "$(hostname)" >> bad_nodes.txt
    exit 1
fi
```

The full pattern (`0716/submit_matrix.sbatch`) goes further: it logs the bad hostname to
`bad_nodes.txt` and **resubmits itself** excluding every node in that file:

```bash
EXCLUDE_ARG=""
[ -s bad_nodes.txt ] && EXCLUDE_ARG="--exclude=$(sort -u bad_nodes.txt | paste -sd,)"
sbatch --job-name="matrix_${JOB_TAG}" $EXCLUDE_ARG "$SCRIPT_DIR/submit_matrix.sbatch"
```

---

## 4. Submitting, watching, killing

```bash
cd /home/li5273/PycharmProjects/scripts/2026/0813
sbatch submit_4D_MACE_v6_p_new_new.sbatch        # -> "Submitted batch job 15595834"

squeue -u li5273                                  # my queue
squeue -u li5273 -o "%.10i %.20j %.8T %.10M %.10l %.6D %R"   # readable: id, name, state, elapsed, limit, nodes, reason
scontrol show job <jobid>                         # everything, incl. the node it landed on
sacct -j <jobid> --format=JobID,JobName%25,State,Elapsed,MaxRSS,ExitCode
sacct -u li5273 -S 2026-09-01 --format=JobID,JobName%25,State,Elapsed   # history since a date

tail -f slurm_logs/<jobid>.out                    # live log (needs python -u)
scancel <jobid>                                   # kill one
scancel -u li5273                                 # kill all mine -- careful
```

Pass variables into a job without editing the script:
```bash
sbatch --export=ALL,GPU_COUNT=4 run_gpu.sbatch
sbatch --job-name=sweep_gpu4 --time=06:00:00 --exclude=h009 submit_matrix.sbatch
```
Command-line `--flags` override the `#SBATCH` lines in the file. Inside the script, read
them with a required-var guard so a forgotten `--export` fails loudly:
```bash
GPU_COUNT="${GPU_COUNT:?set via sbatch --export=ALL,GPU_COUNT=N}"
```

### Interactive GPU session

For debugging, a shell on a compute node beats twenty `sbatch` round-trips:

```bash
sinteractive -A bouman -p ai -N1 -n14 --gpus-per-node=1 -t 02:00:00
# or:
salloc  -A bouman -p ai -N1 -n56 --gpus-per-node=4 -t 01:00:00
```
Then `module load conda && conda activate mbirjax` as usual. The allocation dies when you
disconnect, so run it inside `tmux`/`screen` on the login node if the link is flaky.

---

## 5. Case A — submitting from a Gautschi shell

Nothing special. You are already on `login0X.gautschi`:

```bash
cd /home/li5273/PycharmProjects/scripts/2026/MMDD/expname
mkdir -p slurm_logs
sbatch submit_expname.sbatch
squeue -u li5273
```

This is also the case when Claude Code is running on the login node — check with
`hostname`; if it prints `login0X.gautschi.rcac.purdue.edu`, you're in case A and can
`sbatch` directly.

---

## 6. Case B — submitting from the local machine over SSH

With the `gautschi` host alias from `connect.md`:

**Interactive** — the normal way:
```bash
ssh gautschi
cd /home/li5273/PycharmProjects/scripts/2026/MMDD/expname
sbatch submit_expname.sbatch
```

**One-shot, without keeping a session** (needs the SSH key, or you'll get a Duo push per
command):
```bash
ssh gautschi 'cd /home/li5273/PycharmProjects/scripts/2026/0813 && sbatch submit_4D_MACE_v6_p_new_new.sbatch'
ssh gautschi 'squeue -u li5273'
ssh gautschi 'tail -n 50 /home/li5273/PycharmProjects/scripts/2026/0813/slurm_logs/15595834.out'
```

**Full local-edit → remote-run loop:**
```bash
# 1. push the experiment folder up (code only -- outputs live on scratch, see storage_layout.md)
rsync -avz --progress \
    --exclude '__pycache__' --exclude 'slurm_logs' --exclude '*.npy' --exclude '*.h5' \
    ./0813/ gautschi:/home/li5273/PycharmProjects/scripts/2026/0813/

# 2. submit
ssh gautschi 'cd /home/li5273/PycharmProjects/scripts/2026/0813 && mkdir -p slurm_logs && sbatch submit_4D_MACE_v6_p_new_new.sbatch'

# 3. watch
ssh gautschi 'squeue -u li5273 -o "%.10i %.20j %.8T %.10M %R"'
ssh gautschi 'tail -f /home/li5273/PycharmProjects/scripts/2026/0813/slurm_logs/15595834.out'

# 4. pull just the small results back (never the whole recon volume by accident)
rsync -avz --progress \
    gautschi:/home/li5273/Desktop/data/output/2026/0813/phantom_version6p_newnew/timing_log.csv ./
```

Never `rsync` a `--delete` onto an output directory on Gautschi. One typo in the source
path and it wipes a run that cost 10 GPU-hours.

**OnDemand fallback:** https://gateway.gautschi.rcac.purdue.edu → *Clusters → Gautschi
Shell Access* gives a browser terminal where the same `sbatch` commands work, if SSH is
unavailable.

---

## 7. Environment gotchas seen in real jobs

- **`LD_LIBRARY_PATH` poisoning JAX.** Cluster-set CUDA paths can make JAX pick up an
  incompatible system CUDA/cuDNN. The MACE scripts defend by re-exec'ing themselves with
  it stripped:
  ```python
  if "LD_LIBRARY_PATH" in os.environ and not os.environ.get("_JAX_CLEAN_REEXEC"):
      env = os.environ.copy(); env.pop("LD_LIBRARY_PATH", None); env["_JAX_CLEAN_REEXEC"] = "1"
      os.execvpe(sys.executable, [sys.executable] + sys.argv, env)
  ```
- **Thread-pool blowup.** A 4-GPU job was seen with 400+ OS threads and one core pegged
  while the GPUs idled. Cap the CPU-side pools in the sbatch body:
  ```bash
  export OMP_NUM_THREADS=8
  export MKL_NUM_THREADS=8
  export OPENBLAS_NUM_THREADS=8
  export NUMEXPR_NUM_THREADS=8
  ```
- **Torch OOM from fragmentation:** `export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`.
- **Multi-GPU NCCL hang.** mbirjax's `ConeBeamModel` / `QGGMRFDenoiser` auto-shard across
  every visible GPU unless you call `model.configure_devices([...])`. Running four agents
  concurrently without pinning makes each open its own 4-way NCCL clique and rendezvous
  stalls forever ("Acquire clique: devices=4:[0,1,2,3] ... may be stuck"). Pin every model
  and denoiser to its own single device.
- **`set -x` at the top of the body** — the shell trace in the `.out` file is what tells
  you whether `conda activate` actually worked when the job dies in 3 seconds.
- **Timestamp the run** so you can tell a stall from slow progress:
  ```bash
  echo "start: $(date -Iseconds)"; python -u script.py; EXIT_CODE=$?
  echo "end:   $(date -Iseconds)"; echo "exit_code: $EXIT_CODE"; exit $EXIT_CODE
  ```
  Propagating `$EXIT_CODE` matters — without the final `exit`, Slurm records the job as
  COMPLETED even when the Python script failed.

---

## 8. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| Job vanishes, no `.out` file at all | `slurm_logs/` doesn't exist, or the `-o` path is relative. `mkdir -p slurm_logs`, use absolute paths. |
| `Disk quota exceeded`, job FAILED | Wrote to `/home` (25 GB cap). Move the workdir and outputs under `~/Desktop/data/...` → scratch. See `storage_layout.md`. |
| Every config fails in ~7 s, `CUDA_ERROR_LAUNCH_FAILED` | Bad GPU on that node. Add the §3 sanity gate, log the host to `bad_nodes.txt`, resubmit with `--exclude=`. |
| Job hangs with "Acquire clique ... may be stuck" | Unpinned multi-GPU mbirjax models — call `configure_devices([device])` per agent. |
| `.out` is empty while the job clearly runs | Missing `python -u`. |
| Job shows COMPLETED but produced nothing | Script exit code swallowed. End the sbatch body with `exit $EXIT_CODE`. |
| `PENDING (QOSMaxJobsPerUserLimit)` / long queue | Ask for fewer GPUs/cores, a shorter `-t`, or try `-p smallgpu` for a quick test. |
| Killed exactly at the walltime | `-t` too short. Pad it, and write per-iteration checkpoints. |

### Sources
- [Gautschi User Guide — Running Jobs](https://www.rcac.purdue.edu/knowledge/gautschi/run)
- [Gautschi User Guide — Slurm partitions / queues](https://www.rcac.purdue.edu/knowledge/gautschi/run/queues)
- Live truth on the cluster: `sinfo`, `sacctmgr show assoc user=li5273`, `scontrol show node h000`
