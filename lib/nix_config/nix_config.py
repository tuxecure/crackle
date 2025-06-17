# made by ChromiumOS-Guy (https://github.com/ChromiumOS-Guy)

import shutil
import os
import filecmp # For comparing file contents (if file has not changed why bother applying it)
import config, nix_interact
from openprocess import openprocess

#### START get config path ####

def get_config_path() -> str:
    """
    Determines and verifies the default configuration path for home-manager.

    This function constructs the expected path to the home-manager configuration file
    at `~/.config/home-manager/home.nix` by dynamically getting the current username.
    It then checks if a file actually exists at this path.

    Returns:
        str | None: The absolute path to the home-manager configuration file if it
        exists. Returns `None` if the file is not found at the expected location.
        A message indicating the missing file path will be printed to standard output
        if the file is not found.
    """

    config_path = "/home/{user}/.config/home-manager/home.nix".format(user=openprocess("whoami")[0][0])
    if os.path.exists(config_path):
        return config
    print("config file not found at path {config}".format(config=config))
    return None # everything else has error checks that will catch this

#### END get config path ####

#### START backup config file ####

def _backup_config_file(filename : str) -> tuple:
    """
    Creates a backup of a specified configuration file.

    This function attempts to create a backup of the `filename` by copying it
    to `filename.backup`. If a backup file already exists, it checks if the
    source file and the existing backup are identical.
    - If they are identical, no action is taken, and it reports success.
    - If they are different, the existing backup is replaced with the new
      version from the source file.

    Args:
        filename (str): The absolute path to the configuration file to be backed up.

    Returns:
        tuple[bool, str]: A tuple where:
            - The first element (bool) is `True` if the backup operation was
              successful or if the files were already identical; `False` otherwise.
            - The second element (str) is a success message ("SUCCESS") or an
              error message detailing the failure.
    """

    backup_path = filename + ".backup" # /path/to/home.nix + .backup = /path/to/home.nix.backup
    try:
        if filecmp.cmp(source_file_path, destination_file_path, shallow=False):
        return True , "SUCCESS"
        else:
            os.remove(destination_file_path)
            shutil.copy2(source_file_path, destination_file_path)
            return True, "SUCCESS"
    except Exception as e:
        print(f"Error copying file {source_file_path} to {destination_file_path}: {e}")
        return False, e
    return False, "UNKNOWN FAILURE"
    
#### END backup config file ####

#### START restore config file ####

def _restore_config_file(filename: str) -> tuple[bool, str]:
    """
    Restores a configuration file from its backup.

    This function attempts to restore the specified `filename` by copying its
    corresponding backup file (`filename.backup`) back to the original `filename` path.
    It performs several checks:
    - Verifies that the backup file (`filename.backup`) exists. This is crucial for restoration.
    - If a backup exists, it then checks if the current `filename` (if it exists)
      and the `filename.backup` are already identical. If so, no action is taken.
    - If the files are different, or if the original `filename` doesn't exist,
      the current `filename` is either overwritten or created with the content
      of `filename.backup`.

    Args:
        filename (str): The absolute path to the configuration file to be restored.
                        This is the target path where the backup will be copied to.

    Returns:
        tuple[bool, str]: A tuple where:
            - The first element (bool) is `True` if the restore operation was
              successful or if the files were already identical; `False` otherwise.
            - The second element (str) is a success message ("SUCCESS") or an
              error message detailing the failure.
    """

    backup_path = filename + ".backup"
    try:
        if not os.path.exists(backup_path):
            return False, f"Error: Backup file '{backup_path}' not found. Cannot restore."
        # Check if the current file and the backup are already identical
        if os.path.exists(filename) and filecmp.cmp(filename, backup_path, shallow=False):
            return True, "SUCCESS: Configuration file is already identical to its backup."
        else:
            # Overwrite the current file with the backup
            if os.path.exists(filename):
                os.remove(filename)
            shutil.copy2(backup_path, filename)
            return True, "SUCCESS: Configuration file restored from backup."
    except Exception as e:
        # Catch any other unexpected errors during the file operations
        return False, f"Error restoring '{filename}' from '{backup_path}': {e}"

#### END restore config file ####


#### START read packages ####

def read_packages(package_type : str = "home", filename : str = get_config_path()) -> list: # forward safe function read_packages also default the inputs
    return config.read_packages(filename, package_type)

#### END read packages ####

#### START add packages ####

def add_packages(packages : list, overwrite : bool = False, package_type : str = "home", filename : str = get_config_path()) -> list:
     """
    Adds specified software packages to a configuration file, ensuring system
    stability through backup and restore mechanisms.

    This function first attempts to locate the a configuration file. If found,
    it creates a backup of the existing configuration. If the backup fails, the
    operation is aborted to prevent potential data loss.

    Upon a successful backup, the function proceeds to add the desired packages
    to the configuration. After modifying the configuration, it attempts to apply
    the changes. If applying the new configuration results in errors, it
    automatically tries to restore the system to its last working state using
    the created backup. If the restore also fails, this critical error is
    prioritized in the returned error messages.

    Args:
        packages (list): A list of strings, where each string is the name of a
                         package to add (e.g., `["pkgs.neovim", "pkgs.git"]`).
        overwrite (bool, optional): If `True`, existing package definitions qwill be
                                    overwritten. Defaults to `False`.
        package_type (str, optional): Specifies the type of package block to add to
                                      (e.g., `"home"` for home-manager packages,
                                      `"system"` for NixOS packages if configuration.nix is used). Defaults to `"home"`.
        filename (str, optional): The absolute path to your configuration file.
                                  Defaults to the path returned by `get_config_path()`.

    Returns:
        tuple[list, list]: A tuple where:
            - The first element is `packages_added` (list), a list of packages
              that were successfully added to the configuration (this reflects
              what `config.add_packages` reports).
            - The second element is a list of three sub-lists representing the
              outcome of the configuration application:
                - The first sub-list contains `output` (list[str]): Lines from
                  the standard output of the configuration application command.
                - The second sub-list contains `simple_error` (list[str]): Parsed
                  specific error messages (e.g., attribute errors). If a restore
                  operation fails, its error message is inserted at the beginning
                  of this list.
                - The third sub-list contains `full_error` (list[str]): All lines
                  from the standard error output of the configuration application
                  command, or specific errors related to backup failures.
    """

    if not filename:
        return packages_added , [[] ,["failed to find config file"], []]
    packages_added : list = []
    backup_success, backup_error = _backup_config_file(filename)
    if backup_success:
        packages_added = config.add_packages(filename, packages, package_type, overwrite)
        output : list ,simple_error : list , full_error : list = nix_interact.apply_config()
        if not full_error:
            return packages_added, [output, simple_error, full_error]
        else:
            restore_success, restore_error = _restore_config_file()
            if not restore_success:
                return packages_added, [output , simple_error.insert(0, restore_error), full_error] # make sure we know
            return packages_added, [output , simple_error, full_error]
    else:
        print("failed to backup too risky to run without, exiting.")
    return packages_added , [[] ,["failed to backup too risky to run without, exiting."], [backup_error]]
    
#### END add packages ####

#### START delete packages ####

def delete_packages(packages : list, package_type : str = "home", filename : str = get_config_path()) -> list:
    """
    Deletes specified software packages from a configuration file, ensuring system
    stability through backup and restore mechanisms.

    This function first attempts to locate a configuration file. If found,
    it creates a backup of the existing configuration. If the backup fails, the
    operation is aborted to prevent potential data loss, as modifying the
    configuration without a safety net is too risky.

    Upon a successful backup, the function proceeds to delete the desired packages
    from the configuration. After modifying the configuration, it attempts to
    apply the changes. If applying the new configuration results in errors, it
    automatically tries to restore the system to its last working state using
    the created backup. If the restore also fails, this critical error is
    prioritized in the returned error messages.

    Args:
        packages (list): A list of strings, where each string is the name of a
                         package to delete (e.g., `["pkgs.neovim", "pkgs.git"]`).
        package_type (str, optional): Specifies the type of package block to add to
                                      (e.g., `"home"` for home-manager packages,
                                      `"system"` for NixOS packages if configuration.nix is used). Defaults to `"home"`.
        filename (str, optional): The absolute path to your configuration file.
                                  Defaults to the path returned by `get_config_path()`.

    Returns:
        tuple[list, list]: A tuple where:
            - The first element is `packages_deleted` (list), a list of packages
              that were successfully processed for deletion (this reflects what
              `config.delete_packages` reports).
            - The second element is a list of three sub-lists representing the
              outcome of the configuration application:
                - The first sub-list contains `output` (list[str]): Lines from
                  the standard output of the configuration application command.
                - The second sub-list contains `simple_error` (list[str]): Parsed
                  specific error messages (e.g., attribute errors). If a restore
                  operation fails, its error message is inserted at the beginning
                  of this list.
                - The third sub-list contains `full_error` (list[str]): All lines
                  from the standard error output of the configuration application
                  command, or specific errors related to backup failures.
    """

     if not filename:
        return packages_deleted , [[] ,["failed to find config file"], []]
    packages_deleted : list = []
    backup_success, backup_error = _backup_config_file(filename)
    if backup_success:
        packages_deleted = config.delete_packages(filename, packages, package_type)
        output : list ,simple_error : list , full_error : list = nix_interact.apply_config()
        if not full_error:
            return packages_deleted, [output, simple_error, full_error]
        else:
            restore_success, restore_error = _restore_config_file()
            if not restore_success:
                return packages_deleted, [output , simple_error.insert(0, restore_error), full_error] # make sure we know
            return packages_deleted, [output , simple_error, full_error]
    else:
        print("failed to backup too risky to run without, exiting.")
    return packages_deleted , [[] ,["failed to backup too risky to run without, exiting."], [backup_error]]

#### END delete packages ####