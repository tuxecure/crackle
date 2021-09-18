#!/usr/bin/py
import xdg
import os

from Package import *
from Manager import *


class Crackle:
    def __init__(self):
        self.config_path = os.path.join(xdg.xdg_config_home(), "crackle")
        print("config: ", self.config_path)
        self.cache_path = os.path.join(xdg.xdg_cache_home(), "crackle")
        self._read_config(os.path.join(self.config_path, "crackle.conf"))

        self.managers = ( Manager(name, os.path.join(self.config_path, name[1]+".conf")) for name in self.config.items("Managers") )

    def install(self, pkg_name):
        pkg = None
        for manager in self.managers:
            if manager.has_package(pkg_name):
                pkg = Package(pkg_name, manager)
                
        print(pkg)

    def _read_config(self, configfile_name):
        print(configfile_name)
        self.config = configparser.RawConfigParser()
        self.config.read(configfile_name)
        print(dict(self.config), "\n\n\n")


def main():
    crackle = Crackle()
    crackle.install("test")

if __name__ == "__main__":
    main()
