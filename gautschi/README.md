# Gautschi Cluster Skills

How-to docs for running work on Purdue RCAC's **Gautschi** cluster (user `li5273`,
account `bouman`).

| Doc | Read it when |
|---|---|
| [connect.md](connect.md) | Logging in from the local machine — BoilerKey `PIN,push`, SSH keys, the `ssh gautschi` alias, scp/rsync, OnDemand. |
| [submit_jobs.md](submit_jobs.md) | Writing and submitting Slurm jobs — partitions, the sbatch header, GPU sanity gate, `squeue`/`sacct`/`scancel`, submitting from a Gautschi shell **and** from the Mac over SSH, environment gotchas. |
| [job_times.md](job_times.md) | Choosing the GPU count, partition, and time limit of a job — measured run times by job type and size, queue waits, and the rule for the limit. |
| [storage_layout.md](storage_layout.md) | Deciding where files go — home vs. scratch vs. depot, the code/output tree layout, and the one-folder-per-experiment naming rules that stop runs overwriting each other. |
| [restore_datasets.md](restore_datasets.md) | A dataset on scratch has been partially purged — how to detect it (`check_datasets.sh`) and repair it from depot, and why rerunning `download_and_extract` does **not** repair it. |

## The 60-second version

```bash
hostname          # login0X.gautschi... -> you're on the cluster, just sbatch
                  # otherwise: ssh gautschi   (password = <PIN>,push)

# code on home (25 GB quota), outputs on scratch via the Desktop/data symlink
CODE=/home/li5273/PycharmProjects/scripts/2026/<MMDD>/<exp>
OUT=/home/li5273/Desktop/data/output/2026/<MMDD>/<exp>     # -> /scratch/gautschi/li5273/data
mkdir -p "$CODE/slurm_logs" "$OUT"

cd "$CODE" && sbatch submit_<exp>.sbatch
squeue -u li5273
tail -f slurm_logs/<jobid>.out
```

Six things that bite, each covered in detail in the docs:

1. **Home is only 25 GB.** Every `.npy`/`.h5` goes under `~/Desktop/data/…` (scratch), or
   the job dies on *disk quota exceeded*.
2. **`slurm_logs/` must exist before you `sbatch`**, and `-o`/`-e` must be absolute paths
   with `%j` in them — otherwise the job vanishes with no log at all.
3. **A new run means a new output folder.** Vary it by parameter name or `--tag`; never
   let two runs write the same file.
4. **Scratch datasets rot.** The purge eats `.tif` files out of an extracted dataset and
   leaves the folder standing, and `download_and_extract` cannot tell. Run
   `gautschi/check_datasets.sh` before a campaign — 9 of 15 datasets were incomplete on
   2026-09-16.
5. **Submit GPU jobs with `-q burst`, from the start** (Ziyun, 2026-11-20: "use burst mode, or you will
   never get the gpu").  On `normal` a job gets `gres/hp_gpu=1` and waits behind the group cap of three
   (`AssocGrpGRES`).  `scontrol update qos=burst` on a pending job does not remove that GRES: cancel and
   resubmit with `-q burst`.  Burst allows 8 h and one running job per account.  See submit_jobs.md §1.
6. **From the Mac there is no `gautschi` alias**: use `ssh -o BatchMode=yes li5273@gautschi.rcac.purdue.edu`
   (the SSH key works, no BoilerKey prompt).

Facts here were read off the cluster on 2026-09-15 (datasets, 2026-09-16) and off the real scripts in
`/home/li5273/PycharmProjects/scripts`. Re-check the live ones with `sinfo`,
`myquota`, and `sacctmgr show assoc user=li5273`.
