#!/usr/bin/env python
import os
import configparser
import subprocess as shell

from helper import IO
from Package import *

try:
    from termcolor import colored
except ImportError:
    # if termcolor is not installed, strings should just be plain colourless
    # installed via pip
    def colored(*args, **kwargs):
        return args[0]


class Manager(IO):
    def __init__(self, keyname, configfile_name, verbosity=1, fallback_src_path="~/.local/share/crackle/src", fallback_bin_path="~/.local/share/crackle/bin"):
        super().__init__(module="Manager")
        self.keyname = keyname
        self.verbosity = verbosity
        self._read_config(configfile_name, fallback_bin_path=fallback_bin_path, fallback_src_path=fallback_src_path)

        self.packages = []

    def update_database(self):
        pass

    def _read_config(self, configfile_name, fallback_bin_path, fallback_src_path):
        if not os.path.isfile(configfile_name):
                self.error(f"{configfile_name=} is not a file")
                raise FileNotFoundError("Configuration file must exist")
        else:
            self.debug(f"{configfile_name=}")
            self.config = configparser.RawConfigParser()
            self.config.read(configfile_name)

            self.binary_path = self.config.get("Environment", "binpath", fallback=fallback_bin_path)
            self.debug(f"{self.binary_path=}")
            self.src_path = self.config.get("Environment", "srcpath", fallback=fallback_src_path)
            self.debug(f"{self.src_path=}")

    def has_package(self, pkg_name):
        cmd = self.config.get("Manager", "search").replace("{pkg}", pkg_name)
        self.debug(f"{cmd=}")
        out = shell.run(cmd.split(" "), capture_output=True, text=True).stdout
        return bool(out)

    def get_package(self, pkg_name):
        cmd = self.config.get("Manager", "search").replace("{pkg}", pkg_name)
        self.debug(f"{cmd=}")
        out = shell.run(cmd.split(" "), capture_output=True, text=True).stdout

        if not out:
            return
        else:
            return Package( out.split()[0], self.keyname, (1, 0) )
        

    def __str__(self):
        return str(self.config)
