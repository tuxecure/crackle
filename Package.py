#!/usr/env/bin python
from helper import IO

class Package(IO):
    def __init__(self, name, manager, version=(0, )):
        super().__init__()
        self.name = name
        self.manager = manager
        self.version = version

    def __str__(self):
        return str(self.name) + ":" +"-".join(map(str, self.version))
        

