#!/usr/bin/env python
try:
      from termcolor import colored
except ImportError:
      # if termcolor is not installed, strings should just be plain colourless
      # installed via pip
      def colored(*args, **kwargs):
          return args[0]

class IO:
    def __init__(self, module=None):
        self.verbosity = 1
        self.module = "/"+module if module else ""

    def info(self, args, **kwargs):
        if self.verbosity >= 2:
              print(colored(f"[INFO{self.module}]", "blue", attrs=["bold"]), args, *kwargs)

    def warn(self, args, **kwargs):
        if self.verbosity >= 3:
              print(colored(f"[WARN{self.module}]", "yellow", attrs=["bold"]), args, *kwargs)

    def debug(self, args, **kwargs):
        if self.verbosity >= 3:
              print(colored(f"[DEBUG{self.module}]", "magenta", attrs=[]), args, *kwargs)

    def error(self, args, **kwargs):
        if self.verbosity >= 1:
              print(colored(f"[ERROR{self.module}]", "red", attrs=["bold"]), args, *kwargs)
