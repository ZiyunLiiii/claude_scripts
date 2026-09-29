# 4D viewer: design decisions

This file records the decisions for the 4D viewer on mbirtorch branch `4D_viewer`.  The five designs and the
fifteen choices come from the 2026-09-28 proposal (`../progress.md`, entry of that date).  The designs are:
1 linked windows with playback, 2 a frame slider in `slice_viewer`, 3 any two axes of a 4D array, 4 orthogonal
views over time, and 5 napari.  Choices 1 to 15 come out the same whichever of designs 2 to 4 is built.  Each
entry gives the decision, the alternatives considered, and the reason.

## Scope

- 2026-09-29, Ziyun's rule: the existing 3D viewer is kept as it is.  `mbirtorch/viewers/slice_figure.py` and
  `slice_viewer` are not changed.  The 4D viewer is a new module that builds on the 3D viewer's classes without
  changing them, with its own entry point.
- 2026-09-29, Ziyun's direction: the design is not shaped around the Mac's memory and disk for now.  The full
  Phantom_30s_Run1 recon cannot be opened on the Mac in any case.  Loading it needs 19.5 GB of memory against 16 GB,
  and memory mapping needs the file on the local disk, which had 12 GB free on 2026-09-29.  On the Mac the viewer
  sees center-slice stacks and slabs; full 4D volumes are viewed on Gautschi.

## Data model

### 1. Time axis and axis names
- Decision (2026-09-29): time is always axis 0 of a 4D input, and there is no argument to move it.  Titles and
  slider labels name the axes t, x, y, z.
- Alternatives: a `frame_axis` argument with default 0; labels with axis numbers.
- Reason: MACE4D returns `(num_frames, nx, ny, nz)`, and `save_volume_as_gif` uses these names.  The center-slice
  stacks also fit once a singleton axis is added where the fixed axis was, for example `z_stack[..., None]`.

### 2. How `slice_axis` counts the axes of a 4D input
- Decision (2026-09-29): `slice_axis` counts the array's own axes, so 1, 2, 3 mean x, y, z.  The default is z.
  The radio buttons are labeled x, y, z instead of numbers.
- Alternative: count the axes of one frame (0, 1, 2), as the 3D viewer does, so one script line serves 3D and 4D
  inputs.
- Reason: this matches numpy and `save_volume_as_gif`.

### 3. A 3D volume shown next to 4D volumes
- Decision (2026-09-29): the 3D volume stays fixed in time.  The difference between a 4D volume and a 3D volume is
  defined frame by frame.
- Alternative: refuse 3D inputs in a 4D window.
- Reason: a static reference, such as a phantom or a reconstruction of a static scan, can then sit beside every
  frame.

### 4. 4D volumes with different frame counts
- Decision (2026-09-29): the 4D volumes step together by frame index.  A shorter one holds its last frame, and its title
  says so.
- Alternatives: proportional mapping, as slices use now; mapping by physical time from frame times passed in.
- Reason: this is right when the volumes start together and differ in length, such as a 25-frame and a 99-frame
  reconstruction.
  Proportional mapping is right only when two reconstructions of one scan differ in frame rate, and mapping by time needs
  metadata the viewer does not have.

## Playback

### 5. Playback controls
- Decision (2026-09-29): a Play button sits beside the frame slider.  Space plays and pauses, and comma and period
  step one frame back and forward.  Playback loops at the end.  An `fps` argument sets the speed, with default 5
  as in `save_volume_as_gif`.  In design 3 only the time slider plays.
- Alternatives: a button with no new keys; keys with no button.
- Reason: space, comma, and period are free in matplotlib's default key map.  matplotlib binds the arrow keys to
  Back and Forward, h and r to Home, and k and l to log scale.

### 6. What is redrawn during playback
- Decision (2026-09-29): while the viewer plays, only the images and one frame label are redrawn.  Titles and ROI
  statistics refresh when playback stops.
- Alternative: a full redraw of the figure on every frame.
- Reason: on Agg on the Mac, a full redraw took 35 to 80 ms per frame for one to three panels.  Drawing only the two
  images of a two-panel window took 10 ms, or 20 ms at Retina resolution.
- Open: this path needs a test in a real `macosx` window, because the viewer uses its partial redraw only on Agg and
  TkAgg.  TkAgg is the fallback.

## Display range

### 7. Default display range of a 4D input
- Decision (2026-09-29): Ziyun's direction is to do as the current 3D viewer does.  The default range is the
  minimum and maximum over every voxel of every volume, and passing `vmin` and `vmax` skips that scan.  "Data range"
  also computes the full minimum and maximum.
- Alternatives: the 0.2 and 99.8 percentiles of about five whole frames; the minimum and maximum of that sample;
  the percentile rule for 3D inputs as well.
- Consequence: with no `vmin` and `vmax`, a 4D input is read in full once when the window opens.  For the full
  Phantom_30s_Run1 recon that is 19.5 GB.  The scripts that open 4D results already pass both values.

### 8. Display range and colormap of a difference panel
- Decision (2026-09-29): Ziyun's direction is to do as the current 3D viewer does.  A difference panel shares the
  one display range and the colormap of the other panels.
- Alternatives: a range of its own, symmetric about zero, with a two-hue colormap such as RdBu_r; a range of its
  own with the viewer's colormap.
- Consequence: a small difference fills a small part of the shared range, and with `vmin=0` its negative values
  show as black.  Seeing it means changing the shared range, which changes every panel.

## Differences

### 9. A difference image is computed for the whole 4D volume at once
- Decision (2026-09-29): as in the 3D viewer, the difference is computed for the whole 4D volume when the comparison
  panel is clicked, and it is kept as a new array.  Moving a slider then shows parts of that array.
- Alternatives: subtracting only the two images on the screen each time a slider moves; computing one whole frame
  each time the frame changes.
- Consequences: each difference panel holds one more copy of the 4D volume.  As in 3D, a difference keeps its result when
  the other panel changes later, and a difference of a difference is possible.  Playback shows the stored
  difference, so a difference panel costs no more to play than any other panel.
- Reason: the per-image alternative was proposed to fit the full recon on the Mac, which the scope above rules out.

### 10. Differences keep the input's data type
- Decision (2026-09-29, reversed the same day): differences are computed in the input's data type, as now.  The
  first decision, at least float32, was withdrawn because no one loads a CT reconstruction as integers.
- Alternative: at least float32, float64 for float64 inputs.
- Known effect: unsigned integer inputs wrap around (a uint16 0 minus 1 gives 65535, and the error image gives 65535
  too), and bool inputs raise a TypeError.  Float reconstructions are not affected (checked 2026-09-29).

### 11. Differences in time
- Deferred (2026-09-29): Ziyun does not need this for now.  The ROI curve and the space-time planes already show
  the period-6 jitter, and a k = 6 comparison can be made in a script.  Step 2 is complete without it.
- Decision (2026-09-29): a panel can show frame t minus frame t - k of its own 4D volume, with k typed in.  This comes in
  a second step, after the first 4D version works.
- Alternatives: include it in the first version; leave it out, so such differences are computed outside the
  viewer and passed in as 4D volumes.
- Notes: k = 1 shows the change from each frame to the next.  k = 6 compares frames one rotation apart, which have
  the same phase of the period-6 jitter.  The first k frames have no frame k steps earlier and show zero.  Under
  choice 9 the differences for the whole 4D volume are computed at once.

## ROI

### 12. ROI mean against frame
- Decision (2026-09-29): a small plot below the panels shows the ROI mean of every volume against frame, with a marker
  at the current frame.  It is recomputed when the mouse is released after the circle is drawn or moved.
- Alternatives: the same plot in a separate window, leaving the viewer's layout unchanged; no plot.
- Reason: the period-6 jitter appears as an oscillation of the ROI mean, for example for a circle on an edge.

## Files

### 13. Load of a file that holds a 4D array
- Decision (2026-09-29): the 4D array becomes one 4D volume in the panel it is loaded into.  The file is read in
  full, as now.
- Alternative: split the array along its last axis into separate 3D volumes, one per panel, as now.
- Reason: MACE4D files put time first, so today's split gives one (99, 260, 260) volume per z index.
- Scope (2026-09-29): this rule applies to the 4D viewer only.  The 3D viewer's Load keeps splitting a 4D array
  along its last axis, because the 3D viewer is not changed.

### 14a. What "Save data to h5" writes for a 4D volume
- Decision (2026-09-29): the same rule as the 3D viewer.  Save writes the panel's whole volume as it was passed in,
  with its data dict.  For a 4D volume that is the whole 4D volume, and the existing code writes it with no change.
- Alternative: write only the current frame, as a 3D volume.
- Reason: nothing discussed needs a frame-only save, and the 3D rule needs no new code.

### 14b. Movie export
- Decision (2026-09-29): a "Save movie" menu item writes a panel's view, playing over time, as a GIF.  It comes in a
  second step, after the first 4D version works.
- Alternatives: include it in the first version; leave GIFs to scripts.
- Notes: the item calls `save_volume_as_gif`, which the mbirtorch wrapper passes in as it passes `save_fn`, so
  `slice_figure.py` still imports nothing from mbirtorch.  Every view in designs 2 and 3 corresponds to one call of
  `save_volume_as_gif` with some `frame_axis`, `slice_axis`, and `slice_index`.

## Order of changes

### 15. When the float fix goes to Greg
- Withdrawn (2026-09-29): with choice 10 reversed, there is no float fix to send.
- Note: the Load rule of choice 13 goes with the 4D work, because a 4D volume needs a viewer that can show one.

## Design (approved 2026-09-29)

The 4D viewer is `mbirtorch.slice_viewer4d`, in the new module `mbirtorch/viewers/slice_figure4d.py`.  It takes 2D,
3D, and 4D arrays; a 4D array is `(t, x, y, z)`.  It reuses the 3D viewer's classes by subclassing them
(`VolumeStack4D`, `SliceViewer4D`), and the 3D module is not edited.

The window, top to bottom:
- One panel per volume.  A 4D panel's title reads, for example, "Recon A: t = 41, z = 364", and "t = 48 (last)"
  when a shorter 4D volume holds its last frame.  A 3D volume stays fixed in time and its title has no t.
- Radio buttons labeled x, y, z choose the slice the panels show.
- A frame row: a Play button and a frame slider labeled t, shown when at least one input is 4D.
- The slice slider and the intensity slider, as in the 3D viewer.
- A small plot of the ROI mean against frame, one line per volume, with a marker at the current frame.  It is shown
  when at least one input is 4D and is empty until an ROI is drawn.

Keys: space plays and pauses; comma and period step one frame back and forward; h and Esc work as in the 3D viewer.

Behavior: ROI statistics describe the current slice of the current frame, refresh when the frame changes, and pause
during playback.  The ROI plot is recomputed when the circle is released or the slice changes; a frame change only
moves the marker.  Differences are computed for the whole 4D volume at once; two volumes can be subtracted when their
shapes are equal, or when one is 4D and the other is 3D with the same x, y, z shape, in which case the 3D volume is
subtracted from every frame.  Display range, zoom, transpose, data dicts, and Reset work as in the 3D viewer.  Load
turns a 4D file into one 4D volume in that panel, and Save writes the whole volume.

Function call: `slice_viewer4d(*datasets, ..., slice_axis=None, fps=5, ...)`.  `slice_axis` counts each array's own
axes (1, 2, 3 for a 4D array, 0, 1, 2 for a 3D array), with z as the default for both.  With 3D and 4D inputs
together, a non-default slice axis is given as a list, one entry per volume.

Step 1 files: new `mbirtorch/viewers/slice_figure4d.py` and `tests/test_viewer4d.py`; additions only to
`mbirtorch/view_utils.py`, `mbirtorch/__init__.py`, and `mbirtorch/viewers/__init__.py`.

Step 2: the t-x, t-y, and t-z planes in the radio buttons, with sliders that follow the plane; differences in time
(choice 11); "Save movie" (choice 14b).

Left out: a window with all three slices through one point, and several windows that share one frame slider.

Playback on `macosx` (tested 2026-09-29 in a real window, device pixel ratio 1): two 4D panels of 260 x 260
played at 15.2 fps when 30 were requested, with a median of 35 ms per step.  The panels kept their pixels in the
drawn buffer throughout, so the animated-artist path works on this backend.  The default of 5 fps has a wide margin.

## Step 1 status

Implemented 2026-09-29 on `4D_viewer` and committed as 0a9ea35.  The same day, Ziyun found that the right-click menu opened away from the cursor on a Retina screen.  The fix, in the 4D viewer only, is commit 9997a8d.  The 3D viewer has the same bug, in `_open_menu_dialog` of `slice_figure.py`, and it is left for Greg.  Neither commit is pushed.  `slice_figure.py` is byte-identical to before (md5
db0f0e29a14461d5c4d1af6081aa7e7a).  Tests: `tests/test_viewer4d.py` (13 tests) and the 5 existing viewer tests
pass.  Files: new `mbirtorch/viewers/slice_figure4d.py`, `tests/test_viewer4d.py`; additions to
`mbirtorch/view_utils.py`, `mbirtorch/__init__.py`, `mbirtorch/viewers/__init__.py`.


## Step 2 status

Space-time planes implemented 2026-09-29 on `4D_viewer` and committed as 677fa51, together with the dialog layout fix below and the slider layout (the frame-row slider sits under the slice slider, so the two position sliders sit together, as Ziyun preferred to a third slider).  Not pushed.  A panel keeps its axes in the order rows,
columns, slice axis, second axis.  In a spatial plane the second axis is t, as in step 1.  In a space-time plane
(t-x, t-y, t-z) the frame-row slider moves the second hidden spatial axis.  The defaults are the ones proposed
and approved: the buttons are labeled by plane (replacing choice 2's x, y, z labels); t goes to the frame-row
slider whenever it is hidden, and the slice slider keeps its axis when it can; Play and the ROI plot are hidden in
a space-time plane; a 3D volume is shown constant in time, and a shorter 4D volume shows only its own frames,
lined up in time with the others; space-time images stretch to fill the panel.  Two further choices made in the
implementation: a space-time plane is shown in every panel at once, because one frame-row slider serves all
panels, and the slice slider is labeled with its axis name.  Tests: 7 new, 26 viewer tests pass;
`slice_figure.py` is unchanged.  Differences in time and Save movie are not started.

Dialog layout bug (found by Ziyun on 2026-09-29): in the 4D viewer the "Set intensity range" dialog drew its hint over
the Min box.  The inherited in-figure dialogs place their parts at fixed fractions of the figure height, laid out
for the slice viewer's 8-inch figure, and the 4D figure is 10.5 inches tall.  The data-dict, chooser, and file
dialogs were shifted in the same way, and a full page of 11 files would run past the file panel.  The fix is in
the 4D viewer only: a dialog is laid out as if the figure were 8 inches tall and mapped onto the taller figure, so
it has the slice viewer's size and spacing in inches (a test compares the two).  The 3D viewer has the same fault
when its window is made taller than 8 inches; that is left for Greg.

Slider spacing (2026-09-29, Ziyun's request): the slice slider, the frame row, and the intensity slider are the rows
of one block with small gaps, committed as 68130fc.  Not pushed.

Save movie (choice 14b), implemented 2026-09-29 and committed as 4223797 (not pushed): the right-click item "Save movie" writes a panel's
view as a GIF with `save_volume_as_gif`, which the mbirtorch wrapper passes in as `movie_fn`.  The movie plays along
the frame-row slider's axis (t in a spatial plane, the second hidden spatial axis in a space-time plane) at the
current slice, the displayed intensity range, and the viewer's fps.  A transposed panel keeps its orientation.  On
macOS the native save panel asks for the file, with a default name such as init_x-y_z32.gif; other systems get an
in-figure path box.  The item is left out when the panel has one movie frame, such as a 3D volume in a spatial
plane.  Checks: a model test that every movie frame equals the panel image (spatial and space-time planes,
transposed or not), a test with a recording writer, and an end-to-end GIF through `mbirtorch.slice_viewer4d`; 34
viewer tests pass.  In a live macosx window a 24-frame GIF was written in 2.2 s and the viewer kept working.  A test
script that closed the window from a timer sometimes left plt.show() running, with or without a movie; closing with
the window's close button exits normally.

Pushed (2026-09-29): commits 0a9ea35, 9997a8d, 677fa51, 68130fc, and 4223797 are on origin/4D_viewer, after the full
mbirtorch suite passed on the Mac (214 passed, 92 skipped).  Step 2 is complete; differences in time (choice 11) are deferred.
Before a pull request: a trial with a full 4D volume on Gautschi, the macOS save panel, playback on a Retina screen,
the TkAgg and Qt backends, and a docs page.

Docs (2026-09-29), two commits on 4D_viewer, not pushed: 3b1cff8 adds the "4D Data Viewer" section to
usr_utilities.rst, the slice_viewer4d entry to usr_api_overview.rst, "Viewing the Result" to usr_mace4d.rst, and
fully qualified save_volume_as_gif references in view_utils.py.  be2d2d4 adds figs/slice_viewer4d.py, which draws
two figures at build time (the x-y plane with an ROI and its curve, and the t-y plane) from a shifting Shepp-Logan
phantom, and keeps the viewer's partial-redraw rectangle out of the layout so tight saves are not padded.  A local
build of a docs copy without sphinxext.opengraph (not installed here) reports no warnings before or after.

The first docs commit also carries the docstring sentence that Play steps through the frames and every panel shows
the slice chosen with the plane buttons and the slice slider (Ziyun's request, 2026-09-29, folded into it; the two
docs commits were rebuilt as 3b1cff8 and be2d2d4, and pushed to origin/4D_viewer on 2026-09-29).

## Gautschi trial (2026-09-29)

The trial runs the viewer on a Gautschi compute node and shows it in a browser on the Mac.  The job
`serve_viewer4d.sbatch` opens the viewer with matplotlib's WebAgg backend on two full 4D MACE recons of
Phantom_30s_Run1, without dejitter and with the DCT dejitter.  The browser reaches the page through an SSH tunnel
through the login node.  Details are in the progress log entry of 2026-09-29 evening.

Three faults of the 4D viewer were found in a browser window and fixed in commit 010043e (pushed):
1. Playback marked the playing artists animated on every canvas.  On a canvas that cannot blit, such as the WebAgg
   and notebook canvases, playback redraws the whole figure, and those redraws left the animated images out.  The
   artists are now marked animated only on a canvas that can blit.
2. A plane change moves the slice slider before the ROI plot is hidden, and the slider recomputed the plot for the
   new plane.  In a space-time plane the frame means raised an error.  The plot is computed in a spatial plane
   only, and the ROI circle stays through a plane change, as in the 3D viewer.
3. Each recompute of the ROI plot took the next colors of matplotlib's color cycle.  Each volume keeps one color.

WebAgg itself needed no change to the viewer.  Its mouse events give positions in physical pixels, as the macosx
backend does, so the Retina fix of the right-click menu applies to it too.

