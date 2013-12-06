import os

RRDPATH = os.path.expanduser("~/.torcollect)

if not os.path.exists(RRDPATH):
    os.mkdir(RRDPATH)

