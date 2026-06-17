# made by ChromiumOS-Guy (https://github.com/ChromiumOS-Guy)
# Modified by itisFarzin (https://github.com/itisFarzin)

import copy
from typing import TypedDict


class PackageBlock(TypedDict):
    package_type: str | None
    start_line: int | None
    end_line: int | None
    start_indent: int | None


#### START file processing ####


def process_file(filename: str) -> list[PackageBlock]:
    """
    Generates a list of packages from a configuration file.

    The function reads a configuration file, identifies the '.packages' block,
    and extracts the package type, start line, and end line. It returns a list
    of dictionaries, where each dictionary represents a .packages block.

    Args:
        filename (str): The path to the configuration file.

    Returns:
        list: A list of dictionaries, where each dictionary represents a package.
            Each dictionary contains the following keys:
                - package_type (str): The type of package (e.g., home, system).
                - start_line (int): The line number where the package block starts.
                - end_line (int): The line number where the package block ends.
    """

    package_blocks: list[PackageBlock] = []
    package: PackageBlock = {
        "package_type": None,
        "start_line": None,
        "end_line": None,
        "start_indent": None,
    }
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):  # i is one behind where we actually are.
                stripped_line = line.strip()
                if ".packages" in line and not stripped_line.startswith("#"):
                    package["start_indent"] = len(line) - len(line.lstrip())
                    package_type = line.split(".packages")[0].strip()
                    package["package_type"] = (
                        package_type  # we want to make sure we know where we are installing this package home system?, we want to save that.
                    )
                    package["start_line"] = (
                        i + 1
                    )  # we want to save the start line so we know where to start putting things later (the + 1 is to make sure we are on lines where we describe packages)
                elif ".systemPackages" in line and not stripped_line.startswith(
                    "#"
                ):  # if systemPackages
                    package["start_indent"] = len(line) - len(line.lstrip())
                    package["package_type"] = (
                        "system"  # we want to make sure we know where we are installing this package home system?, we want to save that.
                    )
                    package["start_line"] = (
                        i + 1
                    )  # we want to save the start line so we know where to start putting things later (the + 1 is to make sure we are on lines where we describe packages)
                elif (
                    package["start_line"] is not None
                    and not stripped_line.startswith("#")
                    and len(line) - len(line.lstrip()) == package["start_indent"]
                    and "];" in line
                ):  # check indent and if correct and not comment then this is the end of .packages
                    package["end_line"] = (
                        i  # we want to save the end line so we know where to stop putting things later
                    )
                    package_blocks.append(
                        copy.deepcopy(package)
                    )  # add package to packages
                    package = {
                        "package_type": None,
                        "start_line": None,
                        "end_line": None,
                        "start_indent": None,
                    }
    except FileNotFoundError:
        print("could not find configuration file at path {path}".format(path=filename))
    except Exception as e:
        print("Exception occured! , error is {e}".format(e=e))

    return package_blocks


#### END file processing ####

#### START check package blocks ####


def check_package_blocks(package_blocks: list[PackageBlock]) -> bool:
    """
    Checks if there are any duplicate package block types in the given list, and that package_blocks has data in it.

    Args:
        package_blocks (list): A list of package blocks, where each block is a dictionary containing package block information.

    Returns:
        bool: True if there are any problems with package_blocks list, False otherwise.

    Notes:
        This function prints an error message if a duplicate package block type is found, indicating that this is not supported.
    """

    if not package_blocks:  # check package_blocks has data
        print("no package blocks found in configuration file")
        return True

    # check if there is multiple of same package block
    package_block_types: list[str | None] = []
    for package_block in package_blocks:
        package_block_types.append(package_block["package_type"])

    seen_types: set[str | None] = set()
    for package_type in package_block_types:
        if package_type in seen_types:
            print(
                f"Error: Duplicate package block of type '{package_type}' this is not supported."
            )
            return True
        seen_types.add(package_type)
    return False


#### END check package blocks ####

#### START read packages ####


def read_packages(filename: str, package_type: str) -> list[str]:
    """
    Reads and extracts packages from a configuration file based on the specified packages type.

    Args:
        filename (str): The path to the configuration file.
        package_type (str): The type of packages to extract (e.g., 'home', 'system').

    Returns:
        list: A list of packages extracted from the configuration file, filtered to exclude comments, newlines, and unsupported syntax.

    Notes:
        This function checks for the following conditions:
            - If the configuration file does not contain any package blocks, it prints a message and returns an empty list.
            - If there are duplicate package blocks of the same type, it prints an error message and returns an empty list.
        It also handles exceptions for file not found and other unexpected errors.

    Raises:
        FileNotFoundError: If the configuration file does not exist at the specified path.
        Exception: If any other unexpected error occurs during package extraction.
    """

    packages: list[str] = []
    package_blocks = process_file(filename)

    if check_package_blocks(package_blocks):  # check package_blocks
        return packages

    try:
        for package_block in package_blocks:
            if package_block["package_type"] == package_type:
                with open(filename, "r") as file:
                    lines = file.readlines()  # read lines from file
                    lines = lines[
                        package_block["start_line"] : package_block["end_line"]
                    ]  # make sure to get only the package block and not whole file.
                    for line in lines:  # i is one behind where we actually are.
                        stripped_line = line.strip()
                        if (
                            not stripped_line.startswith("#")
                            and "(" not in stripped_line
                            and ")" not in stripped_line
                            and "[" not in stripped_line
                            and "]" not in stripped_line
                            and stripped_line != ""
                        ):  # filter comments, newlines and unsupported stuff.
                            packages.append(stripped_line)

    except FileNotFoundError:
        print("could not find configuration file at path {path}".format(path=filename))
    except Exception as e:
        print("Exception occured! , error is {e}".format(e=e))

    return packages


#### END read packages ####

#### START add packages ####


def add_packages(
    filename: str, packages: list[str], package_type: str, overwrite: bool = False
) -> list[str]:
    """
    Adds packages to a configuration file.

    Args:
        filename (str): The path to the configuration file.
        packages (list): A list of packages to add to the file.
        package_type (str): The type of package block to add to (e.g., 'home', 'system').
        overwrite (bool, optional): Whether to overwrite existing packages in the file. Defaults to False.

    Returns:
        Packages added in list data type.

    Notes:
        This function checks if the configuration file exists and if the package blocks are valid.
        If the file does not exist or the package blocks are invalid, it prints an error message and returns.
        If overwrite is False, it reads the existing packages from the file and adds them to the packages list to avoid overwriting them.
        It then replaces the lines in the package block with the packages from the packages list, indented correctly.
        If any exceptions occur during the process, it prints an error message.

    Raises:
        FileNotFoundError: If the configuration file does not exist at the specified path.
        Exception: If any other unexpected error occurs during the process.
    """

    processed_packages: list[str] = []  # fix for nix search
    for package in packages:
        if package.startswith("nixpkgs"):
            processed_packages.append("pkgs" + package[len("nixpkgs") :])
        else:
            processed_packages.append(package)
    packages = processed_packages

    package_blocks: list[PackageBlock] = process_file(filename)
    existing_packages: list[str] = (
        read_packages(filename, package_type) if not overwrite else []
    )  # read packages so we can add them back in if override not needed.

    if check_package_blocks(package_blocks):  # check package_blocks
        return []  # if we need to exit specify packages added, which is zero.

    for package in (
        existing_packages
    ):  # readd existing packages to packages so we won't override them.
        if package not in packages:  # skip ones we're already adding to avoid duplicates
            packages.append(package)

    try:
        for package_block in package_blocks:
            if package_block["package_type"] == package_type:
                with open(filename, "r") as file:
                    lines = file.readlines()  # read lines from file
                indent = package_block["start_indent"] or 0
                lines[package_block["start_line"] : package_block["end_line"]] = [
                    " " * (indent + 2) + package + "\n" for package in packages
                ]
                with open(filename, "w") as file:
                    file.writelines(lines)

    except FileNotFoundError:
        print("could not find configuration file at path {path}".format(path=filename))
    except Exception as e:
        print("Exception occured! , error is {e}".format(e=e))

    return packages


#### END add packages ####

#### START delete packages ####


def delete_packages(
    filename: str, packages: list[str], package_type: str | None = None
) -> list[str]:
    """
    Deletes a list of packages from a configuration file.

    Args:
    - filename (str): The name of the file from which to delete packages.
    - packages (list): A list of packages to delete.
    - package_type (str, optional): The type of package to delete. If not specified, all package types will be checked. Defaults to None.

    Returns:
    - list: A list of packages that were successfully deleted.
    """

    deleted_packages: list[str] = []  # total of deleted packages
    package_blocks: list[PackageBlock] = process_file(filename)

    if check_package_blocks(package_blocks):  # check package_blocks
        return []

    seen_types: set[str] = set()
    if not package_type:  # default to checking everywhere for package
        package_block_types: list[str | None] = []
        for package_block in package_blocks:
            package_block_types.append(package_block["package_type"])
        for block_type in package_block_types:
            if (
                block_type is not None and block_type not in seen_types
            ):  # we know we don't need this because of check_package_blocks but sanity.
                seen_types.add(block_type)
    else:  # if specified check for package only in the package block given.
        seen_types.add(package_type)

    for current_type in seen_types:
        existing_packages: list[str] = read_packages(filename, current_type)
        packages_to_delete: list[str] = [
            package for package in packages if package in existing_packages
        ]  # check what we can delete
        updated_packages: list[str] = [
            package
            for package in existing_packages
            if package not in packages_to_delete
        ]  # remove what we need to delete from existing packages

        add_packages(filename, updated_packages, current_type, True)  # delete packages

        for package in (
            packages_to_delete
        ):  # read packages_to_delete and add that to total packages deleted
            deleted_packages.append(package)

    return deleted_packages


#### END delete packages ####
