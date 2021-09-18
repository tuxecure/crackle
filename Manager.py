#!/usr/bin/env python
import configparser

class Manager:
    def __init__(self, keyname, configfile_name):
        self.keyname = keyname
        self._read_config(configfile_name)
        self.packages = []

    def update_database(self):
        pass

    def _read_config(self, configfile_name):
        self.config = configparser.RawConfigParser()
        self.config.read(configfile_name)

    def has_package(self, pkg_name):
        return pkg_name in self.packages


    def __str__(self):
        return str(self.config)
