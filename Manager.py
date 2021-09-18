#!/usr/bin/env python
import configparser

try:
    from termcolor import colored
except ImportError:
    # if termcolor is not installed, strings should just be plain colourless
    # installed via pip
    def colored(*args, **kwargs):
        return args[0]


class Manager:
    def __init__(self, keyname, configfile_name, verbosity=1):
        self.keyname = keyname
        self.verbosity = verbosity
        self._read_config(configfile_name)

        self.packages = []

    def update_database(self):
        pass

    def _read_config(self, configfile_name):
        self.debug(f"{configfile_name=}")
        self.config = configparser.RawConfigParser()
        self.config.read(configfile_name)

    def debug(self, *args, **kwargs):
        if self.verbosity >= kwargs.get("level", 1):
            print(colored("[DEBUG/Manager]", "yellow"), *args, **kwargs)

    def has_package(self, pkg_name):
        return pkg_name in self.packages


    def __str__(self):
        return str(self.config)
