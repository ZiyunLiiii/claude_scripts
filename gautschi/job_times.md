# Job times on Gautschi

Use this file to choose the GPU count, the partition, and the time limit of a new job.  The numbers come from `sacct`
and the job logs of user li5273, read on 2026-10-27.  The run times are those of the mbirtorch work of September and
October 2026.  Add a row to the tables when a new kind of job finishes.

## Rule for the time limit

Request 1.5 x the expected run time plus 5 min, rounded up to 5 min, and at least 10 min.  Use the expected time from
the tables or the scaling rules below.  For code that has never run, run a smoke test first and scale its time.

The limit is a hard stop: a job that reaches it is killed with state TIMEOUT, and a user cannot raise the limit of a
job that is already submitted.  A limit close to the need lets the scheduler fit the job into gaps (backfill).  The GPU
count matters more for the wait than the limit does, as the next table shows.

## Queue wait

Jobs of September and October 2026, from submission to start:

| Partition | GPUs | Limit | Jobs | Median wait | Longest wait |
|---|---|---|---|---|---|
| ai | 1 | up to 15 min | 18 | 0.0 h | 0.4 h |
| ai | 1 | 16 to 30 min | 18 | 0.3 h | 1.7 h |
| ai | 1 | 31 to 60 min | 31 | 0.2 h | 4.9 h |
| ai | 1 | 61 to 120 min | 11 | 0.6 h | 1.8 h |
| ai | 2 | up to 60 min | 9 | 0.9 h | 1.3 h |
| ai | 4 | up to 60 min | 12 | 3.9 h | 19.5 h |
| ai | 4 | 61 to 120 min | 13 | 1.5 h | 5.1 h |
| ai | 4 | over 120 min | 6 | 1.4 h | 6.2 h |
| smallgpu | 1 | 40 and 90 min | 2 | 8.8 and 17.7 h | |

- A 1-GPU job on ai usually starts within half an hour.  A 4-GPU job usually waits 1 to 4 hours.
- smallgpu (2 L40 per node, 6 nodes) waited longer than ai both times.  For a 1-GPU job, use ai with `-n14` instead.
- The estimates of `sbatch --test-only` and `squeue --start` were days too late in October.  For example, the jobs of
  2026-10-20 had an estimated start of 10-28 and started the same day.

## Measured run times

All jobs on ai use H100 GPUs.  "Frames" are frames of 48 views (120 degrees), as in the 4D runs.

| Job | Size | Resources | Run time | Job IDs | Limit to request |
|---|---|---|---|---|---|
| MACE4D, Phantom_30s_Run1 | 99 frames, full resolution, 10 iterations | 4 GPUs | 25 to 27 min (30 min with Gram extraction) | 16482614, 16672777-9, 16872253, 17081657, 17144248 | 45 min |
| MACE4D, Tella_15cP | 65 frames, full resolution, 10 iterations | 4 GPUs | 18.5 to 18.8 min | 16887252-3 | 35 min |
| MACE4D, SimRack-1 | 99 frames, grid 130 x 130 x 364, 10 iterations | 4 GPUs | 20.5 to 22 min | 16872576, 16872608, 16899306-7, 17144249 | 35 min |
| MACE4D, SimRack-1 at 4 or 8 frames per rotation | views 288 to 2105 | 2 GPUs | 8 to 19 min | 16917514-20 | 30 min |
| MACE4D, real scan, 90 or 180 deg frames | full resolution | 4 GPUs | 25 min (90 deg), 13 min (180 deg) | 16909393-7 | 45 / 25 min |
| Per-frame MBIR, SimRack-1 | 99 frames, 15 iterations | 4 GPUs | 16.4 min (17.5 with FDK) | 16872575 | 30 min |
| Per-frame MBIR, Tella_15cP | 65 frames, full resolution, 15 iterations | 4 GPUs | 12.6 min | 16887254 | 25 min |
| Per-frame MBIR, real scan, 90 or 180 deg frames | full resolution; 132 frames of 36 views (90 deg); 180 deg frames | 1 GPU | 17.9 min (90 deg), 10.9 min (180 deg) | 16909392, 16909495 | 30 min |
| Per-frame FDK, SimRack-1 | 99 frames | 4 GPUs | 0.4 min | 16872575 | 10 min |
| Simulation of a SimRack dataset | 2400 views x 5 sub-angles, 99 frames of ground truth | 1 L40S (smallgpu) | 10.7 and 9.7 min | 16850958, 16899305 | 20 min |
| Simulation of SimRack-2 | same size | 1 GPU | 5.0 min | 16907878 | 10 min |
| 4D beam hardening correction, one pass | Tella_15cP downsampled 2, 24 frames | 1 GPU | 5 to 8 min | 17061357-61, 17069354-8 | 15 min |
| Static phantom jitter test | MBIR or MACE4D of 60 deg frames | 1 GPU | 3 to 4 min | 16884364-6 | 10 min |
| MACE4D convergence run, one arm | downsampled 4, 24 frames, 150 iterations | 1 GPU | 62 to 65 min | 16673975, 16674461-3 | 100 min |
| MACE4D smoke test | 12 frames, downsampled 8, 1 iteration | 1 GPU | 0.9 to 1.6 min | 17081656, 17144247 | 10 min |
| MACE4D smoke test, 4 GPUs | small | 4 GPUs | 7.5 to 8.3 min | 16476953, 16477701 | 15 min |
| Gram matrices, metrics, analysis | reads saved volumes, CPU work | 1 GPU or the login node | 0.3 to 4 min | 17127338, 17148672, 17065187 | 10 min |
| dl4dct version-0 training | one run | 1 GPU | 3 to 5 min | 16887641-4 | 10 min |
| mbirtorch test suite | full suite | 1 or 4 GPUs | 39 to 41 min | 16468227, 16474261 | 60 min |

## Scaling rules

- **MACE4D:** about 16 s per frame at full resolution and 13 s per frame at the SimRack grid, for 10 iterations on 4
  H100, plus 1 to 2 min to start.  The time grows about linearly with the frames and the iterations.  Two GPUs take
  about twice as long as four.
- **Per-frame MBIR:** about 40 s per frame on one H100 for the SimRack-1 frames with the mbirtorch defaults, and 46 s
  for Tella_15cP.  The real-scan runs of 2026-10-08 (per_frame_mbir.py, 15 iterations, stop 0.02) took only 8 to 10 s
  per frame, so the time depends on how soon the stopping rule ends each frame.  The first frame on each GPU takes
  about 90 s, because the kernels compile.  Plan with frames x 40 s / GPUs + 1.5 min.  Four GPUs in one process do
  not give four times the speed.  The frames run as four threads of one Python process, and Python runs one thread at
  a time.  On 2026-10-27, with the mbirtorch of mbirtorch_ziyun_fork (0.2.0, d4103890), one H100 alone took 12 to
  21 s per frame (smoke 17354383), but four frames at once on four H100 took 40 to 90 s each, about 18 s of wall time
  per frame; the GPUs were 0 to 8% busy and the process used 1.5 CPU cores.  On 2026-10-05, with mbirtorch 010043e,
  the same setup took 19 to 33 s per frame (10 s of wall time), with the same number of iterations (about 12).  One
  process per GPU would avoid the wait.
- **SimRack simulation:** about 32 ms per view and sub-angle on an L40S (6.3 min for 2400 x 5), and 11 ms on an H100
  (4.4 min for 4752 x 5, 2026-10-27).  The ground truth adds about 1.3 s per frame (2.2 min for 99 frames), and the checks and saving add about
  1 min.  Copying a one-view model costs 0.4 ms, so making a new model for every view adds almost nothing.
- **Filtering a saved 4D volume along the frames:** about 2 s per filter for 99 x 130 x 130 x 364, almost all of it
  copying and saving; the 99 x 99 product takes 5 ms on an H100.
- **Analysis of saved results:** a few minutes.  The login node is fine for it (the Gram matrices of 2026-10-21 took
  2.5 min there).  The `cpu` partition is not available to the account.

## Jobs that hit their limit or failed for lack of resources

- In July and August, the mbirjax 4D MACE runs took 56 to 272 min on 4 to 8 GPUs.  Five of them reached limits of 4 to
  6 h (13358505, 13398468, 13589855, 15297419-20).  Two of these waited 41 h in the queue first.
- 16672780 (MACE4D convergence runs, 1 GPU) ran three arms of 62 to 65 min one after another and reached its 150-min
  limit in the third.  Give each long arm its own job.
- 13620839 (mbirjax MACE, July) and 15448323 (debug run, August) ran out of memory.
- The 4D viewer jobs (16761899) run until their limit by design, because the viewer waits for the user.

## SOR random-angle test of 2026-10-27

Estimates for the jobs submitted on 2026-10-27, from the rules above.  Fill in the actual times when they finish.

| Job | Size | Resources | Estimate | Limit given | Actual |
|---|---|---|---|---|---|
| 17354383 smoke | 6 frames, 2 sub-angles, then their MBIR | 1 GPU (ai) | 10 to 12 min | 25 min | 3.3 min (simulation 29 s; MBIR 49 s for the first frame, then 12 to 21 s per frame); waited 0.1 h |
| 17354384 simulation, each order | 4752 views x 5 sub-angles | 1 GPU (ai) | 17 to 20 min on an L40, less on an H100 | 35 min | 5.1 to 5.5 min (transmission 4.4 min, ground truth 40 s, saving and checks 15 s) |
| 17354385_0, 17359405_1-2 per-frame MBIR, each order | 99 frames | 4 GPUs (ai) | about 20 min | 35 min (task 0), 45 min (tasks 1 and 2) | 24.6, 24.6, and 24.9 min |
| 17360503 filtering | 3 orders: Gram comparison, then DCT, SOR, and low-pass on each full MBIR (99 x 130 x 130 x 364), saving 9 volumes of 2.4 GB | 1 GPU (ai) | about 5 min | 20 min | 48 s in all: Gram comparison 3.1 s; per order, loading the MBIR and the truth 2.5 to 2.8 s, to the GPU 0.5 s; per filter, the product 0.005 s (0.2 s the first time), to the host 0.6 s, saving 1.5 s |

These replace jobs 17353296-8, which were sent to smallgpu with limits of 30, 60, and 45 min and were cancelled while
pending, because smallgpu waited 9 to 18 h in the past.

### 12 frames-per-rotation run (submitted 2026-10-27)

| Job | Size | Resources | Estimate | Limit given | Actual |
|---|---|---|---|---|---|
| 17367617 smoke | 6 frames, 2 sub-angles, then their MBIR on 2 GPUs | 2 GPUs (ai) | 3 to 4 min | 15 min | 2.3 min (simulation 20 s; MBIR about 40 s per frame on each GPU, including the compile) |
| 17367618 simulation, each order | 9456 views x 5 sub-angles, 197 frames of ground truth | 1 GPU (ai) | about 11 min | 25 min | 10.5, 14.2, and 10.5 min; the three tasks started within 1 min of the smoke test |
| 17367619 per-frame MBIR, each order | 197 frames, one process per GPU | 4 GPUs (ai) | about 19 min | 45 min | 15.3, 15.7, and 15.3 min (17.0 s per frame on each GPU on average, 51 s at most); waited 16 to 35 min for a node |
| 17367840 filtering (p = 3), tables, figures, GIFs | 3 orders of 197 frames | 1 GPU (ai) | about 7 min | 20 min | 3.8 min: Gram comparison 10 s, filtering 45 s, plots and p sweep about 1 min, three GIFs of 45 MB about 2 min; waited 8 min |
| 17399665 filtering (p = 6), tables, figures, GIFs | 3 orders of 197 frames | 1 GPU (ai) | about 4 min | 15 min | never ran: pending 2.5 h on 2026-10-28 while ai was full (18 nodes allocated, 2 down, 835 jobs pending; smallgpu also full), cancelled after the Delta run |
| Delta 23292386, the same job | 3 orders of 197 frames | 1 A100 (gpuA100x4 or -interactive) | about 5 min | 15 min | 4.3 min on gpuA100x4-interactive, started at once: Gram comparison 6 s, filtering 87 s (loading 9 to 11 s per order from /work/nvme, saving 5.4 to 5.8 s per volume), then figures and GIFs; 0.14 GPU-hours at the 2x interactive rate |

### 60 degree frames cut from SimRack-1 (submitted 2026-10-29)

| Job | Size | Resources | Estimate | Limit given | Actual |
|---|---|---|---|---|---|
| 17443031 smoke test, frames dataset, per-frame MBIR, DCT and SOR (p = 3 and 6), figures, GIF | 199 frames of 24 views, one setting | 2 GPUs (ai) | about 35 min: smoke 3 min, dataset 3 min, MBIR 17 to 28 min (10 to 17 s per frame on each GPU), filters and figures 8 min | 65 min | 31 min 18 s (started 06:59 after 5.5 h in the queue; smoke 2 min 12 s, dataset 47 s, MBIR 26 min at 13.5 s per frame on each GPU, filters and figures 2 min 7 s) |

### FDK and MACE4D of the 60 degree frames on Delta (submitted 2026-11-04)

| Job | Size | Resources | Estimate | Limit given | Actual |
|---|---|---|---|---|---|
| 23537605 prep: frames dataset, FDK, denoiser strength, MACE-SOR smoke (24 frames, 1 iteration) | 199 frames of 24 views | 1 A100 (gpuA100x4-interactive) | about 12 min | 30 min | 3 min 50 s, started within 1 min: dataset 95 s, FDK of 199 frames 7 s, strength 3 s, Gram matrices 17 s, smoke 63 s (one MACE4D iteration on 24 frames: prox 25 s, denoise 33 s) |
| 23537606 MACE-DCT | 199 frames, 10 iterations | 4 A100 (gpuA100x4) | 45 to 65 min | 1 h 40 min | |
| 23537607 MACE-SOR, p = 6 | 199 frames, 10 iterations | 4 A100 (gpuA100x4) | 45 to 65 min | 1 h 40 min | |

From the smoke test, one iteration on 199 frames and 4 A100 should take about 2 min (prox 25 s x 199 / 24 / 4 and
denoise 33 s x 199 / 24 / 4), so 10 iterations take about 20 to 25 min, well under the 45 to 65 min estimate.

### The same 60 degree runs on the measured phantom, full resolution, on Delta (submitted 2026-11-04)

| Job | Size | Resources | Estimate | Limit given | Actual |
|---|---|---|---|---|---|
| 23539419 prep: NSI load, FDK, strength, MBIR smoke (4 frames), MACE-SOR smoke (24 frames, 1 iteration) | 199 frames of 24 views, grid 260 x 260 x 728 | 1 A100 (interactive), 200 GB | about 25 min | 50 min | 7 min 17 s, started within 1 min: NSI load 25 s, FDK of 199 frames 13 s (33 s with stacking), strength 13 s, saving 39 GB 50 s, slices and Gram 27 s; MBIR 27 s per frame after the first (53 s); one MACE4D iteration on 24 frames 90 s (prox 31 s, denoise 57 s) |
| 23539420 MACE-DCT, 23539421 MACE-SOR | 199 frames, 10 iterations | 4 A100 80 GB (gpuA100x8), 600 GB | about 60 to 75 min | 2 h | |
| 23539422 per-frame MBIR | 199 frames, one process per GPU | 4 A100 (gpuA100x4), 120 GB | about 40 to 90 min | 2 h 30 min | |

From the smoke tests: MACE4D about 3 min per iteration on 4 A100 (31 s and 57 s x 199 / 24 / 4), so about 30 to
40 min with the 39 GB reads and writes; the MBIR about 199 x 27 s / 4 = 22 min.

### 60 degree arc datasets in three orders (submitted 2026-10-29, forked session)

| Job | Size | Resources | Estimate | Limit given | Actual |
|---|---|---|---|---|---|
| 17442971, then 17448863 smoke | 6 frames of 24 views, 2 sub-angles, then their MBIR | 1 GPU (ai) | 3 min | 15 min | 3 min 8 s (17448863) |
| 17442972, then 17448864 simulation, each order | 4776 views x 5 sub-angles, 199 frames of ground truth | 1 GPU (ai) | 8 to 10 min | 20 min | |
| 17442973, then 17448865 per-frame MBIR, each order | 199 frames of 24 views, one process per GPU | 2 GPUs (ai) | 25 to 30 min | 50 min | |
| 17442974, then 17448866 filtering (p = 3 and 8), tables, figures, GIFs | 3 orders of 199 frames | 1 GPU (ai) | 8 min | 25 min | |

The first four jobs were submitted at 01:23 while ai was full (897 jobs pending) and had not started at 03:02, when
they were cancelled for Delta.  The Delta login node dt-login02 then stopped answering commands, so the chain was
submitted again on Gautschi at 03:15.  The smoke job 17448863 waited 4 h in the queue and started at 07:18.  Its MBIR
took 13 to 22 s per frame of 24 views on one H100 after the first frame, so 199 frames on 2 GPUs need about 30 min.
At 09:29 the same chain was also submitted on Delta as 23319029 (smoke), 23319030 (sim), 23319031 (MBIR), and
23319032 (filter).  The Delta smoke job started at once and took 3 min 25 s on an A100, the Delta simulation
started at 09:33, and the Gautschi chain was cancelled.  Actual times on Delta A100s: smoke 3 min 25 s,
simulation 9.3 to 9.5 min per order (limit 25), MBIR 30.2 to 30.6 min per order on 2 A100s (limit 85), filtering
6.5 min (limit 25).  The MBIR on 2 A100s took about as long as the estimate for 2 H100s.

The Delta versions (`*_delta.sbatch` in scripts/2026/1029/sor_arc60) use 1 A100 for the smoke, simulation, and
filtering jobs (limits 20, 25, and 25 min, 60 GB) and 2 A100 per order for the MBIR (85 min, 120 GB), because an A100
may take up to twice as long as an H100.

When ai is full, the same 1-GPU job can run on Delta (paths.md, "Cluster (NCSA Delta)").  Copying 29.5 GB from
Gautschi to Delta through the Mac took 8 min with three zstd streams (about 60 MB/s), against 9.5 MB/s for one plain
stream.  The other way, Delta to Gautschi, is slower: 14.5 GB took 24 min with three zstd streams (about 10 MB/s).

The MBIR limit leaves room for the new one-process-per-GPU code: at the speed of the threaded code it would need
about 60 min.  With one process per GPU the MBIR took 17 s of GPU time per frame, against 60 s per frame with four
threads in one process (99 frames in 24.7 min on 4 GPUs), so it is 3.5 times faster.  Use one process per GPU for
per-frame MBIR from now on.  A run of plot_comparison.py on the login node for 197 frames takes 1.7 min.

To read the actual times of finished jobs:
```bash
sacct -u li5273 -S <date> -X --format=JobID,JobName%30,Partition,State,Timelimit,Elapsed,Submit,Start
```

### IPMR sensitivity sweep on the single-metal simulation (Delta, submitted 2026-11-04)

Each job simulates two_rods (256^3, 360 views) and runs IPMR (mbirjax 0.6.15) once per setting, with the plastic metrics after each pass.

| Job | Size | Resources | Estimate | Limit given | Actual |
|---|---|---|---|---|---|
| Delta 23520310 baseline | data, FDK, MBIR, IPMR of 6 passes | 1 A100 (gpuA100x4) | about 8 min | 20 min | 4.2 min (data 30 s, FDK 6 s, MBIR 31 s, IPMR 160 s); started at once |
| Delta 23520311 order | 6 IPMR runs of 3 passes | 1 A100 | about 20 min | 40 min | 11.8 min (79 to 137 s per run) |
| Delta 23520312 alpha | 7 runs | 1 A100 | about 24 min | 45 min | 12.8 min (80 to 120 s per run) |
| Delta 23520313 beta | 12 runs | 1 A100 | about 40 min | 70 min | 25.0 min (81 to 196 s per run) |
| Delta 23520314 gamma | 12 runs | 1 A100 | about 40 min | 70 min | 25.4 min (85 to 271 s per run) |

An IPMR run of 3 passes on this size takes about 2 min on an A100, and the plastic metrics (with SSIM) add about 2 s per pass.

## IPMR timing study for the reviewers (submitted 2026-11-05)

Scripts in `~/PycharmProjects/scripts/2026/1105/ipmr_timing/` (see IPMR_paper/timing/README.md on the Mac).  On this day
the bouman account was capped at 3 H100 in total (GrpTRES), so the 4-GPU jobs were rejected with AssocGrpGRES and the
1-GPU jobs waited for the group's GPUs.  Estimates from the July 2026 full-detector runs with 900 views on 4 H100
(`~/Desktop/data/output/2026/0723/fulltest/`: IPMR 1451 s and MBIR 625 s for the phantom, IPMR 2197 s for the board).

| Job | Size | Resources | Estimate | Limit given | Actual |
|---|---|---|---|---|---|
| 17821440 smoke | phantom and board at downsample 4, every 4th view: FDK, MBIR, IPMR | 1 GPU (ai) | about 10 min | 30 min | |
| 17821441 sim | two_rods and six_rods, 256^3, 360 views: FDK, MBIR, IPMR | 1 GPU (ai) | about 15 min | 40 min | |
| phantom.sbatch (not accepted) | 1800 views, full detector, 1 metal: FDK, MBIR, IPMR, 3 volumes saved | 4 GPUs | about 1.5 h | 2 h 30 | rejected, AssocGrpGRES |
| board.sbatch (not accepted) | 1800 views, full detector, 2 metals | 4 GPUs | about 2.3 h | 3 h 30 | rejected, AssocGrpGRES |

The same study on NCSA Delta: the first chain (2026-11-05, 20:50 CST) died in its smoke job 23584466 after 4 s,
because job_common.sh wrote the GPU-check error file into scripts/slurm_logs/, which exists only on Gautschi; its
dependents 23584467-69 were cancelled.  Resubmitted 2026-11-06, 08:50 CST: 23600767 smoke (1 A100,
gpuA100x4-interactive, 40 min limit), 23600768 phantom (4 H200 on gpuH200x8, 2 h 30, estimate about 1.5 h) and
23600769 board (4 H200, 3 h 30, estimate about 2.3 h), both afterok of the smoke, 23600770 sim (1 A100, gpuA100x4,
50 min).  The smoke job completed on 2026-11-06 in 10 min 58 s on gpua001 (A100 40 GB; both datasets at
downsample 4 and every 4th view), and the three runs were released at 10:01 CST.  The sim job 23600770 completed
on 2026-11-06 in 7 min 17 s on gpua028 (A100; two_rods 256^3: simulation 51 s, MBIR 29 s including the jax
compilation, IPMR 145 s; six_rods: simulation 55 s, MBIR 19 s, IPMR 111 s; jax peak 1.3 GiB).  The phantom and
board jobs were still pending on gpuH200x8 (reason Priority) 38 h after submission, and Ziyun had them cancelled
on 2026-11-08.

Back on Gautschi (submitted 2026-11-08, 00:31 EST), with half the views at full detector resolution and the
warm-up added to the scripts; both waited at first behind three running and two pending 1-GPU jobs of another
member (AssocGrpGRES):

| Job | Size | Resources | Estimate | Limit given | Actual |
|---|---|---|---|---|---|
| 17958015 sim | two_rods and six_rods, 256^3, 360 views: warm-up, FDK, MBIR, IPMR | 1 H100 (ai, -n14) | about 8 min | 20 min | |
| 17958016 real | phantom then board, 900 views, full detector: warm-up, FDK, MBIR, IPMR, 3 volumes each | 3 H100 (ai, -n42) | about 2 h 25 min | 3 h 45 | |

The same runs were also submitted on Delta (2026-11-07, 23:45 CST, at Ziyun's request, as a second chance to run
first), each on gpuH200x8 with priority 1267 at submission: 23657258 sim (1 H200, 20 min, out/sim_h200),
23657259 phantom (4 H200, 48 cpus, 300G, 1 h 20, estimate 50 min, out/real/phantom), 23657260 board (4 H200,
1 h 45, estimate 1 h 5 min, out/real/board).  Once one cluster has delivered a dataset, cancel its pending copy on
the other.  Ziyun had the Delta sim job 23657258 cancelled on 2026-11-08 before it started: the simulation times
come from the Gautschi rerun 17958015 (H100), even if the measured scans come from Delta (H200).
