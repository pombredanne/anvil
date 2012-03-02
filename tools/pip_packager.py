import sys
import os

possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]), os.pardir, os.pardir))
sys.path.insert(0, possible_topdir)

from devstack import shell as sh
from devstack import settings
from devstack import utils

if __name__ == "__main__":
    ME = os.path.basename(sys.argv[0])
    if len(sys.argv) == 1:
        print("%s distro filename filename filename..." % (ME))
        sys.exit(0)
    distro = sys.argv[1]
    fns = sys.argv[2:len(sys.argv)]
    pips = dict()
    for fn in fns:
        data = utils.load_json(fn)
        if distro in data:
            dpips = data.get(distro)
            for k in dpips.keys():
                data = dpips.get(k)
                version = data.get('version')
                if k in pips:
                    #check versions??
                    pass
                else:
                    pips[k] = version
    for (pip_name, version) in pips.items():
        full_name = pip_name
        if version:
            full_name = full_name + "==" + version
        print("Fetching %s" % (full_name))
        cmd = ['py2pack'] + ['fetch', full_name]
        sh.execute(*cmd)




