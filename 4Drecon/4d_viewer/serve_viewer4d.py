"""Serve the mbirtorch 4D viewer to a browser from a Gautschi compute node.

Usage, in a Slurm job (see serve_viewer4d.sbatch):

    PYTHONPATH=OUT/vendor python -u serve_viewer4d.py --package OUT/mbirtorch_4dviewer \
        --url-file URL_FILE --volumes VOLUME_A.npy VOLUME_B.npy --labels A B

The viewer runs with matplotlib's WebAgg backend.  WebAgg draws the viewer on the node
and serves it as a web page, which a browser on the Mac opens through an SSH tunnel to
the node.  WebAgg needs tornado, which the mbirtorch environment lacks, so the job puts
vendor/ on PYTHONPATH.  vendor/ holds a link to the tornado of the anaconda/2025.12
module, and the script turns off that tornado's C extension.

The server listens on the node's loopback address only, and every page sits under a
random URL prefix.  Another user on the same node therefore cannot open the viewer
without the full URL.  The script writes the node, the port, and the full URL to
--url-file.

--package is a folder holding a copy of the mbirtorch package from the 4D_viewer
branch.  mbirtorch is loaded from it by file path, because the editable install of the
mbirtorch environment loads the package through an import hook that PYTHONPATH does not
override.
"""
import argparse
import importlib.util
import os
import resource
import secrets
import socket
import sys
import time

import numpy as np


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
    parser = argparse.ArgumentParser(description='Serve the mbirtorch 4D viewer to a browser.')
    # The volumes are an option rather than positional arguments, so that they cannot
    # be read as more --labels or --notes.
    parser.add_argument('--volumes', nargs='+', required=True,
                        help='4D .npy files (t, x, y, z)')
    parser.add_argument('--package', required=True,
                        help='folder holding a copy of the mbirtorch package to load')
    parser.add_argument('--url-file', required=True, help='file to write the viewer URL to')
    parser.add_argument('--labels', nargs='+', default=None, help='one panel label per volume')
    parser.add_argument('--notes', nargs='+', default=None,
                        help="one line per volume, shown in the volume's data dict")
    parser.add_argument('--title', default='', help='figure title')
    parser.add_argument('--dpi', type=float, default=100, help='figure dpi on the web page')
    parser.add_argument('--port', type=int, default=8988,
                        help='first port to try; WebAgg tries others if it is taken')
    args = parser.parse_args()

    # The C extension of the borrowed tornado was built for Python 3.13 and fails
    # under the environment's Python 3.11 when the browser sends a message.  This
    # makes tornado use its pure-Python code, which is fast enough for the small
    # messages a browser sends.
    os.environ.setdefault('TORNADO_EXTENSION', '0')
    # Selecting the backend first fails at once if tornado is missing, before the
    # volumes are loaded.
    import matplotlib
    matplotlib.use('webagg')
    matplotlib.rcParams.update({'webagg.address': '127.0.0.1', 'webagg.port': args.port,
                                'webagg.open_in_browser': False, 'figure.dpi': args.dpi})
    import matplotlib.pyplot as plt
    import tornado
    from matplotlib.backends.backend_webagg import WebAggApplication

    mbirtorch = import_mbirtorch_from(os.path.abspath(os.path.expanduser(args.package)))
    print(f'host {socket.gethostname()}, matplotlib {matplotlib.__version__}, tornado '
          f'{tornado.version}, mbirtorch from {os.path.dirname(mbirtorch.__file__)}')

    volumes = []
    for path in args.volumes:
        start = time.perf_counter()
        volume = np.load(path)
        print(f'loaded {path}: shape {volume.shape}, {volume.dtype}, '
              f'{volume.nbytes / 1e9:.1f} GB in {time.perf_counter() - start:.0f} s')
        volumes.append(volume)
    # The display range of the viewing scripts: 0 to the 99.8th percentile of the
    # middle axial slice of the first volume.
    vmax = float(np.percentile(volumes[0][..., volumes[0].shape[-1] // 2], 99.8))

    notes = args.notes or [''] * len(volumes)
    data_dicts = [{'file': path, 'notes': note} for path, note in zip(args.volumes, notes)]
    start = time.perf_counter()
    viewer = mbirtorch.slice_viewer4d(*volumes, data_dicts=data_dicts, title=args.title,
                                      vmin=0, vmax=vmax, slice_label=args.labels,
                                      block=False)
    print(f'viewer built in {time.perf_counter() - start:.1f} s, display range 0 to {vmax:.4g}')

    # The server starts here under a random prefix, and pyplot's show below reuses it.
    WebAggApplication.initialize(url_prefix='/' + secrets.token_hex(16))
    url = (f'http://127.0.0.1:{WebAggApplication.port}{WebAggApplication.url_prefix}'
           f'/{viewer.fig.number}')
    # The file is created readable by its owner only.
    fd = os.open(args.url_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w') as f:
        f.write(f'{socket.gethostname()} {WebAggApplication.port} {url}\n')
    # ru_maxrss is in kilobytes on Linux.
    peak_gb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
    print(f'serving on port {WebAggApplication.port}, peak memory so far {peak_gb:.1f} GB, '
          f'URL written to {args.url_file}')
    plt.show()


if __name__ == '__main__':
    main()
