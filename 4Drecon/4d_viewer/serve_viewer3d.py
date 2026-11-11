"""Serve the mbirtorch 3D slice viewer to a browser from Gautschi.

Usage, on a login node for small volumes (see serve_viewer3d_board.sh):

    PYTHONPATH=VENDOR python -u serve_viewer3d.py --package MBIRTORCH_CHECKOUT \
        --url-file URL_FILE --vmax 0.05 --volumes VOLUME_A.npy VOLUME_B.npy --labels A B

This script is the 3D version of serve_viewer4d.py, and that file explains the WebAgg
backend, the borrowed tornado in VENDOR, and the random URL prefix.  The volumes may
have different shapes.  The viewer scales its one slice slider to the depth of each
volume.
"""
import argparse
import os
import secrets
import socket
import time

import numpy as np

from serve_viewer4d import import_mbirtorch_from


def main():
    parser = argparse.ArgumentParser(description='Serve the mbirtorch 3D slice viewer to a browser.')
    parser.add_argument('--volumes', nargs='+', required=True, help='3D .npy files (row, col, slice)')
    parser.add_argument('--package', required=True,
                        help='folder holding a copy of the mbirtorch package to load')
    parser.add_argument('--url-file', required=True, help='file to write the viewer URL to')
    parser.add_argument('--labels', nargs='+', default=None, help='one panel label per volume')
    parser.add_argument('--notes', nargs='+', default=None,
                        help="one line per volume, shown in the volume's data dict")
    parser.add_argument('--title', default='', help='figure title')
    parser.add_argument('--vmax', type=float, required=True, help='the display maximum')
    parser.add_argument('--dpi', type=float, default=100, help='figure dpi on the web page')
    parser.add_argument('--port', type=int, default=8988,
                        help='first port to try; WebAgg tries others if it is taken')
    args = parser.parse_args()

    # The borrowed tornado needs its C extension turned off.  serve_viewer4d.py explains why.
    os.environ.setdefault('TORNADO_EXTENSION', '0')
    import matplotlib
    matplotlib.use('webagg')
    matplotlib.rcParams.update({'webagg.address': '127.0.0.1', 'webagg.port': args.port,
                                'webagg.open_in_browser': False, 'figure.dpi': args.dpi})
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_webagg import WebAggApplication

    mbirtorch = import_mbirtorch_from(os.path.abspath(os.path.expanduser(args.package)))
    print(f'host {socket.gethostname()}, mbirtorch from {os.path.dirname(mbirtorch.__file__)}')

    volumes = []
    for path in args.volumes:
        start = time.perf_counter()
        volume = np.load(path)
        print(f'loaded {path}: shape {volume.shape}, {volume.dtype}, '
              f'{volume.nbytes / 1e9:.2f} GB in {time.perf_counter() - start:.0f} s')
        volumes.append(volume)

    notes = args.notes or [''] * len(volumes)
    data_dicts = [{'file': path, 'notes': note} for path, note in zip(args.volumes, notes)]
    viewer = mbirtorch.slice_viewer(*volumes, data_dicts=data_dicts, title=args.title,
                                    vmin=0, vmax=args.vmax, slice_label=args.labels, block=False)

    # The server starts here under a random prefix, and pyplot's show below reuses it.
    WebAggApplication.initialize(url_prefix='/' + secrets.token_hex(16))
    url = (f'http://127.0.0.1:{WebAggApplication.port}{WebAggApplication.url_prefix}'
           f'/{viewer.fig.number}')
    # The file is created readable by its owner only.
    fd = os.open(args.url_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w') as f:
        f.write(f'{socket.gethostname()} {WebAggApplication.port} {url}\n')
    print(f'serving on port {WebAggApplication.port}, URL written to {args.url_file}')
    plt.show()


if __name__ == '__main__':
    main()
