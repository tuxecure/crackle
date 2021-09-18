#!/usr/bin/py
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
        self.verbosity = 2 if "--verbose" in kwargs.keys() else 1
        self.debug(f"{args=}, {kwargs=}")
        self.config_path = kwargs.get("config", os.path.join(xdg.xdg_config_home(), "crackle"))
        self.cache_path = kwargs.get("cache", os.path.join(xdg.xdg_cache_home(), "crackle"))

        self.debug(f"{self.config_path=}")
        self.debug(f"{self.cache_path=}")

        self._read_config(os.path.join(self.config_path, "crackle.conf"))

        self.managers = ( Manager(name, os.path.join(self.config_path, name[1]), verbosity=self.verbosity) for name in self.config.items("Managers") )

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
    parser.add_argument("-v", "--verbose", action="store_true")
    options = parser.parse_args()
    
    args, kwargs = options._get_args(), dict(options._get_kwargs())

    main(*args, **kwargs)

