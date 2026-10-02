"""Trial of the mbirtorch 4D viewer on full 4D volumes, in a Gautschi OnDemand desktop.

Usage, in the desktop's terminal:

    ~/.conda/envs/mbirtorch/bin/python gautschi_trial.py \
        --package ~/PycharmProjects/mbirtorch_4dviewer VOLUME.npy [VOLUME2.npy]

--package is a checkout of the 4D_viewer branch.  mbirtorch is loaded from it by file
path, because the editable install of the mbirtorch environment loads the package
through an import hook that PYTHONPATH does not override.  Each volume is a 4D array
(t, x, y, z) and is loaded in full.  The script times a few actions in the open window,
prints a summary, writes it with a test movie to --out, and then leaves the window open
to try by hand.  Pass --difference with two volumes to also time a whole-volume
difference image, which holds one more volume in memory.
"""
import argparse
import importlib.util
import os
import resource
import socket
import sys
import time

import numpy as np

CHECKLIST = """
The window stays open.  Please try these and note how responsive each one feels:
  1. Drag the t slider.  Press space to play, and space again to stop.
  2. Click t-y in the Plane buttons, then move the x and z sliders.
  3. Click x-y, then draw an ROI on an edge: left-click and drag.  Look at the ROI plot.
  4. Click GIF beside the t slider.  Save the GIFs in the output folder.
  5. Right-click the first panel and choose Replace with difference image.  This holds
     one more volume in memory.
Then close the window and paste the summary above to Claude.
"""


def import_mbirtorch_from(root):
    """Import mbirtorch from the checkout at ``root``, ahead of the installed copy."""
    package_dir = os.path.join(root, 'mbirtorch')
    spec = importlib.util.spec_from_file_location(
        'mbirtorch', os.path.join(package_dir, '__init__.py'),
        submodule_search_locations=[package_dir])
    module = importlib.util.module_from_spec(spec)
    sys.modules['mbirtorch'] = module
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description='Trial of the mbirtorch 4D viewer.')
    parser.add_argument('volumes', nargs='+', help='4D .npy files (t, x, y, z)')
    parser.add_argument('--package', required=True,
                        help='checkout of the 4D_viewer branch to load mbirtorch from')
    parser.add_argument('--out', default='~/Desktop/data/output/2026/1001/4d_viewer_trial',
                        help='folder for the summary and the test movie')
    parser.add_argument('--difference', action='store_true',
                        help='also time a whole-volume difference image (two volumes)')
    parser.add_argument('--close-after', type=float, default=None,
                        help='close the window this many seconds after the summary, '
                             'for a scripted run')
    args = parser.parse_args()
    out = os.path.expanduser(args.out)
    os.makedirs(out, exist_ok=True)

    mbirtorch = import_mbirtorch_from(os.path.abspath(os.path.expanduser(args.package)))
    import matplotlib
    import matplotlib.pyplot as plt
    from mbirtorch.viewers.slice_figure4d import PLANE_LABELS

    report = []

    def note(line):
        print(line, flush=True)
        report.append(line)

    note(f'host {socket.gethostname()}, matplotlib backend {matplotlib.get_backend()}')
    note(f'mbirtorch loaded from {os.path.dirname(mbirtorch.__file__)}')

    volumes = []
    for path in args.volumes:
        start = time.perf_counter()
        volume = np.load(os.path.expanduser(path))
        note(f'loaded {path}: shape {volume.shape}, {volume.dtype}, '
             f'{volume.nbytes / 1e9:.1f} GB in {time.perf_counter() - start:.1f} s')
        volumes.append(volume)

    start = time.perf_counter()
    lo = min(float(v.min()) for v in volumes)
    hi = max(float(v.max()) for v in volumes)
    note(f'the default display range (min and max of every voxel) takes '
         f'{time.perf_counter() - start:.1f} s and gives {lo:.4g} to {hi:.4g}')
    # The window uses the range of the viewing scripts instead: 0 to the 99.8th
    # percentile of the middle axial slice of the first volume.
    vmax = float(np.percentile(volumes[0][:, :, :, volumes[0].shape[3] // 2], 99.8))

    labels = [os.path.splitext(os.path.basename(path))[0] for path in args.volumes]
    start = time.perf_counter()
    viewer = mbirtorch.slice_viewer4d(*volumes, vmin=0, vmax=vmax, slice_label=labels,
                                      title='4D viewer trial', block=False)
    note(f'window built in {time.perf_counter() - start:.1f} s')
    canvas = viewer.fig.canvas
    timers = []

    def schedule(step, delay_ms=500):
        timer = canvas.new_timer(interval=delay_ms)
        timer.single_shot = True
        timer.add_callback(step)
        timer.start()
        timers.append(timer)

    def median_redraw_ms(positions):
        times = []
        for position in positions:
            start = time.perf_counter()
            viewer.frame_slider.set_val(int(position))
            canvas.draw()
            times.append(time.perf_counter() - start)
        return 1e3 * float(np.median(times))

    # Playback steps are counted by wrapping the method before playback starts.
    play_count = {'steps': 0, 'start': 0.0}
    play_step = viewer._play_step

    def counted_play_step():
        play_count['steps'] += 1
        play_step()

    viewer._play_step = counted_play_step

    def step_frames():
        ms = median_redraw_ms(range(1, 11))
        note(f'x-y plane: one frame step with a full redraw takes {ms:.0f} ms (median of 10)')
        schedule(step_play_start)

    def step_play_start():
        viewer.fps = 30.0
        play_count['start'] = time.perf_counter()
        viewer._toggle_play()
        schedule(step_play_stop, 3000)

    def step_play_stop():
        elapsed = time.perf_counter() - play_count['start']
        viewer._toggle_play()
        viewer.fps = 5.0
        note(f'playback asked for 30 fps and reached {play_count["steps"] / elapsed:.1f} fps')
        schedule(step_space_time)

    def step_space_time():
        start = time.perf_counter()
        viewer.axis_radios[0].set_active(PLANE_LABELS.index('t-y'))
        canvas.draw()
        note(f'switching to the t-y plane takes {1e3 * (time.perf_counter() - start):.0f} ms')
        positions = np.linspace(0, viewer.stack.second_count - 1, 10)
        note(f't-y plane: one step of the x slider with a full redraw takes '
             f'{median_redraw_ms(positions):.0f} ms (median of 10)')
        viewer.axis_radios[0].set_active(PLANE_LABELS.index('x-y'))
        schedule(step_movie)

    def step_movie():
        start = time.perf_counter()
        viewer._write_gifs('frame', out)
        note(f'the GIF button of the t slider wrote one GIF per 4D panel to {out} in '
             f'{time.perf_counter() - start:.1f} s')
        schedule(step_difference if args.difference and len(volumes) > 1 else step_done)

    def step_difference():
        start = time.perf_counter()
        viewer._apply_difference(0, 1, False)
        note(f'a whole-volume difference image took {time.perf_counter() - start:.1f} s')
        viewer._on_restore(0)
        schedule(step_done)

    def step_done():
        # ru_maxrss is in kilobytes on Linux and in bytes on macOS.
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        peak_gb = peak / (1e9 if sys.platform == 'darwin' else 1e6)
        note(f'peak memory of this process: {peak_gb:.1f} GB')
        summary_path = os.path.join(out, 'trial_summary.txt')
        with open(summary_path, 'w') as f:
            f.write('\n'.join(report) + '\n')
        print(f'(summary written to {summary_path})')
        print(CHECKLIST, flush=True)
        if args.close_after is not None:
            schedule(lambda: plt.close(viewer.fig), int(1000 * args.close_after))

    schedule(step_frames, 1500)
    plt.show()


if __name__ == '__main__':
    main()
