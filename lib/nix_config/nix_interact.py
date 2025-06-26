# made by ChromiumOS-Guy (https://github.com/ChromiumOS-Guy)

import os
import copy
from nix_config.openprocess import openprocess

#### START apply config #### 

def apply_config() -> tuple:
    """
    Applies a configuration by running 'home-manager build' and parses its output, 
    it filters the full error output to identify lines starting with
    "error: attribute" and extracts the specific error message following this prefix,
    adding each as an individual entry to 'simple_error'.

    Returns:
        tuple[list[str], list[str], list[str]]: A tuple containing three lists:
            - output (list[str]): Lines from the standard output of the command.
            - simple_error (list[str]): Specific error messages related to
              "attribute" issues, with each message as a separate item.
            - full_error (list[str]): All lines from the standard error output
              of the command.
    """

    error_prefix : str = "error: "

    simple_error : list = []

    output , full_error = openprocess("home-manager build --no-build-output")
    output : list
    full_error : list

    # Iterate through the full_error to find and extract simple error
    for line in full_error:
        if error_prefix in line:
            # Append everything after the error_prefix to simple_error
            simple_error.append(line.split(error_prefix, 1)[1].strip())
    
    return output , simple_error , full_error

#### END apply config ####
