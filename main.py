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
from helper import IO

class Crackle(IO):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.verbosity = kwargs.get("verbose", 1)
        self.debug(f"{args=}, {kwargs=}")

        # Getting basepaths for Crackle to work with
        # Configuration defaults to ~/.config/crackle
        self.config_path = kwargs.get("config") or os.path.join(xdg.XDG_CONFIG_HOME, "crackle")
        self.debug(f"{self.config_path=}")

        try:
            self._read_config(os.path.join(self.config_path, "crackle.conf"))
        except FileNotFoundError as err:
            raise err

        # Cache defaults to ~/.cache/crackle. Used to store things we don't want to recalculate
        self.cache_path = kwargs.get("cache") or self.config.get("Options", "CRACKLE_CACHE_DIR") or os.path.join(xdg.XDG_CACHE_HOME, "crackle") 
        self.debug(f"{self.cache_path=}")

        # Data files are stored under ~/.local/share/crackle/src by default. We use this for our source code
        self.src_path = kwargs.get("datapath") or self.config.get("Options", "CRACKLE_SRC_DIR") or oos.path.join(xdg.XDG_DATA_HOME, "crackle/src")
        self.debug(f"{self.src_path=}")

        # Binary files built from source are found in ~/.local/share/crackle/bin by default. Add this to your $PATH
        self.bin_path = kwargs.get("binpath") or self.config.get("Options", "CRACKLE_BIN_DIR") or os.path.join(xdg.XDG_DATA_HOME, "crackle/bin")
        self.debug(f"{self.bin_path=}")


        self.managers = {*()}
        for mgr_name, mgr_conf in self.config.items("Managers"):
            config_path = mgr_conf if os.path.isabs(mgr_conf) else os.path.join(self.config_path, mgr_conf) 
            fallback_bin_path = self.bin_path
            fallback_src_path = os.path.join(self.src_path, mgr_name)
            self.debug(f"{config_path=}")

            mgr = Manager(mgr_name, config_path, verbosity=self.verbosity, fallback_src_path=fallback_src_path, fallback_bin_path=fallback_bin_path)
            self.managers.add(mgr)

    def install(self, pkg_name):
        pkg = None
        for manager in self.managers:
            if ( pkg := manager.get_package(pkg_name) ):
                break
                
        self.info(f"Installed {pkg}")

    def _read_config(self, configfile_name):
        if not os.path.isfile(configfile_name):
            self.error(f"{configfile_name=} is not a file")
            raise FileNotFoundError("Configuration file must exist")
        else:
            self.debug(f"{configfile_name=}")
            self.config = configparser.RawConfigParser()
            self.config.read(configfile_name)


def main(*args, **kwargs):
    try:
        crackle = Crackle(*args, **kwargs)
        crackle.install("test")
    except:
        return -1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install applications local to the user")
    parser.add_argument("-c", "--config", type=str)
    parser.add_argument("--cache", type=str)
    parser.add_argument("-v", "--verbose", nargs='?', default=1, const=2, type=int)
    options = parser.parse_args()
    
    args, kwargs = options._get_args(), dict(options._get_kwargs())

    main(*args, **kwargs)

