import signal
import os.path
from datetime import datetime
from mitmproxy.flow import FlowWriter

class Split:
    def __init__(self, path_format):
        self.path_format = os.path.expanduser(os.path.expandvars(path_format))
        self.files = {}

    def add(self, flow):
        path = self.path_format.format(
            req=flow.request,
            res=flow.response,
            time=datetime.utcfromtimestamp(flow.request.timestamp_start),
            flow=flow)

        f = self._ensure_file(path)
        f.add(flow)

    def flush(self):
        for f in self.files.values():
            f.fo.close()
        self.files.clear()

    def _ensure_file(self, path):
        if path in self.files:
            return self.files[path]

        dir_path = os.path.dirname(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        f = FlowWriter(open(path, 'ab'))
        self.files[path] = f
        return f


split = None

def start(context, argv):
    global split
    if len(argv) != 2:
        raise ValueError('Usage: -s "split.py PATH_FORMAT"')

    if split:
        split.flush()
    split = Split(argv[1])

    signal.signal(signal.SIGUSR1, lambda n,s: split.flush())

def response(context, flow):
    try:
        split.add(flow)
    except Exception as e:
        print('split.py error: {}'.format(e))
