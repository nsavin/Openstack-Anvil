# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Copyright (C) 2012 Yahoo! Inc. All Rights Reserved.
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

from devstack import log as logging
from devstack import settings
from devstack import utils

LOG = logging.getLogger("devstack.packager")


class Packager(object):
    def __init__(self, distro, keep_packages):
        self.distro = distro
        self.keep_packages = keep_packages

    def install_batch(self, pkgs):
        raise NotImplementedError()

    def remove_batch(self, pkgs):
        if not self.keep_packages:
            return self._remove_batch(pkgs)
        return []

    def pre_install(self, pkgs, installparams=None):
        for packageinfo in pkgs:
            preinstallcmds = packageinfo.get(settings.PRE_INSTALL)
            if preinstallcmds:
                LOG.info("Running pre-install commands for package %s.",
                         packageinfo['name'])
                utils.execute_template(*preinstallcmds, params=installparams)

    def post_install(self, pkgs, installparams=None):
        for packageinfo in pkgs:
            postinstallcmds = packageinfo.get(settings.POST_INSTALL)
            if postinstallcmds and len(postinstallcmds):
                LOG.info("Running post-install commands for package %s.",
                         packageinfo['name'])
                utils.execute_template(*postinstallcmds, params=installparams)

    def _remove_batch(self, pkgs):
        raise NotImplementedError()
