#!/usr/bin/env python
import xdg
import os, sys
import argparse
try:
    from termcolor import colored
except ImportError:
    # if termcolor is not installed, strings should just be plain colourless
    # installed via pip
    def colored(*args, **kwargs):
        return args[0]
    

from Package import *
from Manager import *


class Crackle:
    def __init__(self, *args, **kwargs):
        self.verbosity = kwargs.get("verbose", 1)
        self.debug(f"{args=}, {kwargs=}")

        # Getting basepaths for Crackle to work with
        # Configuration defaults to ~/.config/crackle
        self.config_path = kwargs.get("config", os.path.join(xdg.xdg_config_home(), "crackle"))
        self.debug(f"{self.config_path=}")

        # Cache defaults to ~/.cache/crackle. Used to store things we don't want to recalculate
        self.cache_path = kwargs.get("cache", os.path.join(xdg.xdg_cache_home(), "crackle")) 
        self.debug(f"{self.cache_path=}")

        # Data files are stored under ~/.local/share/crackle/src by default. We use this for our source code
        self.src_path = kwargs.get("datapath", os.path.join(xdg.xdg_data_home(), "crackle/src"))
        self.debug(f"{self.src_path=}")

        # Binary files built from source are found in ~/.local/share/crackle/bin by default. Add this to your $PATH
        self.bin_path = kwargs.get("binpath", os.path.join(xdg.xdg_data_home(), "crackle/bin"))
        self.debug(f"{self.bin_path=}")

        self._read_config(os.path.join(self.config_path, "crackle.conf"))

        self.managers = {*()}
        for mgr_name, mgr_conf in self.config.items("Managers"):
            config_path = mgr_conf if os.path.isabs(mgr_conf) else os.path.join(self.config_path, mgr_conf) 
            self.debug(f"{config_path=}")

            mgr = Manager(mgr_name, config_path, verbosity=self.verbosity, fallback_src_path=os.path.join(self.bin_path, mgr_conf))
            self.managers.add(mgr)

    def install(self, pkg_name):
        pkg = None
        for manager in self.managers:
            if manager.has_package(pkg_name):
                pkg = Package(pkg_name, manager)
                
        print(colored("[INSTALL]", "green"), pkg)

    def _read_config(self, configfile_name):
        self.debug(f"{configfile_name=}")
        self.config = configparser.RawConfigParser()
        self.config.read(configfile_name)

    def debug(self, *args, **kwargs):
        if self.verbosity >= kwargs.get("level", 1):
            print(colored("[DEBUG]", "yellow"), *args, **kwargs)



def main(*args, **kwargs):
    crackle = Crackle(*args, **kwargs)
    crackle.install("test")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install applications local to the user")
    parser.add_argument("-c", "--config", type=str)
    parser.add_argument("--cache", type=str)
    parser.add_argument("-v", "--verbose", nargs='?', default=1, const=2, type=int)
    options = parser.parse_args()
    
    args, kwargs = options._get_args(), dict(options._get_kwargs())

    main(*args, **kwargs)

