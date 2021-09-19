#!/usr/bin/env python
import configparser
import subprocess as shell

try:
    from termcolor import colored
except ImportError:
    # if termcolor is not installed, strings should just be plain colourless
    # installed via pip
    def colored(*args, **kwargs):
        return args[0]


class Manager:
    def __init__(self, keyname, configfile_name, verbosity=1, fallback_src_path="~/.local/share/crackle/src", fallback_bin_path="~/.local/share/crackle/bin"):
        self.keyname = keyname
        self.verbosity = verbosity
        self._read_config(configfile_name, fallback_bin_path=fallback_bin_path, fallback_src_path=fallback_src_path)

        self.packages = []

    def update_database(self):
        pass

    def _read_config(self, configfile_name, fallback_bin_path, fallback_src_path):
        self.debug(f"{configfile_name=}")
        self.config = configparser.RawConfigParser()
        self.config.read(configfile_name)

        self.binary_path = self.config.get("Environment", "binpath", fallback=fallback_bin_path)
        self.debug(f"{self.binary_path=}")
        self.src_path = self.config.get("Environment", "srcpath", fallback=fallback_src_path)
        self.debug(f"{self.src_path=}")

    def debug(self, *args, **kwargs):
        if self.verbosity >= kwargs.get("level", 1):
            print(colored("[DEBUG/Manager]", "yellow"), *args, **kwargs)

    def has_package(self, pkg_name):
        cmd = self.config.get("Manager", "search").replace("{pkg}", pkg_name)
        self.debug(f"{cmd=}")
        out = shell.run(cmd.split(" "), capture_output=True).stdout
        print(out)

    def __str__(self):
        return str(self.config)
