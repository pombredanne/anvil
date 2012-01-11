# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import Logger
import Component
from Component import (ComponentBase, RuntimeComponent,
                       UninstallComponent, InstallComponent)
import Util
from Util import (RABBIT,
                  get_pkg_list)
import Trace
from Trace import (TraceWriter, TraceReader)
import Shell
from Shell import (mkdirslist, execute, deldir)

LOG = Logger.getLogger("install.rabbit")
TYPE = RABBIT
START_CMD = ["/etc/init.d/rabbitmq-server", "start"]
STOP_CMD = ["/etc/init.d/rabbitmq-server", "stop"]
PWD_CMD = ['rabbitmqctl', 'change_password', 'guest']


class RabbitUninstaller(ComponentBase, UninstallComponent):
    def __init__(self, *args, **kargs):
        ComponentBase.__init__(self, TYPE, *args, **kargs)
        self.tracereader = TraceReader(self.tracedir, Trace.IN_TRACE)

    def unconfigure(self):
        #nothing to unconfigure, we are just a pkg
        pass

    def uninstall(self):
        #clean out removeable packages
        pkgsfull = self.tracereader.packages_installed()
        if(len(pkgsfull)):
            am = len(pkgsfull)
            LOG.info("Removing %s packages" % (am))
            self.packager.remove_batch(pkgsfull)
        dirsmade = self.tracereader.dirs_made()
        if(len(dirsmade)):
            am = len(dirsmade)
            LOG.info("Removing %s created directories" % (am))
            for dirname in dirsmade:
                deldir(dirname)
                LOG.info("Removed %s" % (dirname))


class RabbitInstaller(ComponentBase, InstallComponent):
    def __init__(self, *args, **kargs):
        ComponentBase.__init__(self, TYPE, *args, **kargs)
        self.tracewriter = TraceWriter(self.tracedir, Trace.IN_TRACE)

    def download(self):
        #nothing to download, we are just a pkg
        pass

    def configure(self):
        #nothing to configure, we are just a pkg
        pass

    def _setup_pw(self):
        passwd = self.cfg.getpw("passwords", "rabbit")
        cmd = PWD_CMD + [passwd]
        execute(*cmd, run_as_root=True)

    def install(self):
        #just install the pkg
        pkgs = get_pkg_list(self.os, TYPE)
        pkgnames = pkgs.keys()
        pkgnames.sort()
        LOG.debug("Installing packages %s" % (", ".join(pkgnames)))
        self.packager.install_batch(pkgs)
        for name in pkgnames:
            packageinfo = pkgs.get(name)
            version = packageinfo.get("version", "")
            remove = packageinfo.get("removable", True)
            # This trace is used to remove the pkgs
            self.tracewriter.package_install(name, remove, version)
        dirsmade = mkdirslist(self.tracedir)
        # This trace is used to remove the dirs created
        self.tracewriter.dir_made(*dirsmade)
        self._setup_pw()
        # TODO - stop it (since it usually autostarts)
        # so that we control the start/stop, not it
        return self.tracedir


class RabbitRuntime(ComponentBase, RuntimeComponent):
    def __init__(self, *args, **kargs):
        ComponentBase.__init__(self, TYPE, *args, **kargs)
        self.tracereader = TraceReader(self.tracedir, Trace.IN_TRACE)

    def start(self):
        pkgsinstalled = self.tracereader.packages_installed()
        if(len(pkgsinstalled) == 0):
            msg = "Can not start %s since it was not installed" % (TYPE)
            raise StartException(msg)
        execute(*START_CMD, run_as_root=True)
        return None

    def stop(self):
        pkgsinstalled = self.tracereader.packages_installed()
        if(len(pkgsinstalled) == 0):
            msg = "Can not stop %s since it was not installed" % (TYPE)
            raise StopException(msg)
        execute(*STOP_CMD, run_as_root=True)
        return None
